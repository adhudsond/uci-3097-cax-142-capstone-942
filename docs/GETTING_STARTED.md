# 🚀 Step-by-Step Setup Guide

A complete walkthrough to get the **Business Process Optimization** app running
from a fresh machine. Follow the steps in order. Estimated time: 15–30 minutes
(most of it is downloading the LLM model).

> **What you'll have at the end:** a working Streamlit web app (and CLI) that
> analyzes an IT process and generates an optimized workflow using a local,
> free, open-source LLM. No paid APIs.

---

## Step 0 — Check your machine

| Requirement | Minimum | Recommended |
| ----------- | ------- | ----------- |
| RAM         | 16 GB   | 32 GB       |
| Disk free   | ~10 GB  | (for the model + venv) |
| Python      | 3.10+   | 3.11 or 3.12 |
| OS          | macOS, Linux, or Windows | — |

> 💡 If your machine can't run a local model, you can use Google Colab or
> Hugging Face Inference instead — see **Step 8 (Alternative)** at the bottom.

Check your Python version:
```bash
python --version
# or, on some systems:
python3 --version
```
If it's below 3.10, install a newer Python from https://www.python.org/downloads/.

---

## Step 1 — Install `uv` (package manager)

`uv` replaces pip/venv and is much faster.

**macOS / Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows (PowerShell):**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Close and reopen your terminal, then verify:
```bash
uv --version
```
You should see a version number. If "command not found," restart your terminal
or follow the PATH instructions printed by the installer.

---

## Step 2 — Install Ollama (the local LLM runtime)

Ollama runs the open-source model on your computer for free.

1. Go to **https://ollama.com/download** and install for your OS.
   - macOS: download the app, open it.
   - Windows: download and run the installer.
   - Linux: `curl -fsSL https://ollama.com/install.sh | sh`
2. Verify it's installed:
   ```bash
   ollama --version
   ```

---

## Step 3 — Download a model

Pull Llama 3 (a good default, ~4.7 GB). This downloads once.
```bash
ollama pull llama3
```

> 🐢 On 16 GB RAM, a smaller/faster model may feel better. Alternatives:
> ```bash
> ollama pull mistral      # ~4 GB
> ollama pull gemma:2b     # ~1.7 GB, fastest, lower quality
> ```
> Whatever you pull, set the same name as `LLM_MODEL` in Step 6.

Confirm the model is available:
```bash
ollama list
```

---

## Step 4 — Get the project files

If you have the zip, unzip it and `cd` into it. If it's on GitHub:
```bash
git clone <your-repo-url>
cd Business-Process-Optimization
```

If using the zip:
```bash
cd path/to/Business-Process-Optimization
```

Confirm you're in the right place (you should see `pyproject.toml`):
```bash
ls
```

---

## Step 5 — Install dependencies with `uv`

From the project root:
```bash
uv sync
```
This creates a `.venv/` folder and installs Streamlit, the Ollama client, and
python-dotenv automatically.

**Optional add-ons** (install only if you want them):
```bash
uv sync --extra dev           # pytest, for running tests
uv sync --extra rag           # ChromaDB + embeddings (optional RAG features)
uv sync --extra huggingface   # transformers + torch (alternative backend)

# combine multiple:
uv sync --extra dev --extra rag
```

---

## Step 6 — Configure environment variables

Copy the template:
```bash
cp .env.example .env
```
(Windows PowerShell: `copy .env.example .env`)

Open `.env` in any editor. Defaults work out of the box for Ollama + Llama 3.
**Only change `LLM_MODEL`** if you pulled a different model in Step 3:
```
LLM_PROVIDER=ollama
LLM_MODEL=llama3        # <-- match what you pulled (e.g. mistral, gemma:2b)
OLLAMA_HOST=http://localhost:11434
LLM_TEMPERATURE=0.4
LLM_MAX_TOKENS=1024
LOG_LEVEL=INFO
```

---

## Step 7 — Verify it works (no model needed)

Run the test suite. These use a fake LLM, so they pass even if Ollama isn't
running — a quick sanity check that the install is correct.
```bash
uv run pytest
```
Expected: `6 passed`.

> If you skipped `--extra dev`, install it first: `uv sync --extra dev`.

---

## Step 8 — Run the app 🎉

Make sure Ollama is running in the background. On macOS/Windows the app starts
it automatically; on Linux you may need:
```bash
ollama serve
```
(Leave that running in its own terminal if needed.)

### Option A — Web UI (recommended)
In the project root:
```bash
uv run streamlit run src/ui/streamlit_app.py
```
Your browser opens to `http://localhost:8501`. Paste an IT process and click
**Analyze + Optimize**.

### Option B — Command line
```bash
# Use the included sample process
uv run python -m src.ui.cli --file data/sample_processes/onboarding.txt
```

### Option C — Quick test with your own text
```bash
uv run python -m src.ui.cli "When a ticket is created, an engineer manually triages it, assigns it, and emails the requester before starting work."
```

The first run may take a little longer while the model loads into memory.

---

## ✅ Success checklist

- [ ] `uv --version` works
- [ ] `ollama list` shows your model
- [ ] `uv sync` finished without errors
- [ ] `.env` exists and `LLM_MODEL` matches your pulled model
- [ ] `uv run pytest` shows `6 passed`
- [ ] The Streamlit page loads and returns an analysis + optimized workflow

---

## 🛠️ Troubleshooting

| Symptom | Fix |
| ------- | --- |
| `uv: command not found` | Restart terminal; re-check Step 1 PATH note. |
| `Error: ... 'ollama' package is not installed` | Run `uv sync` again from the project root. |
| App hangs or errors mentioning connection | Ollama isn't running — run `ollama serve`. |
| `model "llama3" not found` | Run `ollama pull llama3` (or set `LLM_MODEL` to a model you pulled). |
| Very slow / freezes | Use a smaller model (`gemma:2b`) or close other apps; you may be low on RAM. |
| Streamlit "module not found: src" | Run the command from the **project root**, not inside `src/`. |
| `pytest: command not found` | Install dev deps: `uv sync --extra dev`. |

---

## Step 8 (Alternative) — No local model? Use Colab

If your computer can't run a local model:
1. Open `notebooks/demo.ipynb` in **Google Colab**.
2. Use the Hugging Face backend instead of Ollama by setting in `.env`:
   ```
   LLM_PROVIDER=huggingface
   LLM_MODEL=<a small HF text-generation model>
   ```
3. Install the HF extra: `uv sync --extra huggingface` (or `pip install` the
   transformers/torch deps in the Colab cell).

---

## Next steps

- Read [`docs/USAGE.md`](USAGE.md) for all the ways to run the app.
- Read [`docs/ARCHITECTURE.md`](ARCHITECTURE.md) to understand how it fits together.
- Add your own IT processes to `data/sample_processes/` and try them.
