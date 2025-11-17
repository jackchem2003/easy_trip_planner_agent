# Smart Travel Assistant

A minimal starter repository for a GPU-accelerated ADK-based agent ("Smart Travel Assistant") using Gemma/LiteLlm + Ollama and a Google Maps MCP toolset. This README explains the structure, how to run locally with Docker or Python, environment variables, and useful notes. ✨

---

## 🔎 Project summary

- Name: Smart Travel Assistant (production ADK agent — Lab 3)
- Purpose: Provide a conversational agent that can answer location, mapping, and routing questions using:
	- google-adk Agent/Tool integrations
	- LiteLlm (Gemma) via an Ollama backend
	- A Model Context Protocol (MCP) Google Maps tool (served via an npx MCP server)

This repo contains a small FastAPI wrapper (via `google.adk.cli.fast_api`) that exposes the agent over HTTP and a Dockerized Ollama backend for hosting the Gemma model. 🧭🌤️

---

## 📁 Repository structure

- `adk-agent/` — Production ADK agent implementation and Dockerfile
	- `server.py` — FastAPI app created with `get_fast_api_app(...)`, exposes `/` and `/health` endpoints
	- `production_agent/agent.py` — defines `production_agent` (an ADK Agent) using `LiteLlm` and `MCPToolset` configured to run an `npx` MCP server for Google Maps
	- `elasticity_test.py` — placeholder for load/elasticity tests (TODO)
	- `pyproject.toml` — project metadata and dependency list used by the agent
	- `Dockerfile` — container image for the ADK FastAPI service (uses `uv` helper image and `uv sync`)
- `ollama-backend/` — Dockerfile to create an Ollama container and pre-pull the Gemma model

---

## ⚙️ Key files & behavior

- `adk-agent/server.py`
	- Creates a FastAPI app via `get_fast_api_app(agents_dir=..., web=True)`.
	- Adds simple endpoints:
		- `GET /` — basic service info + docs link
		- `GET /health` — health check returning `{status: "healthy"}`
	- Runs with `uvicorn` in the Dockerfile.

- `adk-agent/production_agent/agent.py`
	- Loads `.env` from the repo root (or `adk-agent` root) for secrets.
	- Configures `LiteLlm` to use an Ollama-based model: `ollama_chat/{GEMMA_MODEL_NAME}` with `OLLAMA_API_BASE`.
	- Injects a `MCPToolset` that launches an `npx @modelcontextprotocol/server-google-maps` process and forwards `GOOGLE_MAPS_API_KEY` into that process' environment so the MCP Google Maps tool can function.

- `ollama-backend/Dockerfile`
	- Uses `ollama/ollama:latest`, sets environment for host/paths, pulls the configured `MODEL` (default `gemma3:270m`) so model weights are available in the image.

---

## ✅ Prerequisites

- Docker (recommended for easiest setup) 🐳
- Python 3.13 (if running locally without Docker) 🐍
- Optional: Ollama installed locally if you prefer not to use the provided Ollama container

Environment variables used by the project (set these in `.env` or the container env):

- `GOOGLE_MAPS_API_KEY` — required for the Google Maps MCP tool
- `OLLAMA_API_BASE` — host:port of the Ollama server (default `localhost:10010`)
- `GEMMA_MODEL_NAME` — model identifier for Gemma (default `gemma3:270m`)
- `GOOGLE_CLOUD_PROJECT` / `GOOGLE_CLOUD_LOCATION` — optional cloud config used in `agent.py`

---

## 🐳 Run with Docker (recommended)

1) Start the Ollama backend (pre-pulls model weights):

```powershell
cd .\ollama-backend
docker build -t ollama-gemma .
docker run -d --name ollama -p 10010:8080 ollama-gemma
```

Note: The `ollama` image in this repo expects to run `ollama serve` and exposes an internal port; the Dockerfile sets `OLLAMA_HOST` and pulls the model so the container is ready.

2) Start the ADK agent service:

```powershell
cd .\adk-agent
docker build -t adk-agent .
docker run -d --name adk-agent -p 8080:8080 `
	-e OLLAMA_API_BASE="host.docker.internal:10010" `
	-e GOOGLE_MAPS_API_KEY="<your-key>" `
	adk-agent
```

Replace `<your-key>` with your Google Maps API key. On Windows Docker for Desktop, `host.docker.internal` forwards to the host where the Ollama container is reachable.

Visit: http://localhost:8080/docs for interactive API docs. 🚪

---

## 🧪 Run locally (without Docker)

1) Create and activate a venv (PowerShell):

```powershell
cd .\adk-agent
python -m venv .venv
. .\.venv\Scripts\Activate.ps1
```

2) Install dependencies (based on `pyproject.toml`):

```powershell
pip install google-adk==1.12.0 python-dotenv==1.1.0 httpx>=0.25.0 google-auth>=2.23.0 litellm==1.77.0
# (Dev) pytest, ruff if desired
```

3) Run the app:

```powershell
# ensure OLLAMA_API_BASE and GOOGLE_MAPS_API_KEY are set in environment or .env
$env:OLLAMA_API_BASE = "localhost:10010"
$env:GOOGLE_MAPS_API_KEY = "<your-key>"
python server.py
# or use uvicorn if available:
python -m uvicorn server:app --host 0.0.0.0 --port 8080
```

Then open: http://localhost:8080/docs

---

## 🔒 Security & secrets

- Keep your `GOOGLE_MAPS_API_KEY` secret; do not commit `.env` to source control.
- The repository currently assumes local/contained usage of Ollama. If you expose it publicly, require proper authentication and network controls.

---

## 🧩 Notes & TODOs

- `adk-agent/elasticity_test.py` is currently a placeholder (TODO). The `pyproject.toml` lists `locust` for load testing — you can add a Locust test file to exercise the endpoints.
- The Docker `adk-agent` image uses a helper `uv` tool (`ghcr.io/astral-sh/uv`) and `uv sync` to install dependencies. If you prefer standard Python packaging, adapt the Dockerfile or add a `requirements.txt`.

---

## 📬 Questions / Next steps

- Add a `README` for `ollama-backend/` describing model choices and disk requirements for model weights.
- Implement `elasticity_test.py` with a `locust` scenario to validate horizontal scaling.

If you'd like, I can:
- add a quick `docker-compose.yml` to start Ollama + ADK agent together 🤝
- implement a minimal Locust test for basic throughput checks 🧪

---

Made with ❤️ and a bit of AI magic ✨

