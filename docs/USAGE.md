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

## Tips

- Start with the included sample in `data/sample_processes/onboarding.txt`.
- Lower `LLM_TEMPERATURE` for more consistent output.
- Larger models give better results but need more RAM (16 GB min, 32 GB rec.).
