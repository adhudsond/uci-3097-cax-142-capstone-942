# Usage

## Web UI (Streamlit)

```bash
uv run streamlit run src/ui/streamlit_app.py
```

1. Paste an IT process description into the text area.
2. Click **Analyze** for analysis only, or **Analyze + Optimize** for both.
3. Read the analysis and optimized workflow rendered on the page.

## Command-line

```bash
# From text argument
uv run python -m src.ui.cli "Describe your IT process here..."

# From a file
uv run python -m src.ui.cli --file data/sample_processes/onboarding.txt

# From stdin
cat data/sample_processes/onboarding.txt | uv run python -m src.ui.cli

# Analysis only
uv run python -m src.ui.cli --analyze-only --file data/sample_processes/onboarding.txt
```

## Programmatic

```python
from src.main import run_pipeline

results = run_pipeline("When a ticket is created, an engineer manually triages it...")
print(results["analysis"])
print(results["optimized"])
```

## Generating report documents

After a run, you can save the analysis + optimized workflow as a document.

**Web UI:** download buttons appear below the results — Markdown, Text, HTML,
and Word (.docx). The .docx button is enabled only if `python-docx` is installed
(`uv sync --extra docs`).

**CLI:** use `--save` (format is inferred from the file extension):
```powershell
# Markdown
& "$env:USERPROFILE\.local\bin\uv.exe" run python -m src.ui.cli --file data/sample_processes/ticket_triage.txt --save report.md

# Word document
& "$env:USERPROFILE\.local\bin\uv.exe" run python -m src.ui.cli --file data/sample_processes/onboarding.txt --save report.docx

# Force a format explicitly
& "$env:USERPROFILE\.local\bin\uv.exe" run python -m src.ui.cli "Some process..." --save out.html --format html
```
Supported formats: `markdown` (.md), `text` (.txt), `html` (.html), `docx`.
For `.docx`, install the extra first: `uv sync --extra docs`.

## Tips

- Start with the included sample in `data/sample_processes/onboarding.txt`.
- Lower `LLM_TEMPERATURE` for more consistent output.
- Larger models give better results but need more RAM (16 GB min, 32 GB rec.).
