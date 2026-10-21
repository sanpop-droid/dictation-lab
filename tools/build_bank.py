"""Build exam/data/xbank.js: mind maps that cover every word in the word bank (คลังคำ).

Words come from index.html: the notebook VOCAB (merged like the app's word list W) plus the exam words (EXAM_WORDS).
Each word gets a topic and sub-branch from tools/bank_topics.py; maps are topic × level band
(A1–A2, B1–B2, คำศัพท์ข้อสอบ), at most MAXW words each. Every word has one fill-the-missing-branch question.
Question ids are 'mb-' + word, so progress stays with the word even if maps are regrouped later.
Run:  python3 tools/build_bank.py
"""
import json, os, random, re, hashlib
from examdata import D
import bank_topics as B

ROOT = os.path.join(os.path.dirname(__file__), '..')
MAXW = 24
BANDS = [('A', 'A1–A2', ('A1', 'A2')), ('B', 'B1–B2', ('B1', 'B2')), ('E', 'คำศัพท์ข้อสอบ', ('EXAM',))]

def words():
    s = open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read()
    i = s.index('var VOCAB = ') + len('var VOCAB = '); V = json.loads(s[i:s.index('];', i) + 1])
    i = s.index('var EXAM_WORDS = ') + len('var EXAM_WORDS = '); X = json.loads(s[i:s.index(']];', i) + 2])
    order = {'A1': 0, 'A2': 1, 'B1': 2, 'B2': 3}; g = {}; out = []
    for x in V:
        w = re.sub(r'\d+$', '', x['w']).strip()
        if len(w) > 1 and w == w.upper() and re.search('[A-Z]', w): continue
        k = w.lower()
        if k not in g: g[k] = dict(w=w, m=[], l=x['lvl']); out.append(g[k])
        e = g[k]
        if x['m'] and x['m'] not in e['m']: e['m'].append(x['m'])
        if order[x['lvl']] < order[e['l']]: e['l'] = x['lvl']
    for t in X:
        k = t[0].lower()
        if k in g: continue
        g[k] = dict(w=t[0], m=[t[1]], l='EXAM'); out.append(g[k])
    return out

def short(m):
    t = re.split(r'\s*[,/;]\s*', ' / '.join(m))[0].strip()
    return t[:34]

def labels():
    lab = {}
    for blk in B.L:
        for ln in [x for x in blk.strip().split('\n') if x.strip()]:
            c, ws = ln.split(':', 1)
            for w in ws.split('|'):
                w = w.strip().lower()
                if w: lab[w] = c.strip()
    return lab

def slug(w): return re.sub(r'[^a-z0-9]+', '_', w.lower()).strip('_')

def main():
    W = words(); lab = labels()
    gname = {g: n for t in B.TOPICS.values() for g, n in t[2]}
    gtopic = {g: tid for tid, t in B.TOPICS.items() for g, _ in t[2]}
    miss = [x['w'] for x in W if x['w'].lower() not in lab]
    assert not miss, ('unlabelled', miss[:20])
    lessons = []; seen = set()
    for tid, (tth, tem, gs) in B.TOPICS.items():
        for bid, bth, lv in BANDS:
            ws = [x for x in W if gtopic[lab[x['w'].lower()]] == tid and x['l'] in lv]
            if not ws: continue
            branches = []
            for g, gn in gs:
                gw = sorted([x for x in ws if lab[x['w'].lower()] == g], key=lambda x: x['w'].lower())
                if g in ('qual', 'do') and len(gw) > MAXW:       # big groups: split by word shape so branches stay meaningful
                    parts = [('ly', gn + ' · คำลงท้าย -ly', [x for x in gw if x['w'].endswith('ly') and ' ' not in x['w']]),
                             ('ph', gn + ' · วลีหลายคำ', [x for x in gw if ' ' in x['w']]),
                             ('', gn, [x for x in gw if not (x['w'].endswith('ly') and ' ' not in x['w']) and ' ' not in x['w']])]
                else:
                    parts = [('', gn, gw)]
                for _, pn, pw in parts:
                    for x in pw: branches.append((pn, x))
            # pack into maps of at most MAXW words, keeping a sub-branch together when it fits
            maps, cur = [], []
            for pn, x in branches:
                if len(cur) >= MAXW: maps.append(cur); cur = []
                cur.append((pn, x))
            if cur:
                if maps and len(cur) < 8 and len(maps[-1]) + len(cur) <= MAXW + 6: maps[-1] += cur
                else: maps.append(cur)
            for mi, mp in enumerate(maps):
                lid = 'mbl-%s-%s%s' % (tid, bid, '' if len(maps) == 1 else mi + 1)
                th = '%s · %s' % (tth, bth) + ('' if len(maps) == 1 else ' (%d/%d)' % (mi + 1, len(maps)))
                gl = []
                for pn, _ in mp:
                    if pn not in gl: gl.append(pn)
                b = [[x['w'], short(x['m']), gl.index(pn)] for pn, x in mp]
                q = []
                for i, y in enumerate(b):
                    seed = int(hashlib.md5(y[0].lower().encode()).hexdigest()[:8], 16); rnd = random.Random(seed)
                    cand = [z[0] for z in b if z[0] != y[0] and z[1] != y[1]]
                    if len(cand) < 3:
                        cand += [x['w'] for x in ws if x['w'] != y[0] and short(x['m']) != y[1] and x['w'] not in cand]
                    cand = sorted(set(cand), key=str.lower)
                    o = [y[0]] + rnd.sample(cand, 3); rnd.shuffle(o)
                    iid = 'mb-' + slug(y[0]); k2 = 2
                    while iid in seen: iid = 'mb-%s_%d' % (slug(y[0]), k2); k2 += 1
                    seen.add(iid)
                    q.append([iid, '|'.join(o), o.index(y[0])])
                lessons.append(dict(id=lid, th=th, grp=tem + ' ' + tth, mm=dict(root=tth, rt=bth, em=tem, gs=gl, b=b), q=q))
    n = sum(len(L['q']) for L in lessons)
    assert n == len(W), (n, len(W))
    js = '(window.__X=window.__X||{})["xbank"]=' + json.dumps({'v': 1, 'bank': 1, 'lessons': lessons}, ensure_ascii=False, separators=(',', ':')) + ';\n'
    open(os.path.join(D, 'xbank.js'), 'w', encoding='utf-8').write(js)
    print(len(lessons), 'maps', n, 'words', len(js.encode()), 'bytes')

if __name__ == '__main__':
    main()
