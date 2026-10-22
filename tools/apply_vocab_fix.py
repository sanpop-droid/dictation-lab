"""Apply tools/vocab_fix.py to the VOCAB list in index.html (meanings only; spelling where a fix says so).
Entries that repeat an earlier entry exactly (same word, part of speech and meaning) get the same fix.
Run:  python3 tools/apply_vocab_fix.py   then rebuild the word maps:  python3 tools/build_bank.py
"""
import json, os
from vocab_fix import FIX
P = os.path.join(os.path.dirname(__file__), '..', 'index.html')

def main():
    s = open(P, encoding='utf-8').read()
    a = s.index('var VOCAB = ') + len('var VOCAB = '); b = s.index('];', a) + 1
    V = json.loads(s[a:b]); orig = [dict(x) for x in V]; n = 0
    first = {}
    for i, x in enumerate(orig):
        first.setdefault((x['w'], x.get('p'), x.get('m')), i)
    for i, x in enumerate(V):
        f = FIX.get(i)
        if f is None:
            j = first[(orig[i]['w'], orig[i].get('p'), orig[i].get('m'))]
            if j != i: f = FIX.get(j)
        if f is None: continue
        if isinstance(f, tuple): x['w'] = f[1]; x['m'] = f[2]
        else: x['m'] = f
        n += 1
    out = json.dumps(V, ensure_ascii=False)
    s = s[:a] + out + s[b:]
    open(P, 'w', encoding='utf-8').write(s)
    print('fixed', n, 'entries of', len(V))

if __name__ == '__main__':
    main()
