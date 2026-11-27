# Lab 35: Vibe-code a multi-agent research team

> Day 2 · Multi-Agent Research System · Task statements 1.2, 1.3, 5.3 · Vibe-coding lab · Claude Haiku 5.5 · 60 minutes

**Be the manager of your own AI research department, on any topic: "AI impact on the healthcare industry", "market research on one-person companies", your own business question. A coordinator splits the topic into areas and delegates to four subagents: one searches the web, one reads your documents, one synthesizes the findings and one writes the cited report. Then a test shows why the coordinator's first rule matters: with the narrow plan from the exam scenario, every agent succeeds and the report still misses three sectors.**

**Lab page:** [the main lab page](https://tertiarycourses.github.io/C437-Claude-Certified-Architect-Foundations-Certification/) lists every lab. Copy the prompts from [this lab's prompt page](https://tertiarycourses.github.io/C437-Claude-Certified-Architect-Foundations-Certification/lab-35.html) (one Copy button per prompt), or from `prompts.html` in this folder.

This is a **new project**, not the Orderly agent from Labs 31 to 34. Make a fresh folder for it.

## What you'll build

```
  uv run research.py "AI impact on the healthcare industry"
        |
        v
  research.py -- the coordinator (claude-haiku-5-5). It never searches,
        |        reads or writes the report itself: it delegates.
        |        Its rule 1 splits the topic into 4 to 6 areas.
        |
        |  turn 1, run in parallel:
        +--> 1. web search agent: one per area (Claude's web search) --+  each one: a fresh
        +--> 2. document analysis agent: your files in docs/, if any --+  conversation, only its
        |                                                                 own tool, only its task
        |  turn 2:
        +--> 3. synthesis agent: every finding + source + gap pasted in
        |  turn 3:
        +--> 4. report generation agent: the synthesis pasted in
        |
        v
  report.json + report.md: every claim cited, every gap listed

  uv run test_research.py: the same team on fixed sample data (sources.json),
  first with the exam scenario's narrow plan, then with rule 1. Ten checks.
```

On Day 1 you watched these failures in Lab 2 (a narrow plan), Lab 3 (searches that ran one by one), Lab 27 (a timeout hidden as success) and Lab 30 (a vendor number treated like a peer-reviewed one). Today you build a team that avoids all four, and a test that proves it.

## What's in this folder

| File | What it is |
|---|---|
| `starter/sources.json` | fixed sample data for the tests: search results for four creative sectors (film always times out) and two internal PDFs. Every name, number and URL is invented. Prompt 1 downloads it. |
| `starter/.env.example` | the one line your `.env` needs |
| `prompts.html` | every prompt below, each with a Copy button |
| `solution/` | our finished code, for your trainer. You don't need it: build your own with the prompts. |
| `sample-output.txt` | live runs of `solution/`: a healthcare topic, a market-research topic, then `test_research.py` with 10/10 checks |

## Before you start (5 minutes)

- **1. Open your AI coding tool in a new, empty folder** called `research-team` (a new folder, not `orderly-agent`). In VS Code, Cursor, Windsurf or Antigravity: **File → Open Folder → New Folder**. Claude Code or Codex in a terminal: start it from that folder. Any agent that can create files and run terminal commands works; the prompts use no tool-specific feature.
- **2. Have your Anthropic API key ready.** It starts with `sk-ant-`. You'll paste it into a file in Step 1, never into the chat.

That's all. **Prompt 1 does the rest of the set-up:** it installs uv (the Python tool) if your computer doesn't have it, downloads the lab's sample data and creates the project.

**Cost.** One research run makes about nine `claude-haiku-5-5` calls and about 12 web searches (web search costs US$10 per 1,000 searches): roughly US$0.15. `test_research.py` uses the sample data, no web searches: a few US cents. Web search must be switched on for your Claude Console organisation; Step 3 tells you if it isn't.

**You run the code yourself.** A prompt writes the code; the command under **Run it in your terminal** runs it, with its own Copy button. Open a terminal in your project folder: in VS Code, Cursor, Windsurf or Antigravity, **Terminal → New Terminal**; in Claude Code you can also type `!` and then the command. If the output doesn't match the Checkpoint, paste it back into the chat.

**Tested on 27 Nov 2026.** Our `solution/` ran live on "AI impact on the healthcare industry" (six areas, 23 cited findings), "Market research on one-person companies" (six areas, 18 cited findings) and a business question with a notes file in `docs/` (the documents agent read it), and passed `test_research.py` 10/10 in 2 of 2 runs. We also pasted the five prompts verbatim into Claude Code (one build): its code passed `check_tools.py`, but we couldn't run its live checks the same day, because our test API key had reached its monthly usage limit. Not a benchmark: your tool, model and wording will differ. Antigravity has no headless mode, so we couldn't machine-test it; the prompts use no tool-specific features.

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
3. Run `uv init --bare`, then `uv add anthropic python-dotenv pypdf`. (uv installs Python itself if it needs to.)
4. Create an empty docs/ folder: the user's own .txt, .md and .pdf files for the research team go there.
5. Create .gitignore with: .env, .venv/, __pycache__/, report.json, report.md
6. Create .env.example with one line: ANTHROPIC_API_KEY=paste-your-key-here
   If .env does not exist yet, create it with that same line. After that, never open, print or ask me for .env or my key.
7. Create AGENTS.md with these project rules for any AI coding assistant:
   - Claude model: claude-haiku-5-5 through the official anthropic Python SDK, max_tokens 8000.
   - Research data comes from Claude's web search, the user's files in docs/, or sources.json (fixed sample data for
     test_research.py). Never invent a source, URL or number.
   - A subagent sees only its task text. Never pass one agent's message history to another agent.
   - Run Python with `uv run`.
   - Never open, print or ask for .env or the API key.
8. Create CLAUDE.md containing the single line @AGENTS.md so Claude Code reads the same rules.

Then show me the file tree, and tell me to open .env in the editor and replace paste-your-key-here with my API key.
```

**Checkpoint.** You see `pyproject.toml`, `uv.lock`, `.gitignore`, `.env.example`, `AGENTS.md`, `CLAUDE.md`, `sources.json` and an empty `docs/` folder.

**Now the one thing you type yourself:** open `.env` in your editor, replace `paste-your-key-here` with your API key and save. Never paste the key into the AI chat: anything you type there is sent to the coding tool's servers. If Prompt 1 installed uv, restart your coding tool's terminal before you run commands yourself.

## Step 2 · Write the team's own tools (10 minutes)

The web search agent will use Claude's own web search tool, which runs on Anthropic's servers. You write the team's other tools yourself: one reads documents, one searches the fixed sample data that the tests use.

### Prompt 2

```text
Read AGENTS.md and sources.json. Create research_tools.py with the research team's own tools.

1. sector_of(text): return the first sector in sources.json "sectors" (in file order) whose keyword appears in the
   lower-cased text, or None.
2. search_web(query), over the sample data: find the query's sector with sector_of. No sector: return {"query",
   "sector": None, "results": []}. If that sector's "web" entry is a list, return {"query", "sector", "results": the
   list}. If it is an object with "error", raise ToolFailure("timeout", ...) carrying sector, attempted_query and its
   partial_results.
