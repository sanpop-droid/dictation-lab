"""Build exam/data/xpart7.js: reading lessons (Part 7) from all 540 questions of the 10 tests, by question type.

Run:  python3 tools/build_part7.py
"""
import json, os
from examdata import load, D

COMMON = ['อ่านคำถามก่อน แล้วค่อยไปหาคำตอบในบทความ ไม่ต้องอ่านทุกคำ',
          'คำตอบที่ถูกมักใช้คำอื่นที่มีความหมายเดียวกัน (paraphrase)',
          'ลำดับคำถามมักไล่ตามลำดับเนื้อหาในบทความ']

LESSONS = [
 dict(id='main', en='Purpose & main idea', th='จุดประสงค์และใจความหลัก',
  intro='What is the purpose of the e-mail? / Why was the notice written? / What is the article mainly about?',
  r=[['ดูหัวเรื่องและย่อหน้าแรก', 'จุดประสงค์มักอยู่ใน 1–2 ประโยคแรก เช่น I am writing to ... / This is to inform you ...', [['<b>I am writing to</b> confirm your reservation.', 'ฉันเขียนมาเพื่อยืนยันการจองของคุณ']]],
     ['คำตอบเป็นภาพรวม', 'ตัวเลือกที่พูดถึงรายละเอียดย่อยมักเป็นตัวลวง', []]],
  tips=[]),
 dict(id='detail', en='Details', th='รายละเอียด',
  intro='คำถามถามข้อมูลเฉพาะ เช่น วันที่ ราคา ใครทำอะไร ให้หาคำสำคัญจากคำถาม แล้วกวาดตาหาในบทความ (scanning)',
  r=[['หาคำสำคัญ', 'ชื่อคน ชื่อบริษัท ตัวเลข วันที่ ในคำถาม แล้วหาในบทความ จากนั้นอ่านประโยครอบๆ ให้ละเอียด', []],
     ['ระวังตัวลวงคำซ้ำ', 'ตัวเลือกที่ลอกคำจากบทความแต่เนื้อหาผิดเล็กน้อย เช่น ผิดคน ผิดวัน', []]],
  tips=[]),
 dict(id='not-true', en='NOT / true questions', th='คำถาม NOT และข้อใดจริง',
  intro='What is NOT mentioned ...? / What is indicated about ...? / What is true about ...? ต้องตรวจทีละตัวเลือก',
  r=[['NOT: ตัด 3 ตัวเลือกที่มีในบทความ', 'ตัวที่เหลือคือคำตอบ ใช้เวลามาก ควรทำเป็นข้อท้ายๆ', []],
     ['indicated / true: ตรวจทีละตัวเลือก', 'คำตอบที่ถูกมักใช้คำอื่นที่มีความหมายเดียวกัน', []]],
  tips=['สังเกตคำว่า NOT ที่พิมพ์ตัวใหญ่ในคำถามเสมอ']),
 dict(id='inference', en='Inference', th='อนุมาน (most likely / suggested)',
  intro='What is suggested about ...? / Who most likely is ...? / Where would the notice most likely be found? บทความไม่บอกตรงๆ ต้องรวมคำใบ้',
  r=[['รวมคำใบ้หลายจุด', 'คำใบ้มักกระจายอยู่ 2–3 ประโยค', []],
     ['อย่าคิดเกินบทความ', 'คำตอบต้องมีหลักฐานในบทความรองรับ ไม่ใช่ใช้ความรู้รอบตัว', []]],
  tips=[]),
 dict(id='synonym', en='Word meaning', th='ความหมายของคำตามบริบท',
  intro='The word "..." in paragraph 1, line 2, is closest in meaning to ... เลือกความหมายที่เข้ากับประโยคนั้น ไม่ใช่ความหมายที่พบบ่อยที่สุด',
  r=[['แทนค่าแล้วอ่านใหม่', 'เอาตัวเลือกไปแทนคำนั้นในประโยค ตัวไหนอ่านแล้วความหมายเท่าเดิมคือคำตอบ', [['The offer will <b>run</b> until May. → <b>continue</b>', 'ข้อเสนอจะมีผลถึงเดือนพฤษภาคม (run ≠ วิ่ง)']]]],
  tips=['ตัวลวงคือความหมายอื่นของคำเดียวกันที่ไม่เข้ากับบริบท']),
 dict(id='intent', en='Writer\'s intention (chats)', th='ความหมายแฝงในแชท',
  intro='At 10:32 A.M., what does Ms. Kim most likely mean when she writes, "..."? อ่านข้อความก่อนหน้าและถัดไป',
  r=[['อ่านบริบทก่อนและหลัง', 'ประโยคสั้นๆ อย่าง "Sure thing." หรือ "That\'s a relief." มีความหมายตามสิ่งที่อีกฝ่ายพูดก่อนหน้า', []]],
  tips=['หาเวลาที่ระบุในคำถามในแชทก่อน']),
 dict(id='insert', en='Sentence position', th='ตำแหน่งของประโยค [1]–[4]',
  intro='In which of the positions marked [1], [2], [3], and [4] does the following sentence best belong?',
  r=[['ดูคำอ้างอิงในประโยคที่ให้มา', 'this, these, such, it, they, also, however ต้องเชื่อมกับประโยคก่อนหน้าได้', []],
     ['ลองวางทีละตำแหน่ง', 'อ่านประโยคก่อนและหลังตำแหน่งนั้น ต้องต่อกันได้ทั้งสองฝั่ง', []]],
  tips=['ทำข้อนี้หลังจากอ่านบทความแล้ว จะเร็วกว่า']),
 dict(id='cross', en='Linking passages', th='เชื่อมข้อมูลหลายเอกสาร',
  intro='ชุดที่มี 2–3 เอกสาร คำถามบางข้อต้องใช้ข้อมูลจากสองเอกสารรวมกัน เช่น ตารางราคา + อีเมลสั่งของ',
  r=[['หาข้อมูลที่เชื่อมกัน', 'เอกสารหนึ่งให้เงื่อนไข อีกเอกสารให้ข้อเท็จจริง เช่น อีเมลบอกว่าสั่ง 50 ชิ้น + ตารางบอกส่วนลดเมื่อสั่งเกิน 40 ชิ้น', []],
     ['ตัวลวงใช้ข้อมูลเอกสารเดียว', 'ตัวเลือกที่ตอบจากเอกสารเดียวโดยไม่เชื่อมกันมักผิด', []]],
  tips=['เปิดดูทุกเอกสารในชุด ก่อนเลือกคำตอบ']),
]

