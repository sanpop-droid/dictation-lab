"""Break every word-bank word into prefix + root/base + suffix, find its part of speech and word family,
and write exam/data/wmorph.js (word bank, flashcards) and exam/data/xroot.js (root mind maps in the learning map).

Sources, in order of trust:
  1. tools/morph_fix.py — corrections checked by hand (always wins)
  2. etymology-db (Wiktionary) via tools/ety_bank.json — English affix structure, and Latin/Greek ancestors that prove a root
  3. WordNet (nltk) — real English words, parts of speech, derivationally related forms
  4. spelling rules for transparent suffixes (-ness, -ly, -ment ...) when the base is a real word
A word that cannot be broken down honestly is marked as a basic word (คำพื้นฐาน) instead of being given a guessed root.
Run:  python3 tools/build_morph.py            (needs: pip install nltk; python3 -m nltk.downloader wordnet)
      python3 tools/build_morph.py --review   (print the automatic decisions for checking)
"""
import json, os, re, sys, unicodedata, collections
import build_bank as B
from morph_data import PREFIX, SUFFIX, ROOT
from morph_lemma import LEMMA
import morph_fix as FIX

HERE = os.path.dirname(__file__)
os.environ.setdefault('NLTK_ALLOW_PROXIED_URLOPEN', '1')
from nltk.corpus import wordnet as wn

def N(t): return ''.join(c for c in unicodedata.normalize('NFD', t) if unicodedata.category(c) != 'Mn').lower()

W = B.words()
BANK = {x['w'].lower(): x for x in W}
ETY = json.load(open(os.path.join(HERE, 'ety_bank.json'), encoding='utf-8'))
WN = set(n.replace('_', ' ') for n in wn.all_lemma_names())
def real(w): return w in BANK or w in WN
def known(w): return w in BANK or w in FIX.MEAN
BASE_NOUN_ER = {}
def tidy(segs):
    out = []
    for x in segs:
        if out and out[-1][1] == x[1] and (out[-1][2] == x[2] or out[-1][0] == x[0]) and x[1] in 'ps': continue   # the same affix listed twice
        if out and out[-1][1] == 's' and x[1] == 's' and x[0].endswith(out[-1][0]) and len(x[0]) > len(out[-1][0]): out[-1] = x; continue   # -al + -ical, -ic + -ics
        if out and out[-1][1] == 's' and x[1] == 's' and x[0].endswith(out[-1][0][-2:]) and out[-1][2] == x[2]: out[-1] = x; continue   # -cy + -ency
        out.append(x)
    for i, x in enumerate(out):      # -al makes a noun only after a verb (arrive -> arrival); otherwise it is the adjective -al
        if x[2] == 'al_n' and not (i and out[i-1][1] == 'b' and 'v' in wn_pos(out[i-1][0])[:1]): x[2] = 'al'
    return out

# ---------- part of speech ----------
def vocab_pos():
    s = open(os.path.join(HERE, '..', 'index.html'), encoding='utf-8').read()
    i = s.index('var VOCAB = ') + len('var VOCAB = '); V = json.loads(s[i:s.index('];', i) + 1])
    out = {}
    for x in V:
        w = re.sub(r'\d+$', '', x['w']).strip().lower()
        out.setdefault(w, [])
        for p in re.findall(r'[a-z]+\.?(?: v\.)?', x.get('p', '')):
            out[w].append(p)
    return out
VP = vocab_pos()
PMAP = {'n.': 'n', 'v.': 'v', 'adj.': 'adj', 'adv.': 'adv', 'prep.': 'prep', 'pron.': 'pron', 'conj.': 'conj', 'det.': 'det',
        'exclam.': 'excl', 'number': 'num', 'modal v.': 'v', 'auxiliary v.': 'v', 'article': 'det', 'indefinite': 'det', 'definite': 'det',
        'modal': 'v', 'auxiliary': 'v', 'infinitive': 'part', 'marker': 'part', 'ordinal': 'num'}
WNP = {'n': 'n', 'v': 'v', 'a': 'adj', 's': 'adj', 'r': 'adv'}
PARTICLES = {'up', 'down', 'off', 'out', 'in', 'on', 'away', 'back', 'over', 'through', 'around', 'about', 'along', 'into', 'forward', 'ahead', 'aside', 'apart', 'by', 'together'}

