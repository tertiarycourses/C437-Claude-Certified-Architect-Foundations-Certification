"""Live tests for the research team: two real runs, ten checks on the recorded delegations and tool calls.
Run 1 replays the exam question (the coordinator's narrow decomposition); run 2 is the fixed coordinator.
Run:  uv run test_research.py"""
from research import run_research
from research_tools import DATA

TOPIC = "Impact of AI on creative industries"
URLS = {h["url"]: s for s, hits in DATA["web"].items()
        for h in (hits["partial_results"] if isinstance(hits, dict) else hits)}
DOCS = {d["name"] for d in DATA["documents"]}
TOOLS = {"search": {"search_web"}, "documents": {"read_document"}, "synthesis": set(), "report": set()}
results = []


def check(name, ok, detail=""):
    results.append(ok)
    print(f"{'PASS' if ok else 'FAIL'}  {name}" + (f"  ({detail})" if detail and not ok else ""))


def cited(source):
    """The sandbox URL or document a cited source points to, or None if it is not in sources.json."""
    return next((u for u in URLS if u in source), None) or next((d for d in DOCS if d in source), None)


print("Run 1 · BEFORE the fix: the coordinator's narrow decomposition from the exam question\n")
b = run_research(TOPIC, narrow=True)
print("\n--- checks, run 1 (before the fix) ---")
failed = [x["agent"] for x in b["delegations"] if x["json"] is None or any(c["is_error"] for c in x["calls"])]
check("every subagent completed: each returned its JSON and no tool call failed", not failed, f"failed: {failed}")
check("yet the coverage check flags music, writing and film as never searched",
      {"music", "writing", "film"} <= set(b["missing"]), f"never searched: {b['missing']}")

print("\nRun 2 · AFTER the fix: rule 1 of the coordinator's system prompt covers every sector\n")
a = run_research(TOPIC)
d = a["delegations"]
print("\n--- checks, run 2 (after the fix) ---")
check("a search ran for every sector: music, writing, film, visual arts", not a["missing"], f"never searched: {a['missing']}")
turns = [x["turn"] for x in d if x["agent"] == "search"]
check("two or more searches ran in parallel (same coordinator turn)", any(turns.count(t) >= 2 for t in turns), f"turns {turns}")
bad = [(x["agent"], c["tool"]) for x in d for c in x["calls"] if c["tool"] not in TOOLS[x["agent"]]]
check("every subagent used only its own tools", not bad, f"{bad}")
for agent, what in [("synthesis", "the findings"), ("report", "the synthesis")]:
    tasks = [x["task"] for x in d if x["agent"] == agent]
    n = sum(u in tasks[-1] for u in URLS) if tasks else 0
    check(f"the {agent} task carried {what} (3+ source URLs pasted in)", n >= 3, f"{n} URLs in the task")
srcs = [f.get("source", "") for f in a["report"].get("findings", [])]
unknown = [s for s in srcs if not cited(s)]
check("every source in report.json exists in sources.json", bool(srcs) and not unknown, f"unknown: {unknown[:3]}")
sectors = {URLS[cited(s)] for s in srcs if cited(s) in URLS}
check("the report cites sources from 3+ sectors", len(sectors) >= 3, f"sectors {sorted(sectors)}")
check("the report lists the film search failure as a gap", any("film" in g.lower() for g in a["report"].get("gaps", [])),
      f"gaps: {a['report'].get('gaps')}")

print(f"\n{sum(results)}/{len(results)} checks passed")
raise SystemExit(0 if all(results) else 1)
