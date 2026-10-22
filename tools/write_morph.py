"""Write the word-part data built by tools/build_morph.py:
  exam/data/wmorph.js  window.WMORPH  — parts, part of speech, origin and word family of every word-bank word (word bank, flashcards)
  exam/data/xroot.js   learning-map module "แผนผังรากศัพท์" — one mind map per root / prefix / suffix / shared compound part,
                       every word with parts gets exactly one question (id 'mr-' + word) so progress stays with the word.
Run:  python3 tools/write_morph.py   (after editing morph_data / morph_lemma / morph_fix)
"""
import json, os, re, random, hashlib, collections
import build_morph as M
import build_bank as B
from morph_data import PREFIX, SUFFIX, ROOT
import morph_fix as FIX
from examdata import D

POSTH = {'n': 'คำนาม', 'v': 'คำกริยา', 'adj': 'คำคุณศัพท์', 'adv': 'คำกริยาวิเศษณ์', 'prep': 'คำบุพบท', 'pron': 'คำสรรพนาม', 'conj': 'คำสันธาน',
         'det': 'คำนำหน้านาม', 'excl': 'คำอุทาน', 'num': 'ตัวเลข', 'pv': 'phrasal verb', 'phr': 'วลี', 'part': 'คำเล็ก'}
INFLECT = {'s', 'ed', 'er_c', 'est'}          # grammar endings: shown in the parts, but not a map of their own
MAXW, MINW = 24, 3

def meaning(w):
    w = w.lower()
    if w in FIX.BASE_MEAN: return FIX.BASE_MEAN[w]
    if w in M.BANK: return B.short(M.BANK[w]['m'])
    return FIX.MEAN.get(w, '')

def part_th(t, k, i):
    if k == 'p': return PREFIX[i][1]
    if k == 's': return SUFFIX[i][1]
    if k == 'r': return ROOT[i][1]
    if k in 'bc': return meaning(t)
    return ''

def slug(w): return re.sub(r'[^a-z0-9]+', '_', w.lower()).strip('_')