def wn_pos(w):
    c = collections.Counter()
    for s in wn.synsets(w.replace(' ', '_')):
        for l in s.lemmas():
            if l.name().lower() == w.replace(' ', '_'): c[WNP[s.pos()]] += l.count() + 1
    return [p for p, _ in c.most_common()]

def pos_of(w):
    if w in VP and VP[w]:
        out = []
        for p in VP[w]:
            q = PMAP.get(p) or PMAP.get(p.split()[0])
            if q and q not in out: out.append(q)
        if out: return out
    p = wn_pos(w)
    if p: return p
    if ' ' in w:
        ws = w.split()
        if ws[-1] in PARTICLES and 'v' in wn_pos(ws[0]): return ['pv']
        return ['phr']
    return []

# ---------- affix lookup ----------
PFORM = {}
for k, (f, m, var) in PREFIX.items():
    for t in [f.strip('-')] + var: PFORM.setdefault(t, []).append(k)
SFORM = {}
for k, (f, m, var, p) in SUFFIX.items():
    for t in [f.strip('-')] + [v for v in var if not v.endswith('_n')]: SFORM.setdefault(t, []).append(k)
GREEK_FORM = {'tele': 'tele', 'micro': 'micro', 'auto': 'auto', 'photo': 'photo', 'bio': 'bio', 'geo': 'geo', 'psycho': 'psych', 'psych': 'psych',
              'philo': 'phil', 'phil': 'phil', 'hydro': 'hydr', 'thermo': 'therm', 'astro': 'astro', 'chrono': 'chron', 'techno': 'techn',
              'phone': 'phon', 'phono': 'phon', 'scope': 'scope', 'graph': 'graph', 'graphy': 'graph', 'gram': 'graph', 'meter': 'meter', 'metre': 'meter',
              'logy': 'log', 'ology': 'log', 'cracy': 'crat', 'crat': 'crat', 'nomy': 'nomos', 'sophy': 'soph', 'electro': 'electr', 'eco': 'eco',
              'cycle': 'cycl', 'cyclo': 'cycl', 'demo': 'dem', 'morph': 'morph', 'path': 'path', 'pathy': 'path', 'phobia': None, 'cardio': 'cardi', 'aqua': 'aqu'}

def pick_suffix(t, w, pos):
    t = t.strip('-').split('#')[0]
    ks = SFORM.get(t)
    if t in ('logy', 'ology'): return ('s', 'logy')
    if not ks: return None
    if t == 'ing': return ('s', 'ing_n' if pos and pos[0] == 'n' else 'ing')
    if pos is None and t in ('al', 'ly', 'en'): return ('s', {'al': 'al', 'ly': 'ly_adj', 'en': 'en_adj'}[t])
    if t == 'ly': return ('s', 'ly_adj' if pos and pos[0] == 'adj' else 'ly')
    if t == 'al': return ('s', 'al_n' if pos and pos[0] == 'n' and not w.endswith('ical') else 'al')
    if t == 'en': return ('s', 'en' if pos and pos[0] == 'v' else 'en_adj')
    if t == 'er':
        return ('s', 'er_c' if pos and pos[0] == 'adj' else 'er')
    if t == 'y': return ('s', 'y')
    if t == 'ty': return ('s', 'ty_n' if w.endswith(('twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety')) else 'ity')
    return ('s', ks[0])

def pick_prefix(t, w, rest):
    t = t.strip('-').split('#')[0]
    if t in GREEK_FORM and GREEK_FORM[t]: return ('r', GREEK_FORM[t])
    ks = PFORM.get(t)
    if not ks: return None
    if 'in_not' in ks:
        neg = False
        for s in wn.synsets(w.replace(' ', '_')):
            for l in s.lemmas():
                if any(a.name().lower() == rest for a in l.antonyms()): neg = True
        if neg or (rest and real(rest) and wn_pos(rest)[:1] == ['adj'] and (POS.get(w) or wn_pos(w))[:1] in (['adj'], ['adv']) and t in ('in', 'im', 'il', 'ir')): return ('p', 'in_not')
        return ('p', 'in_into')
    if t == 'a': return ('p', 'a_on') if real(rest) else ('p', 'ad')
    if t == 'em': return ('p', 'en')
    return ('p', ks[0])

