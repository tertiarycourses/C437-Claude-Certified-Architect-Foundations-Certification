# Claude Certified Architect - Foundations (CCAR-F) Exam Prep

Two days that take you through all 30 task statements of Anthropic's CCAR-F exam: you answer each one as an exam question, then watch Claude run it live.

| Course detail | Information |
|---|---|
| Course code | `C437` |
| Programme | Non-WSQ |
| Duration | 2 days / 15 hours (9:30am – 5:30pm daily) |
| Registration | [View course details and register](https://www.tertiarycourses.com.sg/claude-certified-architect-foundations-ccar-f-exam-prep.html) |
| Lab site | [Open the labs in your browser](https://tertiarycourses.github.io/C437-Claude-Certified-Architect-Foundations-Certification/) |

## About the course

The CCAR-F exam gives you 60 questions in 120 minutes, drawn from six scenarios and five domains, and it tests judgement more than recall. This course is built on that shape.

Day 1 needs no installation. Every one of the 30 task statements has a lab on the [lab site](https://tertiarycourses.github.io/C437-Claude-Certified-Architect-Foundations-Certification/): a four-option question in the exam's style, then a live run on `claude-haiku-5-5` with your own Anthropic API key, with the agentic loop, the code and each API request shown as it happens. A lab usually costs under one US cent.

Day 2 you build with prompts. In Labs 31 to 34 you paste copy-ready prompts into your AI coding tool (Claude Code, Codex, Antigravity or Cursor) and grow one customer resolution agent: the agentic loop, an MCP server for its tools, a PreToolUse hook that stops a $780 refund, and a PostToolUse hook with live tests. Lab 35 builds a coordinator and its subagents for a research team. The day ends with a 60-question practice exam.

## Learning outcomes

By the end of the course you will be able to:

- Design bounded agentic loops and multi-agent orchestration with explicit handoffs, state and stop conditions.
- Engineer reliable tool and MCP integrations with precise schemas, structured errors and least-privilege tool distribution.
- Configure Claude Code projects with scoped instructions, reusable skills, rules, plan mode and CI/CD workflows.
- Produce validated structured outputs using clear criteria, few-shot examples, batching and review loops.
- Manage context, uncertainty, provenance and human escalation in large, long-running AI systems.

## Topics covered

| Topic | Exam domain | Exam weight | Labs |
|---|---|---:|---|
| Topic 1 | Agentic Architecture & Orchestration | 27% | 1–7 |
| Topic 2 | Tool Design & MCP Integration | 18% | 8–12 |
| Topic 3 | Claude Code Configuration & Workflows | 20% | 13–18 |
| Topic 4 | Prompt Engineering & Structured Output | 20% | 19–24 |
| Topic 5 | Context Management & Reliability | 15% | 25–30 |
| Bonus Topic A | Build a customer resolution agent with MCP and hooks | | 31–34 |
| Bonus Topic B | Build a multi-agent research team | | 35 |
| Bonus | Practice exam: 60 questions in Practice mode, then a score review by domain | | |

## Labs

Each lab has its own folder with a `README.md` and a PDF of every step.

### Day 1: one lab per task statement, live in your browser

**Topic 1: Agentic Architecture & Orchestration**

- Lab 1 (Task 1.1): [Watch one refund go round the loop](labs/lab-01-watch-one-refund-go-round-the-loop/README.md) · [run it](https://tertiarycourses.github.io/C437-Claude-Certified-Architect-Foundations-Certification/lab.html?n=1)
- Lab 2 (Task 1.2): [Every subagent succeeds, and the report still misses half the topic](labs/lab-02-every-subagent-succeeds-and-the-report/README.md) · [run it](https://tertiarycourses.github.io/C437-Claude-Certified-Architect-Foundations-Certification/lab.html?n=2)
- Lab 3 (Task 1.3): [A /parallel-review that can't fan out because Task isn't allowed](labs/lab-03-a-parallel-review-that-can-t-fan-out/README.md) · [run it](https://tertiarycourses.github.io/C437-Claude-Certified-Architect-Foundations-Certification/lab.html?n=3)
- Lab 4 (Task 1.4): [12% of cases skip get_customer: fix it with a gate, not a sentence](labs/lab-04-12-of-cases-skip-get-customer-fix-it/README.md) · [run it](https://tertiarycourses.github.io/C437-Claude-Certified-Architect-Foundations-Certification/lab.html?n=4)
- Lab 5 (Task 1.5): [The prompt forgot the $500 rule. The hook did not.](labs/lab-05-the-prompt-forgot-the-500-rule-the-hook/README.md) · [run it](https://tertiarycourses.github.io/C437-Claude-Certified-Architect-Foundations-Certification/lab.html?n=5)
- Lab 6 (Task 1.6): [60-page packets: section passes first, reconcile second](labs/lab-06-60-page-packets-section-passes-first/README.md) · [run it](https://tertiarycourses.github.io/C437-Claude-Certified-Architect-Foundations-Certification/lab.html?n=6)
- Lab 7 (Task 1.7): [Two attempts, one analysis: fork the session, checkpoint the files](labs/lab-07-two-attempts-one-analysis-fork-the/README.md) · [run it](https://tertiarycourses.github.io/C437-Claude-Certified-Architect-Foundations-Certification/lab.html?n=7)

**Topic 2: Tool Design & MCP Integration**

- Lab 8 (Task 2.1): [One analyze_document tool does three jobs badly](labs/lab-08-one-analyze-document-tool-does-three/README.md) · [run it](https://tertiarycourses.github.io/C437-Claude-Certified-Architect-Foundations-Certification/lab.html?n=8)
- Lab 9 (Task 2.2): [The refund failed. The customer was told it worked.](labs/lab-09-the-refund-failed-the-customer-was-told/README.md) · [run it](https://tertiarycourses.github.io/C437-Claude-Certified-Architect-Foundations-Certification/lab.html?n=9)
- Lab 10 (Task 2.3): [Review and test generation fight over one Claude call](labs/lab-10-review-and-test-generation-fight-over/README.md) · [run it](https://tertiarycourses.github.io/C437-Claude-Certified-Architect-Foundations-Certification/lab.html?n=10)
- Lab 11 (Task 2.4): [Commit the server, never the token](labs/lab-11-commit-the-server-never-the-token/README.md) · [run it](https://tertiarycourses.github.io/C437-Claude-Certified-Architect-Foundations-Certification/lab.html?n=11)
- Lab 12 (Task 2.5): [/find-callers needs Grep with a glob, not Bash](labs/lab-12-find-callers-needs-grep-with-a-glob-not/README.md) · [run it](https://tertiarycourses.github.io/C437-Claude-Certified-Architect-Foundations-Certification/lab.html?n=12)

**Topic 3: Claude Code Configuration & Workflows**

- Lab 13 (Task 3.1): [Which instructions actually reached Claude?](labs/lab-13-which-instructions-actually-reached/README.md) · [run it](https://tertiarycourses.github.io/C437-Claude-Certified-Architect-Foundations-Certification/lab.html?n=13)
- Lab 14 (Task 3.2): [Keep a noisy case review out of your main session](labs/lab-14-keep-a-noisy-case-review-out-of-your/README.md) · [run it](https://tertiarycourses.github.io/C437-Claude-Certified-Architect-Foundations-Certification/lab.html?n=14)
- Lab 15 (Task 3.3): [Testing rules for test files spread across every folder](labs/lab-15-testing-rules-for-test-files-spread/README.md) · [run it](https://tertiarycourses.github.io/C437-Claude-Certified-Architect-Foundations-Certification/lab.html?n=15)
- Lab 16 (Task 3.4): [Replacing the auth layer: nobody agrees on the boundary, so plan](labs/lab-16-replacing-the-auth-layer-nobody-agrees/README.md) · [run it](https://tertiarycourses.github.io/C437-Claude-Certified-Architect-Foundations-Certification/lab.html?n=16)
- Lab 17 (Task 3.5): [Two linked defects go in one detailed request](labs/lab-17-two-linked-defects-go-in-one-detailed/README.md) · [run it](https://tertiarycourses.github.io/C437-Claude-Certified-Architect-Foundations-Certification/lab.html?n=17)
- Lab 18 (Task 3.6): [The nightly job hangs because nobody can press Enter](labs/lab-18-the-nightly-job-hangs-because-nobody-can/README.md) · [run it](https://tertiarycourses.github.io/C437-Claude-Certified-Architect-Foundations-Certification/lab.html?n=18)

**Topic 4: Prompt Engineering & Structured Output**

- Lab 19 (Task 4.1): ["Only high confidence" didn't quiet the reviewer](labs/lab-19-only-high-confidence-didn-t-quiet-the/README.md) · [run it](https://tertiarycourses.github.io/C437-Claude-Certified-Architect-Foundations-Certification/lab.html?n=19)
- Lab 20 (Task 4.2): ["Clean this up" means three things: show which one you mean](labs/lab-20-clean-this-up-means-three-things-show/README.md) · [run it](https://tertiarycourses.github.io/C437-Claude-Certified-Architect-Foundations-Certification/lab.html?n=20)
- Lab 21 (Task 4.3): [Know your tool_choice options, and check what came back](labs/lab-21-know-your-tool-choice-options-and-check/README.md) · [run it](https://tertiarycourses.github.io/C437-Claude-Certified-Architect-Foundations-Certification/lab.html?n=21)
- Lab 22 (Task 4.4): [Retry when the format is wrong, stop when the data is absent](labs/lab-22-retry-when-the-format-is-wrong-stop-when/README.md) · [run it](https://tertiarycourses.github.io/C437-Claude-Certified-Architect-Foundations-Certification/lab.html?n=22)
- Lab 23 (Task 4.5): [Prove the template before 35,000 transcripts](labs/lab-23-prove-the-template-before-35-000/README.md) · [run it](https://tertiarycourses.github.io/C437-Claude-Certified-Architect-Foundations-Certification/lab.html?n=23)
- Lab 24 (Task 4.6): [14 files, shallow comments: split the review](labs/lab-24-14-files-shallow-comments-split-the/README.md) · [run it](https://tertiarycourses.github.io/C437-Claude-Certified-Architect-Foundations-Certification/lab.html?n=24)

**Topic 5: Context Management & Reliability**

- Lab 25 (Task 5.1): [Refund amount jumped to the wrong order](labs/lab-25-refund-amount-jumped-to-the-wrong-order/README.md) · [run it](https://tertiarycourses.github.io/C437-Claude-Certified-Architect-Foundations-Certification/lab.html?n=25)
- Lab 26 (Task 5.2): [55% first-contact resolution: calibrate with criteria and examples](labs/lab-26-55-first-contact-resolution-calibrate/README.md) · [run it](https://tertiarycourses.github.io/C437-Claude-Certified-Architect-Foundations-Certification/lab.html?n=26)
- Lab 27 (Task 5.3): [The search timed out: tell the coordinator everything](labs/lab-27-the-search-timed-out-tell-the/README.md) · [run it](https://tertiarycourses.github.io/C437-Claude-Certified-Architect-Foundations-Certification/lab.html?n=27)
- Lab 28 (Task 5.4): [Delegate the noisy search, keep a scratchpad](labs/lab-28-delegate-the-noisy-search-keep-a/README.md) · [run it](https://tertiarycourses.github.io/C437-Claude-Certified-Architect-Foundations-Certification/lab.html?n=28)
- Lab 29 (Task 5.5): [The aggregate masks a segment: break it and watch](labs/lab-29-the-aggregate-masks-a-segment-break-it/README.md) · [run it](https://tertiarycourses.github.io/C437-Claude-Certified-Architect-Foundations-Certification/lab.html?n=29)
- Lab 30 (Task 5.6): [A vendor benchmark isn't a peer-reviewed study](labs/lab-30-a-vendor-benchmark-isn-t-a-peer-reviewed/README.md) · [run it](https://tertiarycourses.github.io/C437-Claude-Certified-Architect-Foundations-Certification/lab.html?n=30)

### Day 2: two bonus topics, built with prompts

- Lab 31 (Bonus Topic A, Tasks 1.1, 2.1): [Vibe-code the customer resolution agent with the Python SDK](labs/lab-31-build-the-customer-resolution-agent/README.md) · [prompts](https://tertiarycourses.github.io/C437-Claude-Certified-Architect-Foundations-Certification/lab-31.html)
- Lab 32 (Bonus Topic A, Tasks 2.4, 2.2): [Vibe-code an MCP server for the agent's tools](labs/lab-32-move-the-tools-to-an-mcp-server/README.md) · [prompts](https://tertiarycourses.github.io/C437-Claude-Certified-Architect-Foundations-Certification/lab-32.html)
- Lab 33 (Bonus Topic A, Tasks 1.5, 1.4): [Vibe-code a PreToolUse hook that blocks the $780 refund](labs/lab-33-pretooluse-hook-blocks-the-780-refund/README.md) · [prompts](https://tertiarycourses.github.io/C437-Claude-Certified-Architect-Foundations-Certification/lab-33.html)
- Lab 34 (Bonus Topic A, Tasks 1.5): [Vibe-code a PostToolUse hook that cleans the data, then prove the agent works](labs/lab-34-posttooluse-hook-cleans-the-data/README.md) · [prompts](https://tertiarycourses.github.io/C437-Claude-Certified-Architect-Foundations-Certification/lab-34.html)
- Lab 35 (Bonus Topic B, Tasks 1.2, 1.3, 5.3): [Vibe-code a multi-agent research team](labs/lab-35-build-a-multi-agent-research-team/README.md) · [prompts](https://tertiarycourses.github.io/C437-Claude-Certified-Architect-Foundations-Certification/lab-35.html)

### Extra code builds (optional, not taught in class)

- Lab 36: [From one API call to a working agent loop](labs/lab-36-first-api-call-to-agent-loop/README.md)
- Lab 37: [Build the hooks that the prompt can't be trusted with](labs/lab-37-build-agent-hooks/README.md)
- Lab 38: [Be the coordinator: brief your subagents or they work blind](labs/lab-38-coordinator-and-subagents/README.md)
- Lab 39: [Write the tool description Claude actually reads](labs/lab-39-tool-design-and-tool-choice/README.md)
- Lab 40: [Build an MCP server once, plug it into any agent](labs/lab-40-build-an-mcp-server/README.md)
- Lab 41: [Teach Claude Code your repo: a /review skill and a rule that loads only for tests](labs/lab-41-skills-and-path-rules/README.md)
- Lab 42: [Put Claude Code in the pipeline and let the exit code decide](labs/lab-42-claude-code-in-ci/README.md)
- Lab 43: [Valid JSON is the floor: check the meaning yourself](labs/lab-43-structured-output/README.md)
- Lab 44: [Half price, no hurry: triage tickets with the Batches API](labs/lab-44-message-batches/README.md)
- Lab 45: [Keep the facts, cache the handbook](labs/lab-45-context-and-prompt-caching/README.md)
- Lab 46: [When a subagent fails, tell the coordinator everything](labs/lab-46-error-propagation/README.md)

The Day 1 labs also run locally on the Python simulators in [labs/simulators/](labs/simulators/); see [labs/START-LABS.md](labs/START-LABS.md).

## What is in this repository

| Item | Files |
|---|---|
| Trainer slides v3.0 | [PPTX](courseware/C437-Claude-Certified-Architect-Foundations-CCAR-F-Exam-Prep-Trainer-Slides-v3.0.pptx) · [PDF](courseware/C437-Claude-Certified-Architect-Foundations-CCAR-F-Exam-Prep-Trainer-Slides-v3.0.pdf) |
| Lesson Plan v2.0 | [DOCX](courseware/LP-Claude-Certified-Architect-Foundations-CCAR-F-Exam-Prep-v2.0.docx) · [PDF](courseware/LP-Claude-Certified-Architect-Foundations-CCAR-F-Exam-Prep-v2.0.pdf) |
| Learner Guide v2.0 | [DOCX](courseware/LG-Claude-Certified-Architect-Foundations-CCAR-F-Exam-Prep-v2.0.docx) · [PDF](courseware/LG-Claude-Certified-Architect-Foundations-CCAR-F-Exam-Prep-v2.0.pdf) · [Markdown](courseware/LG-Claude-Certified-Architect-Foundations-CCAR-F-Exam-Prep-v2.0.md) |
| Labs | [labs/](labs/): 46 lab folders and the six Python simulators |
| Lab site source | [docs/](docs/): the pages served at the lab site |

Your API key stays on your machine: the lab site keeps it in your browser only, and the Day 2 labs read it from a `.env` file that is never committed.

## Provider

Tertiary Infotech Academy Pte Ltd (UEN 201200696W) · [www.tertiarycourses.com.sg](https://www.tertiarycourses.com.sg)

This is independent exam-preparation courseware. Claude and the Claude Certified Architect exam are Anthropic's.
