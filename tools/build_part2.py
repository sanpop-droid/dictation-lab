"""Build exam/data/xpart2.js: question-response lessons (Part 2) from all 250 questions of the 10 tests, with the real audio.

Run:  python3 tools/build_part2.py
"""
import json, os, re, collections
from examdata import load, D

TRAPS = ['เสียงคล้าย: คำในตัวเลือกออกเสียงคล้ายคำในคำถาม (copy / coffee, review / view) มักเป็นตัวลวง',
         'คำซ้ำ: ตัวเลือกที่ซ้ำคำจากคำถามตรงๆ มักผิด',
         'คำเกี่ยวข้อง: ถาม building แล้วตัวเลือกพูดถึง office หรือ floor มักเป็นกับดัก',
         'ตอบอ้อม: "I\'ll check.", "Ask Ms. Lee.", "It hasn\'t been decided yet." มักเป็นคำตอบที่ถูก']

LESSONS = [
 dict(id='who', en='Who questions', th='คำถาม Who',
  intro='ถามว่า "ใคร" คำตอบที่ถูกบอกคน ตำแหน่ง แผนก หรือบริษัท',
  r=[['ตอบด้วยคน ตำแหน่ง แผนก', 'ไม่จำเป็นต้องเป็นชื่อคน', [['Who will lead the training? — <b>The new manager</b>.', 'ใครจะนำการอบรม — ผู้จัดการคนใหม่'], ['<b>Someone from accounting</b>.', 'คนจากฝ่ายบัญชี']]],
     ['ตอบอ้อมก็ถูก', 'บอกว่าไม่รู้ หรือให้ไปถามคนอื่น', [['<b>I haven\'t heard yet</b>.', 'ยังไม่ได้ข่าวเลย']]]],
  tips=['ฟังคำแรกให้ชัด: Who ต่างจาก How และ Where', 'ตัวเลือกที่ตอบ Yes / No ตัดทิ้งได้ทันที']),
 dict(id='what', en='What / Which questions', th='คำถาม What / Which',
  intro='คำนามที่ตามหลัง What / Which บอกว่าถามเรื่องอะไร ต้องฟังให้ได้',
  r=[['ฟังคำนามหลัง What / Which', 'What type of ... / Which apartment ... / What time ... (ถามเวลา)', [['What type of job are you looking for? — <b>Something in marketing</b>.', 'คุณหางานแบบไหน — งานด้านการตลาด']]],
     ['What should we do with ...?', 'ถามว่าจะจัดการอย่างไร ตอบด้วยการกระทำ', [['What should we do with these brochures? — <b>Put them in the lobby</b>.', 'จะทำอะไรกับโบรชัวร์พวกนี้ — วางไว้ที่ล็อบบี้']]]],
  tips=['จดคำนามหลัง What ไว้ในใจ แล้วหาตัวเลือกที่ตอบเรื่องนั้น']),
 dict(id='when', en='When questions', th='คำถาม When',
  intro='ถามเวลา คำตอบมักเป็นวัน เวลา หรือช่วงเวลา',
  r=[['When will / When is (อนาคต) กับ When did (อดีต)', 'ถามอนาคตต้องตอบเวลาข้างหน้า ถามอดีตต้องตอบเวลาที่ผ่านมา', [['When will the caterer arrive? — <b>In about an hour</b>.', 'ผู้จัดเลี้ยงจะมาเมื่อไร — อีกประมาณหนึ่งชั่วโมง']]],
     ['คำตอบเวลาแบบอื่น', 'Not until Friday (ไม่ก่อนวันศุกร์) / As soon as ... / Sometime next week / By the end of the month', [['<b>Not until next Monday</b>.', 'ไม่ก่อนวันจันทร์หน้า']]]],
  tips=['ระวัง When กับ Where เสียงคล้ายกันในบางสำเนียง', 'ตัวเลือกที่บอกสถานที่ (In the ...) มักผิด']),
 dict(id='where', en='Where questions', th='คำถาม Where',
  intro='ถามสถานที่ คำตอบอาจเป็นสถานที่ ทิศทาง หรือคนที่รู้',
  r=[['ตอบด้วยสถานที่ หรือคน', 'In the supply cabinet / Next to the elevator / Ask the receptionist', [['Where can I buy a charger? — <b>At the electronics store downstairs</b>.', 'ซื้อที่ชาร์จได้ที่ไหน — ที่ร้านอิเล็กทรอนิกส์ชั้นล่าง']]],
     ['ตอบอ้อม', 'ของถูกย้ายไปแล้ว หรือยังไม่ได้ตัดสินใจ', [['<b>They\'ve been moved</b>.', 'ถูกย้ายไปแล้ว']]]],
  tips=['ตัวเลือกที่บอกเวลา (Yesterday, At 3) มักผิด']),
 dict(id='why', en='Why questions', th='คำถาม Why',
  intro='ถามเหตุผล คำตอบบอกสาเหตุหรือจุดประสงค์ อาจไม่มีคำว่า Because',
  r=[['เหตุผลหรือจุดประสงค์', 'Because ... / To ... (เพื่อ) / หรือบอกสาเหตุตรงๆ', [['Why is there no flour on the shelf? — <b>We sold out this morning</b>.', 'ทำไมไม่มีแป้งบนชั้น — ขายหมดตั้งแต่เช้า']]],
     ['Why don\'t we ...? ไม่ใช่ถามเหตุผล', 'แปลว่า "ทำ ... กันไหม" (ชวน) อยู่ในบทขอร้อง เสนอ และชวน', []]],
  tips=['คำตอบขึ้นต้นด้วย Because ไม่ได้แปลว่าถูกเสมอ ต้องฟังเนื้อหา']),
 dict(id='how', en='How questions', th='คำถาม How',
  intro='How + คำคุณศัพท์ หรือคำกริยาวิเศษณ์ ถามปริมาณ ระยะเวลา ความถี่ ส่วน How + กริยา ถามวิธีหรือความเห็น',
  r=[['How + คำขยาย', 'How long (นานแค่ไหน) / How much (ราคา, ปริมาณ) / How many (จำนวน) / How often (บ่อยแค่ไหน) / How far (ไกลแค่ไหน) / How soon (อีกนานแค่ไหน)', [['How often do you travel? — <b>About twice a month</b>.', 'เดินทางบ่อยแค่ไหน — ประมาณเดือนละสองครั้ง']]],
     ['How did / How was', 'ถามวิธีหรือความเห็น', [['How was the conference? — <b>It was very informative</b>.', 'การประชุมเป็นอย่างไร — ได้ความรู้มาก']]]],
  tips=['ฟังคำที่ตามหลัง How ให้ชัด เพราะเปลี่ยนความหมายทั้งประโยค']),
 dict(id='yn', en='Yes / No questions', th='คำถาม Yes / No',
  intro='ขึ้นต้นด้วย Do, Is, Have, Can, Will ฯลฯ คำตอบอาจขึ้นต้นด้วย Yes / No หรือไม่มีก็ได้',
  r=[['Yes / No + ข้อมูลเพิ่ม', 'ข้อมูลที่ตามมาต้องตรงกับคำถาม', [['Did management make a decision? — <b>Yes, they hired Ms. Ortiz</b>.', 'ผู้บริหารตัดสินใจแล้วหรือยัง — แล้ว จ้างคุณออร์ติซ']]],
     ['ละ Yes / No แต่ตอบเนื้อหา', 'คำตอบที่ถูกบ่อยที่สุด', [['Are there tickets left? — <b>Only a few in the back row</b>.', 'ยังมีตั๋วเหลือไหม — เหลือไม่กี่ใบแถวหลัง']]]],
  tips=['Yes / No ที่ตามด้วยข้อมูลไม่ตรงคำถามคือตัวลวง']),
 dict(id='neg', en='Negative & tag questions', th='คำถามปฏิเสธและคำถามท้ายประโยค',
  intro='Didn\'t you ...? / ..., isn\'t it? / ..., right? ให้ตอบเหมือนคำถามธรรมดา ไม่ต้องสนใจคำว่า not',
  r=[['ตอบเหมือนคำถามปกติ', 'Yes = ใช่ ทำแล้ว / No = ไม่ ยังไม่ได้ทำ', [['Didn\'t you e-mail the contract? — <b>Yes, this morning</b>.', 'คุณส่งสัญญาทางอีเมลแล้วไม่ใช่เหรอ — ส่งแล้ว เมื่อเช้า']]],
     ['..., right? / ..., haven\'t you?', 'เป็นการขอยืนยัน', [['You\'ve booked a hotel, haven\'t you? — <b>Not yet</b>.', 'คุณจองโรงแรมแล้วใช่ไหม — ยังเลย']]]],
  tips=['แปลงในหัวเป็นคำถามธรรมดาก่อน เช่น Didn\'t you ...? = Did you ...?']),
 dict(id='req', en='Requests, offers & suggestions', th='ขอร้อง เสนอ และชวน',
  intro='Could you ...? / Would you like ...? / Why don\'t we ...? / How about ...? / Let\'s ... คำตอบคือตอบรับหรือปฏิเสธอย่างสุภาพ',
  r=[['ตอบรับ', 'Sure. / Of course. / I\'d be happy to. / That\'s a good idea.', [['Can you come to my performance tonight? — <b>Sure, what time does it start?</b>', 'มาดูการแสดงคืนนี้ได้ไหม — ได้สิ เริ่มกี่โมง']]],
     ['ปฏิเสธพร้อมเหตุผล', 'Sorry, I have a meeting. / I\'m afraid I can\'t.', [['<b>Sorry, I\'m working late tonight</b>.', 'ขอโทษ คืนนี้ทำงานดึก']]]],
  tips=['Why don\'t you / we ...? = ชวน ไม่ใช่ถามเหตุผล', 'How about ...? = ... ดีไหม']),
 dict(id='choice', en='Choice questions', th='คำถามให้เลือก (A or B)',
  intro='มีคำว่า or ให้เลือก คำตอบเลือกอย่างใดอย่างหนึ่ง เลือกทั้งสอง ไม่เลือกทั้งคู่ หรือเสนอทางที่สาม',
  r=[['เลือกอย่างหนึ่ง', 'มักพูดซ้ำด้วยคำอื่น ไม่ใช่คำเดิม', [['Coffee or tea? — <b>Tea, please</b>.', 'กาแฟหรือชา — ชาครับ']]],
     ['ไม่เลือกเจาะจง', 'Either is fine. / Whichever is cheaper. / Neither, thanks.', [['Friday or Saturday? — <b>Either works for me</b>.', 'วันศุกร์หรือเสาร์ — วันไหนก็ได้']]]],
  tips=['ตัวเลือกที่ขึ้นต้นด้วย Yes / No มักผิด']),
 dict(id='stmt', en='Statements', th='ประโยคบอกเล่า',
  intro='ไม่ใช่คำถาม ต้องเข้าใจสถานการณ์ แล้วหาคำตอบที่ตอบโต้ได้เป็นธรรมชาติ เป็นแบบที่ยากที่สุดของ Part 2',
  r=[['รูปแบบคำตอบ', 'ตอบรับ เห็นด้วย เสนอช่วย ถามกลับ หรือให้ข้อมูลเพิ่ม', [['I\'m going to try to fix this printer. — <b>Do you need any help?</b>', 'ฉันจะลองซ่อมเครื่องพิมพ์นี้ — ต้องการให้ช่วยไหม'], ['We achieved our sales targets. — <b>That\'s great news</b>.', 'เราทำยอดขายถึงเป้าแล้ว — ข่าวดีมาก']]]],
  tips=['ถามตัวเองว่า "ถ้ามีคนพูดแบบนี้ ฉันจะตอบว่าอะไร"']),
]

