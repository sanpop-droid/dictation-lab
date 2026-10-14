"""Build the vocabulary lessons from the two books in exam/data/books.js:
  exam/data/x600.js  — 600 Essential Words: 50 topic lessons, word list + practice (meaning, and a gap in the book's example)
  exam/data/xcyev.js — Check Your English Vocabulary: 42 units to read, do on paper, then check with the answer key
Run:  python3 tools/build_vocab.py
"""
import json, os, random, re, html
from examdata import load, D

def esc(x): return html.escape(str(x), quote=True)
SPK = '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M4 9v6h4l5 4V5L8 9H4z"/><path d="M16 8.5a5 5 0 0 1 0 7" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>'
TH600 = ['สัญญา', 'การตลาด', 'การรับประกันสินค้า', 'การวางแผนธุรกิจ', 'การประชุมสัมมนา', 'คอมพิวเตอร์', 'เทคโนโลยีในสำนักงาน', 'ขั้นตอนงานในสำนักงาน', 'อิเล็กทรอนิกส์', 'การติดต่อทางจดหมาย', 'ประกาศรับสมัครงานและการสรรหา', 'การสมัครงานและการสัมภาษณ์', 'การจ้างงานและการฝึกอบรม', 'เงินเดือนและสวัสดิการ', 'การเลื่อนตำแหน่ง เงินบำนาญ และรางวัล', 'การซื้อของ', 'การสั่งซื้อวัสดุสิ้นเปลือง', 'การขนส่งสินค้า', 'ใบแจ้งหนี้', 'สินค้าคงคลัง', 'การธนาคาร', 'การบัญชี', 'การลงทุน', 'ภาษี', 'งบการเงิน', 'อาคารสถานที่และแผนกต่างๆ', 'การประชุมคณะกรรมการ', 'การควบคุมคุณภาพ', 'การพัฒนาผลิตภัณฑ์', 'การเช่าและการให้เช่า', 'การเลือกร้านอาหาร', 'การทานอาหารนอกบ้าน', 'การสั่งอาหารกลางวัน', 'อาชีพด้านการทำอาหาร', 'การจัดงานและอีเวนต์', 'การเดินทางทั่วไป', 'สายการบิน', 'รถไฟ', 'โรงแรม', 'การเช่ารถ', 'ภาพยนตร์', 'ละครเวที', 'ดนตรี', 'พิพิธภัณฑ์', 'สื่อ', 'คลินิกแพทย์', 'คลินิกทันตกรรม', 'ประกันสุขภาพ', 'โรงพยาบาล', 'ร้านขายยา']
THCY = ['การเปลี่ยนแปลง 1', 'การเปลี่ยนแปลง 2', 'การเปรียบเทียบและความแตกต่าง', 'คอมพิวเตอร์และเทคโนโลยีสารสนเทศ', 'เงื่อนไขและข้อกำหนด', 'คำที่มักสับสน', 'การทำต่อ ทำซ้ำ และเริ่มใหม่', 'สัญญา', 'สถานการณ์ต่างๆ', 'รายได้ รางวัล และสวัสดิการ', 'บันเทิง ศิลปะ กีฬา และสื่อ', 'อาหารและการทานนอกบ้าน', 'โรงแรม', 'ประกาศรับสมัครงาน', 'การสรรหาพนักงาน', 'การเชื่อมความคิด: เพิ่มเติม เทียบเท่า และสรุป', 'ตำแหน่งและทิศทาง', 'การประชุมและการนำเสนอ', 'เรื่องเงิน 1', 'เรื่องเงิน 2', 'ข้อบังคับและทางเลือก', 'คำตรงข้าม 1: กริยาและคุณศัพท์', 'คำตรงข้าม 2: คำนำหน้าคุณศัพท์', 'คำตรงข้าม 3: คำนำหน้ากริยา', 'ความเป็นเจ้าของ การให้ การยืม', 'Phrasal verbs 1', 'Phrasal verbs 2', 'Phrasal verbs 3', 'คำบุพบท 1', 'คำบุพบท 2', 'การขายและการตลาด', 'การซื้อของและการบริโภค', 'คำความหมายใกล้กัน 1: คำนาม', 'คำความหมายใกล้กัน 2: คำกริยา', 'คำความหมายใกล้กัน 3: คำคุณศัพท์', 'การเริ่มและการหยุด', 'การเดินทาง 1', 'การเดินทาง 2', 'รูปคำ 1: คำนามจากคำกริยา', 'รูปคำ 2: คำนามจากคำคุณศัพท์', 'รูปคำ 3: คำคุณศัพท์จากคำกริยา', 'ปัญหาในที่ทำงาน']
POS = {'n': 'คำนาม', 'v': 'คำกริยา', 'adj': 'คำคุณศัพท์', 'adv': 'คำกริยาวิเศษณ์', 'prep': 'คำบุพบท', 'conj': 'คำเชื่อม'}

