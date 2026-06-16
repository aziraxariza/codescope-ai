"""
Architecture diagram generator.
Queries Neo4j for cross-file CALLS relationships and
converts them into a Mermaid.js graph string.

The frontend renders the Mermaid string client-side —
no extra infrastructure needed.
"""

import re

from ..graph.neo4j_client import GraphDB

_db = GraphDB()


def _sanitize(name: str) -> str:
    """
    Convert a file name into a valid Mermaid node ID.
    Strips .py extension, replaces non-alphanumeric chars with underscores.
    """
    name = name.split("/")[-1]          # keep only the filename
    name = name.replace(".py", "")      # strip extension
    name = re.sub(r"[^a-zA-Z0-9]", "_", name)  # sanitize
    return name.strip("_") or "unknown"


def generate_file_diagram() -> str:
    """
    Generate a Mermaid graph TD diagram showing file-level architecture.
    Each arrow represents at least one cross-file function call.
    Returns a Mermaid diagram string.
    """
    try:
        edges = _db.query(
            """
            MATCH (a:Function)-[:CALLS]->(b:Function)
            WHERE a.file IS NOT NULL
              AND b.file IS NOT NULL
              AND a.file <> b.file
            RETURN DISTINCT
              a.file AS src_file,
              b.file AS dst_file
            LIMIT 30
            """
        )
    except Exception as e:
        return f"graph TD\n  A[Graph unavailable: {str(e)[:40]}]"

    if not edges:
        return "graph TD\n  A[No cross-file calls found\\nAnalyze a repo first]"

    lines = ["graph TD"]
    seen: set[str] = set()

    for edge in edges:
        src = _sanitize(edge.get("src_file", ""))
        dst = _sanitize(edge.get("dst_file", ""))

        if not src or not dst or src == dst:
            continue

        key = f"{src}-->{dst}"
        if key not in seen:
            lines.append(f"  {src} --> {dst}")
            seen.add(key)

    if len(lines) == 1:
        return "graph TD\n  A[No cross-file relationships found]"

    return "\n".join(lines)


def generate_class_diagram() -> str:
    """
    Generate a Mermaid classDiagram showing classes and their methods.
    Returns a Mermaid diagram string.
    """
    try:
        classes = _db.query(
            """
            MATCH (c:Class)
            OPTIONAL MATCH (f:Function {cls: c.name})
            RETURN c.name AS cls, collect(DISTINCT f.name)[0..4] AS methods
            LIMIT 12
            """
        )
    except Exception:
        return "classDiagram\n  class NoData"

    if not classes:
        return "classDiagram\n  class NoClasses"

    lines = ["classDiagram"]
    for row in classes:
        cls = re.sub(r"[^a-zA-Z0-9_]", "_", row.get("cls") or "Unknown")
        lines.append(f"  class {cls}")
        for method in (row.get("methods") or [])[:4]:
            m = re.sub(r"[^a-zA-Z0-9_]", "_", method)
            lines.append(f"  {cls} : +{m}()")

    return "\n".join(lines)