def main():
    out, fam = M.main()
    W = M.W
    used = set()
    lines = []
    for x in W:
        k = x['w'].lower(); seg = out.get(k) or []
        for t, kk, i in seg:
            if kk in 'prs': used.add(kk + ':' + i)
        segs = '|'.join('%s~%s~%s' % (t, kk, i or '') for t, kk, i in seg)
        lines.append('\t'.join([k, segs, ','.join(M.POS.get(k) or []), M.origin(k), fam.get(k, '')]))
    A = {}
    for u in sorted(used):
        kk, i = u.split(':')
        if kk == 'p': A[u] = [PREFIX[i][0], PREFIX[i][1]]
        elif kk == 's': A[u] = [SUFFIX[i][0], SUFFIX[i][1], SUFFIX[i][3]]
        else: A[u] = [ROOT[i][0], ROOT[i][1], ROOT[i][2]]
    bases = {}
    for x in W:
        for t, kk, i in out.get(x['w'].lower()) or []:
            if kk in 'bc' and t not in M.BANK and meaning(t): bases[t] = meaning(t)
            if kk in 'bc' and t in FIX.BASE_MEAN: bases[t] = FIX.BASE_MEAN[t]
    js = 'window.WMORPH=' + json.dumps({'a': A, 'b': bases, 'p': POSTH, 'm': '\n'.join(lines)}, ensure_ascii=False, separators=(',', ':')) + ';\n'
    open(os.path.join(D, 'wmorph.js'), 'w', encoding='utf-8').write(js)
    print('wmorph', len(lines), 'words', len(js.encode()), 'bytes')

    # ---------- maps ----------
    singles = [x for x in W if ' ' not in x['w'] and '-' not in x['w'] and out.get(x['w'].lower())]
    cnt = collections.Counter()
    for x in singles:
        seg = out[x['w'].lower()]
        for t, kk, i in seg:
            if kk == 'r': cnt['r:' + i] += 1
            elif kk == 'p': cnt['p:' + i] += 1
            elif kk == 's' and i not in INFLECT: cnt['s:' + i] += 1
            elif kk == 'c': cnt['c:' + t] += 1
    def keys_of(seg):
        return [('r:' + i) for t, kk, i in seg if kk == 'r'] + [('p:' + i) for t, kk, i in seg if kk == 'p'] + \
               [('s:' + i) for t, kk, i in seg if kk == 's' and i not in INFLECT] + [('c:' + t) for t, kk, i in seg if kk == 'c']
    rank = {'r': 0, 'p': 1, 's': 2, 'c': 3}
    banned = set()
    while True:      # a root first (the one with most words), then prefix, suffix, compound part; drop maps that end up too small and place their words again
        home = collections.defaultdict(list)
        for x in singles:
            ks = [q for q in keys_of(out[x['w'].lower()]) if cnt[q] >= MINW and q not in banned]
            home[sorted(ks, key=lambda q: (rank[q[0]], -cnt[q]))[0] if ks else 'zz'].append(x)
        small = [q for q in home if q != 'zz' and len(home[q]) < MINW]
        if not small: break
        banned.update(small)
    def title(key):
        kk, i = key.split(':', 1)
        if kk == 'r': return ROOT[i][0], ROOT[i][1], 'รากศัพท์ · ' + ROOT[i][2], '🌱'
        if kk == 'p': return PREFIX[i][0], PREFIX[i][1], 'คำเติมหน้า (prefix)', '⬅️'
        if kk == 's': return SUFFIX[i][0], SUFFIX[i][1], 'คำเติมท้าย (suffix) → ' + POSTH.get(SUFFIX[i][3].split(',')[0], ''), '➡️'
        if kk == 'z': return {'comp': ('คำประสมอื่นๆ', 'คำสองคำต่อกันเป็นคำใหม่', '🧩'), 'infl': ('-s / -ed / -er', 'คำลงท้ายไวยากรณ์', '🔤'),
                              'rare': ('ส่วนที่พบน้อย', 'รากหรือคำเติมที่มีในคลังไม่กี่คำ', '🧷')}[i][:2] + ('รวมคำแยกส่วนอื่นๆ',) + ({'comp': '🧩', 'infl': '🔤', 'rare': '🧷'}[i],)
        return i, meaning(i), 'คำประสม (compound) ที่มีคำนี้', '🧩'
    # maps of a root or a prefix show every bank word that has it (questions only for the words whose home it is)
    show = collections.defaultdict(list)
    for x in singles:
        ks = set(keys_of(out[x['w'].lower()]))
        for q in ks:
            if q[0] in 'rp' and cnt[q] >= MINW: show[q].append(x)
    for x in home.pop('zz', []):
        seg = out[x['w'].lower()]
        z = 'z:comp' if all(kk == 'c' for t, kk, i in seg) else 'z:infl' if any(kk == 's' and i in INFLECT for t, kk, i in seg) and not any(kk in 'pr' for t, kk, i in seg) else 'z:rare'
        home[z].append(x)
    for q in list(home):
        if q[0] in 'scz' or q not in show: show[q] = home[q]
    order = sorted(show, key=lambda q: ({'r': 0, 'p': 1, 's': 2, 'c': 3, 'z': 4}[q[0]], -len(show[q]), q))
    homeof = {x['w'].lower(): q for q in home for x in home[q]}
    lessons, seen = [], set()
    GRPS = ['คำนาม', 'คำกริยา', 'คำคุณศัพท์', 'คำกริยาวิเศษณ์', 'อื่นๆ']
    def grp(k):
        p = (M.POS.get(k) or ['x'])[0]
        return {'n': 0, 'v': 1, 'adj': 2, 'adv': 3}.get(p, 4)
    def parts(seg): return ' + '.join((t + '-') if kk == 'p' else ('-' + t) if kk == 's' else t for t, kk, i in seg)
    def parts_th(seg): return ' + '.join((part_th(t, kk, i) or '…').split(' / ')[0] for t, kk, i in seg)
    for key in order:
        ws = sorted(show[key], key=lambda x: (grp(x['w'].lower()), x['w'].lower()))
        chunks = [ws[i:i + MAXW] for i in range(0, len(ws), MAXW)]
        if len(chunks) > 1 and len(chunks[-1]) < 6:
            last = chunks.pop(); chunks[-1] += last
        form, th, kind, em = title(key)
        for ci, ch in enumerate(chunks):
            lid = 'mrl-' + key.replace(':', '-') + ('' if len(chunks) == 1 else '-%d' % (ci + 1))
            b = []
            for x in ch:
                k = x['w'].lower(); seg = out[k]
                b.append([x['w'], B.short(x['m']), grp(k), parts(seg), parts_th(seg)])
            q = []
            for n, y in enumerate(b):
                if homeof.get(y[0].lower()) != key: continue
                seed = int(hashlib.md5(y[0].lower().encode()).hexdigest()[:8], 16); rnd = random.Random(seed)
                seg = out[y[0].lower()]
                cand = sorted(set(z[0] for z in b if z[0] != y[0] and z[1] != y[1]), key=str.lower)
                if len(cand) < 3: cand += [z['w'] for z in singles if z['w'] != y[0] and z['w'] not in cand][:20]
                o = [y[0]] + rnd.sample(cand, 3); rnd.shuffle(o)
                iid = 'mr-' + slug(y[0]); k2 = 2
                while iid in seen: iid = 'mr-%s_%d' % (slug(y[0]), k2); k2 += 1
                seen.add(iid)
                # type 1: which part means ...? (only for words with a prefix/root/suffix that has a meaning)
                aff = [j for j, (t, kk, i) in enumerate(seg) if kk in 'prs' and i not in INFLECT]
                if aff and rnd.random() < 0.4:
                    j = rnd.choice(aff); t, kk, i = seg[j]; right = part_th(t, kk, i)
                    pool = sorted(set(v[1] for kk2, d in (('p', PREFIX), ('r', ROOT), ('s', SUFFIX)) for v in d.values() if v[1] != right))
                    wrong = rnd.sample(pool, 3); opts = [right] + wrong; rnd.shuffle(opts)
                    lab = (t + '-') if kk == 'p' else ('-' + t) if kk == 's' else t
                    q.append([iid, 2, '|'.join(opts), opts.index(right), n, lab])
                else:
                    q.append([iid, 1, '|'.join(o), o.index(y[0]), n])
            th2 = '%s %s' % (form, th) + ('' if len(chunks) == 1 else ' (%d/%d)' % (ci + 1, len(chunks)))
            lessons.append(dict(id=lid, th=th2, grp=kind.split(' · ')[0] if key[0] == 'r' else kind.split(' →')[0], mm=dict(root=form, rt=th, em=em, kind=kind, b=b), q=q))
    n = sum(len(L['q']) for L in lessons)
    left = len(home.get('zz', []))
    js = '(window.__X=window.__X||{})["xroot"]=' + json.dumps({'v': 1, 'root': 1, 'gs': GRPS, 'lessons': lessons}, ensure_ascii=False, separators=(',', ':')) + ';\n'
    open(os.path.join(D, 'xroot.js'), 'w', encoding='utf-8').write(js)
    by = collections.Counter(L['grp'] for L in lessons)
    p = os.path.join(os.path.dirname(__file__), '..', 'index.html'); h = open(p, encoding='utf-8').read()
    h2 = re.sub(r'var XL_NR = \d+;', 'var XL_NR = %d;' % n, h)
    if h2 != h: open(p, 'w', encoding='utf-8').write(h2)
    print('xroot', len(lessons), 'maps', n, 'words', len(js.encode()), 'bytes', dict(by), '| words with parts but no map', left)

if __name__ == '__main__':
    main()
