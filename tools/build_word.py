"""Build the two authored modules of the learning map:
  exam/data/xword.js  สร้างคำและรากศัพท์ — Parts of Speech (11), Prefixes & Suffixes (11), Word Families & roots (12)   ids 'wf-<lesson>-<n>'
  exam/data/xwork.js  Business & Technical English — Business Writing (10), Technical English (10)                      ids 'wk-<lesson>-<n>'
Lessons are written by hand (tools/word_pos.py, word_affix.py, word_family.py, work_biz.py, work_tech.py). Lessons with `gen` also get
practice questions made from the word bank (parts and parts of speech from tools/build_morph.py), numbered after the hand-written ones,
so saved answers keep their ids when the bank grows. Then XL_N in index.html is updated with the question counts.
Run:  python3 tools/build_word.py
"""
import json, os, re, random, collections
import build_basic as BB
from examdata import D
from word_pos import POS
from word_affix import AFFIX
from word_family import FAMILY
from work_biz import BIZ
from work_tech import TECH
from morph_data import PREFIX, SUFFIX, ROOT

ROOTDIR = os.path.join(os.path.dirname(__file__), '..')
e = BB.e
KCLS = {'p': 'wp-p', 'r': 'wp-r', 's': 'wp-s', 'b': 'wp-b', 'c': 'wp-b', 'x': 'wp-x'}
KTH = {'p': 'prefix', 'r': 'root', 's': 'suffix', 'b': 'base', 'c': 'คำ', 'x': ''}
_vis = BB.vis_html
def vis_html(v):
    if v[0] == 'parts':
        rows = ''.join('<div class="wp-row"><b class="wp-w" lang="en">%s</b><span class="wp-eq">=</span><span class="wp-chips">%s</span><span class="wp-th">%s</span></div>' % (
            e(w), '<i class="wp-plus">+</i>'.join('<span class="wp %s"><b lang="en">%s</b><small>%s</small></span>' % (KCLS[k], e(t), e(m)) for t, k, m in parts), e(th)) for w, parts, th in v[1])
        return '<figure class="bv bv-parts">%s<figcaption>%s</figcaption></figure>' % (rows, e(v[2]))
    if v[0] == 'doc':
        rows = ''.join('<div class="wd-r"><span class="wd-l">%s</span><div class="wd-t" lang="en">%s</div></div>' % (e(lab), e(txt).replace('\n', '<br>')) for lab, txt in v[2])
        return '<figure class="bv bv-doc"><div class="wd"><div class="wd-h" lang="en">%s</div>%s</div><figcaption>%s</figcaption></figure>' % (e(v[1]), rows, e(v[3]))
    return _vis(v)
BB.vis_html = vis_html

# ---------- practice made from the word bank ----------
def bank():
    import build_morph as M
    out, fam = M.main()
    return M, out, fam

POSN = {'n': 'noun (คำนาม)', 'v': 'verb (คำกริยา)', 'adj': 'adjective (คำคุณศัพท์)', 'adv': 'adverb (คำกริยาวิเศษณ์)'}
def parts_text(seg): return ' + '.join((t + '-') if k == 'p' else ('-' + t) if k == 's' else t for t, k, i in seg)

