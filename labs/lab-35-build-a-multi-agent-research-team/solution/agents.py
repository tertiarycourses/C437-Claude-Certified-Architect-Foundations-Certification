"""The four subagents of a research team: web search, document analysis, synthesis and report generation.
Each run starts a FRESH conversation that holds only its task: no subagent sees the coordinator's messages or another
subagent's work. Each gets only its own tools. The search agent uses Claude's web search tool; with sample=True it
searches the fixed sample data in sources.json instead (test_research.py uses that, so its checks are repeatable)."""
import json
import re
import sys

import anthropic
from dotenv import load_dotenv

from research_tools import TOOLS, run_tool

load_dotenv()
MODEL = "claude-haiku-5-5"
WEB_SEARCH = {"type": "web_search_20250305", "name": "web_search", "max_uses": 2}   # Claude's server-side web search

AGENTS = {
    "search": {
        "tools": ["web_search"],
        "system": """You are a web-search subagent. Research only the area named in your task, with at most two web searches.
Prefer recent surveys, official statistics, peer-reviewed studies and industry reports.
Return ONLY a JSON object: {"area": str, "findings": [{"claim": str, "source_url": str, "source_title": str, "published": str}], "gaps": [str]}.
Every claim must come from a search result in this conversation; copy its url exactly, and put "unknown" when a result
shows no date. Return at most four findings, each one sentence with its number. "gaps" lists only searches that failed or
found nothing relevant. Never invent a source, URL or number.""",
    },
    "documents": {
        "tools": ["read_document"],
        "system": """You are a document-analysis subagent. Read every document named in your task with read_document.
Return ONLY a JSON object: {"findings": [{"claim": str, "source": "<file name>, p.<page>", "evidence": "<kind of document and its method>"}], "gaps": [str]}.
Leave out ", p.<page>" when a document has no page. Say which findings are peer-reviewed, which come from a vendor and
which come from the user's own files. "gaps" lists only documents you could not read. Never invent a source.""",
    },
    "synthesis": {
        "tools": [],
        "system": """You are a synthesis subagent. Combine the findings in your task into one evidence set, using ONLY those findings.
Return ONLY a JSON object: {"findings": [{"area": str, "claim": str, "source": str, "evidence": str}], "conflicts": [str], "gaps": [str]}.
Group the findings by area. "source" is ONLY the url or "<file name>, p.<page>", copied exactly: never a finding without one.
"evidence" says what kind of source it is (survey, poll, peer-reviewed article, vendor benchmark). "conflicts" names
figures that disagree or measure different things. "gaps" lists, one short line each, the failed searches, the searches
that found nothing and the unreadable documents you were told about.""",
    },
    "report": {
        "tools": [],
        "system": """You are a report-generation subagent. Write the final research report from the synthesized findings in your
task, using ONLY those findings. Return ONLY a JSON object:
{"title": str, "summary": str, "findings": [{"area": str, "claim": str, "source": str}], "gaps": [str]}.
Summary under 80 words. One finding per source: "claim" is one sentence with its number and evidence type, and "source"
is ONLY the url or "<file name>, p.<page>", copied exactly: never a finding without one. "gaps": one short line per gap
and one per conflict, at most 8 lines.""",
    },
}
# The fixed sample data (sample=True): the search agent gets search_web over sources.json and this prompt instead.
SAMPLE_SEARCH_SYSTEM = """You are a web-search subagent. Research only the area named in your task, with at most two search_web calls.
Return ONLY a JSON object: {"area": str, "findings": [{"claim": str, "source_url": str, "source_title": str, "published": str}], "gaps": [str]}.
Every claim must come from a search result; copy its url exactly. The search index is a small curated sample: treat its
results as authoritative and do not comment on the sources. "gaps" lists only searches that failed or found nothing: if a
search fails, keep any partial_results as findings and add a gap that says what failed and for which query. Never invent a source."""


def parse_json(text):
    """Pull the JSON object out of a reply, even when it is wrapped in ``` fences."""
    m = re.search(r"\{.*\}", text, re.S)
    try:
        return json.loads(m.group(0)) if m else None
    except json.JSONDecodeError:
        return None


def web_calls(content):
    """The web searches Claude ran on the server in one response, recorded like tool calls."""
    results = {b.tool_use_id: b.content for b in content if b.type == "web_search_tool_result"}
    calls = []
    for b in content:
        if b.type == "server_tool_use" and b.name == "web_search":
            out = results.get(b.id)
            if isinstance(out, list):                       # success: a list of search results
                result = {"query": b.input.get("query", ""), "results": [
                    {"url": r.url, "title": r.title, "published": r.page_age or "unknown"} for r in out]}
                calls.append({"tool": "web_search", "input": b.input, "result": result, "is_error": False})
            else:                                           # an error object, or no result block at all
                code = getattr(out, "error_code", "no_result")
                calls.append({"tool": "web_search", "input": b.input, "is_error": True,
                              "result": {"errorCategory": code, "query": b.input.get("query", "")}})
    return calls


def run_subagent(agent, task, max_turns=6, sample=False):
    """Run one subagent on its task in a fresh context. Returns {"agent", "task", "text", "json", "calls"}.
    sample=True gives the search agent search_web over sources.json instead of Claude's web search."""
    spec = AGENTS[agent]
    names = ["search_web"] if sample and agent == "search" else spec["tools"]
    system = SAMPLE_SEARCH_SYSTEM if sample and agent == "search" else spec["system"]
    tools = [WEB_SEARCH if n == "web_search" else TOOLS[n] for n in names]
    client = anthropic.Anthropic()
    messages = [{"role": "user", "content": task}]          # the task is ALL this subagent knows
    calls = []
    for _ in range(max_turns):
        kwargs = {"tools": tools} if tools else {}
        response = client.messages.create(model=MODEL, max_tokens=8000, system=system, messages=messages, **kwargs)
        messages.append({"role": "assistant", "content": response.content})
        calls += web_calls(response.content)
        if response.stop_reason == "pause_turn":            # the server paused its search loop: send it back to resume
            continue
        if response.stop_reason != "tool_use":
            text = "".join(b.text for b in response.content if b.type == "text")
            return {"agent": agent, "task": task, "text": text, "json": parse_json(text), "calls": calls}
        results = []
        for block in response.content:
            if block.type == "tool_use":
                if block.name not in names:                     # a subagent may only use its own tools
                    result, is_error = {"message": f"{block.name} is not available to this agent"}, True
                else:
                    result, is_error = run_tool(block.name, block.input)
                calls.append({"tool": block.name, "input": block.input, "result": result, "is_error": is_error})
                results.append({"type": "tool_result", "tool_use_id": block.id, "content": json.dumps(result), "is_error": is_error})
        messages.append({"role": "user", "content": results})
    return {"agent": agent, "task": task, "text": "(stopped: turn limit)", "json": None, "calls": calls}


if __name__ == "__main__":
    out = run_subagent(sys.argv[1], sys.argv[2])
    for c in out["calls"]:
        print(f"  {c['tool']}({json.dumps(c['input'])}) -> {'ERROR ' if c['is_error'] else ''}{json.dumps(c['result'])[:160]}")
    print(out["text"])
