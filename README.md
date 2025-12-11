# GenUI Workflow

A generative UI system using recursive idea-based expansion with LangGraph. The system takes natural language prompts and generates hierarchical component structures through parallel LLM expansion.

## Project Structure

```
.
├── backend/              # Python FastAPI backend
│   ├── main.py          # FastAPI application with streaming endpoints
│   ├── graph/           # LangGraph workflow
│   │   ├── workflow.py  # Graph definition
│   │   ├── nodes.py     # Expansion nodes
│   │   ├── state.py     # State management with reducers
│   │   └── components.py # Component library (30+ components)
│   └── pyproject.toml   # Python project configuration
└── frontend/            # React frontend
    ├── src/
    │   ├── pages/
    │   │   └── GraphDebug.jsx # Graph state viewer
    │   ├── main.jsx     # Application entry point
    │   ├── App.jsx      # Router configuration
    │   └── index.css    # Global styles
    ├── index.html
    ├── package.json
    └── vite.config.js
```

## Architecture

**Recursive Idea-Based Expansion:**
- Components can contain "idea" fields - high-level descriptions that spawn recursive LLM calls
- LangGraph state reducers automatically merge parallel expansions into the component tree
- Map-reduce pattern for parallel idea expansion using `Send[]`

**Component Library:**
30+ pre-defined components across categories:
- Layout: rail, stack, cluster, grid
- Content: card, panel, tabs, accordion
- Typography: header, text, code, blockquote
- Media: image, icon, avatar, video
- Interactive: button, input, select, checkbox
- Data Display: table, list, stat, chart
- Navigation: breadcrumb, menu, link

**Graph Flow:**
1. Root expansion: User prompt → top-level component tree
2. Parallel expansion: All components with "idea" fields expand simultaneously
3. Recursive loop: Process continues until no pending ideas remain
4. State reducer: Merges all updates into final tree

## Prerequisites

- Python 3.11+
- [uv](https://github.com/astral-sh/uv) - Fast Python package installer
- Node.js 18+
- [Just](https://github.com/casey/just) command runner
- OpenAI API key (set in `backend/.env`)

Install uv:
```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or with pip
pip install uv
```

Install Just:
```bash
# macOS
brew install just

# Linux
cargo install just

# Or download from releases
```

## Environment Setup

Create `backend/.env` with your OpenAI API key:
```bash
OPENAI_API_KEY=your-api-key-here
```

## Quick Start

```bash
# Install all dependencies
just install

# Run both backend and frontend
just dev
```

## Available Commands

```bash
just                  # List all commands
just install          # Install all dependencies
just install-backend  # Install backend dependencies only
just install-frontend # Install frontend dependencies only
just dev              # Run both servers in parallel
just dev-backend      # Run backend only (localhost:8000)
just dev-frontend     # Run frontend only (localhost:5173)
just build            # Build frontend for production
just clean            # Remove all build artifacts and dependencies
```

## Manual Setup

### Backend

```bash
cd backend
uv venv
uv pip install -r pyproject.toml
uv run uvicorn main:app --reload
```

Backend runs at http://localhost:8000

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at http://localhost:5173

## API Endpoints

- `GET /api/health` - Health check endpoint
- `POST /api/generate-ui` - Generate component tree from prompt (returns final result)
- `POST /api/generate-ui/stream` - Stream graph state updates in real-time (SSE)

### Example Request

```bash
curl -X POST http://localhost:8000/api/generate-ui \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Create a dashboard with metrics and charts"}'
```

### Streaming Response

The `/stream` endpoint sends Server-Sent Events with graph state updates:

```javascript
const response = await fetch('http://localhost:8000/api/generate-ui/stream', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ prompt: 'your prompt' })
})

const reader = response.body.getReader()
// Process SSE events: state_update, done, error
```

## Development

- Backend auto-reloads on file changes
- Frontend hot-reloads on file changes
- Graph Debug UI at http://localhost:5173 shows real-time state evolution
- Console logs show expansion progress and parallel execution

## How It Works

1. **Prompt Input**: User provides natural language UI description
2. **Root Expansion**: LLM generates top-level structure with "idea" placeholders
3. **Parallel Processing**: All "idea" fields expand simultaneously via `Send[]`
4. **State Merging**: Custom reducer merges child expansions into parent components
5. **Recursive Loop**: Process repeats until no "idea" fields remain
6. **Final Tree**: Complete component hierarchy ready for rendering
