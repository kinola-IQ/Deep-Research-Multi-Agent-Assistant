Deep Research Multi-Agent Assistant
===================

A FastAPI-based research assistant that runs a multi-agent workflow for question refinement, web research, report drafting, and review. The API exposes both a synchronous endpoint and a streaming endpoint using Server-Sent Events (SSE). A lightweight Streamlit UI is also included for local experimentation.

Visual representation of the workflow
--------
![image alt](https://github.com/kinola-IQ/Deep-Research-Multi-Agent-Assistant/blob/0245963d7c09257a40be1db618b094f8cd3946fc/workflow%20diagram.png)

Features
--------
- Multi-agent research workflow with separate question, research, report, and review agent components.
- Server-Sent Events (SSE) streaming endpoint to emit progress updates and the final report.
- Ollama-backed model loading with retry/backoff and a shared `LLMSwitcher` loader.
- Basic health endpoint to confirm the API and model readiness.
- Minimal Streamlit frontend in `app/GUI/` for local testing.

Architecture
------------
- `app/main.py` launches FastAPI and loads the model during startup using an async lifespan manager.
- `app/interface/routes.py` defines `/v1/health`, `/v1/agent`, and `/v1/agent/stream`.
- `app/system/agents/` contains agent factories and workflow orchestration.
- `app/system/model/` handles model selection and loading via Ollama.
- `app/system/tools.py` provides helper tools used by agents.
- `app/system/utils/` stores event models, response schemas, and logging utilities.

Prerequisites
-------------
- Python 3.11 recommended.
- Ollama installed and running locally.
- Tavily API key configured in `TAVILY_API_KEY` if the workflow uses the web search helper.

Installation
------------
1) Clone the repository and enter the project directory.
2) Create and activate a virtual environment.
3) Install dependencies:
```
pip install -r requirements.txt
```
4) Set required environment variables:
```
set TAVILY_API_KEY=YOUR_KEY_HERE
```

Running the API
---------------
Start the FastAPI app with uvicorn:
```
uvicorn app.main:app --host 127.0.0.1 --port 8501
```

Available endpoints
-------------------
- `GET /v1/health` — returns service status and whether the model is loaded.
- `POST /v1/agent` — synchronous request returning the final markdown report.
- `POST /v1/agent/stream` — SSE streaming endpoint that emits progress updates and a final result.

Example request body
--------------------
```
{
  "text": "What is the current state of quantum computing research?"
}
```

Streamlit UI
------------
Launch the UI locally:
```
streamlit run app/GUI/streamlit_ui.py
```
Use the sidebar to configure the API base URL and view backend health.

Project layout
--------------
```
app/
  main.py
  interface/routes.py
  GUI/
    index.html
    streamlit_ui.py
  system/
    agents/
      research_agents.py
      review_agents.py
      workflow.py
      write_agents.py
    model/
      llm_switcher.py
      llms.py
      model_loader.py
    tools.py
    utils/
      events.py
      logger.py
      schema.py
    tests/
      test_model_and_agents.py
      test_routes.py
```

Development & Testing
---------------------
- Install dev dependencies:
```
pip install -r requirements-dev.txt
```
- Run tests:
```
pytest -q
```

Linting & CI
------------
- Formatting and linting are configured in `pyproject.toml`.
- Pre-commit hooks are available via `.pre-commit-config.yaml`.
- GitHub Actions workflows are defined in `.github/workflows/`.

Troubleshooting
---------------
- If the model fails to load, ensure Ollama is running and the configured model is available.
- If web search behaves unexpectedly, verify `TAVILY_API_KEY` and network access.
- If streaming fails, confirm the client supports SSE and is not buffering the response.
