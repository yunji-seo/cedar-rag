# Actual environment and provenance

- Run date: 2026-10-22; raw output includes a UTC timestamp.
- Python: 3.12.14; locally isolated `.venv` created from the app-bundled Python.
- Packages: sentence-transformers 6.2.0, numpy 2.5.4, torch 2.14.1, transformers 5.20.2, huggingface-hub 2.2.0.
- Model: sentence-transformers/all-MiniLM-L6-v2, CPU.
- Downloaded model revision: `1110a243fdf4706b3f48f1d95db1a4f5529b4d41` (actual local cache refs/main).
- Full installed dependency versions: `requirements-lock.txt`.
- All embedding numbers and rankings are actual local results; no borrowed output.

## Setup problems and corrections

1. `python` was not on PATH; `py -0p` reported no installed Pythons. Located the app's bundled Python and used it directly.
2. venv creation reported an `ensurepip` subprocess failure, leaving a usable interpreter without pip. Used the bundled pip's `--python` option to install pip and dependencies into the venv.
3. Initial package download failed with `NameResolutionError` for pypi.org under restricted network access. Retried the same installation with approved network access; installation succeeded.
4. Model download emitted a Windows symlink-cache warning and an unauthenticated rate-limit warning. The download and CPU model execution completed successfully; no model API key was used.

The code was initially named `keyword.py` during preparation and renamed to `keyword_retriever.py` before use to avoid shadowing Python's standard-library `keyword` module. Source paragraphs and scoring rules were not changed.