3. my_documents(): the sorted names of the .txt, .md and .pdf files in docs/ (empty if docs/ is missing).
4. read_document(name): if name is one of my_documents(), return {"name", "kind": "your file in docs/", "text",
   "truncated"}: the text of a .txt or .md file, or of every page of a .pdf (pypdf), cut to 20,000 characters, with
   truncated true when it was cut. Otherwise return the document from sources.json "documents" whose name matches
   (ignore case). Unknown name: raise ToolFailure("not_found", ...) carrying the list of available names.

- Give both tools a one-line docstring that says what they do and when to use them.
- ToolFailure is an exception carrying errorCategory, isRetryable (false), message and any extra fields.
- Add TOOLS: a dict from tool name to its Anthropic tool definition (name, description, input_schema).
- Add run_tool(name, args) that returns (result, is_error). On ToolFailure it returns the error fields and True.

- Create check_tools.py: it calls run_tool for search_web "AI in music production", search_web "AI in film production"
  and read_document "BrightCanvas-Customer-Benchmark-2026.pdf", calls sector_of "AI in graphic design", prints
  my_documents(), and prints each result on one line.
```

**Run it in your terminal**, in your project folder:

```bash
uv run check_tools.py
```

**Checkpoint.** Music returns two results. Film returns `is_error True` with `errorCategory: timeout` **and** one `partial_results` hit: a failure that still tells you what it found (Day 1, Lab 27). Graphic design maps to `visual_arts`. Your documents: `[]` for now.

## Step 3 · Write the four subagents (10 minutes)

### Prompt 3

```text
Create agents.py with the research team's four subagents (web search, document analysis, synthesis, report
generation) and one function that runs any of them. Follow AGENTS.md.

