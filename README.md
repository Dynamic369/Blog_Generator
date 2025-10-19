Blog Generator (FastAPI + LangGraph)

Build SEO-friendly blog posts from a topic, with optional translation into selected languages, using LangGraph state machines and a Groq LLM backend.

## Features

- FastAPI server with a single endpoint: POST `/blogs`
- LangGraph orchestration with two graphs:
	- Topic graph: title_creation → content_generation
	- Language graph: title_creation → content_generation → route → translation (hindi/french)
- Groq LLM integration via `langchain_groq`
- Strongly-typed state using Pydantic and LangGraph merge semantics

## Project structure

- `app.py` — FastAPI app and route
- `src/graph/graph_builder.py` — builds the LangGraph graphs
- `src/nodes/blog_node.py` — node functions (title, content, routing, translation)
- `src/states/blogstate.py` — Blog and BlogState data models
- `requirements.txt` / `pyproject.toml` — dependencies

## Prerequisites

- Python 3.12+
- A Groq API key
- (Optional) LangSmith key for tracing

## Quick start

1) Create and activate venv

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2) Install dependencies

```powershell
pip install -r requirements.txt
```

3) Configure environment

Create a `.env` at the project root (do NOT commit this file):

```env
GROQ_API_KEY="your_groq_api_key"
LANGCHAIN_API_KEY="your_langsmith_key_optional"
```

4) Run the server

```powershell
python app.py
```

Server will start on http://127.0.0.1:8000 (or 0.0.0.0:8000)

## API usage

Endpoint: `POST /blogs`

Request (JSON):

```json
{
	"topic": "Agentic AI",
	"language": "hindi"
}
```

Notes:
- `topic` is required for all flows.
- `language` is optional. If provided, accepted values are `hindi` or `french` (others will default to `french`).

Response example:

```json
{
	"data": {
		"blog": {
			"title": "...",
			"content": "..."
		}
	}
}
```

## How it works (LangGraph)

- Topic graph
	- Nodes: `title_creation`, `content_generation`
	- Edges: START → title_creation → content_generation → END

- Language graph
	- Nodes: `title_creation`, `content_generation`, `route`, `hindi_translation`, `french_translation`
	- Edges: START → title_creation → content_generation → route → (conditional) → translation → END
	- Routing: currently supports `hindi` and `french`, with a safe fallback to `french` for unknown languages

State contract:
- Input: `{ "topic": str, "current_language"?: str }
- Output: merges partials like `{ "blog": { "title": str, "content": str } }`

## Troubleshooting

- Cannot import langgraph
	- Ensure you’re using the venv Python: `.\.venv\Scripts\python.exe -c "import langgraph; print('ok')"`
	- Reinstall: `pip install langgraph`

- PowerShell cannot run Activate.ps1
	- Run once: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned -Force`

- 500 errors during translation
	- Ensure `GROQ_API_KEY` is set and valid
	- Our translation node filters LLM output to the expected Blog schema and preserves title if missing

- Push blocked by GitHub (secrets)
	- Remove `.env` from history and add to `.gitignore`
	- See GitHub push protection docs


