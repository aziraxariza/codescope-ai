"""
Repository parser using tree-sitter.
Clones a GitHub repo and extracts all functions, classes,
and call relationships into a list of structured dicts.
"""

import os
import subprocess
import shutil
import stat
from typing import Any

from tree_sitter_languages import get_parser

def _remove_readonly(func, path, exc_info):
    """Handle read-only file deletion on Windows (used by .git internals)."""
    os.chmod(path, stat.S_IWRITE)
    func(path)

def clone_repo(github_url: str, dest: str = "/tmp/repo") -> str:
    if os.path.exists(dest):
        shutil.rmtree(dest, onerror=_remove_readonly)
    result = subprocess.run(
        ["git", "clone", "--depth=1", github_url, dest],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"git clone failed: {result.stderr}")
    return dest


def extract_calls(node: Any, source: bytes) -> list[str]:
    """
    Walk a function AST node and collect all function call names.
    Returns a deduplicated list of callee name strings.
    """
    calls: list[str] = []

    def find_calls(n: Any) -> None:
        if n.type == "call":
            fn_node = n.child_by_field_name("function")
            if fn_node:
                name = fn_node.text.decode(errors="ignore").strip()
                # Strip method chains: "self.validate" → "validate"
                name = name.split(".")[-1]
                if name:
                    calls.append(name)
        for child in n.children:
            find_calls(child)

    find_calls(node)
    # Deduplicate while preserving order
    seen: set[str] = set()
    unique: list[str] = []
    for c in calls:
        if c not in seen:
            seen.add(c)
            unique.append(c)
    return unique


def parse_file(filepath: str) -> list[dict]:
    """
    Parse a single .py file and return a list of nodes:
      - {"type": "function", "name": ..., "file": ..., "class": ...,
         "calls": [...], "start_line": ...}
      - {"type": "class", "name": ..., "file": ...}
    """
    parser = get_parser("python")

    with open(filepath, "rb") as f:
        source = f.read()

    tree = parser.parse(source)
    results: list[dict] = []

    def walk(node: Any, parent_class: str | None = None) -> None:
        if node.type == "function_definition":
            name_node = node.child_by_field_name("name")
            fn_name = name_node.text.decode(errors="ignore") if name_node else "unknown"
            calls = extract_calls(node, source)

            results.append({
                "type": "function",
                "name": fn_name,
                "file": filepath,
                "class": parent_class or "",
                "calls": calls,
                "start_line": node.start_point[0] + 1,  # 1-indexed
            })

        elif node.type == "class_definition":
            name_node = node.child_by_field_name("name")
            cls_name = name_node.text.decode(errors="ignore") if name_node else "unknown"

            results.append({
                "type": "class",
                "name": cls_name,
                "file": filepath,
            })

            # Walk children with this class as parent
            for child in node.children:
                walk(child, parent_class=cls_name)
            return  # don't re-walk children below

        for child in node.children:
            walk(child, parent_class)

    walk(tree.root_node)
    return results


def parse_repo(repo_path: str) -> list[dict]:
    """
    Walk all .py files in a cloned repo and return the combined
    list of function + class nodes from every file.
    """
    all_nodes: list[dict] = []

    for root, dirs, files in os.walk(repo_path):
        # Skip virtual envs, hidden dirs, test dirs
        dirs[:] = [
            d for d in dirs
            if d not in {"venv", ".venv", "__pycache__", ".git", "node_modules"}
        ]

        for filename in files:
            if not filename.endswith(".py"):
                continue
            filepath = os.path.join(root, filename)
            try:
                nodes = parse_file(filepath)
                all_nodes.extend(nodes)
            except Exception:
                # Skip files that can't be parsed (encoding issues, syntax errors, etc.)
                pass

    return all_nodes
