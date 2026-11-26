"""The coordinator of a multi-agent research team (Scenario 3). It plans, delegates to four subagents, and runs every
delegation from one turn IN PARALLEL. Run:  uv run research.py "Impact of AI on creative industries" [--narrow]
--narrow replays Scenario 1: the coordinator's first, narrow plan."""
import json
import sys
import time
from concurrent.futures import ThreadPoolExecutor

import anthropic
from dotenv import load_dotenv

from agents import AGENTS, MODEL, run_subagent
from research_tools import DATA, sector_of

load_dotenv()
MAX_TURNS = 8
# Rule 1 is the coordinator's task decomposition. RULE_1_NARROW is the first plan (Scenario 1);
# RULE_1 is the fix (Scenario 2). The fix is one rule in the coordinator's system prompt: no subagent changes.
RULE_1_NARROW = "1. Decompose the topic into three search subtasks: AI in digital art creation; AI in graphic design; AI in photography."
RULE_1 = """1. Decompose the topic into the distinct sectors it spans before you split it. For creative industries, cover at
   least music, writing, film and visual arts: one search subtask per sector. Breadth first: a narrow plan makes a narrow report."""
SYSTEM = """You are the coordinator of a research team. You never search, read documents or write the report yourself: you delegate.
{rule_1}
2. In ONE turn, delegate one "search" task per subtask (they run in parallel), plus one "documents" task that names
   both internal documents: Halden-Rao-2026-Journal-of-Creative-Economies.pdf and BrightCanvas-Customer-Benchmark-2026.pdf.
3. Subagents see nothing but their task text. Put everything a subagent needs in its task.
4. When the results are back, delegate ONE "synthesis" task. Paste into it every finding with its exact source and
   every gap the subagents reported.
5. When the synthesis is back, delegate ONE "report" task. Paste the synthesis JSON into it, unchanged.
6. Then reply with a two-sentence summary for the user."""
DELEGATE = {
    "name": "delegate",
    "description": "Give one task to a subagent and get its result back. agent: 'search' (web search on one sector), "
                   "'documents' (reads the internal PDFs), 'synthesis' (combines the findings you paste in), "
                   "'report' (writes the final cited report from the synthesis you paste in). "
                   "The subagent sees ONLY the task text, never this conversation.",
    "input_schema": {"type": "object", "properties": {
        "agent": {"type": "string", "enum": list(AGENTS)},
        "task": {"type": "string", "description": "everything the subagent needs to know"}},
        "required": ["agent", "task"]},
}


def coverage(delegations):
    """Which sectors were actually searched, and which were never searched at all."""
    searched = {c["result"].get("sector") or sector_of(c["input"].get("query", ""))
                for d in delegations for c in d["calls"] if c["tool"] == "search_web"}
    return sorted(s for s in searched if s), sorted(set(DATA["sectors"]) - searched)


def known_sources():
    """Every URL and document name in sources.json."""
    urls = [h["url"] for hits in DATA["web"].values() for h in (hits["partial_results"] if isinstance(hits, dict) else hits)]
    return urls + [d["name"] for d in DATA["documents"]]


def check_provenance(report):
    """A gate in code: a finding whose source names no URL or document from sources.json moves to gaps."""
    known = known_sources()
    kept, dropped = [], []
    for f in report.get("findings", []):
        (kept if any(k in str(f.get("source", "")) for k in known) else dropped).append(f)
    for f in dropped:
        print(f"  provenance check: dropped unsourced finding {f.get('claim', '')[:70]!r}")
    if report:
        report["findings"] = kept
        report["gaps"] = report.get("gaps", []) + [f"Unsourced claim removed: {f.get('claim', '')}" for f in dropped]
    return report


def run_research(topic, narrow=False):
    """narrow=True runs Scenario 1: the coordinator's first, narrow plan."""
    client = anthropic.Anthropic()
    system = SYSTEM.format(rule_1=RULE_1_NARROW if narrow else RULE_1)
    messages = [{"role": "user", "content": f"Research topic: {topic}"}]
    delegations, summary = [], ""
    for turn in range(1, MAX_TURNS + 1):
        response = client.messages.create(model=MODEL, max_tokens=8000, system=system, tools=[DELEGATE], messages=messages)
        messages.append({"role": "assistant", "content": response.content})
        uses = [b for b in response.content if b.type == "tool_use"]
        print(f"\nCoordinator turn {turn}: stop_reason={response.stop_reason}, {len(uses)} delegation(s)")
        if response.stop_reason != "tool_use":
            summary = "".join(b.text for b in response.content if b.type == "text")
            break
        t0 = time.time()
        with ThreadPoolExecutor() as pool:                     # every delegation from this turn runs at once
            outs = list(pool.map(lambda b: run_subagent(b.input["agent"], b.input["task"]), uses))
        results = []
        for block, out in zip(uses, outs):
            out["turn"] = turn
            delegations.append(out)
            print(f"  -> {out['agent']}: {out['task'][:90]!r} ({len(out['calls'])} tool calls)")
            for c in out["calls"]:
                print(f"       {c['tool']}({json.dumps(c['input'])}) {'ERROR ' + c['result'].get('errorCategory', '') if c['is_error'] else 'ok'}")
            results.append({"type": "tool_result", "tool_use_id": block.id, "content": out["text"]})
        print(f"  ({len(uses)} subagent(s) in {time.time() - t0:.0f}s)")
        messages.append({"role": "user", "content": results})
    final = [d for d in delegations if d["agent"] == "report"]
    report = check_provenance(final[-1]["json"] if final and final[-1]["json"] else {})
    searched, missing = coverage(delegations)
    return {"topic": topic, "summary": summary, "report": report, "delegations": delegations,
            "searched": searched, "missing": missing}


def to_markdown(r):
    rep = r["report"]
    lines = [f"# {rep.get('title', r['topic'])}", "", rep.get("summary", ""), ""]
    lines += [f"- **{f.get('sector', '')}**: {f.get('claim', '')} ({f.get('source', '')})" for f in rep.get("findings", [])]
    lines += ["", "## Gaps"] + [f"- {g}" for g in rep.get("gaps", [])] or ["- none"]
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    args = sys.argv[1:]
    narrow = "--narrow" in args
    topic = next((a for a in args if a != "--narrow"), "Impact of AI on creative industries")
    print("Coordinator rule 1:", RULE_1_NARROW if narrow else RULE_1)
    r = run_research(topic, narrow)
    with open("report.json", "w") as f:
        json.dump(r["report"], f, indent=2)
    with open("report.md", "w") as f:
        f.write(to_markdown(r))
    print("\n=== Report (report.md) ===\n" + to_markdown(r))
    print(f"Coverage: searched {', '.join(r['searched']) or 'nothing'}; never searched: {', '.join(r['missing']) or 'none'}")
    print("\n=== Coordinator ===\n" + r["summary"])
