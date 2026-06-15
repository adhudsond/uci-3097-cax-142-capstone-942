# Setup Guide

## Prerequisites

1. **Python 3.10+**
2. **uv** (package manager)
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```
3. **Ollama** (local LLM runtime) — https://ollama.com/
   ```bash
   ollama pull llama3      # or mistral, gemma
   ollama serve            # usually runs automatically after install
   ```

## Install

```bash
uv sync                   # create venv + install core deps
cp .env.example .env
```

### Optional feature groups

```bash
uv sync --extra rag           # ChromaDB + sentence-transformers (RAG)
uv sync --extra huggingface   # transformers + torch backend
uv sync --extra dev           # pytest
# combine:
uv sync --extra rag --extra dev
```

## Configure

Edit `.env`:

| Variable        | Default                  | Notes                          |
| --------------- | ------------------------ | ------------------------------ |
| `LLM_PROVIDER`  | `ollama`                 | or `huggingface`               |
| `LLM_MODEL`     | `llama3`                 | any model you've pulled        |
| `OLLAMA_HOST`   | `http://localhost:11434` | Ollama server URL              |
| `LLM_TEMPERATURE` | `0.4`                  | 0 = deterministic              |
| `LOG_LEVEL`     | `INFO`                   | DEBUG for verbose logs         |

## Verify

```bash
uv run pytest                 # should pass without a running model
uv run python -m src.ui.cli "When a ticket comes in, an engineer manually triages and assigns it."
```

If the CLI errors about Ollama, confirm `ollama serve` is running and the model
is pulled.
