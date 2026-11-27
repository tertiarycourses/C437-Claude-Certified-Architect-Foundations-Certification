"""Check the tools on their own, no Claude call: uv run check_tools.py"""
import json

from research_tools import my_documents, run_tool, sector_of

for name, args in [("search_web", {"query": "AI in music production"}),
                   ("search_web", {"query": "AI in film production"}),
                   ("read_document", {"name": "BrightCanvas-Customer-Benchmark-2026.pdf"})]:
    result, is_error = run_tool(name, args)
    print(f"{name}({json.dumps(args)}) is_error={is_error} -> {json.dumps(result)}")
print(f'sector_of("AI in graphic design") -> {sector_of("AI in graphic design")}')
print(f"your documents in docs/: {my_documents()}")
