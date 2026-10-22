# Cedar Lab RAG Challenge

Author: **yunji-seo**. Partner: **none**. Prepared with Codex assistance.
Fictional classroom documents only; not operational safety guidance.

This project separates preparation (six labeled paragraphs), retrieval (keyword or actual CPU embeddings), and generation (a fresh, restricted answer context). It is a teaching workflow, not a deployed application.

## Reproduce

Use Python 3.12. From this directory, in PowerShell:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe keyword_retriever.py "May a trained graduate student operate the laser alone at 19:00?" -k 2
.\.venv\Scripts\python.exe embedding.py "May a trained graduate student operate the laser alone at 19:00?" -k 2 --inspect
.\.venv\Scripts\python.exe run_experiments.py
.\.venv\Scripts\python.exe review_results.py
.\.venv\Scripts\python.exe -m unittest discover -v
```

macOS/Linux: use `python3 -m venv .venv` and `.venv/bin/python` in the subsequent commands. Windows-specific transitive dependencies in `requirements-lock.txt` describe the original run; use `requirements.txt` for the direct dependencies.

An internet connection is needed for package installation and the first model download. Inference runs locally on CPU without an API key. Model cache and the virtual environment are excluded from Git. The original host supplied a bundled Python rather than a system Python; its venv lacked pip initially, so the bundled pip's `--python .venv/Scripts/python.exe install ...` option bootstrapped it. Package and Python versions are recorded in `evidence/embedding-inspection.txt`.

## Files and interpretation

- `docs/`: the six assignment paragraphs verbatim, with IDs and filenames retained separately by the loader.
- `keyword_retriever.py`: standard library only, exact stopword set, distinct word overlap, descending score then ascending ID, positive scores only.
- `embedding.py`: `sentence-transformers/all-MiniLM-L6-v2`, CPU, normalized 384-coordinate vectors, dot products and a direct cosine check. Always selects top k, even when the answer is absent.
- `run_experiments.py`: encodes all documents once, reuses them for Q1–Q4 and the k experiment, saves actual run output and fresh-answer input packets.
- `results-unjudged.csv`: original comparison rows with judgment fields blank.
- `results.csv`: reviewed comparison with **Codex-prepared judgments**, for the student to verify.
- `evidence/`: raw vector inspection, retrieval rankings, k experiment, restricted answer inputs, answers and claim audits.
- `REFLECTION_WORKSHEET.md`: student-authored reflection still required; Codex has not written a personal explanation.

Raw keyword counts and embedding similarities have different scales; do not compare their numeric sizes. Evidence coverage counts required chunks in the selected set: Q1 denominator 2, Q2/Q3 denominator 1. Q4 has no answer-bearing passage and coverage is not applicable.

`review_results.py` applies the recorded Codex audit to the original run; its prose observations refer to this run's exact scores. If package/model versions or inputs change, re-audit and update those observations rather than treating them as new measurements. The generator answers are manual handoffs, so experiment reruns do not regenerate the answer audits.

Observed result: Q1 keyword retrieval is complete (A1/A2), while embeddings select A2/T1 and miss A1. Increasing k to 3 adds B1 without repairing that omission. Both methods retrieve the target for Q2 and Q3. Q4 has no wavelength evidence. The original Q1 answer omitted the access-hours uncertainty; one instruction revision fixed its disclosure. See `evidence/retrieval-audit.md`, both answer audits, and `SUBMISSION_CHECKLIST.md`.

## How the code works

`load_chunks` reads three files and separates each label from its paragraph. `words` lowercases, extracts alphanumeric tokens and removes exactly the specified stopwords. A set counts each word once. `retrieve` intersects query words with passage words, counts the intersection, sorts the results, and selects only positive scores.

Code locations: loading is `keyword_retriever.py` lines 9–18; scoring is lines 23–26; ranking is line 27; positive-score selection is line 28. Document encoding is `embedding.py` lines 15–17; query encoding is lines 32–33; dot product is line 38; direct cosine is line 39; ranking is line 41; top-k selection is line 45.

The embedding model converts each paragraph into a row of 384 numbers: six rows form a `(6, 384)` matrix. A question has shape `(384,)`. Compatible dimensions and the same learned coordinate space are required for meaningful coordinate-by-coordinate comparison. Document and query encoding functions distinguish their roles; this model uses the same underlying encoding behavior for both. Neither encoding step generates an answer.

Normalization divides a vector by its length. Dot products multiply corresponding coordinates and sum all 384 products. The code additionally divides the dot product by the two measured lengths to check direct cosine agreement. Sorting six scores and slicing the first k records turns scores into selected passages. Rounding is for display only.

An individual coordinate has no dependable label such as "safety". The displayed minimum and maximum cannot independently identify a passage's meaning; the full vector represents learned relationships. Similarity does not prove truth, sufficiency, or answerability. RAG changes the generator's supplied context, not its learned weights.

## References

- [Official model card](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)
- [Sentence Transformers semantic search guide](https://www.sbert.net/examples/sentence_transformer/applications/semantic-search/README.html)

Only the assignment's six fictional passages are factual evidence for the answers. The references above concern implementation, not Cedar Lab rules.