- WEB_SEARCH = {"type": "web_search_20250305", "name": "web_search", "max_uses": 2}: Claude's server-side web search.
- AGENTS is a dict: agent name -> {"tools": [tool names], "system": its system prompt}. Use these exactly:
  "search", tools ["web_search"], system:
    "You are a web-search subagent. Research only the area named in your task, with at most two web searches.
    Prefer recent surveys, official statistics, peer-reviewed studies and industry reports.
    Return ONLY a JSON object: {"area": str, "findings": [{"claim": str, "source_url": str, "source_title": str, "published": str}], "gaps": [str]}.
    Every claim must come from a search result in this conversation; copy its url exactly, and put "unknown" when a result
    shows no date. Return at most four findings, each one sentence with its number. "gaps" lists only searches that failed or
    found nothing relevant. Never invent a source, URL or number."
  "documents", tools ["read_document"], system:
    "You are a document-analysis subagent. Read every document named in your task with read_document.
    Return ONLY a JSON object: {"findings": [{"claim": str, "source": "<file name>, p.<page>", "evidence": "<kind of document and its method>"}], "gaps": [str]}.
    Leave out ", p.<page>" when a document has no page. Say which findings are peer-reviewed, which come from a vendor and
    which come from the user's own files. "gaps" lists only documents you could not read. Never invent a source."
  "synthesis", no tools, system:
    "You are a synthesis subagent. Combine the findings in your task into one evidence set, using ONLY those findings.
    Return ONLY a JSON object: {"findings": [{"area": str, "claim": str, "source": str, "evidence": str}], "conflicts": [str], "gaps": [str]}.
    Group the findings by area. "source" is ONLY the url or "<file name>, p.<page>", copied exactly: never a finding without one.
    "evidence" says what kind of source it is (survey, poll, peer-reviewed article, vendor benchmark). "conflicts" names
    figures that disagree or measure different things. "gaps" lists, one short line each, the failed searches, the searches
    that found nothing and the unreadable documents you were told about."
  "report", no tools, system:
    "You are a report-generation subagent. Write the final research report from the synthesized findings in your
    task, using ONLY those findings. Return ONLY a JSON object:
    {"title": str, "summary": str, "findings": [{"area": str, "claim": str, "source": str}], "gaps": [str]}.
    Summary under 80 words. One finding per source: "claim" is one sentence with its number and evidence type, and "source"
    is ONLY the url or "<file name>, p.<page>", copied exactly: never a finding without one. "gaps": one short line per gap
    and one per conflict, at most 8 lines."
- SAMPLE_SEARCH_SYSTEM, the search agent's prompt on the sample data, exactly:
    "You are a web-search subagent. Research only the area named in your task, with at most two search_web calls.
    Return ONLY a JSON object: {"area": str, "findings": [{"claim": str, "source_url": str, "source_title": str, "published": str}], "gaps": [str]}.
    Every claim must come from a search result; copy its url exactly. The search index is a small curated sample: treat its
    results as authoritative and do not comment on the sources. "gaps" lists only searches that failed or found nothing: if a
    search fails, keep any partial_results as findings and add a gap that says what failed and for which query. Never invent a source."
