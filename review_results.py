"""Codex-prepared audit judgments, explicitly subject to student review."""
import csv
from keyword_retriever import ROOT

OBSERVATIONS = {
    'Q1': 'Keyword coverage 2/2; embedding coverage 1/2. Embeddings retrieve A2 and T1 but omit access-hours rule A1. The operating restriction is supported, but the full time explanation is incomplete.',
    'Q2': 'Both methods cover A2 (1/1). Embedding A2=0.585193515 matches the paraphrase about another person; keyword A2 scores 2 from laser and present.',
    'Q3': 'Both methods cover T1 (1/1). Embedding T1=0.742027521 handles refresh/qualification versus renewed/training. Keyword also succeeds from must and laser; this is not an embedding-only win.',
    'Q4': 'Answer absent from the six-source corpus. Embeddings still return T1=0.347721398 and A2=0.320827246 because top-k has no answerability check. Neither method retrieves a wavelength; no coverage ratio applies.',
}

def main():
    with (ROOT / 'results-unjudged.csv').open(encoding='utf-8') as handle:
        rows = list(csv.DictReader(handle))
    for row in rows:
        required = set(row['required_ids'].split(';'))
        for method in ['keyword', 'embedding']:
            row[f'{method}_evidence_complete'] = str(
                row['required_ids'] != 'absent' and required <= set(row[f'{method}_top_ids'].split(';'))).lower()
        row['observation'] = OBSERVATIONS[row['question_id']]
    with (ROOT / 'results.csv').open('w', newline='', encoding='utf-8') as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

if __name__ == '__main__':
    main()
