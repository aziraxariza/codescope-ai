Here's your complete README — copy this exactly into `codescope/README.md`:

```markdown
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

---

## Run locally (free, no paid APIs)

### Prerequisites
- Python 3.11+
- Node.js 20+
- Git
- [Ollama](https://ollama.com) installed

### 1. Clone the repo

```bash
git clone https://github.com/YOUR_USERNAME/codescope-ai.git
cd codescope-ai
```

### 2. Get free credentials (no credit card needed)

| Service | Where to get it | What you need |
|---------|----------------|---------------|
| Neo4j Aura Free | [console.neo4j.io](https://console.neo4j.io) | URI + password |
| Qdrant Cloud Free | [cloud.qdrant.io](https://cloud.qdrant.io) | URL + API key |
| Groq (cloud only) | [console.groq.com](https://console.groq.com) | API key |

### 3. Set up environment

```bash
cp .env.example .env
# Fill in your Neo4j and Qdrant credentials
```

### 4. Pull the LLM model

```bash
ollama pull llama3.2:3b
```

### 5. Start the backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### 6. Start the frontend

```bash
cd frontend
npm install
npm run dev
```

### 7. Open the app

Go to [http://localhost:3000](http://localhost:3000), paste a GitHub URL, click **Analyze**.

---

## Deploy to cloud (free)

### Backend → Railway

```bash
npm install -g @railway/cli
railway login
cd backend
railway init
railway up
```

Set these environment variables in the Railway dashboard:
```
LLM_PROVIDER=groq
GROQ_API_KEY=your_key
NEO4J_URI=neo4j+s://xxx.databases.neo4j.io
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password
QDRANT_URL=https://xxx.qdrant.io
QDRANT_API_KEY=your_key
```

### Frontend → Vercel

```bash
cd frontend
npx vercel --prod
# Set NEXT_PUBLIC_API_URL to your Railway backend URL
```

---

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

```
User question
    ↓
Vector search → top 5 functions by similarity
    ↓
Neo4j traversal → their callers + callees (depth 2)
    ↓
Combined context (15+ functions)
    ↓
LLM answer with richer codebase understanding
```

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

## Resume Bullet

> Developed **CodeScope AI**, an autonomous code intelligence platform using GraphRAG (Neo4j Aura + Qdrant), local LLM inference via Ollama (LLaMA 3), and tree-sitter AST parsing to analyze GitHub repositories, detect security vulnerabilities, generate architecture insights, and answer codebase-level questions via a Next.js interface — deployed on Railway + Vercel at zero cost.
```

---

Also create a `.env.example` file so people know what to fill in (without your real credentials):

```bash
# .env.example
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
GROQ_API_KEY=your_groq_api_key_here

NEO4J_URI=neo4j+s://xxxxxxxx.databases.neo4j.io
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_neo4j_password_here

QDRANT_URL=https://xxxxxxxx.qdrant.io
QDRANT_API_KEY=your_qdrant_api_key_here

REPO_PATH=C:/temp/codescope_repo
```

Then push both files:

```bash
git add README.md .env.example
git commit -m "Add README and .env.example"
git push
```
