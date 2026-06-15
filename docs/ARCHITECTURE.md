# Architecture

## Overview

The app follows a layered design so each concern is isolated and testable.

```
                ┌─────────────────────────────┐
                │        UI Layer             │
                │  streamlit_app.py / cli.py  │
                └──────────────┬──────────────┘
                               │ calls
                ┌──────────────▼──────────────┐
                │        Core Layer           │
                │  ProcessAnalyzer            │
                │  WorkflowOptimizer          │
                │  prompt_templates           │
                └──────────────┬──────────────┘
                               │ uses
                ┌──────────────▼──────────────┐
                │      LLM Provider           │
                │  get_llm_client()           │
                │  Ollama / HuggingFace       │
                └──────────────┬──────────────┘
                               │
                ┌──────────────▼──────────────┐
                │   Open-source LLM (local)   │
                │   Llama 3 / Mistral / Gemma │
                └─────────────────────────────┘

   Optional RAG path:  Core ──► database/ (ChromaDB) ──► retrieve similar processes
```

## Data flow

1. **Input** — user submits a process description (UI text area, CLI arg/file/stdin).
2. **Validation** — `utils/validators.py` checks length/content.
3. **Analysis** — `ProcessAnalyzer` builds an analysis prompt and calls the LLM.
4. **Optimization** — `WorkflowOptimizer` feeds the process + analysis back to
   the LLM to produce an optimized workflow.
5. **(Optional) Persistence/Retrieval** — `database/` stores processes in
   ChromaDB and retrieves similar past processes for added context (RAG).
6. **Output** — results are rendered in the UI or printed by the CLI.

## Key components

| Module                        | Responsibility                                   |
| ----------------------------- | ------------------------------------------------ |
| `config.py`                   | Env-driven settings (single `settings` object).  |
| `llm_provider.py`             | Backend abstraction; swap Ollama/HF via env.     |
| `core/prompt_templates.py`    | All prompts in one place for easy iteration.     |
| `core/process_analyzer.py`    | Produces structured analysis.                    |
| `core/optimizer.py`           | Produces optimized workflow + comparison.        |
| `database/vector_store.py`    | ChromaDB wrapper (optional).                      |
| `database/process_repository.py` | Save/retrieve processes with metadata.        |
| `utils/logger.py`             | Shared logging.                                  |
| `utils/validators.py`         | Input validation.                                |

## Design choices

- **Backend abstraction** lets the app run on Ollama by default and switch to
  Hugging Face without touching core logic.
- **Single pipeline function** (`run_pipeline`) keeps UI, CLI, and tests
  consistent.
- **Fake LLM in tests** means the suite runs anywhere without a model or GPU.
