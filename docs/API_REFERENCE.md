# API Reference

Internal module reference for the skeleton. Signatures may expand in Phase 2.

## `src.main`

### `run_pipeline(process_description: str) -> dict[str, str]`
Runs analyze → optimize end to end. Returns `{"analysis": ..., "optimized": ...}`.

---

## `src.config`

### `settings: Settings`
Singleton settings loaded from environment variables. Key fields:
`llm_provider`, `llm_model`, `ollama_host`, `temperature`, `max_tokens`,
`vector_db_path`, `embedding_model`, `collection_name`, `log_level`.

---

## `src.llm_provider`

### `get_llm_client() -> LLMClient`
Factory returning the configured backend (`OllamaClient` or `HuggingFaceClient`).

### `LLMClient.generate(prompt: str, system: str | None = None) -> str`
Protocol method every backend implements.

---

## `src.core.process_analyzer`

### `ProcessAnalyzer(llm: LLMClient | None = None)`
- `.analyze(process_description: str) -> AnalysisResult`

### `AnalysisResult`
Fields: `process_description: str`, `analysis_text: str`.

---

## `src.core.optimizer`

### `WorkflowOptimizer(llm: LLMClient | None = None)`
- `.optimize(process_description: str, analysis: str | None = None) -> OptimizationResult`
- `.compare(original: str, optimized: str) -> str`

### `OptimizationResult`
Fields: `process_description: str`, `optimized_workflow: str`, `analysis_used: str | None`.

---

## `src.core.prompt_templates`

- `SYSTEM_PROMPT: str`
- `analysis_prompt(process_description: str) -> str`
- `optimization_prompt(process_description: str, analysis: str | None = None) -> str`
- `comparison_prompt(original: str, optimized: str) -> str`

---

## `src.database.vector_store`

### `VectorStore()`
- `.add_process(doc_id: str, text: str, metadata: dict | None = None) -> None`
- `.search(query: str, n_results: int = 3) -> list[dict]`

## `src.database.process_repository`

### `ProcessRepository(store: VectorStore | None = None)`
- `.save(process_text: str, optimized_text: str | None = None, tags: list[str] | None = None) -> str`
- `.find_similar(query: str, n_results: int = 3) -> list[dict]`

---

## `src.utils.validators`

- `validate_process_description(text: str) -> str` (raises `ValidationError`)

---

## `src.core.exporter`

Generates downloadable report documents from results.

### `ExportPayload`
Dataclass holding everything a document contains. Fields:
`process_description: str`, `analysis: str`, `optimized: str`,
`comparison: str | None = None`, `title: str`, `generated_at: str` (auto-set).

### Renderers
- `to_markdown(payload: ExportPayload) -> str`
- `to_text(payload: ExportPayload) -> str`
- `to_html(payload: ExportPayload) -> str`
- `to_docx(payload: ExportPayload) -> bytes` (requires `python-docx`)

### `FORMATS`
Dict mapping format name → `(renderer, extension, is_binary)`. Used by the CLI
to infer format from a file extension.

## `src.utils.logger`

- `get_logger(name: str) -> logging.Logger`
