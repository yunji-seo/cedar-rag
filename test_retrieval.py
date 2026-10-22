"""Check assignment invariants, not a replica of the implementation."""
import unittest
from keyword_retriever import load_chunks, retrieve, words

class KeywordTests(unittest.TestCase):
    def test_metadata_and_count(self):
        chunks = load_chunks()
        self.assertEqual([c['id'] for c in chunks], ['A1', 'A2', 'B1', 'B2', 'T1', 'T2'])
        self.assertTrue(all('[' not in c['text'] for c in chunks))

    def test_hand_counted_q1(self):
        _, selected = retrieve(load_chunks(), 'May a trained graduate student operate the laser alone at 19:00?')
        self.assertEqual([(r['id'], r['score']) for r in selected], [('A1', 3), ('A2', 2)])
        self.assertEqual(selected[0]['matched'], ['00', 'graduate', 'trained'])

    def test_repetition_no_match_and_tie(self):
        chunks = load_chunks()
        self.assertEqual(retrieve(chunks, 'laser')[1], retrieve(chunks, 'laser laser laser')[1])
        self.assertEqual(retrieve(chunks, 'xyzzy')[1], [])
        self.assertEqual([r['id'] for r in retrieve(chunks, 'laser')[1]], ['A2', 'B1'])

    def test_no_stemming(self):
        self.assertNotEqual(words('student'), words('students'))
        self.assertEqual(words('the the and I'), set())

if __name__ == '__main__':
    unittest.main()
