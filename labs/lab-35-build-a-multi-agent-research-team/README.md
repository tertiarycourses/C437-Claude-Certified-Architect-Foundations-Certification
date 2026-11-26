# Lab 35: Vibe-code a multi-agent research team

> Day 2 · Multi-Agent Research System · Task statements 1.2, 1.3, 5.3 · Vibe-coding lab · Claude Haiku 5.5 · 60 minutes

**Be the manager of your own AI research department. A coordinator delegates to four subagents: one searches the web, one analyzes documents, one synthesizes the findings and one writes the cited report. In Scenario 1 every agent does its job, yet the report covers only visual arts. You find the one agent that caused it, fix one rule in its system prompt, and in Scenario 2 the same team covers music, writing, film and visual arts.**

**Lab page:** [the main lab page](https://tertiarycourses.github.io/C437-Claude-Certified-Architect-Foundations-Certification/) lists every lab. Copy the prompts from [this lab's prompt page](https://tertiarycourses.github.io/C437-Claude-Certified-Architect-Foundations-Certification/lab-35.html) (one Copy button per prompt), or from `prompts.html` in this folder.

This is a **new project**, not the Orderly agent from Labs 31 to 34. Make a fresh folder for it.

## What you'll build

```
  "Impact of AI on creative industries"
        |
        v
  research.py -- the coordinator (claude-haiku-5-5). It never searches,
        |        reads or writes the report itself: it delegates.
        |        Its system prompt's rule 1 decides the subtasks.
        |
        |  turn 1, run in parallel:
        +--> 1. web search agent: one per subtask   --+  each one: a fresh
        +--> 2. document analysis agent: 2 PDFs     --+  conversation, only its
        |                                                own tool, only its task
        |  turn 2:
        +--> 3. synthesis agent: every finding + source + gap pasted in
        |  turn 3:
        +--> 4. report generation agent: the synthesis pasted in
        |
        v
  report.json + report.md (every claim cited) and a coverage check in code

  Scenario 1, rule 1 = a first plan:  digital art; graphic design; photography
  Scenario 2, rule 1 = the fix:       every sector: music, writing, film, visual arts
```

On Day 1 you watched these failures in Lab 2 (a narrow plan), Lab 3 (searches that ran one by one), Lab 27 (a timeout hidden as success) and Lab 30 (a vendor number treated like a peer-reviewed one). Today you build the system, run into the first one and fix it, and avoid the other three.

## What's in this folder

| File | What it is |
|---|---|
| `starter/sources.json` | the research sandbox: web results for four sectors (film always times out) and two internal PDFs. Every name, number and URL is invented. Prompt 1 downloads it into your project. |
| `starter/.env.example` | the one line your `.env` needs |
| `prompts.html` | every prompt below, each with a Copy button |
| `solution/` | our finished code (after the fix), for your trainer. You don't need it: build your own with the prompts. |
| `sample-output.txt` | a live run of `solution/`: before the fix, after the fix, then `test_research.py` with 10/10 checks |

## Before you start (5 minutes)

- **1. Open your AI coding tool in a new, empty folder** called `research-team` (a new folder, not `orderly-agent`). In VS Code, Cursor, Windsurf or Antigravity: **File → Open Folder → New Folder**. Claude Code or Codex in a terminal: start it from that folder. Any agent that can create files and run terminal commands works; the prompts use no tool-specific feature.
- **2. Have your Anthropic API key ready.** It starts with `sk-ant-`. You'll paste it into a file in Step 1, never into the chat.

That's all. **Prompt 1 does the rest of the set-up:** it installs uv (the Python tool) if your computer doesn't have it, downloads the lab's data file and creates the project.

One full research run makes about nine Claude calls with `claude-haiku-5-5`: a few US cents at most.

**You run the code yourself.** A prompt writes the code; the command under **Run it in your terminal** runs it, with its own Copy button. Open a terminal in your project folder: in VS Code, Cursor, Windsurf or Antigravity, **Terminal → New Terminal**; in Claude Code you can also type `!` and then the command. If the output doesn't match the Checkpoint, paste it back into the chat.

**Tested on 26 Nov 2026.** We pasted these exact six prompts, in one conversation, into Claude Code 2.1.331 (four runs) and Codex 0.171.0 (four runs), then ran `uv run test_research.py` once on each build. Claude Code: 3 of 4 builds passed 10/10; the fourth scored 8/10, because a Scenario 1 photography search containing "photojournalism" counted as a writing search, and two report findings lost their sources. Codex: 3 of 4 passed 10/10; the fourth scored 9/10, because its build added its own limit on a third search, which counted as a failed tool call. After these runs `sources.json` lists visual arts before writing, so that photography query now maps to visual arts; we checked this offline against all 146 search queries from our runs (only that one changed sector), but have not re-run the builds since. Our `solution/` passed 10/10 in 4 of 4 runs, also before the reorder. Not a benchmark: your tool, model and wording will differ. Antigravity has no headless mode, so we couldn't machine-test it; the prompts use no tool-specific features.

## Step 1 · Set up the project (5 minutes)

### Prompt 1

```text
Set up this folder as a new Python project for a multi-agent research team. Do each step, then tell me what you did.

1. Check uv with `uv --version`. If uv is missing, install it with its official installer:
   macOS or Linux: curl -LsSf https://astral.sh/uv/install.sh | sh
   Windows (PowerShell): powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
   If uv is still not found after installing, use its full path (~/.local/bin/uv, or %USERPROFILE%\.local\bin\uv.exe
   on Windows) for the rest of this chat.
2. If sources.json is not in this folder, download it into this folder from
   https://raw.githubusercontent.com/tertiarycourses/C437-Claude-Certified-Architect-Foundations-Certification/main/labs/lab-35-build-a-multi-agent-research-team/starter/sources.json
3. Run `uv init --bare`, then `uv add anthropic python-dotenv`. (uv installs Python itself if it needs to.)
4. Create .gitignore with: .env, .venv/, __pycache__/, report.json, report.md
5. Create .env.example with one line: ANTHROPIC_API_KEY=paste-your-key-here
   If .env does not exist yet, create it with that same line. After that, never open, print or ask me for .env or my key.
6. Create AGENTS.md with these project rules for any AI coding assistant:
   - Claude model: claude-haiku-5-5 through the official anthropic Python SDK, max_tokens 8000.
   - All research data comes from sources.json, a fictional sandbox. Never invent a source, URL or number.
   - A subagent sees only its task text. Never pass one agent's message history to another agent.
   - Run Python with `uv run`.
   - Never open, print or ask for .env or the API key.
7. Create CLAUDE.md containing the single line @AGENTS.md so Claude Code reads the same rules.

Then show me the file tree, and tell me to open .env in the editor and replace paste-your-key-here with my API key.
```

**Checkpoint.** You see `pyproject.toml`, `uv.lock`, `.gitignore`, `.env.example`, `AGENTS.md`, `CLAUDE.md` and `sources.json`.

**Now the one thing you type yourself:** open `.env` in your editor, replace `paste-your-key-here` with your API key and save. Never paste the key into the AI chat: anything you type there is sent to the coding tool's servers. If Prompt 1 installed uv, restart your coding tool's terminal before you run commands yourself.

## Step 2 · Write the two tools (10 minutes)

### Prompt 2

```text
Read AGENTS.md and sources.json. Create research_tools.py with the research team's two tools. Both read sources.json.

1. sector_of(text): return the first sector in sources.json "sectors" (in file order) whose keyword appears in the
   lower-cased text, or None.
2. search_web(query): find the query's sector with sector_of. No sector: return {"query", "sector": None, "results": []}.
   If that sector's "web" entry is a list, return {"query", "sector", "results": the list}. If it is an object with
   "error", raise ToolFailure("timeout", ...) carrying sector, attempted_query and its partial_results.
3. read_document(name): return the document from "documents" whose name matches (ignore case). Unknown name: raise
   ToolFailure("not_found", ...) carrying the list of available names.

- Give both tools a one-line docstring that says what they do and when to use them; read_document's tool description
  also lists the available document names.
- ToolFailure is an exception carrying errorCategory, isRetryable (false), message and any extra fields.
- Add TOOLS: a dict from tool name to its Anthropic tool definition (name, description, input_schema).
- Add run_tool(name, args) that returns (result, is_error). On ToolFailure it returns the error fields and True.

- Create check_tools.py: it calls run_tool for search_web "AI in music production", search_web "AI in film production"
  and read_document "BrightCanvas-Customer-Benchmark-2026.pdf", calls sector_of "AI in graphic design", and prints
  each result on one line.
```

**Run it in your terminal**, in your project folder:

```bash
uv run check_tools.py
```

**Checkpoint.** Music returns two results. Film returns `is_error True` with `errorCategory: timeout` **and** one `partial_results` hit: a failure that still tells you what it found (Day 1, Lab 27). Graphic design maps to `visual_arts`.

## Step 3 · Write the four subagents (10 minutes)

### Prompt 3

```text
Create agents.py with the research team's four subagents (web search, document analysis, synthesis, report
generation) and one function that runs any of them. Follow AGENTS.md.

- AGENTS is a dict: agent name -> {"tools": [tool names], "system": its system prompt}. Use these exactly:
  "search", tools ["search_web"], system:
    "You are a web-search subagent. Research only the sector named in your task, with at most two search_web calls.
    Return ONLY a JSON object: {"sector": str, "findings": [{"claim": str, "source_url": str, "source_title": str, "published": str}], "gaps": [str]}.
    Every claim must come from a search result; copy its url exactly. The search index is a small curated sandbox: treat its
    results as authoritative and do not comment on the sources. "gaps" lists only searches that failed or found nothing: if a
    search fails, keep any partial_results as findings and add a gap that says what failed and for which query. Never invent a source."
  "documents", tools ["read_document"], system:
    "You are a document-analysis subagent. Read every document named in your task with read_document.
    Return ONLY a JSON object: {"findings": [{"claim": str, "source": "<file name>, p.<page>", "evidence": "<kind of document and its method>"}], "gaps": [str]}.
    Say which findings are peer-reviewed and which come from a vendor. "gaps" lists only documents you could not read.
    Never invent a source."
  "synthesis", no tools, system:
    "You are a synthesis subagent. Combine the findings in your task into one evidence set, using ONLY those findings.
    Return ONLY a JSON object: {"findings": [{"sector": str, "claim": str, "source": str, "evidence": str}], "conflicts": [str], "gaps": [str]}.
    Group the findings by sector. "source" is ONLY the url or "<file name>, p.<page>", copied exactly: never a finding without one.
    "evidence" says what kind of source it is (survey, poll, peer-reviewed article, vendor benchmark). "conflicts" names
    figures that disagree or measure different things. "gaps" lists, one short line each, the failed searches, the searches
    that found nothing and the unreadable documents you were told about."
  "report", no tools, system:
    "You are a report-generation subagent. Write the final research report from the synthesized findings in your
    task, using ONLY those findings. Return ONLY a JSON object:
    {"title": str, "summary": str, "findings": [{"sector": str, "claim": str, "source": str}], "gaps": [str]}.
    Summary under 80 words. One finding per source: "claim" is one sentence with its number and evidence type, and "source"
    is ONLY the url or "<file name>, p.<page>", copied exactly: never a finding without one. "gaps": one short line per gap
    and one per conflict, at most 8 lines."
- run_subagent(agent, task): a FRESH agentic loop whose first and only user message is the task text. Pass only that
  agent's own tools (send no tools parameter when it has none). Same loop rules as Lab 31: append the whole
  response.content, all tool_result blocks in ONE user message with is_error, stop when stop_reason is not "tool_use"
  or after 6 turns. Refuse any tool that is not in the agent's list with an error tool_result.
  Return {"agent", "task", "text": the final text, "json": the JSON object parsed from the text (strip ``` fences;
  None if it does not parse), "calls": every tool call with tool, input, result and is_error}.
