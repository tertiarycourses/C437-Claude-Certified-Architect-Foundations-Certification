"""The research team's own tools. read_document reads your files in docs/ (and the sample PDFs in sources.json).
search_web searches sources.json, the fixed sample data that test_research.py uses so its checks are repeatable.
For real research the search agent uses Claude's web search tool instead (see agents.py)."""
import json
from pathlib import Path

HERE = Path(__file__).parent
DATA = json.loads((HERE / "sources.json").read_text())
DOCS = HERE / "docs"
MAX_CHARS = 20000


class ToolFailure(Exception):
    def __init__(self, category, message, retryable=False, **extra):
        super().__init__(message)
        self.info = {"errorCategory": category, "isRetryable": retryable, "message": message, **extra}


def sector_of(text):
    """The first sector in sources.json whose keyword appears in the text, or None."""
    low = text.lower()
    return next((s for s, words in DATA["sectors"].items() if any(w in low for w in words)), None)


def search_web(query):
    """Search the sample data for recent surveys and reports on ONE area of the topic. Use a short query that names the area."""
    sector = sector_of(query)
    if sector is None:
        return {"query": query, "sector": None, "results": []}
    hits = DATA["web"][sector]
    if isinstance(hits, dict):                      # this sector's search always times out
        raise ToolFailure("timeout", f"search timed out for '{query}'", retryable=False,
                          sector=sector, attempted_query=query, partial_results=hits["partial_results"])
    return {"query": query, "sector": sector, "results": hits}


def my_documents():
    """The names of your files in docs/ (.txt, .md, .pdf)."""
    return sorted(p.name for p in DOCS.glob("*") if p.suffix.lower() in {".txt", ".md", ".pdf"}) if DOCS.is_dir() else []


def read_document(name):
    """Load one document by its exact file name: a file in docs/ or a sample PDF from sources.json."""
    path = DOCS / Path(name.strip()).name
    if path.is_file() and path.name in my_documents():
        if path.suffix.lower() == ".pdf":
            from pypdf import PdfReader
            text = "\n".join(page.extract_text() or "" for page in PdfReader(path).pages)
        else:
            text = path.read_text(errors="replace")
        return {"name": path.name, "kind": "your file in docs/", "text": text[:MAX_CHARS], "truncated": len(text) > MAX_CHARS}
    doc = next((d for d in DATA["documents"] if d["name"].lower() == name.strip().lower()), None)
    if doc is None:
        raise ToolFailure("not_found", f"no document named '{name}'",
                          available=my_documents() + [d["name"] for d in DATA["documents"]])
    return doc


FUNCTIONS = {"search_web": search_web, "read_document": read_document}
TOOLS = {
    "search_web": {"name": "search_web", "description": search_web.__doc__,
                   "input_schema": {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}},
    "read_document": {"name": "read_document", "description": read_document.__doc__,
                      "input_schema": {"type": "object", "properties": {"name": {"type": "string"}}, "required": ["name"]}},
}


def run_tool(name, args):
    """Run one tool. Returns (result, is_error)."""
    try:
        return FUNCTIONS[name](**args), False
    except ToolFailure as e:
        return e.info, True
