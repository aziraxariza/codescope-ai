# CodeScope AI 🔍

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