# ---------- roots ----------
LEM = {r: set(N(x) for x in xs) for r, xs in LEMMA.items()}
def anc_set(w, depth=0):
    e = ETY.get(w)
    out = set()
    if e:
        for lang, t in e['anc']:
            if lang != 'English': out.add(N(t).strip('-').strip())
            if lang != 'English': out.add(N(t))
    return out

def root_hits(core, ancs):
    """roots whose spelling is inside core and whose Latin/Greek word is in the ancestors; non-overlapping, left to right"""
    hits = []
    for r, (form, th, org, rx) in ROOT.items():
        if r not in LEM or not (LEM[r] & ancs): continue
        for m in re.finditer(rx, core):
            hits.append((m.start(), m.end(), r))
    hits = [h for h in hits if not (h[0] >= 2 and parse_suffixes(core[h[0]:], core, None))]   # 'ag' inside -age, 'ment' inside -ment is a suffix, not a root
    hits.sort(key=lambda h: (h[0], -(h[1] - h[0])))
    out, end = [], -1
    for h in hits:
        if h[0] >= end: out.append(h); end = h[1]
    return out

def parse_prefixes(s, w, rest_after):
    """split s into known prefixes, longest first; None if impossible"""
    if not s: return []
    for n in range(len(s), 0, -1):
        t = s[:n]
        if t in PFORM or (t in GREEK_FORM and GREEK_FORM[t]):
            tail = parse_prefixes(s[n:], w, rest_after)
            if tail is not None:
                p = pick_prefix(t, w, s[n:] + rest_after)
                if p: return [[t, p[0], p[1]]] + tail
    return None

def parse_suffixes(s, w, pos):
    if not s: return []
    for n in range(len(s), 0, -1):
        t = s[:n]
        if t in SFORM:
            tail = parse_suffixes(s[n:], w, pos)
            if tail is not None:
                p = pick_suffix(t, w, pos if not tail else ['n'])
                if p: return [[t, p[0], p[1]]] + tail
    return None

def root_segment(core, w, ancs, pos):
    hits = root_hits(core, ancs)
    if not hits: return None
    segs, i = [], 0
    for k, (a, b, r) in enumerate(hits):
        gap = core[i:a]
        if gap:
            if k == 0:
                pp = parse_prefixes(gap, w, core[a:])
                segs += pp if pp is not None else [[gap, 'x', None]]
            else:
                segs.append([gap, 'x', None])
        segs.append([core[a:b], 'r', r]); i = b
    tail = core[i:]
    if tail:
        ss = parse_suffixes(tail, w, pos)
        if ss is None:            # letters that belong to the root's spelling (scrib-e, duc-e) or a suffix after them
            for cut in range(1, len(tail)):
                ss2 = parse_suffixes(tail[cut:], w, pos)
                if ss2 is not None:
                    segs[-1][0] += tail[:cut]; segs += ss2; break
            else:
                segs[-1][0] += tail
        else:
            segs += ss
    return segs

# ---------- base word + suffix by spelling rules ----------
def bases(stem, suf):
    c = [stem, stem + 'e']
    if stem.endswith('i'): c += [stem[:-1] + 'y', stem[:-1] + 'ie']
    if len(stem) > 2 and stem[-1] == stem[-2] and stem[-1] not in 'aeiouls': c.append(stem[:-1])
    if suf in ('ly', 'ity') and stem.endswith(('b', 'p', 'd', 'g', 't')): c.append(stem + 'le')
    if suf == 'ity' and stem.endswith('bil'): c.append(stem[:-3] + 'ble')
    if suf in ('ation', 'ion', 'ive', 'or'): c += [stem + 'ate', stem + 'e']
    if suf == 'ication': c += [stem + 'y', stem + 'ify']
    if suf in ('ence', 'ency'): c += [stem + 'ent']
    if suf in ('ance', 'ancy'): c += [stem + 'ant']
    if suf == 'sion': c += [stem + 'de', stem + 'd', stem + 't', stem + 'se']
    if suf in ('ous', 'ious'): c += [stem + 'y', stem + 'e']
    if suf == 'ily': c.append(stem + 'y')
    if suf == 'ally': c += [stem + 'al', stem]
    if suf == 'ically': c += [stem + 'ic', stem + 'ical']
    if suf == 'ed': c.append(stem + 'e')
    return [b for b in c if len(b) >= 3]