- run_subagent(agent, task, sample=False): a FRESH agentic loop whose first and only user message is the task text.
  Pass only that agent's own tools (WEB_SEARCH for "web_search", TOOLS from research_tools.py for the others; send no
  tools parameter when it has none). With sample=True the "search" agent gets search_web and SAMPLE_SEARCH_SYSTEM instead.
  Same loop rules as Lab 31: append the whole response.content, all tool_result blocks in ONE user message with
  is_error, stop when stop_reason is not "tool_use" or after 6 turns. Refuse any tool that is not in the agent's list
  with an error tool_result. Web searches run on the server inside one response: record every server_tool_use block
  named web_search as a call (tool "web_search", its input, is_error) with its matching web_search_tool_result: a list
  is a success (keep each result's url, title, and page_age as "published"); anything else is an error (errorCategory =
  its error_code). When stop_reason is "pause_turn", call again with the same messages (no new user message).
  Return {"agent", "task", "text": the final text, "json": the JSON object parsed from the text (strip ``` fences;
  None if it does not parse), "calls": every tool call with tool, input, result and is_error}.
- agents.py run directly: uv run agents.py <agent> "<task>" prints each tool call, then the final text.
```

**Run it in your terminal**, in your project folder:

```bash
uv run agents.py search "Research how AI is changing medical imaging."
```

**Checkpoint.** The search agent makes one or two `web_search` calls, then prints JSON with up to four findings, each with a real URL from its own search results. If you get an API error that says web search isn't enabled, web search is switched off for your Claude Console organisation: ask its admin to switch it on.

## Step 4 · Write the coordinator (10 minutes)

The coordinator's system prompt has six rules. **Rule 1 is its task decomposition**: it decides which areas the search agents get, so it decides what the report can cover. The rule says *how* to plan, not *what* to plan, so it works on any topic. Keep the narrow first plan from the exam scenario beside it: the test in Step 7 uses it.

### Prompt 4

```text
Create research.py, the coordinator. It never searches, reads documents or writes the report itself: it delegates to
the four subagents in agents.py.

- One tool for Claude, "delegate", with input {agent: one of the AGENTS names (enum), task: string}. Description:
  "Give one task to a subagent and get its result back. agent: 'search' (web search on one area), 'documents' (reads
  the documents you name), 'synthesis' (combines the findings you paste in), 'report' (writes the final cited report
  from the synthesis you paste in). The subagent sees ONLY the task text, never this conversation."
- Rule 1 of the system prompt is the task decomposition. Keep it in its own constant, exactly:
  RULE_1 = "1. Decompose the topic into the distinct areas it spans (sectors, segments or questions) before you split it,
     and cover the four to six major ones: one search subtask per area. For example, creative industries span at least
     music, writing, film and visual arts. Breadth first: a narrow plan makes a narrow report."
  And the narrow first plan from the exam scenario, used only by the tests:
  RULE_1_NARROW = "1. Decompose the topic into three search subtasks: AI in digital art creation; AI in graphic design; AI in photography."
- SYSTEM is this system prompt exactly, with a rule 1 in place of {rule_1} and the documents clause in place of {documents}:
  "You are the coordinator of a research team. You never search, read documents or write the report yourself: you delegate.
  {rule_1}
  2. In ONE turn, delegate one "search" task per subtask (they run in parallel){documents}.
  3. Subagents see nothing but their task text. Put everything a subagent needs in its task.
  4. When the results are back, delegate ONE "synthesis" task. Paste into it every finding with its exact source and
     every gap the subagents reported.
  5. When the synthesis is back, delegate ONE "report" task. Paste the synthesis JSON into it, unchanged.
  6. Then reply with a two-sentence summary for the user."
  The documents are my_documents() (or, with sample=True, the two document names in sources.json). If there are any,
  {documents} is ', plus one "documents" task that names these documents: <names, comma-separated>'. If there are
  none, it is '. There are no documents to read: send no "documents" task'.
- run_research(topic, narrow=False, sample=False): the coordinator's agentic loop (claude-haiku-5-5, max 8 turns), user
  message "Research topic: <topic>". narrow=True uses RULE_1_NARROW; sample=True passes sample=True to every
  run_subagent call. Run ALL the delegate calls from one turn AT THE SAME TIME with a ThreadPoolExecutor, then send
  every subagent's final text back as the tool_result blocks in ONE user message. Record each delegation (run_subagent's
  dict plus the coordinator turn number). If a turn stops with stop_reason "max_tokens", print "STOPPED: the
  coordinator ran out of max_tokens while writing its delegations".
- coverage(delegations, sample=False): with sample=True, the sectors that a search_web call actually hit (the result's
  sector, or sector_of the query when it failed) and the sectors in sources.json that were never searched. Otherwise,
  the areas the search agents covered (each one's JSON "area") and those whose web searches all failed or found nothing.
- check_provenance(report, delegations), a gate in code: a finding whose source contains no URL that a search returned
  in this run (results or partial_results) and no known document name is removed from findings and added to gaps as
  "Unsourced claim removed: <claim>". Print each one with its claim and its source.
- run_research returns {"topic", "summary": the coordinator's final text, "report": the last report agent's JSON after
  check_provenance (or {}), "delegations", "searched", "missing"}.
- research.py run directly: uv run research.py "<topic>". With no topic, ask "What should the research team look
  into? " and read it from the keyboard. Print the topic and the documents in docs/, each coordinator turn with its
  stop_reason and number of delegations, each delegation with its agent, the first 90 characters of its task and its
  tool calls (ok or the error category), and how many seconds the turn's subagents took. Write report.json and
  report.md (title, summary, one bullet per finding with its area and source, then the gaps). Print report.md, then
  "Coverage: searched <areas>. Found nothing for: <areas>", then the coordinator's summary.
```

**Checkpoint.** `research.py` exists with `RULE_1`, `RULE_1_NARROW`, `SYSTEM`, `run_research`, `coverage` and `check_provenance`.

## Step 5 · Research anything (10 minutes)

**Run it in your terminal**, in your project folder:

```bash
uv run research.py "AI impact on the healthcare industry"
```

**Checkpoint.** Turn 1 sends **four to six search delegations at once**, one per area your coordinator picked (for example diagnostics, drug discovery, clinical operations, patient care, regulation), and no documents task, because `docs/` is empty. Each search agent shows one or two `web_search(...) ok` calls. They finish in roughly the time of the slowest one, not the sum (Day 1, Lab 3). Then come the synthesis, the report and `end_turn`, in about two minutes. `report.md` cites a real URL for every claim. The provenance check moves any claim whose URL no search in this run returned to **Gaps**, and prints it.

Now your own topic. Type it after the command, or run the command on its own and the team asks you:

```bash
uv run research.py "Market research on one-person companies"
```

```bash
uv run research.py
```

**Your own documents.** Put a `.txt`, `.md` or `.pdf` file in `docs/` (your business notes, a report you trust) and run a topic again. Turn 1 now also sends a **documents** task that names your file, and the report cites it next to the web sources.

## Step 6 · Why rule 1 matters (5 minutes)

The exam's multi-agent research scenario describes a coordinator whose report on "the impact of AI on creative industries" covers only visual arts. Every subagent completed its task successfully. The coordinator had split the topic into three subtasks: digital art, graphic design and photography. That is `RULE_1_NARROW`. In Step 7 the test runs your team with it, then with your rule 1, on the same fixed sample data, so you can see which agent caused the gap:

| Agent | Did it fail? | What the narrow run shows |
|---|---|---|
| Web search agents | No | Each searched its own subtask well. None of them was given music, writing or film. |
| Document analysis agent | No | It read both PDFs and reported both. |
| Synthesis agent | No | It combined every finding it was given. It can't add music it never received. |
| Report agent | No | It wrote up every finding from the synthesis, each with its source. |
| **Coordinator** | **Yes** | It split "creative industries" into three visual-arts subtasks. That split decided everything after it. |

**Where the fix goes: the coordinator's system prompt.** The coordinator decides the subtasks from two inputs: the topic and its system prompt. The topic was already broad, so the narrowing came from **rule 1**. Your `RULE_1` makes it work out the areas a topic spans first, and only then split the work. That's why the same team handles healthcare, market research or creative industries without a code change.

**What stays in code.** `coverage()` doesn't fix anything: it shows the gap. On the sample data it compares the sectors actually searched with every sector in `sources.json`, so a narrow plan prints `never searched: ...` whatever the report says. `check_provenance()` drops any claim no search returned. A report can look complete and cited without being either, so those checks live in code, not in a question to Claude.

## Step 7 · Prove it with live tests (10 minutes)

The tests run on the fixed sample data, not the web: web results change from run to run, the sample data doesn't, so the same ten checks pass or fail for the same reason every time.

### Prompt 5

```text
Write test_research.py. It imports run_research from research.py, does two live runs on the sample data, prints PASS
or FAIL for each check, prints "N/10 checks passed" and exits 1 if any check fails. Check the recorded delegations and
tool calls, not Claude's wording. Print a heading before each scenario.

Scenario 1, the narrow plan: run_research("Impact of AI on creative industries", narrow=True, sample=True)
  1. every subagent completed: each returned its JSON and none of its tool calls failed
  2. yet "missing" includes music, writing and film
Scenario 2, rule 1: run_research("Impact of AI on creative industries", sample=True)
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

**Checkpoint.** `10/10 checks passed`. Scenario 1: four delegations, every subagent succeeds, and check 2 still finds music, writing and film never searched. Scenario 2: five or more delegations at once, every sector searched, the film timeout listed under Gaps, BrightCanvas flagged as a vendor poll. The only difference between the two runs is rule 1. Take a screenshot of the final lines: that's your evidence for this lab.

## Run it

From your project folder. Run them yourself in a terminal, or paste one into your coding tool's chat as "Run: <command> and show me the output."

| What | Command |
|---|---|
| Research any topic | `uv run research.py "AI impact on the healthcare industry"` |
| Let the team ask for the topic | `uv run research.py` |
| Use your own documents too | put `.txt`, `.md` or `.pdf` files in `docs/`, then research a topic |
| One search agent on its own | `uv run agents.py search "Research how AI is changing medical imaging."` |
| Check the tools on their own | `uv run check_tools.py` |
| The live tests: the narrow plan, then rule 1, ten checks | `uv run test_research.py` |
| The last report | open `report.md` |

 Our runs are in `sample-output.txt`.

## Stretch · The same team in the Claude Agent SDK

```text
Make sdk_team.py: the same research team built with the Claude Agent SDK (uv add claude-agent-sdk), model
claude-haiku-5-5. Define "search", "documents", "synthesis" and "report" as AgentDefinition subagents with the same
system prompts, give the search agent the SDK's WebSearch tool and expose read_document through an in-process SDK MCP
server, give each subagent only its own tool, and let the coordinator spawn them with the Task tool, using RULE_1.
sdk_team.py takes the topic as its first argument.
```

**Run it in your terminal**, in your project folder:

```bash
uv run sdk_team.py "AI impact on the healthcare industry"
```

Compare the two. The SDK runs the loops and the Task tool for you, but the rules don't change: a subagent knows only what its prompt says, and the coordinator's system prompt owns the plan.

## Explain it back (with your trainer)

- **1.** In the test's Scenario 1 every subagent succeeded. Which agent caused the missing sectors, and which line fixes it? Why not the synthesis or search agent's prompt? (Day 1, Lab 2.)
- **2.** The report agent never saw the search agents' work. How did the findings reach it? What happens if the coordinator writes only "write the report"?
- **3.** Why do `coverage()` and `check_provenance()` live in code instead of asking Claude whether the report is complete and cited?
- **4.** On the sample data the film search fails, yet one film finding reaches the report. Where does it come from, and why is it listed as a gap too? (Day 1, Lab 27.)
- **5.** The tests run on fixed sample data, not the web. What could a test on live web results check, and what couldn't it?

## Troubleshooting

| You see | Fix prompt |
|---|---|
| An API error that says web search is not enabled | Web search is switched off for your Claude Console organisation. Ask its admin to switch it on. `uv run test_research.py` still works: it uses the sample data. |
| The delegations run one after another (turn time = the sum) | "Run every delegate call from one coordinator turn at the same time with a ThreadPoolExecutor." |
| The coordinator searches one area per turn | "Rule 2 says delegate every search in ONE turn. Keep the system prompt exactly as given." |
| `STOPPED: the coordinator ran out of max_tokens` and an empty report | The plan was too wide. "Rule 1 must say four to six areas, and each search agent returns at most four findings." |
| `report.json` is `{}` | "The report agent's reply must parse as JSON: strip ``` fences, and set max_tokens to 8000." |
| Many findings are moved to Gaps as unsourced | "The synthesis and report tasks must paste every finding with its exact source; "source" holds only the URL or "<file>, p.<page>". check_provenance must accept the URLs that the web_search calls returned in this run." |
| A file in `docs/` is never read | "When docs/ holds files, rule 2 must name them in one documents task. my_documents() lists .txt, .md and .pdf files." |
| Scenario 1 of the test already searches music, writing or film | "With narrow=True, SYSTEM must use RULE_1_NARROW in place of {rule_1}; don't add sectors to the user message." |
| The film timeout disappears from the test's report | "On a failed search, keep partial_results as findings and add a gap; never return an empty success." |
| Test check 2 fails once: Scenario 1 searched film, music or writing | A Scenario 1 search query used another sector's word (for example "film photography" or "animation"). Run `uv run test_research.py` again. If it repeats, paste: "In narrow runs each search task names only its subtask." |
| Test check 1 fails: a search_web call shows a limit error you never asked for | "Don't limit search_web calls in code: the search agent's system prompt already says at most two. Remove the limit." |
| `tool_use ids were found without tool_result blocks` | "Send every delegate tool_result in one user message right after the coordinator turn." |