def ess600():
    e = load('books')['essential600']; rnd = random.Random(600)
    tracks = {t['n']: 'exam/' + t['url'] for t in e['tracks']}
    lessons = []
    for L in e['lessons']:
        ws = L['words']; n = L['n']; words = [w['word'] for w in ws]
        h = ['<div class="xl-wtools">']
        if n in tracks: h.append('<button class="btn ghost small" data-xlaudio="%s">%sฟังเสียงจริงทั้งบท</button>' % (esc(tracks[n]), SPK))
        h.append('<button class="btn ghost small" data-xladd="%s">+ เพิ่มคำบทนี้เข้าฝึกสะกด</button></div><ul class="xl-words">' % esc('|'.join(words)))
        for w in ws:
            h.append('<li><div class="xl-wh"><button class="icon-btn" data-say="%s" aria-label="ฟังคำ %s">%s</button><b>%s</b><span class="xl-pos">%s</span><span class="xl-wth">%s</span></div>'
                     % (esc(w['word']), esc(w['word']), SPK, esc(w['word']), esc(POS.get(w['pos'], w['pos'])), esc(w.get('th', ''))))
            h.append('<p class="xl-def">%s</p>' % esc(w.get('def', '')))
            for x in w['ex'][:2]:
                h.append('<div class="xl-ex"><button class="icon-btn" data-say="%s" aria-label="ฟังตัวอย่าง">%s</button><span>%s</span></div>' % (esc(x), SPK, esc(x)))
            h.append('</li>')
        h.append('</ul>')
        items = []
        for i, w in enumerate(ws):
            others = [x for x in words if x != w['word']]
            opts = [w['word']] + rnd.sample(others, 3); rnd.shuffle(opts)
            K = 'ABCD'; o = {K[j]: v for j, v in enumerate(opts)}; a = K[opts.index(w['word'])]
            items.append(dict(id='e6-%d-%d-m' % (n, i), p=0, s='คำไหนแปลว่า "%s"?' % w.get('th', ''), o=o, oth={}, a=a,
                              x='%s (%s) = %s — %s' % (w['word'], w['pos'], w.get('th', ''), w.get('def', '')), v=[]))
        for i, w in enumerate(ws):
            ex = next((x for x in w['ex'] if re.search(r'\b' + re.escape(w['word']) + r'\b', x, re.I)), None)
            if not ex: continue
            s = re.sub(r'\b' + re.escape(w['word']) + r'\b', '_____', ex, count=1, flags=re.I)
            others = [x for x in words if x != w['word']]
            opts = [w['word']] + rnd.sample(others, 3); rnd.shuffle(opts)
            K = 'ABCD'; o = {K[j]: v for j, v in enumerate(opts)}; a = K[opts.index(w['word'])]
            items.append(dict(id='e6-%d-%d-s' % (n, i), p=0, s=s, gap=1, o=o, oth={}, a=a, x='%s = %s' % (w['word'], w.get('th', '')), v=[]))
        lessons.append(dict(id='e6-%d' % n, en=L['title'], th=TH600[n-1], intro='12 คำ พร้อมความหมาย ตัวอย่างประโยค และเสียงจริงจากหนังสือ อ่านและฟังก่อน แล้วทำแบบฝึกท้ายบท',
                            html=''.join(h), r=[], tips=[], items=items))
    return lessons

def cyev():
    us = load('books')['workbook']['units']; lessons = []
    for i, u in enumerate(us):
        text = '\n'.join(re.sub(r'\s{3,}', '  ', ln.strip()) for ln in u['text'].split('\n')).strip('\n')
        text = re.sub(r'\n{3,}', '\n\n', text)
        h = ('<div class="panel xl-tips"><b>วิธีใช้บทนี้</b><ul><li>อ่านโจทย์ แล้วเขียนคำตอบลงสมุด</li><li>เปิดเฉลยตรวจเอง แล้วจดคำที่ยังไม่รู้</li><li>ข้อที่บอกว่า "underlined" ในหนังสือมีการขีดเส้นใต้ ซึ่งแสดงในแอปไม่ได้ ให้หาคำที่ผิดจากทั้งประโยคเอง</li><li>เสร็จแล้วกด "ทำบทนี้เสร็จแล้ว"</li></ul></div>'
             '<div class="xl-pass xl-book">%s</div><details class="xl-orig"><summary>เปิดเฉลย</summary><div class="xl-pass xl-book">%s</div></details>') % (esc(text), esc(u.get('answers', '')))
        lessons.append(dict(id='cy-%d' % i, en=u['title'], th=THCY[i], intro='แบบฝึกจากหนังสือ Check Your English Vocabulary (ทำในสมุดแล้วตรวจกับเฉลย)',
                            html=h, r=[], tips=[], items=[], mark='cy-%d' % i))
    return lessons

def write(key, lessons):
    js = '(window.__X=window.__X||{})["%s"]=' % key + json.dumps({'v': 1, 'lessons': lessons}, ensure_ascii=False, separators=(',', ':')) + ';\n'
    open(os.path.join(D, key + '.js'), 'w', encoding='utf-8').write(js)
    print(key, len(lessons), 'lessons', sum(len(L['items']) for L in lessons), 'questions', len(js.encode()), 'bytes')

if __name__ == '__main__':
    write('x600', ess600())
    write('xcyev', cyev())