- agents.py run directly: uv run agents.py <agent> "<task>" prints each tool call, then the final text.
```

**Run it in your terminal**, in your project folder:

```bash
uv run agents.py search "Research how AI is affecting the film sector."
```

**Checkpoint.** The film search agent makes one or two `search_web` calls, both `timeout`. Its JSON still holds the Indie Screen Council finding from `partial_results`, plus a gap saying the film search timed out. It didn't crash, and it didn't pretend the search worked.

## Step 4 · Write the coordinator (10 minutes)

The coordinator's system prompt has six rules. **Rule 1 is its task decomposition**: it decides which subtasks the search agents get. This first version of rule 1 is a quick first draft that lists three subtasks itself: digital art, graphic design and photography. It looks reasonable. All three are creative work.

### Prompt 4

```text
Create research.py, the coordinator. It never searches, reads documents or writes the report itself: it delegates to
the four subagents in agents.py.

- One tool for Claude, "delegate", with input {agent: one of the AGENTS names (enum), task: string}. Description:
  "Give one task to a subagent and get its result back. agent: 'search' (web search on one sector), 'documents' (reads
  the internal PDFs), 'synthesis' (combines the findings you paste in), 'report' (writes the final cited report from
  the synthesis you paste in). The subagent sees ONLY the task text, never this conversation."
