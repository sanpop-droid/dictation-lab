"""Pull the etymology of every word-bank word out of etymology-db (Wiktionary data, CC BY-SA) into tools/ety_bank.json.

  curl -L -o ety.csv.gz https://github.com/droher/etymology-db/releases/latest/download/etymology.csv.gz
  python3 tools/ety_extract.py ety.csv.gz

ety_bank.json: word -> {en: [[relation, English part], ...], anc: [[language, term], ...] (ancestors, nearest first),
                        org: [language, ...] (the borrowing / inheritance chain)}
Only tools/build_morph.py reads it; the app never loads it.
"""
import csv, gzip, json, os, sys, unicodedata
import build_bank as B

HERE = os.path.dirname(__file__)
SKIP = {'cognate_of', 'doublet_with', 'calque_of', 'semantic_loan_of', 'group_related_root', 'etymologically_related_to_skip'}
CHAIN = {'inherited_from', 'borrowed_from', 'derived_from', 'learned_borrowing_from', 'unadapted_borrowing_from', 'orthographic_borrowing_from'}
AFFIX = {'has_prefix', 'has_suffix', 'has_affix', 'has_confix', 'compound_of', 'has_prefix_with_root', 'blend_of', 'clipping_of', 'back-formation_from'}

def N(t): return ''.join(c for c in unicodedata.normalize('NFD', t) if unicodedata.category(c) != 'Mn').lower()

def scan(path, keys):
    got = {}
    with gzip.open(path, 'rt', encoding='utf-8') as f:
        r = csv.reader(f); next(r)
        for row in r:
            if len(row) < 11: continue
            k = (row[1], N(row[2]))
            if k in keys: got.setdefault(k, []).append((row[3], row[5], row[6], row[8], row[9]))
    return got

def follow(rs):
    """the rows worth following: the borrowing/inheritance chain, affix parts, and members of an affix group"""
    groups = {g for rel, lang, term, g, p in rs if rel == 'group_affix_root'}
    return [(rel, lang, term) for rel, lang, term, g, p in rs
            if term and not lang.startswith('Proto-') and (rel in CHAIN or rel in AFFIX or (p and p in groups))]

def main(path):
    words = [x['w'] for x in B.words()]
    rows = scan(path, {('English', N(w)) for w in words})
    level = rows
    for _ in range(7):
        nxt = {(lang, N(term)) for rs in level.values() for rel, lang, term in follow(rs)} - set(rows)
        if not nxt: break
        level = scan(path, nxt); rows.update(level)
    out = {}
    for w in words:
        k0 = ('English', N(w)); rs = rows.get(k0, [])
        en = [[rel, term] for rel, lang, term, g, p in rs if rel in AFFIX and lang == 'English']
        anc, seen, queue = [], {k0}, [(k0, 0)]
        while queue:
            k, d = queue.pop(0)
            if d > 7: continue
            for rel, lang, term in follow(rows.get(k, [])):
                kk = (lang, N(term))
                if kk in seen: continue
                seen.add(kk); anc.append([lang, kk[1]]); queue.append((kk, d + 1))
        org, k = [], k0                      # main line: first chain row at each step
        for _ in range(8):
            nx = [(lang, N(term)) for rel, lang, term, g, p in rows.get(k, []) if rel in CHAIN and term and not lang.startswith('Proto-')]
            if not nx: break
            for x in nx:
                if x[0] not in org: org.append(x[0])
            k = nx[-1]
        if en or anc: out[w.lower()] = {'en': en, 'anc': anc[:80], 'org': org}
    json.dump(out, open(os.path.join(HERE, 'ety_bank.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    print(len(out), 'words with etymology of', len(words))

if __name__ == '__main__':
    main(sys.argv[1])