def make_gen(spec, lid, M, out, fam):
    kind, n = spec[0], spec[1]; ids = spec[2] if len(spec) > 2 else None
    rnd = random.Random('gen-' + lid)
    W = [x for x in M.W if ' ' not in x['w'] and '-' not in x['w']]
    def short(x):
        t = re.split(r'\s*[,/;]\s*', ' / '.join(x['m']))[0].strip()
        if len(t) > 34: t = t[:34]
        if t.count('(') > t.count(')'): t = t[:t.rfind('(')].strip()
        return t
    wnp = lambda x: set(M.wn_pos(x['w'].lower()))
    one = [x for x in W if len(M.VP.get(x['w'].lower(), [])) == 1 and M.VP[x['w'].lower()][0] in ('n.', 'v.', 'adj.', 'adv.')]
    posof = lambda x: {'n.': 'n', 'v.': 'v', 'adj.': 'adj', 'adv.': 'adv'}[M.VP[x['w'].lower()][0]]
    one = [x for x in one if posof(x) in wnp(x) or not wnp(x)]            # the word list and WordNet agree
    only = [x for x in one if wnp(x) <= {posof(x)}]                         # words with one part of speech only
    notp = lambda p: [y for y in one if p not in wnp(y) and posof(y) != p]   # safe wrong answers: never that part of speech
    segof = lambda x: [] if any(k == 'b' and t not in M.BANK for t, k, i in (out.get(x['w'].lower()) or [])) else (out.get(x['w'].lower()) or [])
    qs, used = [], set()
    def pick(pool):
        pool = [x for x in pool if x['w'] not in used]
        if not pool: return None
        x = rnd.choice(pool); used.add(x['w']); return x
    tries = 0
    while len(qs) < n and tries < 400:
        tries += 1
        if kind == 'pos':
            x = pick(only)
            if not x: break
            p = posof(x); opts = [POSN[p]] + [POSN[q] for q in ('n', 'v', 'adj', 'adv') if q != p]
            suf = [t for t, k, i in segof(x) if k == 's']
            qs.append(['คำว่า "%s" (%s) เป็นคำชนิดใด?' % (x['w'], short(x)), opts, '%s เป็น %s%s' % (x['w'], POSN[p], (' สังเกตส่วนท้าย -' + suf[-1]) if suf else '')])
        elif kind in ('noun', 'verb', 'adj', 'adv'):
            p = {'noun': 'n', 'verb': 'v', 'adj': 'adj', 'adv': 'adv'}[kind]
            good = [x for x in only if posof(x) == p and segof(x) and segof(x)[-1][1] == 's' and SUFFIX[segof(x)[-1][2]][3].split(',')[0] == p]
            x = pick(good)
            if not x: break
            others = rnd.sample([y for y in notp(p) if y['w'] not in used], 3)
            suf = [t for t, k, i in segof(x) if k == 's'][-1]
            qs.append(['คำใดเป็น %s?' % POSN[p], [x['w']] + [y['w'] for y in others], '%s (%s) ลงท้ายด้วย -%s ซึ่งเป็น suffix ของ %s ส่วนคำอื่น: %s' % (
                x['w'], short(x), suf, POSN[p].split(' ')[0], ', '.join('%s = %s' % (y['w'], POSN[posof(y)].split(' ')[0]) for y in others))])
        elif kind == 'prefix':
            good = [x for x in W if any(k == 'p' and i in ids for t, k, i in segof(x)) and any(k in 'bc' for t, k, i in segof(x))]
            x = pick(good)
            if not x: break
            seg = segof(x); pk = [(t, i) for t, k, i in seg if k == 'p' and i in ids][0]
            same = [y for y in good if y['w'] != x['w'] and short(y) != short(x)]
            if len(same) < 3: same = [y for y in W if y['w'] != x['w']]
            wr = [short(y) for y in rnd.sample(same, 3)]
            if short(x) in wr or len(set(wr)) < 3: continue
            qs.append(['"%s" = %s แปลว่าอะไร? (%s- = %s)' % (x['w'], parts_text(seg), pk[0], PREFIX[pk[1]][1]), [short(x)] + wr, '%s = %s → %s' % (x['w'], parts_text(seg), short(x))])
        elif kind == 'suffix':
            good = [x for x in only if segof(x) and segof(x)[-1][1] == 's' and segof(x)[-1][2] in ids and SUFFIX[segof(x)[-1][2]][3].split(',')[0] == posof(x)]
            x = pick(good)
            if not x: break
            seg = segof(x); sk = (seg[-1][0], seg[-1][2]); p = posof(x)
            opts = [POSN[p]] + [POSN[q] for q in ('n', 'v', 'adj', 'adv') if q != p]
            qs.append(['"%s" (%s) ลงท้าย -%s เป็นคำชนิดใด?' % (x['w'], short(x), sk[0]), opts, '-%s (%s) ทำให้เป็น %s' % (sk[0], SUFFIX[sk[1]][1], POSN[p])])
        elif kind == 'root':
            good = [x for x in W if len(segof(x)) >= 2 and any(k == 'r' and i in ids for t, k, i in segof(x))]
            x = pick(good)
            if not x: break
            seg = segof(x); rk = [(t, i) for t, k, i in seg if k == 'r' and i in ids][0]
            if rnd.random() < 0.5:
                pool = sorted(set(v[1] for r, v in ROOT.items() if v[1] != ROOT[rk[1]][1]))
                wr = rnd.sample(pool, 3)
                qs.append(['ราก "%s" ในคำว่า "%s" (%s) แปลว่าอะไร?' % (rk[0], x['w'], short(x)), [ROOT[rk[1]][1]] + wr, '%s = %s ราก %s มาจาก%s แปลว่า %s' % (x['w'], parts_text(seg), ROOT[rk[1]][0], ROOT[rk[1]][2], ROOT[rk[1]][1])])
            else:
                bad = [y for y in W if not any(k == 'r' and i == rk[1] for t, k, i in segof(y)) and len(y['w']) >= 5 and not re.search(ROOT[rk[1]][3], y['w'].lower())]
                wr = [y['w'] for y in rnd.sample(bad, 3)]
                qs.append(['คำใดมีราก %s (%s)?' % (ROOT[rk[1]][0], ROOT[rk[1]][1]), [x['w']] + wr, '%s = %s' % (x['w'], parts_text(seg))])
        elif kind == 'split':
            good = [x for x in W if len(segof(x)) >= 3 and all(k != 'x' for t, k, i in segof(x)) and ''.join(t for t, k, i in segof(x)) == x['w'].lower()]
            x = pick(good)
            if not x: break
            seg = segof(x); right = parts_text(seg); w = x['w'].lower(); cuts = []
            pos = 0
            for t, k, i in seg[:-1]: pos += len(t); cuts.append(pos)
            wrong = set()
            for _ in range(30):
                c2 = sorted(set(min(len(w) - 1, max(1, c + rnd.choice((-2, -1, 1, 2)))) for c in cuts))
                if c2 == cuts or len(c2) != len(cuts): continue
                pieces = [w[a:b] for a, b in zip([0] + c2, c2 + [len(w)])]
                wrong.add(' + '.join(pieces))
                if len(wrong) >= 3: break
            if len(wrong) < 3: continue
            qs.append(['คำว่า "%s" (%s) แยกส่วนอย่างไรจึงถูกต้อง?' % (x['w'], short(x)), [right] + sorted(wrong)[:3], '%s = %s (%s)' % (x['w'], right, ' + '.join(
                (PREFIX[i][1].split(' / ')[0] if k == 'p' else SUFFIX[i][1] if k == 's' else ROOT[i][1].split(' / ')[0] if k == 'r' else t) for t, k, i in seg))])
        elif kind in ('fam', 'slot'):
            groups = collections.defaultdict(list)
            for x in one: groups[fam.get(x['w'].lower(), '')].append(x)
            fams = [g for k, g in groups.items() if k and len(set(posof(y) for y in g)) >= 3]
            if not fams: break
            g = rnd.choice(fams); key = fam[g[0]['w'].lower()]
            if key in used: continue
            used.add(key)
            if kind == 'slot':
                byp = {}
                for y in g: byp.setdefault(posof(y), y)
                p = rnd.choice(list(byp)); x = byp[p]
                if p not in wnp(x) and wnp(x): continue
                others = [byp[q]['w'] for q in byp if q != p and p not in wnp(byp[q])][:3]
                if len(others) < 2: continue
                if len(others) < 3:
                    extra = [y['w'] for y in notp(p) if y['w'] not in others and fam.get(y['w'].lower()) != key]
                    others += rnd.sample(extra, 3 - len(others))
                qs.append(['ในครอบครัวคำ "%s" คำใดเป็น %s?' % (key, POSN[p]), [x['w']] + others, '%s (%s) เป็น %s' % (x['w'], short(x), POSN[p])])
            else:
                x = rnd.choice(g); y2 = rnd.choice([y for y in g if y['w'] != x['w']])
                bad = [y['w'] for y in rnd.sample([y for y in one if fam.get(y['w'].lower()) != key and y['w'][0] == x['w'][0]] or one, 3)]
                qs.append(['คำใดอยู่ในครอบครัวเดียวกับ "%s" (%s)?' % (x['w'], short(x)), [y2['w']] + bad, '%s กับ %s มีแกนเดียวกัน (ครอบครัว %s)' % (x['w'], y2['w'], key)])
    # options must be unique
    return [q for q in qs if len(set(q[1])) == 4]