- Rule 1 of the system prompt is the task decomposition. Keep it in its own constant:
  RULE_1 = "1. Decompose the topic into three search subtasks: AI in digital art creation; AI in graphic design; AI in photography."
- SYSTEM is this system prompt exactly, with RULE_1 put in place of {rule_1}:
  "You are the coordinator of a research team. You never search, read documents or write the report yourself: you delegate.
  {rule_1}
  2. In ONE turn, delegate one "search" task per subtask (they run in parallel), plus one "documents" task that names
     both internal documents: Halden-Rao-2026-Journal-of-Creative-Economies.pdf and BrightCanvas-Customer-Benchmark-2026.pdf.
  3. Subagents see nothing but their task text. Put everything a subagent needs in its task.
  4. When the results are back, delegate ONE "synthesis" task. Paste into it every finding with its exact source and
     every gap the subagents reported.
  5. When the synthesis is back, delegate ONE "report" task. Paste the synthesis JSON into it, unchanged.
  6. Then reply with a two-sentence summary for the user."
- run_research(topic): the coordinator's agentic loop (claude-haiku-5-5, max 8 turns), user message
  "Research topic: <topic>". Run ALL the delegate calls from one turn AT THE SAME TIME with a ThreadPoolExecutor, then
  send every subagent's final text back as the tool_result blocks in ONE user message. Record each delegation
  (run_subagent's dict plus the coordinator turn number).
- coverage(delegations): the sectors that a search_web call actually hit (the result's sector, or sector_of the query
  when it failed) and the sectors in sources.json that were never searched.
- check_provenance(report), a gate in code: a finding whose source contains no URL or document name from
  sources.json is removed from findings and added to gaps as "Unsourced claim removed: <claim>". Print each one.
- run_research returns {"topic", "summary": the coordinator's final text, "report": the last report agent's JSON after
  check_provenance (or {}), "delegations", "searched", "missing"}.
- research.py run directly: uv run research.py "<topic>". First print "Coordinator rule 1: " and the rule in use. Print
  each coordinator turn with its stop_reason and number of delegations, each delegation with its agent, the first 90
  characters of its task and its tool calls (ok or the error category), and how many seconds the turn's subagents took.
  Write report.json and report.md (title, summary, one bullet per finding with its source, then the gaps). Print
  report.md, then "Coverage: searched ...; never searched: ...", then the coordinator's summary.
```

**Checkpoint.** `research.py` exists with `RULE_1`, `SYSTEM`, `run_research`, `coverage` and `check_provenance`. Now run it.

## Step 5 · Scenario 1: the coordinator's first plan (5 minutes, no code change)

**Run it in your terminal**, in your project folder:

```bash
uv run research.py "Impact of AI on creative industries"
```

Read the output. Did any agent fail? Which sectors does the report cover?

**Checkpoint.** Turn 1 sends **four delegations at once**: three searches (digital art, graphic design, photography) and one documents task. Turn 2 is the synthesis, turn 3 the report, turn 4 is `end_turn`. **Every subagent succeeds**: no errors, a tidy, cited, confident report. But it covers only visual arts, and the last line says `never searched: film, music, writing`. Music, writing and film are part of the creative industries too, and nobody looked at them.

## Step 6 · The fix: rule 1 of the coordinator's system prompt (5 minutes)

**Which agent caused it?** Check each one against your run:

| Agent | Did it fail? | What your run shows |
|---|---|---|
| Web search agents | No | Each searched its own subtask well. None of them was given music, writing or film. |
| Document analysis agent | No | It read both PDFs and reported both. |
| Synthesis agent | No | It combined every finding it was given. It can't add music it never received. |
| Report agent | No | It wrote up every finding from the synthesis, each with its source. |
| **Coordinator** | **Yes** | It split "creative industries" into three visual-arts subtasks. That split decided everything after it. |

**Where the fix goes: the coordinator's system prompt.** The coordinator decides the subtasks from two inputs: your topic (the user message) and its system prompt. Your topic, "creative industries", was already broad, so the narrowing came from **rule 1 of the system prompt**. You fix it by rewriting rule 1. That rule is a text string kept in `research.py` as `RULE_1`, so you edit `research.py`, but no program logic changes: no subagent, no tool, no loop.

**How the new rule fixes it.** The old rule handed the coordinator a finished list of three subtasks. The new rule makes it work out everything the topic covers first, and only then split the work, one search per sector, with the four sectors of this topic as the minimum:

```
1. Decompose the topic into the distinct sectors it spans before you split it. For creative industries, cover at
   least music, writing, film and visual arts: one search subtask per sector. Breadth first: a narrow plan makes a narrow report.
```

**What stays in code.** `coverage()` doesn't fix anything: it shows the gap. It compares the sectors actually searched with every sector in `sources.json` and prints `never searched: ...` on every run, whatever the prompt says. A report can look complete without being complete, so that check lives in code, not in a question to Claude.

### Prompt 5

```text
Fix the coordinator's task decomposition. Change only research.py, and in it only rule 1 of the coordinator's system
prompt. Do not change agents.py, research_tools.py or rules 2 to 6.

- Rename the RULE_1 constant to RULE_1_NARROW and keep its text: it is the first plan, used in Scenario 1.
- Add a new RULE_1, exactly:
  "1. Decompose the topic into the distinct sectors it spans before you split it. For creative industries, cover at
     least music, writing, film and visual arts: one search subtask per sector. Breadth first: a narrow plan makes a narrow report."
- SYSTEM puts RULE_1 in place of {rule_1}. run_research(topic, narrow=False) puts RULE_1_NARROW there instead when
  narrow is True, so Scenario 1 can still be replayed.
- research.py run directly takes an optional --narrow flag that calls run_research(topic, narrow=True). It still prints
  "Coordinator rule 1: " and the rule in use first.
```

**Checkpoint.** `research.py` now has `RULE_1_NARROW` (the old rule) and a new `RULE_1`. Nothing else changed: check with your tool's diff, or ask it "what did you change?".

## Step 7 · Scenario 2: the same topic, with the fix (5 minutes)

**Run it in your terminal**, in your project folder. Same command as Scenario 1:

```bash
uv run research.py "Impact of AI on creative industries"
```

**Checkpoint.** Turn 1 now sends **five or more delegations at once**: one search per sector and one documents task. They finish in roughly the time of the slowest one, not the sum (Day 1, Lab 3). Turn 2 is the synthesis, turn 3 the report, turn 4 `end_turn`. `report.md` cites a URL or PDF page for every claim (the provenance check removes any claim without one), flags BrightCanvas as a vendor poll, lists the film timeout under **Gaps**, and the last line says `never searched: none`.

To see both scenarios side by side, replay Scenario 1 with the old rule:

```bash
uv run research.py "Impact of AI on creative industries" --narrow
```

The only difference between the two runs is rule 1.

## Step 8 · Prove it with live tests (5 minutes)

### Prompt 6

```text
Write test_research.py. It imports run_research from research.py, does two live runs, prints PASS or FAIL for each
check, prints "N/10 checks passed" and exits 1 if any check fails. Check the recorded delegations and tool calls,
not Claude's wording. Print a heading before each scenario.

Scenario 1, BEFORE the fix: run_research("Impact of AI on creative industries", narrow=True)
  1. every subagent completed: each returned its JSON and none of its tool calls failed
  2. yet "missing" includes music, writing and film
Scenario 2, AFTER the fix: run_research("Impact of AI on creative industries")
  3. a search ran for every sector: music, writing, film, visual arts (nothing in "missing")
  4. two or more search delegations ran in the same coordinator turn (parallel)
  5. every subagent used only its own tools (search: search_web; documents: read_document; synthesis and report: none)
  6. the synthesis task carried the findings: at least 3 URLs from sources.json appear in its task text
  7. the report task carried the synthesis: at least 3 URLs from sources.json appear in its task text
  8. every finding's source in the report contains a URL or document name from sources.json
  9. the report's findings cite URLs from at least 3 different sectors
  10. one of the report's gaps mentions film
```

**Run it in your terminal**, in your project folder:

```bash
uv run test_research.py
```

If a check fails, paste this into your AI coding tool:

```text
test_research.py has a failing check. Run uv run test_research.py, show me which check fails and why, and fix
research.py or agents.py, not the test. Then run it again.
```

**Checkpoint.** `10/10 checks passed`. Scenario 1 proves the problem (every agent succeeds, three sectors missing); Scenario 2 proves the fix. Take a screenshot of the final lines: that's your evidence for this lab.

## Run it

From your project folder. Run them yourself in a terminal, or paste one into your coding tool's chat as "Run: <command> and show me the output."

| What | Command |
|---|---|
| Check the tools on their own | `uv run check_tools.py` |
| One subagent on its own | `uv run agents.py search "Research how AI is affecting the music sector."` |
| Scenario 2: the fixed team on the topic | `uv run research.py "Impact of AI on creative industries"` |
| Scenario 1 again: the first plan | `uv run research.py "Impact of AI on creative industries" --narrow` |
| The live tests: both scenarios, ten checks | `uv run test_research.py` |
| The last report | open `report.md` |

 Our run is in `sample-output.txt`.

## Stretch · The same team in the Claude Agent SDK

```text
Make sdk_team.py: the same research team built with the Claude Agent SDK (uv add claude-agent-sdk), model
claude-haiku-5-5. Define "search", "documents", "synthesis" and "report" as AgentDefinition subagents with the same
system prompts, expose search_web and read_document through an in-process SDK MCP server, give each subagent only its
own tool, and let the coordinator spawn them with the Task tool, using the fixed rule 1. sdk_team.py takes the topic
as its first argument.
```

**Run it in your terminal**, in your project folder:

```bash
uv run sdk_team.py "Impact of AI on creative industries"
```

Compare the two. The SDK runs the loops and the Task tool for you, but the rules don't change: a subagent knows only what its prompt says, and the coordinator's system prompt owns the plan.

## Explain it back (with your trainer)

- **1.** In Scenario 1 every subagent succeeded. Which agent caused the missing sectors, and which line did you change to fix it? Why not the synthesis or search agent's prompt? (Day 1, Lab 2.)
- **2.** The report agent never saw the search agents' work. How did the findings reach it? What happens if the coordinator writes only "write the report"?
- **3.** Why do `coverage()` and `check_provenance()` live in code instead of asking Claude whether the report is complete and cited?
- **4.** The film search failed, yet one film finding reached the report. Where did it come from, and why is it listed as a gap too? (Day 1, Lab 27.)

## Troubleshooting

| You see | Fix prompt |
|---|---|
| Scenario 1 already searches music, writing or film | "Rule 1 must be RULE_1 exactly as given, put into SYSTEM in place of {rule_1}. Don't add sectors to the user message." |
| The delegations run one after another (turn time = the sum) | "Run every delegate call from one coordinator turn at the same time with a ThreadPoolExecutor." |
| The coordinator searches one sector per turn | "Rule 2 says delegate every search in ONE turn. Keep the system prompt exactly as given." |
| `report.json` is `{}` | "The report agent's reply must parse as JSON: strip ``` fences, and set max_tokens to 8000." |
| A report URL isn't in sources.json, or real findings are removed as unsourced | "The synthesis and report tasks must paste every finding with its exact source; "source" holds only the URL or "<file>, p.<page>"." |
| `--narrow` still searches music | "With --narrow, SYSTEM must use RULE_1_NARROW in place of {rule_1}; don't add the plan to the user message." |
| The film timeout disappears | "On a failed search, keep partial_results as findings and add a gap; never return an empty success." |
| Test check 2 fails once: Scenario 1 searched film, music or writing | A Scenario 1 search query used another sector's word (for example "film photography"). Run `uv run test_research.py` again. If it repeats, paste: "In --narrow runs the coordinator must use RULE_1_NARROW only, and each search task names only its subtask." |
| Test check 1 fails: a search_web call shows a limit error you never asked for | "Don't limit search_web calls in code: the search agent's system prompt already says at most two. Remove the limit." |
| `tool_use ids were found without tool_result blocks` | "Send every delegate tool_result in one user message right after the coordinator turn." |