def main():
    byid = {L['id']: dict(L, items=[]) for L in LESSONS}
    for L in byid.values(): L['tips'] = L['tips'] + COMMON
    ctx = {}
    for t in range(1, 11):
        rc = load('rc%02d' % t); tt = '%02d' % t
        for st in rc['parts']['7']:
            key = tt + '-' + st['set']
            ps = []
            for p in st['passages']:
                img = ('exam/' + p['image']) if p.get('image') else ''
                if img: assert os.path.exists(os.path.join(D, '..', p['image'])), p['image']
                ps.append(dict(l=p.get('label', ''), en=p['text'], th=p.get('text_th', ''), img=img))
            ctx[key] = dict(type=st.get('type', ''), ps=ps)
            first = True
            for q in st['questions']:
                lid = q.get('type')
                if lid not in byid: raise SystemExit('unknown type %r in %s' % (lid, key))
                byid[lid]['items'].append(dict(id=tt+'-'+str(q['n']), t=tt, n=q['n'], p=7, s=q['question'], sth=q.get('question_th', ''),
                    o=q['options'], oth=q.get('options_th', {}), a=q['answer'], c=q.get('category_th', ''), x=q.get('explain_th', ''),
                    ev=q.get('evidence_quotes', []), pa=q.get('paraphrase', []), cx=key, v=st.get('vocab', [])[:12] if first else []))
                first = False
    out = [byid[L['id']] for L in LESSONS]
    js = '(window.__X=window.__X||{})["xpart7"]=' + json.dumps({'v': 1, 'lessons': out, 'ctx': ctx}, ensure_ascii=False, separators=(',', ':')) + ';\n'
    open(os.path.join(D, 'xpart7.js'), 'w', encoding='utf-8').write(js)
    for L in out: print('%-10s %3d  %s' % (L['id'], len(L['items']), L['th']))
    print('total', sum(len(L['items']) for L in out), 'sets', len(ctx), 'bytes', len(js.encode()))

if __name__ == '__main__':
    main()
