# Individual reflection

Author: Yunji Seo. Partner: none.

In this assignment, I learned how a RAG system transforms a question into a vector, retrieves relevant passages using similarity scores, and generates an answer supported by citations.

One important limitation I observed was that retrieving relevant passages does not guarantee complete evidence. For Q1, the model correctly concluded that operating the laser alone was prohibited, but it could not verify whether 19:00 was within permitted access hours because the relevant passage (A1) was missing. For Q4, the retriever returned laser-related passages even though none contained the wavelength. Fortunately, the model acknowledged the missing information instead of inventing an answer.

As a next step, I would experiment with different values of k and evaluate evidence coverage. I would also explore methods for detecting when retrieved passages are insufficient to answer a question.
