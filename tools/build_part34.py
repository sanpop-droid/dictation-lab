"""Build exam/data/xpart34.js: conversation & talk lessons (Part 3–4) from all 690 questions of the 10 tests.

Lessons follow the question type. Each question carries its set (audio, transcript, graphic) by reference,
plus the sentence that holds the answer (evidence) and the time where it is spoken.
Run:  python3 tools/build_part34.py
"""
import json, os, re
from examdata import load, D

COMMON = ['อ่านคำถามและตัวเลือกก่อนเสียงเริ่ม แล้วขีดเส้นใต้คำสำคัญ (ใคร ทำอะไร ที่ไหน)',
          'คำตอบที่ถูกมักพูดด้วยคำอื่น (paraphrase) ไม่ใช่คำเดิมในบทสนทนา',
          'ลำดับคำตอบในเสียงมักตรงกับลำดับคำถาม 3 ข้อ']

LESSONS = [
 dict(id='main', en='Topic & purpose', th='หัวข้อและจุดประสงค์',
  intro='What are the speakers mainly discussing? / Why is the man calling? / What is the purpose of the talk? คำตอบมักอยู่ใน 1–2 ประโยคแรก',
  r=[['ฟังต้นเรื่องให้ดี', 'ผู้พูดมักบอกเหตุผลที่โทรหรือหัวข้อทันที เช่น I\'m calling about ... / I wanted to talk to you about ...', [['I\'m calling <b>about the order</b> I placed last week.', 'ฉันโทรมาเรื่องคำสั่งซื้อที่สั่งไปสัปดาห์ที่แล้ว']]],
     ['คำตอบเป็นภาพรวม', 'ตัวเลือกที่พูดถึงรายละเอียดเล็กๆ ที่ได้ยินช่วงกลางเรื่องมักเป็นตัวลวง', []]],
  tips=['ข้อนี้มักเป็นข้อแรกของชุด']),
 dict(id='who', en='Speakers & place', th='ผู้พูดเป็นใคร อยู่ที่ไหน',
  intro='Who most likely is the man? / Where do the speakers work? / What industry ...? ต้องเดาจากคำศัพท์เฉพาะทาง',
  r=[['ฟังคำศัพท์ประจำอาชีพหรือสถานที่', 'patient, prescription → คลินิก / check in, reservation → โรงแรม / deadline, article → สำนักข่าว', [['I\'m glad we were assigned to <b>cover the press conference</b>.', 'ได้รับมอบหมายให้ทำข่าวแถลงข่าว → นักข่าว']]],
     ['most likely = อนุมาน', 'คำตอบอาจไม่ได้พูดตรงๆ ต้องรวมหลายคำใบ้', []]],
  tips=['ข้อนี้มักเป็นข้อแรกของชุด ฟัง 2–3 ประโยคแรกให้ดี']),
 dict(id='prob', en='Problems & concerns', th='ปัญหาและข้อกังวล',
  intro='What problem does the woman mention? / What is the man concerned about? ฟังคำที่บอกปัญหา',
  r=[['คำสัญญาณบอกปัญหา', 'but, unfortunately, I\'m afraid, the problem is, I\'m worried that, actually', [['<b>Unfortunately</b>, the shipment has been delayed.', 'น่าเสียดาย การจัดส่งล่าช้า']]]],
  tips=['เมื่อได้ยิน but / unfortunately ให้ตั้งใจฟังประโยคต่อไป']),
 dict(id='ask', en='Requests, suggestions & offers', th='ขอร้อง แนะนำ และเสนอ',
  intro='What does the woman ask the man to do? / What does the speaker suggest? / What does the man offer? ฟังประโยคขอร้องหรือแนะนำ',
  r=[['รูปประโยคขอร้อง', 'Could you ...? / Can you ...? / Please ... / I need you to ...', [['<b>Could you send me</b> the updated schedule?', 'ช่วยส่งตารางที่อัปเดตให้หน่อยได้ไหม']]],
     ['รูปประโยคแนะนำและเสนอ', 'You should ... / Why don\'t you ...? / I suggest ... / I can ... / Let me ...', [['<b>Why don\'t you</b> try the new software?', 'ลองใช้ซอฟต์แวร์ตัวใหม่ดูไหม'], ['<b>I can</b> give you a ride.', 'ฉันไปส่งคุณได้']]],
     ['ดูว่าใครพูด', 'ถาม "woman asks" ต้องฟังประโยคที่ผู้หญิงพูด', []]],
  tips=['ข้อนี้มักเป็นข้อที่ 2 หรือ 3 ของชุด']),
 dict(id='next', en='What happens next', th='จะทำอะไรต่อ',
  intro='What will the man do next? / What does the woman say she will do? คำตอบมักอยู่ในประโยคท้ายๆ',
  r=[['ฟังประโยคแสดงแผนอนาคต', 'I\'ll ... / I\'m going to ... / Let me ... / I\'ll go ahead and ...', [['<b>I\'ll call</b> the supplier right now.', 'เดี๋ยวจะโทรหาผู้ขายเลย']]]],
  tips=['ข้อนี้มักเป็นข้อสุดท้ายของชุด ตั้งใจฟังช่วงท้าย']),
 dict(id='detail3', en='Details — conversations', th='รายละเอียด (Part 3 บทสนทนา)',
  intro='คำถามถามข้อมูลเฉพาะ เช่น เวลา จำนวน เหตุผล สิ่งที่พูดถึง ต้องจับคำสำคัญในคำถามแล้วรอฟังจุดนั้น',
  r=[['จับคำสำคัญในคำถาม', 'ชื่อคน สถานที่ ตัวเลข หรือคำนามเฉพาะในคำถาม จะถูกพูดใกล้ๆ คำตอบ', []],
     ['ระวังตัวเลือกที่ใช้คำเดิมทั้งหมด', 'คำตอบที่ถูกมักเปลี่ยนคำ เช่น "inexpensive" ↔ "low cost"', []]],
  tips=[]),
 dict(id='detail4', en='Details — talks', th='รายละเอียด (Part 4 บทพูดคนเดียว)',
  intro='บทพูดคนเดียว เช่น ข้อความโทรศัพท์ ประกาศ โฆษณา ข่าว ผู้พูดคนเดียวให้ข้อมูลยาว ต้องจับคำสำคัญในคำถาม',
  r=[['โครงสร้างบทพูดที่พบบ่อย', 'ข้อความโทรศัพท์: แนะนำตัว → เรื่องที่โทร → ขอให้ทำ / ประกาศ: สถานที่ → ข่าว → คำแนะนำ / โฆษณา: สินค้า → จุดเด่น → ข้อเสนอพิเศษ', []],
     ['According to the speaker, ...', 'ถามสิ่งที่ผู้พูดพูดตรงๆ ฟังคำสำคัญในคำถาม', []]],
  tips=['อ่านคำถามทั้ง 3 ข้อก่อน จะรู้ว่าบทพูดเกี่ยวกับอะไร']),
 dict(id='intent', en='Speaker\'s intention', th='ความหมายแฝง (ถามเจตนา)',
  intro='What does the woman mean when she says, "..."? / Why does the speaker say, "..."? ต้องเข้าใจบริบทรอบประโยคนั้น ไม่ใช่แปลตรงตัว',
  r=[['ฟังก่อนและหลังประโยคที่ยกมา', 'ความหมายขึ้นกับสถานการณ์ เช่น "it\'s very hot today" อาจแปลว่า "ควรเปิดแอร์" หรือ "ขายเครื่องดื่มเย็นได้ดี"', []],
     ['ตัวเลือกที่แปลตรงตัวมักผิด', 'คำตอบคือเหตุผลที่ผู้พูดพูดประโยคนั้น', []]],
  tips=['อ่านประโยคในเครื่องหมายคำพูดก่อน แล้วรอฟังว่าอยู่ตรงไหนในเสียง']),
 dict(id='graphic', en='Graphic questions', th='คำถามดูภาพประกอบ',
  intro='Look at the graphic. ... ภาพอาจเป็นตาราง แผนที่ ตารางเวลา หรือรายการราคา ผู้พูดมักพูดถึงข้อมูลอีกฝั่งหนึ่งของตาราง',
  r=[['หาว่าตัวเลือกอยู่คอลัมน์ไหน', 'ถ้าตัวเลือกเป็นชื่อสถานที่ ผู้พูดมักพูดถึงข้อมูลอีกคอลัมน์ เช่น ราคา หรือจำนวน แล้วเราต้องจับคู่เอง', [['the largest cluster ... off the coast of <b>Winston</b> → Site D', 'ได้ยินชื่อเมือง ต้องไปดูในภาพว่าเป็น Site ไหน']]],
     ['ดูภาพก่อนเสียงเริ่ม', 'สังเกตสิ่งที่โดดเด่น เช่น มากที่สุด ถูกที่สุด อยู่มุมไหน', []]],
  tips=['อย่าฟังหาคำในตัวเลือกตรงๆ เพราะมักไม่ได้ถูกพูดถึง']),
]