TRANSPARENT = {'ness', 'ly', 'ily', 'ally', 'less', 'ful', 'ment', 'ship', 'hood', 'ist', 'ism', 'ize', 'ise', 'ify', 'able', 'ible', 'er', 'or',
               'ee', 'ity', 'ation', 'ition', 'ion', 'sion', 'ive', 'ative', 'ous', 'ious', 'al', 'ial', 'ical', 'ic', 'y', 'ish', 'ence', 'ance',
               'ency', 'ancy', 'ant', 'ent', 'age', 'ure', 'ery', 'ry', 'en', 'ing', 'ed', 'ward', 'wards', 'wise', 'some', 'like', 'teen', 'ty', 'dom', 'ics', 'th', 'an', 'ian', 'ese', 'ary', 'ory', 'est', 'ically', 'ication', 's', 'es'}
def deriv_linked(w, b):
    for s in wn.synsets(w.replace(' ', '_')):
        for l in s.lemmas():
            if l.name().lower() != w: continue
            for d in l.derivationally_related_forms():
                if d.name().lower() == b: return True
            for p in l.pertainyms():
                if p.name().lower() == b: return True
    return False

def auto_suffix(w, pos):
    for suf in sorted(SFORM, key=len, reverse=True):
        if not w.endswith(suf) or len(w) - len(suf) < 2 or suf not in TRANSPARENT: continue
        if suf in ('s', 'es', 'ed', 'en', 'an', 'th', 'y', 'ty', 'er', 'or', 'ry', 'ant', 'ent', 'age', 'ure', 'ic', 'al', 'ist', 'ive', 'ary', 'ory', 'ish', 'ee', 'ing', 'est'):
            strict = True          # short endings: only when WordNet links the two words, or the base is a bank word with a matching meaning
        else:
            strict = False
        for b in bases(w[:-len(suf)], suf):
            if b == w or not known(b): continue
            ok = deriv_linked(w, b) or deriv_linked(b, w)
            if not ok and not strict and b in BANK: ok = True
            if not ok and suf in ('ly', 'ily', 'ally', 'ness', 'less', 'ful', 'ment') and known(b): ok = True
            if ok: return b, suf
    return None

SAFE_PRE = ['un', 'non', 'mis', 'over', 'under', 'out', 'multi', 'semi', 'self', 'anti', 'inter', 'super', 'mid', 'fore', 'pre', 'post', 'dis', 're', 'sub', 'tele', 'micro', 'auto', 'mini', 'co', 'in', 'im', 'il', 'ir', 'up', 'down', 'counter', 'trans', 'extra', 'ultra', 'mega', 'bi', 'tri', 'uni', 'mono', 'de', 'en', 'em', 'with', 'be', 'a']
def auto_prefix(w):
    for p in sorted(SAFE_PRE, key=len, reverse=True):
        rest = w[len(p):].lstrip('-')
        if w.startswith(p) and len(rest) >= 3 and known(rest):
            return p, rest
    return None

def auto_compound(w):
    if len(w) < 6 or not w.isalpha(): return None
    best = None
    for i in range(3, len(w) - 2):
        a, b = w[:i], w[i:]
        if a in BANK and b in BANK and len(b) >= 3:
            if best is None or abs(len(a) - len(b)) < abs(len(best[0]) - len(best[1])): best = (a, b)
    return best

# ---------- main analysis ----------
MEMO = {}
LOG = collections.defaultdict(list)

def analyze(w, depth=0):
    """list of [text, kind, id] or None; kind p=prefix r=root s=suffix b=base word c=part of a compound/phrase x=other letters"""
    if w in MEMO: return MEMO[w]
    if depth > 4: return None
    MEMO[w] = None
    CUR.append(w)
    try: res = _analyze(w, depth)
    finally: CUR.pop()
    MEMO[w] = res
    return res

