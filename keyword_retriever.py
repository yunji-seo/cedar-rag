"""Transparent standard-library word overlap retriever."""
import argparse
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
STOPWORDS = set('a an the is are to of in at for and or may can i it be'.split())

def load_chunks():
    chunks = []
    for path in sorted((ROOT / 'docs').glob('*.txt')):
        for paragraph in path.read_text(encoding='utf-8').strip().split('\n\n'):
            match = re.fullmatch(r'\[([A-Z]\d+)\] (.+)', paragraph.strip())
            if not match:
                raise ValueError(f'Malformed paragraph in {path.name}')
            chunks.append(dict(id=match[1], filename=path.name, text=match[2]))
    assert len(chunks) == 6 and len({c['id'] for c in chunks}) == 6
    return sorted(chunks, key=lambda c: c['id'])

def words(text):
    return set(re.findall(r'[a-z0-9]+', text.lower())) - STOPWORDS

def retrieve(chunks, question, k=2):
    query = words(question)
    rows = [dict(**c, matched=sorted(query & words(c['text'])),
                 score=len(query & words(c['text']))) for c in chunks]
    rows.sort(key=lambda row: (-row['score'], row['id']))
    return rows, [r for r in rows if r['score'] > 0][:k]

def show(rows, selected):
    for row in rows:
        print(f"{row['id']} score={row['score']} matched={', '.join(row['matched']) or '(none)'}")
    if not selected:
        print('No matching passages.')
    for row in selected:
        print(f"SELECTED [{row['id']}] {row['filename']}: {row['text']}")

def positive(value):
    number = int(value)
    if number < 1:
        raise argparse.ArgumentTypeError('k must be positive')
    return number

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('question')
    parser.add_argument('-k', type=positive, default=2)
    args = parser.parse_args()
    show(*retrieve(load_chunks(), args.question, args.k))
