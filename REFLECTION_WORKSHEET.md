# Individual reflection

Author: Yunji Seo. Partner: none.

The following reflection was written and supplied by Yunji Seo and is reproduced verbatim.

## Reflection

In this assignment, I learned how a RAG system transforms a question into a vector, retrieves relevant passages using similarity scores, and generates an answer supported by citations.

One important limitation I observed was that retrieving relevant passages does not guarantee complete evidence. For Q1, the model correctly concluded that operating the laser alone was prohibited, but it could not verify whether 19:00 was within permitted access hours because the relevant passage (A1) was missing. For Q4, the retriever returned laser-related passages even though none contained the wavelength. Fortunately, the model acknowledged the missing information instead of inventing an answer.

As a next step, I would experiment with different values of k and evaluate evidence coverage. I would also explore methods for detecting when retrieved passages are insufficient to answer a question.

## Review before submission

- Read the code explanation and manually verify the Q1 keyword score.
- Review the judgments in results.csv; these were prepared by Codex, not personally entered by the student.
- Read both answer audits and verify each claim against its supplied passage.
- Submit your repository URL to the course Sign Up Sheet (its link was not present in the pasted assignment).