GROUPS_WORD = [('Parts of Speech — ชนิดของคำ', POS), ('Prefixes & Suffixes — คำเติมหน้าและคำเติมท้าย', AFFIX), ('Word Families — ครอบครัวคำและรากศัพท์', FAMILY)]
GROUPS_WORK = [('Business Writing — งานเขียนธุรกิจ', BIZ), ('Technical English — ภาษาอังกฤษเทคนิค', TECH)]

def module(key, prefix, seed, groups, M=None, out=None, fam=None):
    lessons = [L for g, Ls in groups for L in Ls]
    ids = [L['id'] for L in lessons]
    assert len(ids) == len(set(ids)), 'duplicate lesson id'
    gen = {}
    for L in lessons:
        for q in L['q']: assert len(q[1]) == 4 and len(set(q[1])) == 4, (L['id'], q[0])
        if L.get('gen') and M: gen[L['id']] = make_gen(L['gen'], L['id'], M, out, fam)
    built = BB.build([dict(id=L['id'], en=L['en'], th=L['th'], intro=L['intro'], r=L['r'], q=L['q']) for L in lessons], prefix, seed,
                     extra=gen or None, groups=[(g, [L['id'] for L in Ls]) for g, Ls in groups])
    byid = {L['id']: L for L in lessons}
    for L in built:
        src = byid[L['id']]
        L['html'] = BB.rich_html(L, src['rich']); L['r'] = []
        say, eg, rule = src['easy']; L['easy'] = {'say': say, 'eg': list(eg), 'rule': rule}
    js = '(window.__X=window.__X||{})["%s"]=' % key + json.dumps({'v': 1, 'lessons': built}, ensure_ascii=False, separators=(',', ':')) + ';\n'
    open(os.path.join(D, key + '.js'), 'w', encoding='utf-8').write(js)
    n = sum(len(L['items']) for L in built)
    print(key, len(built), 'lessons', n, 'questions (%d from the word bank)' % sum(len(v) for v in gen.values()), len(js.encode()), 'bytes')
    return n

def main():
    M, out, fam = bank()
    nw = module('xword', 'wf', 41, GROUPS_WORD, M, out, fam)
    nk = module('xwork', 'wk', 42, GROUPS_WORK)
    p = os.path.join(ROOTDIR, 'index.html'); s = open(p, encoding='utf-8').read()
    s2 = re.sub(r'var XL_N = \{ xword:\d+, xwork:\d+ \};', 'var XL_N = { xword:%d, xwork:%d };' % (nw, nk), s)
    if s2 != s: open(p, 'w', encoding='utf-8').write(s2); print('index.html XL_N updated')

if __name__ == '__main__':
    main()