def qtype(q):
    s = q.strip(); low = s.lower(); w = re.sub(r"'.*", '', s.split()[0].lower().strip(','))
    if not s.endswith('?'): return 'stmt'
    if ' or ' in low and w not in ('who', 'what', 'which', 'when', 'where', 'why', 'how', 'whose'): return 'choice'
    if re.match(r"^(could|can|would|will) you\b|^would you (like|mind)|^why don't|^why not|^how about|^what about|^let's|^shall we|^do you want|^would you be", low): return 'req'
    if re.search(r", (isn't|aren't|wasn't|weren't|don't|doesn't|didn't|haven't|hasn't|won't|can't|shouldn't|right|correct)\b[^?]*\?$", low) or \
       re.match(r"^(isn't|aren't|wasn't|weren't|don't|doesn't|didn't|haven't|hasn't|won't|can't|shouldn't|wouldn't|couldn't)\b", low): return 'neg'
    if w in ('who', 'whose', 'whom'): return 'who'
    if w == 'when' or low.startswith('what time'): return 'when'
    if w in ('what', 'which'): return 'what'
    if w in ('where', 'why', 'how'): return w
    return 'yn'

def main():
    amap = load('tests')['audio']
    byid = {L['id']: dict(L, items=[]) for L in LESSONS}
    for L in byid.values(): L['tips'] = L['tips'] + TRAPS
    for t in range(1, 11):
        lc = load('lc%02d' % t); tt = '%02d' % t
        def where(sec):
            for ch in lc['audio_chunks']:
                if sec >= ch['offset'] and (ch['end'] is None or sec < ch['end']): return amap[ch['file']], ch['offset']
            raise SystemExit('no audio chunk for %s %s' % (tt, sec))
        for it in lc['parts']['2']:
            f, off = where(it['audio']['start'])
            r2 = lambda x: round(x - off, 2)
            sg = {('q' if k == 'question' else k): [r2(v['start']), r2(v['end'])] for k, v in it['segments'].items()}
            byid[qtype(it['question'])]['items'].append(dict(id=tt+'-'+str(it['n']), t=tt, n=it['n'], p=2,
                s=it['question'], sth=it.get('question_th', ''), o=it['options'], oth=it.get('options_th', {}), a=it['answer'],
                x=it.get('explain_th', ''), v=it.get('vocab', []), au=dict(f='exam/'+f, s=r2(it['audio']['start']), e=r2(it['audio']['end'])), sg=sg))
    out = [byid[L['id']] for L in LESSONS]
    js = '(window.__X=window.__X||{})["xpart2"]=' + json.dumps({'v': 1, 'lessons': out}, ensure_ascii=False, separators=(',', ':')) + ';\n'
    open(os.path.join(D, 'xpart2.js'), 'w', encoding='utf-8').write(js)
    for L in out: print('%-7s %3d  %s' % (L['id'], len(L['items']), L['th']))
    print('total', sum(len(L['items']) for L in out), 'bytes', len(js.encode()))

if __name__ == '__main__':
    main()