def qtype(q, part):
    s = q['question'].lower()
    if q.get('type') == 'graphic' or s.startswith('look at the graphic'): return 'graphic'
    if q.get('type') == 'intent' or re.search(r'why does the (wo)?man say|what does the (wo)?man (mean|imply)|why does the speaker say|what does the speaker (mean|imply)|when (s)?he says', s): return 'intent'
    if re.search(r'mainly (about|discussing)|main topic|purpose of|why is the (wo)?man calling|why is the speaker calling|what is the (talk|conversation|message|announcement|broadcast|speech) (mainly )?about|what are the speakers (mainly )?discussing|topic', s): return 'main'
    if re.search(r"^who (most likely )?(is|are)|^where (do|does|is|are|most likely)|what (industry|kind of business|type of business|department|field)|(wo)?man's (job|profession|occupation)|who is the (wo)?man|who is the speaker|who are the listeners|who most likely", s): return 'who'
    if re.search(r'(do|will|be doing) next|most likely (do|happen)|will (happen|take place)|plan(s)? to do|what will (the )?(wo)?man|what will the speaker|what will (the )?listeners|what does the (wo)?man say (s)?he will', s): return 'next'
    if re.search(r'suggest|recommend|ask(s)? .* to|ask(s)? (for|about)|offer|request|advise|encourage|instruct|remind', s): return 'ask'
    if re.search(r'problem|concern|worried|issue|complain|disappoint|difficult|why .* (unable|delay|cancel)', s): return 'prob'
    return 'detail3' if part == '3' else 'detail4'