BASEOF = collections.defaultdict(set)
CUR = []
def expand_base(t, depth):
    """a base word inside another word: break it further when possible"""
    if CUR: BASEOF[CUR[-1]].add(t)
    sub = analyze(t, depth + 1)
    if sub and not (len(sub) == 1 and sub[0][1] == 'b'): return [list(x) for x in sub] , True
    return [[t, 'b', None]], False

def _analyze(w, depth):
    pos = POS.get(w) or pos_of(w)
    if w in FIX.SEG:
        v = FIX.SEG[w]
        if v is None: return None
        return [list(x) for x in v]
    if ' ' in w or '-' in w:
        parts = [p for p in re.split(r'[ -]', w) if p]
        return [[p, 'c', None] for p in parts]
    e = ETY.get(w)
    ancs = anc_set(w)
    if e and e['en'] and w not in FIX.NO_ETY:
        rels = e['en']
        comp = [t for r, t in rels if r == 'compound_of']
        if len(comp) >= 2 and all(real(c.lower()) for c in comp) and ''.join(c.lower() for c in comp).replace('-', '') in (w, w.replace('-', '')) :
            LOG['ety-compound'].append('%s = %s' % (w, ' + '.join(comp)))
            return [[c.lower(), 'c', None] for c in comp]
        pre = [t for r, t in rels if r == 'has_prefix']
        base = [t.split('#')[0].lower() for r, t in rels if r == 'has_prefix_with_root']
        suf = [t for r, t in rels if r == 'has_suffix']
        aff = []
        for r, t in rels:
            if r in ('has_affix', 'has_confix'):
                t2 = t.split('#')[0]
                if t2 not in aff: aff.append(t2)
        segs = []
        conf = [t.split('#')[0] for r, t in rels if r == 'has_confix']
        if len(conf) >= 2 and not (pre or suf or base):
            pre, suf, base = [conf[0] + '-'], ['-' + conf[-1]], [c.lower() for c in conf[1:-1]]
        elif aff and not (pre or suf or base):
            ps = [a for a in aff if a.endswith('-')]; ss = [a for a in aff if a.startswith('-')]; ms = [a.lower() for a in aff if not a.startswith('-') and not a.endswith('-')]
            pre, suf, base = ps, ss, ms
        for p in pre:
            rest = w[len(p.strip('-')):] if w.startswith(p.strip('-')) else (base[0] if base else '')
            pk = pick_prefix(p, w, rest)
            if not pk: segs = None; break
            segs.append([p.strip('-'), pk[0], pk[1]])
        if segs is not None:
            if pre and not base and not suf:
                p0 = pre[-1].strip('-'); rest = w[len(p0):] if w.startswith(p0) else ''
                if rest: base = [rest]
            for b in base[:1]:
                if known(b) and b != w:
                    sub, _ = expand_base(b, depth); segs += sub
                else:
                    sub = analyze(b, depth + 1) if real(b) and b != w else None
                    rs = sub or (root_segment(b, w, ancs | anc_set(b), pos) if b else None)
                    if rs and any(k in 'pr' for _, k, _ in rs): segs += [list(x) for x in rs]
                    elif b in GREEK_FORM and GREEK_FORM[b]: segs.append([b, 'r', GREEK_FORM[b]])
                    else: segs = None; break
            if segs is not None and not base and suf and not pre:
                # suffix only (florist = flor + ist): the rest of the word is the stem
                st = suf[-1].strip('-')
                stem = w[:-len(st)] if w.endswith(st) else w
                rs = root_segment(stem, w, ancs, pos)
                if rs: segs += rs
                elif known(stem) and stem != w: segs += expand_base(stem, depth)[0]
                else: segs = None
        if segs is not None:
            for n, sx in enumerate(suf):
                t = sx.strip('-')
                if t in GREEK_FORM and GREEK_FORM[t]: segs.append([t, 'r', GREEK_FORM[t]]); continue
                last = n == len(suf) - 1
                sk = pick_suffix(t, w, pos if last else None)
                if t == 'er' and base and known(base[0]) and wn_pos(base[0])[:1] == ['adj'] and not BASE_NOUN_ER.get(w): sk = ('s', 'er_c')
                if not sk: segs = None; break
                segs.append([t, sk[0], sk[1]])
        segs = tidy(segs) if segs else segs
        if segs and any(k in 'prs' for _, k, _ in segs):
            LOG['ety'].append('%s = %s' % (w, ' + '.join('%s[%s]' % (t, i or k) for t, k, i in segs)))
            return segs
    # no usable etymology structure: suffix rules, then a root inside the word, then prefix / compound checks
    a = auto_suffix(w, pos) if w not in FIX.NOT_SUFFIX else None
    if a:
        b, suf = a
        sk = pick_suffix(suf, w, pos)
        if sk:
            sub, _ = expand_base(b, depth)
            LOG['auto-suffix'].append('%s = %s + -%s' % (w, b, suf))
            return sub + [[suf, sk[0], sk[1]]]
    rs = root_segment(w, w, ancs, pos)
    if rs:
        LOG['root'].append('%s = %s' % (w, ' + '.join('%s[%s]' % (t, i or k) for t, k, i in rs)))
        return rs
    p = auto_prefix(w) if w not in FIX.NOT_PREFIX else None
    if p:
        pk = pick_prefix(p[0], w, p[1])
        if pk:
            sub, _ = expand_base(p[1], depth)
            LOG['auto-prefix'].append('%s = %s- + %s' % (w, p[0], p[1]))
            return [[p[0], pk[0], pk[1]]] + sub
    c = auto_compound(w)
    if c and w not in FIX.NOT_COMPOUND:
        LOG['auto-compound'].append('%s = %s + %s' % (w, c[0], c[1]))
        return [[c[0], 'c', None], [c[1], 'c', None]]
    return None

