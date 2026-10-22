# Retrieval audit (Codex-prepared; student review required)

No output is borrowed or invented. The model was run locally on CPU on 2026-10-22. The preserved blank comparison is `results-unjudged.csv`; judged results are `results.csv`.

## Keyword audit

Exactly six paragraphs match the supplied handout verbatim (see `source-verification.txt`). IDs and filenames are metadata; neither is searched or embedded.

For Q1, the query's distinct remaining words are `trained, graduate, student, operate, laser, alone, 19, 00`. A1 shares `00, graduate, trained`, giving 3. A2 shares `laser, trained`, giving 2. Repeating `laser` does not raise a score. `student` does not match `students`, and `operate` does not match `operating`, because stemming is prohibited. The token `00` matches times without understanding their meaning.

Selected Q1 keyword IDs: A1, A2. Both required passages are present; coverage 2/2.

## Observed comparisons

| Question | Keyword top 2 | Embedding top 2 | Keyword coverage | Embedding coverage |
|---|---|---|---|---|
| Q1 | A1 (3), A2 (2) | A2 (0.686445773), T1 (0.581952810) | 2/2 | 1/2 |
| Q2 | A2 (2), B1 (1) | A2 (0.585193515), T1 (0.434760809) | 1/1 | 1/1 |
| Q3 | T1 (2), A2 (1) | T1 (0.742027521), B1 (0.471195340) | 1/1 | 1/1 |
| Q4 | A2 (1), B1 (1) | T1 (0.347721398), A2 (0.320827246) | N/A: absent | N/A: absent |

Q1 is an observed embedding failure relative to the complete evidence target: A1 ranks fourth (0.374249041). A2 supports the prohibition on solo operation, but does not establish numeric access hours. A correct "no" alone does not make the retrieval complete.

For Q2, A2 matches "another person present" despite the source's "two trained people" wording. For Q3, T1 strongly matches the training-renewal paraphrase. The keyword retriever also retrieves T1, using `must` and `laser`; embeddings did not uniquely solve this case.

Q4 is unanswerable from the entire six-paragraph corpus. Embeddings return the closest passages because this exercise always selects the top k; a positive similarity is neither a wavelength nor an answerability test. Both CSV completeness fields are false, while coverage is not defined. Returning no wavelength is the correct generation behavior.

## k experiment

- k=1: A2; coverage 1/2.
- k=2: A2, T1; coverage 1/2.
- k=3: A2, T1, B1; coverage 1/2.

T1 adds an operating qualification condition (current training and 12-month renewal), but no access-hours interval. B1 adds booking duration and reservation method, which do not resolve solo operation at 19:00. Increasing k to 3 does not repair the missing A1 evidence in this run. The observed ranking places A1 fourth; no k=4 experiment is claimed here.

## Visible vector calculation

The actual document matrix is (6, 384), and Q1 is (384,). Measured lengths are approximately 1 (B2 is 1.000000119 due to floating-point precision). For Q1 and A2, the first 12 coordinate products sum to 0.016111501290; the remaining 372 sum to 0.670334252097. Their float64 sum is 0.686445753387, agreeing within tolerance with the float32 dot/cosine 0.686445772648. The implementation uses full stored precision and rounds only for printing.

Among the displayed document and Q1 coordinates, the minimum is T1 coordinate 5 (-0.1167) and the maximum is T1 coordinate 12 (0.1357). Neither coordinate alone identifies the passage's meaning. The whole learned vector, in a compatible space, determines the comparison.

These four questions are a small classroom check, not a general performance estimate.
