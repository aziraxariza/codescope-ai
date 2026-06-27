# CodeScope AI 🔍
abcdefg
> GraphRAG-powered autonomous code intelligence platform. Paste a GitHub URL — get architecture diagrams, security vulnerability detection, and AI-powered codebase Q&A.

![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat-square&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-green?style=flat-square&logo=fastapi)
![Neo4j](https://img.shields.io/badge/Neo4j-Aura-blue?style=flat-square&logo=neo4j)
![Next.js](https://img.shields.io/badge/Next.js-14-black?style=flat-square&logo=nextdotjs)

---

## What it does

CodeScope AI analyzes any public GitHub repository and gives you:

- **AST Parsing** — extracts every function, class, and call relationship using tree-sitter
- **Knowledge Graph** — stores the full code graph in Neo4j (nodes = functions/classes, edges = CALLS relationships)
- **GraphRAG Q&A** — answers questions about the codebase using vector search (Qdrant) + graph traversal (Neo4j), not just plain RAG
- **Security Scanning** — detects SQL injection, hardcoded secrets, command injection, and path traversal with LLM-generated explanations
- **Architecture Diagrams** — auto-generates Mermaid.js diagrams from cross-file call relationships

---

## Demo

> Paste any public GitHub URL → stats appear in seconds → switch to Architecture or Chat

**Test repos to try:**
- `https://github.com/psf/requests`
- `https://github.com/pallets/flask`
- `https://github.com/tiangolo/fastapi`

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Code parsing | tree-sitter + tree-sitter-languages |
| Backend | FastAPI + Uvicorn |
| LLM (local) | Ollama + LLaMA 3.2 3B |
| LLM (cloud) | Groq API + LLaMA 3 8B |
| Embeddings | sentence-transformers (all-MiniLM-L6-v2) |
| Graph DB | Neo4j Aura Free |
| Vector DB | Qdrant Cloud Free |
| Frontend | Next.js 14 + Tailwind CSS |
| Diagrams | Mermaid.js |
| Deployment | Railway (backend) + Vercel (frontend) |

---

## Architecture

```
GitHub URL
    ↓
tree-sitter AST Parser
    ↓
┌─────────────────────────────────┐
│         Neo4j Aura              │
│  Function → CALLS → Function    │
│  Class → CONTAINS → Function    │
└─────────────────────────────────┘
    ↓
┌─────────────────────────────────┐
│         Qdrant Cloud            │
│  sentence-transformers vectors  │
│  per-function embeddings        │
└─────────────────────────────────┘
    ↓
GraphRAG Pipeline
  Vector Search + Graph Traversal
    ↓
LLM (Ollama / Groq)
    ↓
Next.js Frontend
```
## Project Structure

```
codescope/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI routes
│   │   ├── llm.py               # Ollama/Groq unified wrapper
│   │   ├── parser/
│   │   │   └── repo_parser.py   # tree-sitter AST parser
│   │   ├── graph/
│   │   │   └── neo4j_client.py  # Neo4j graph operations
│   │   ├── embeddings/
│   │   │   ├── embedder.py      # sentence-transformers
│   │   │   └── vector_store.py  # Qdrant operations
│   │   └── agents/
│   │       ├── graph_rag.py     # GraphRAG pipeline
│   │       ├── security_agent.py # Vulnerability scanner
│   │       └── diagram_agent.py  # Mermaid diagram generator
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── app/
│   │   ├── page.tsx             # Main UI (3 tabs)
│   │   └── layout.tsx
│   └── components/
│       └── MermaidDiagram.tsx   # Client-side Mermaid renderer
├── docker-compose.yml
└── .env.example
```

---

## API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check + LLM provider |
| POST | `/analyze` | Clone + parse + embed a repo |
| POST | `/chat` | GraphRAG Q&A |
| GET | `/security` | Vulnerability scan |
| GET | `/diagram/architecture` | File-level Mermaid diagram |
| GET | `/diagram/classes` | Class diagram |
| GET | `/stats` | Current graph statistics |

---

## What is GraphRAG?

Standard RAG retrieves context using only **vector similarity** — it finds functions that *sound like* they match your query. GraphRAG adds a second layer: after finding the top-k functions by vector search, it **traverses the Neo4j call graph** to pull in their callers and callees — functions that are structurally related even if semantically different.

User question
    ↓
Vector search → top 5 functions by similarity
    ↓
Neo4j traversal → their callers + callees (depth 2)
    ↓
Combined context (15+ functions)
    ↓
LLM answer with richer codebase understanding


This surfaces context that pure vector search misses — and it's the core technical differentiator of this project.

---

## Future Work

- Multi-language support (JavaScript, Go, Java via tree-sitter)
- Autonomous PR review agent
- GitHub Actions CI integration
- Real-time repo sync on push events
- Custom embedding fine-tuning on code corpora
- Self-improving security rule generation

---


