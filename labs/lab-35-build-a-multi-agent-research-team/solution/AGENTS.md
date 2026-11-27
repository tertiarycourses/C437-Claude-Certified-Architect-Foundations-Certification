# Project rules for any AI coding assistant

- Claude model: claude-haiku-5-5 through the official anthropic Python SDK, max_tokens 8000.
- Research data comes from Claude's web search, the user's files in docs/, or sources.json (fixed sample data for
  test_research.py). Never invent a source, URL or number.
- A subagent sees only its task text. Never pass one agent's message history to another agent.
- Run Python with `uv run`.
- Never open, print or ask for .env or the API key.
