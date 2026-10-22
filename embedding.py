"""Actual CPU embeddings; no API, database, or relevance cutoff."""
import argparse
from importlib.metadata import version
import platform
import numpy as np
from sentence_transformers import SentenceTransformer
from keyword_retriever import ROOT, load_chunks, positive

MODEL = 'sentence-transformers/all-MiniLM-L6-v2'

class Retriever:
    def __init__(self):
        self.chunks = load_chunks()
        self.model = SentenceTransformer(MODEL, device='cpu', cache_folder=str(ROOT / '.cache'))
        self.documents = self.model.encode_document(
            [c['text'] for c in self.chunks], normalize_embeddings=True,
            convert_to_numpy=True, show_progress_bar=False)
        assert self.documents.shape == (6, 384)
        assert np.allclose(np.linalg.norm(self.documents, axis=1), 1, atol=1e-6)

    def describe(self):
        print(f'Model: {MODEL}\nDevice: cpu\nPython: {platform.python_version()}')
        for package in ['sentence-transformers', 'numpy', 'torch', 'transformers', 'huggingface-hub']:
            print(f'{package}: {version(package)}')
        print(f'Document matrix shape: {self.documents.shape}')
        print('All 384 coordinates are used; only the first 12 are displayed.')
        for chunk, vector in zip(self.chunks, self.documents):
            print(f"{chunk['id']} first12: " + ' '.join(f'{x:.4f}' for x in vector[:12]))
            print(f"{chunk['id']} length: {np.linalg.norm(vector):.9f}")

    def retrieve(self, question, k=2, inspect=False):
        vector = self.model.encode_query(question, normalize_embeddings=True,
                                         convert_to_numpy=True, show_progress_bar=False)
        print(f'Question: {question}\nQuestion vector shape: {vector.shape}')
        print('Question first12: ' + ' '.join(f'{x:.4f}' for x in vector[:12]))
        print(f'Question length: {np.linalg.norm(vector):.9f}')
        assert vector.shape == (384,) and np.isclose(np.linalg.norm(vector), 1, atol=1e-6)
        scores = self.documents @ vector
        cosine = scores / (np.linalg.norm(self.documents, axis=1) * np.linalg.norm(vector))
        assert np.allclose(scores, cosine, atol=1e-6)
        order = sorted(range(6), key=lambda i: (-float(scores[i]), self.chunks[i]['id']))
        rows = [dict(**self.chunks[i], score=float(scores[i])) for i in order]
        for row in rows:
            print(f"{row['id']} score={row['score']:.9f}")
        selected = rows[:k]
        for row in selected:
            print(f"SELECTED [{row['id']}] {row['filename']}: {row['text']}")
        print(f'Dot/cosine agree (atol=1e-6); max difference={np.max(np.abs(scores-cosine)):.12g}')
        if inspect:
            i = order[0]
            products = self.documents[i].astype(np.float64) * vector.astype(np.float64)
            print(f"Q1 products with top passage {self.chunks[i]['id']}:")
            print('First12 products: ' + ' '.join(f'{x:.9f}' for x in products[:12]))
            print(f'First12 subtotal: {products[:12].sum():.12f}')
            print(f'Remaining372 subtotal: {products[12:].sum():.12f}')
            print(f'Full384 sum: {products.sum():.12f}; direct cosine: {cosine[i]:.12f}')
            shown = [(float(v), c['id'], j+1) for c, d in zip(self.chunks, self.documents) for j,v in enumerate(d[:12])]
            shown += [(float(v), 'Q1', j+1) for j,v in enumerate(vector[:12])]
            print(f'Displayed-coordinate minimum (value, vector, coordinate): {min(shown)}')
            print(f'Displayed-coordinate maximum (value, vector, coordinate): {max(shown)}')
        return rows, selected

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('question')
    parser.add_argument('-k', type=positive, default=2)
    parser.add_argument('--inspect', action='store_true')
    args = parser.parse_args()
    retriever = Retriever()
    retriever.describe()
    retriever.retrieve(args.question, args.k, args.inspect)