POS = {}
ORG = [('Latin', 'ละติน'), ('Medieval Latin', 'ละติน'), ('Late Latin', 'ละติน'), ('New Latin', 'ละติน'), ('Vulgar Latin', 'ละติน'), ('Old Latin', 'ละติน'),
       ('Ecclesiastical Latin', 'ละติน'), ('Classical Latin', 'ละติน'), ('Ancient Greek', 'กรีก'), ('Koine Greek', 'กรีก'), ('Byzantine Greek', 'กรีก'), ('Greek', 'กรีก'), ('Mycenaean Greek', 'กรีก'),
       ('Old English', 'อังกฤษดั้งเดิม'), ('Middle English', 'อังกฤษดั้งเดิม'), ('English', 'อังกฤษดั้งเดิม'),
       ('Old French', 'ฝรั่งเศส'), ('French', 'ฝรั่งเศส'), ('Middle French', 'ฝรั่งเศส'), ('Anglo-Norman', 'ฝรั่งเศส'), ('Old Northern French', 'ฝรั่งเศส'),
       ('Old Norse', 'นอร์สโบราณ (ไวกิ้ง)'), ('Frankish', 'แฟรงก์ (เยอรมันโบราณ)'), ('German', 'เยอรมัน'), ('Old High German', 'เยอรมัน'), ('Middle High German', 'เยอรมัน'),
       ('Dutch', 'ดัตช์'), ('Middle Dutch', 'ดัตช์'), ('Old Dutch', 'ดัตช์'), ('Middle Low German', 'ดัตช์'), ('Old Saxon', 'เยอรมัน'), ('Italian', 'อิตาลี'), ('Spanish', 'สเปน'),
       ('Portuguese', 'โปรตุเกส'), ('Arabic', 'อาหรับ'), ('Japanese', 'ญี่ปุ่น'), ('Chinese', 'จีน'), ('Mandarin', 'จีน'), ('Cantonese', 'จีน'), ('Sanskrit', 'สันสกฤต'), ('Hindi', 'ฮินดี'),
       ('Persian', 'เปอร์เซีย'), ('Hebrew', 'ฮีบรู'), ('Gaulish', 'กอล (เคลต์)'), ('Turkish', 'ตุรกี'), ('Ottoman Turkish', 'ตุรกี'), ('Malay', 'มลายู'), ('Russian', 'รัสเซีย'),
       ('Old Irish', 'ไอริช'), ('Irish', 'ไอริช'), ('Middle Irish', 'ไอริช'), ('Etruscan', 'อีทรัสคัน'), ('Egyptian', 'อียิปต์'), ('Phoenician', 'ฟินิเชีย'), ('Nahuatl', 'แอซเท็ก (นาวัตล์)'),
       ('Classical Nahuatl', 'แอซเท็ก (นาวัตล์)'), ('Tamil', 'ทมิฬ'), ('Malayalam', 'มลยาฬัม'), ('Swedish', 'สวีเดน'), ('Danish', 'เดนมาร์ก'), ('Norwegian', 'นอร์เวย์'), ('Icelandic', 'ไอซ์แลนด์'),
       ('Welsh', 'เวลส์'), ('Scots', 'สกอต'), ('Old Occitan', 'ฝรั่งเศส'), ('Occitan', 'ฝรั่งเศส'), ('Catalan', 'สเปน'), ('Polish', 'โปแลนด์'), ('Czech', 'เช็ก'), ('Hungarian', 'ฮังการี'),
       ('Korean', 'เกาหลี'), ('Thai', 'ไทย'), ('Taino', 'ไทโน (แคริบเบียน)'), ('Quechua', 'เกชัว (อินคา)'), ('Tupi', 'ตูปี (บราซิล)')]