def norm(x): return re.sub(r'[^a-z0-9]+', ' ', x.lower()).strip()

def main():
    amap = load('tests')['audio']
    byid = {L['id']: dict(L, items=[]) for L in LESSONS}
    for L in byid.values(): L['tips'] = L['tips'] + COMMON
    ctx = {}; miss = 0
    for t in range(1, 11):
        lc = load('lc%02d' % t); tt = '%02d' % t
        def chunk(sec):
            return next(c for c in lc['audio_chunks'] if sec >= c['offset'] and (c['end'] is None or sec < c['end']))
        for part in '34':
            for st in lc['parts'][part]:
                ch = chunk(st['audio']['start']); off = ch['offset']; r2 = lambda x: round(x - off, 2)
                f = 'exam/' + amap[ch['file']]
                key = tt + '-' + st['set']
                lines = [[ln['spk'], ln['en'], ln.get('th', ''), r2(ln['start']), r2(ln['end'])] for ln in st['transcript']]
                sents = [(norm(se['en']), r2(se['start']), r2(se['end'])) for ln in st['transcript'] for se in ln.get('sentences', [])]
                c = dict(type=st.get('type', ''), lines=lines, f=f, s=r2(st['audio']['start']), e=r2(st['audio']['end']))
                if st.get('graphic'):
                    g = st['graphic']; c['g'] = dict(img=('exam/' + g['image']) if g.get('image') else '', items=g.get('items', []), kind=g.get('kind', ''))
                    if c['g']['img']: assert os.path.exists(os.path.join(D, '..', g['image'])), g['image']
                ctx[key] = c
                for q in st['questions']:
                    qc = chunk(q['audio']['start']); assert qc is ch or True
                    ev = (q.get('evidence_quotes') or [q.get('evidence', '')])[0]; ea = None
                    if ev:
                        ne = norm(ev)[:40]
                        for se in sents:
                            if ne and (ne in se[0] or se[0][:40] in norm(ev)): ea = [se[1], se[2]]; break
                    if ev and not ea: miss += 1
                    byid[qtype(q, part)]['items'].append(dict(id=tt+'-'+str(q['n']), t=tt, n=q['n'], p=int(part), s=q['question'], sth=q.get('question_th', ''),
                        o=q['options'], oth=q.get('options_th', {}), a=q['answer'], x=q.get('explain_th', ''), ev=q.get('evidence', ''), pa=q.get('paraphrase', ''),
                        ea=ea, qa=[round(q['audio']['start'] - qc['offset'], 2), round(q['audio']['end'] - qc['offset'], 2)], qf='exam/' + amap[qc['file']], cx=key, v=[]))
                # set vocabulary goes on the first question of the set only (shown after answering)
                first = next(i for L in byid.values() for i in L['items'] if i['cx'] == key and i['n'] == st['questions'][0]['n'])
                first['v'] = st.get('vocab', [])[:12]
    out = [byid[L['id']] for L in LESSONS]
    for L in out: L['items'].sort(key=lambda i: (i['t'], i['n']))
    js = '(window.__X=window.__X||{})["xpart34"]=' + json.dumps({'v': 1, 'lessons': out, 'ctx': ctx}, ensure_ascii=False, separators=(',', ':')) + ';\n'
    open(os.path.join(D, 'xpart34.js'), 'w', encoding='utf-8').write(js)
    for L in out: print('%-8s %3d  %s' % (L['id'], len(L['items']), L['th']))
    print('total', sum(len(L['items']) for L in out), 'sets', len(ctx), 'evidence not timed', miss, 'bytes', len(js.encode()))

if __name__ == '__main__':
    main()
