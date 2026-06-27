# Setup Guide (Windows · PowerShell in VS Code)

This guide assumes a **fresh Windows machine** with **nothing installed yet**,
and that you're using the **PowerShell terminal inside Visual Studio Code**.
We use **`uv`** as the package manager (not pip directly).

> **About the command style in this guide:** instead of relying on `uv` and
> `ollama` being on your PATH (which fails until you reopen the terminal, and
> sometimes after), we call each tool by its **full path**. This works
> immediately after install with no terminal restart required. Once you've
> confirmed everything works, the short forms (`uv ...`, `ollama ...`) will also
> work in any newly opened terminal.

> Open the integrated terminal in VS Code with **`Ctrl + ` `** (backtick), or
> menu **Terminal → New Terminal**. Make sure the dropdown on the right of the
> terminal panel says **PowerShell** (not Git Bash or Command Prompt).

---

## Step 1 — Install Python 3.10+

1. Check whether you already have it:
   ```powershell
   python --version
   ```
2. If the version is below 3.10, or you get an error / the Microsoft Store
   opens, download Python from https://www.python.org/downloads/ and install it.
   **During install, tick "Add python.exe to PATH."**
3. Close VS Code completely and reopen it, then verify again:
   ```powershell
   python --version
   ```

---

## Step 2 — Install `uv` (package manager)

In the VS Code PowerShell terminal, run the installer:
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

If you get an execution-policy error, run this once, then retry the line above:
```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

`uv` installs to `C:\Users\<you>\.local\bin`. Confirm the file is there:
```powershell
ls $env:USERPROFILE\.local\bin
```
You should see `uv.exe` (and `uvx.exe`) listed.

Now verify it runs by calling it **by full path** (works right away, no restart):
```powershell
& "$env:USERPROFILE\.local\bin\uv.exe" --version
```
You should see a version number.

> From here on, this guide uses `& "$env:USERPROFILE\.local\bin\uv.exe"` wherever
> a `uv` command is needed. If you'd rather type the short `uv`, close the
> terminal and open a new one first so PATH refreshes.

---

## Step 3 — Install Ollama (local LLM runtime)

Ollama runs the open-source model locally for free.

1. Download the Windows installer from https://ollama.com/download/windows
   (`OllamaSetup.exe`) and run it.
2. After installing, Ollama runs in the background — look for the **llama icon
   in the system tray** (bottom-right, near the clock).

Ollama installs to your user profile. Confirm the file is there:
```powershell
ls $env:LOCALAPPDATA\Programs\Ollama
```
You should see `ollama.exe` listed.

Verify it runs by calling it **by full path**:
```powershell
& "$env:LOCALAPPDATA\Programs\Ollama\ollama.exe" --version
```

> This guide uses `& "$env:LOCALAPPDATA\Programs\Ollama\ollama.exe"` wherever an
> `ollama` command is needed.

---

## Step 4 — Download a model

```powershell
& "$env:LOCALAPPDATA\Programs\Ollama\ollama.exe" pull llama3
```
This is a one-time ~4.7 GB download. On 16 GB RAM, a smaller model may feel
snappier — pick one and remember the name for Step 6:
```powershell
& "$env:LOCALAPPDATA\Programs\Ollama\ollama.exe" pull mistral      # ~4 GB
& "$env:LOCALAPPDATA\Programs\Ollama\ollama.exe" pull gemma:2b     # ~1.7 GB, fastest, lower quality
```
Confirm it's available:
```powershell
& "$env:LOCALAPPDATA\Programs\Ollama\ollama.exe" list
```

---

## Step 5 — Open the project and install dependencies

In VS Code, **File → Open Folder** and select the project folder (the one
containing `pyproject.toml`). Then in the PowerShell terminal, confirm you're in
the right place:
```powershell
ls
```
You should see `pyproject.toml`, `src`, `docs`, etc.

Install dependencies with `uv` (this creates a `.venv` folder automatically):
```powershell
& "$env:USERPROFILE\.local\bin\uv.exe" sync
```