ORGD = dict(ORG)
def origin(w):
    e = ETY.get(w)
    if not e or not e['org']: return ''
    labs = []
    for lang in e['org']:
        t = ORGD.get(lang)
        if t and (not labs or labs[-1] != t): labs.append(t)
    if not labs: return ''
    deep = labs[-1]
    if deep == 'อังกฤษดั้งเดิม': return 'อังกฤษดั้งเดิม'
    via = [x for x in labs[:-1] if x not in ('อังกฤษดั้งเดิม', deep)]
    return deep + (' (ผ่าน' + via[-1] + ')' if via else '')

def families(out):
    parent = {}
    def f(x):
        parent.setdefault(x, x)
        while parent[x] != x: parent[x] = parent[parent[x]]; x = parent[x]
        return x
    def u(a, b): parent[f(a)] = f(b)
    singles = [k for k in out if ' ' not in k and '-' not in k]
    for k in singles:
        for b in BASEOF.get(k, ()):
            if b in BANK and ' ' not in b and len(b) >= 3 and k not in FIX.FAM_SKIP: u(k, b)
        for s in wn.synsets(k):
            for l in s.lemmas():
                if l.name().lower() != k: continue
                for d in l.derivationally_related_forms():
                    dn = d.name().lower()
                    if dn in BANK and dn != k and dn[:2] == k[:2] and ' ' not in dn and k not in FIX.FAM_SKIP and dn not in FIX.FAM_SKIP: u(k, dn)
    groups = collections.defaultdict(list)
    for k in singles: groups[f(k)].append(k)
    fam = {}
    for g in groups.values():
        if len(g) < 2: continue
        key = sorted(g, key=lambda x: (len(x), x))[0]
        for k in g: fam[k] = key
    return fam, groups

def main(review=False):
    for x in W: POS[x['w'].lower()] = pos_of(x['w'].lower())
    out = {}
    for x in W:
        k = x['w'].lower(); out[k] = analyze(k)
    n = sum(1 for v in out.values() if v); single = [k for k in out if ' ' not in k and '-' not in k]
    print('analysed', n, 'of', len(out), '| single words', len(single), 'with parts', sum(1 for k in single if out[k]))
    fam, groups = families(out)
    sizes = collections.Counter(len(g) for g in groups.values() if len(g) > 1)
    print('families', sum(sizes.values()), 'words in families', sum(k * v for k, v in sizes.items()), 'biggest', max(sizes))
    if review:
        for k, v in LOG.items():
            print('\n=====', k, len(v))
            for line in v: print(line)
        big = sorted((g for g in groups.values() if len(g) > 1), key=len, reverse=True)
        print('\n===== families (largest 40)')
        for g in big[:40]: print(len(g), ' '.join(sorted(g)))
    return out, fam

if __name__ == '__main__':
    main('--review' in sys.argv)