Optional add-on groups — install only what you need:
```powershell
& "$env:USERPROFILE\.local\bin\uv.exe" sync --extra dev           # pytest (for running tests)
& "$env:USERPROFILE\.local\bin\uv.exe" sync --extra rag           # ChromaDB + sentence-transformers (RAG features)
& "$env:USERPROFILE\.local\bin\uv.exe" sync --extra huggingface   # transformers + torch (alternative backend)

# combine:
& "$env:USERPROFILE\.local\bin\uv.exe" sync --extra rag --extra dev
```

---

## Step 6 — Configure environment variables

Copy the template (PowerShell uses `copy`, not `cp`):
```powershell
copy .env.example .env
```

Open `.env` in VS Code (it's in the file explorer on the left). The defaults
work for Ollama + Llama 3. **Only change `LLM_MODEL`** if you pulled a different
model in Step 4:
```
LLM_PROVIDER=ollama
LLM_MODEL=llama3        # <-- match what you pulled (e.g. mistral, gemma:2b)
OLLAMA_HOST=http://localhost:11434
LLM_TEMPERATURE=0.4
LLM_MAX_TOKENS=1024
LOG_LEVEL=INFO
```

---

## Step 7 — Verify (no model needed)

The tests use a fake LLM, so they pass even without Ollama running — a quick
check that the install is healthy:
```powershell
& "$env:USERPROFILE\.local\bin\uv.exe" run pytest
```
Expected: `6 passed`. (If pytest is missing, run
`& "$env:USERPROFILE\.local\bin\uv.exe" sync --extra dev` first.)

---

## Step 8 — Run the app

Make sure the Ollama tray icon is present (it starts automatically on Windows).

**Web UI (recommended):**
```powershell
& "$env:USERPROFILE\.local\bin\uv.exe" run streamlit run src/ui/streamlit_app.py
```
Your browser opens to http://localhost:8501. Paste an IT process and click
**Analyze + Optimize**.

**Command line:**
```powershell
& "$env:USERPROFILE\.local\bin\uv.exe" run python -m src.ui.cli --file data/sample_processes/onboarding.txt
```

The first run is a little slower while the model loads into memory.

---

## Optional — Make the short commands work everywhere

Once everything runs, you can avoid typing full paths. Add both tools to your
user PATH, then **close and reopen the terminal**:
```powershell
[Environment]::SetEnvironmentVariable("Path", $env:Path + ";$env:USERPROFILE\.local\bin;$env:LOCALAPPDATA\Programs\Ollama", "User")
```
After reopening, these short forms will work:
```powershell
uv --version
ollama --version
```

---

## Troubleshooting (Windows / VS Code)

| Symptom | Fix |
| ------- | --- |
| `uv` / `ollama` "is not recognized" | Use the full-path commands in this guide, or add them to PATH (see the section above) and reopen the terminal. |
| `ls` of the install folder is empty / errors | The installer didn't finish, or installed elsewhere. Re-run the installer and watch for the install location. |
| Microsoft Store opens on `python` | Python isn't installed, or App Execution Aliases are hijacking it. Install from python.org with "Add to PATH" ticked. |
| Execution-policy error running the uv installer | Run `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned`, then retry. |
| App errors mentioning a connection | Ollama isn't running — check the tray icon, or run `& "$env:LOCALAPPDATA\Programs\Ollama\ollama.exe" serve` in a separate terminal. |
| `model "llama3" not found` | Pull it (Step 4), or set `LLM_MODEL` in `.env` to a model shown by `ollama ... list`. |
| Streamlit "module not found: src" | Run from the **project root** (where `pyproject.toml` is), not inside `src/`. |
| Terminal is Git Bash / CMD, not PowerShell | Click the **`∨`** next to the `+` in the terminal panel → **Select Default Profile → PowerShell**, then open a new terminal. |

---

## Notes

- The full-path command style (`& "...\uv.exe"`, `& "...\ollama.exe"`) avoids
  the "not recognized" PATH problem entirely — it works the instant a tool is
  installed, with no terminal restart.
- If you do switch to the short forms, remember PowerShell only reads PATH when
  it starts, so open a fresh terminal after changing it.
- Stick to one terminal type (PowerShell) to avoid `cp` vs `copy` and PATH
  differences between shells.
