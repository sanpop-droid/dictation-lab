"""Build exam/data/xpart1.js: photograph lessons (Part 1) from all 60 questions of the 10 tests, with picture and real audio.

Run:  python3 tools/build_part1.py
"""
import json, os, re
from examdata import load, D

TRAPS = ['wearing (สวมอยู่) ≠ putting on / trying on (กำลังสวม) — ข้อสอบชอบหลอกจุดนี้',
         'holding (ถืออยู่) ≠ carrying (ถือไปด้วย / หิ้วเดิน)',
         'is being + p.p. ต้องมีคนกำลังทำอยู่ในภาพ ถ้าภาพไม่มีคน ตัวเลือกนี้มักผิด',
         'ตัวเลือกที่พูดถึงสิ่งที่ไม่มีในภาพ หรือใช้กริยาไม่ตรงกับท่าทาง ตัดทิ้งได้ทันที']

LESSONS = [
 dict(id='one', en='One person', th='ภาพคนเดียว',
  intro='ภาพมีคนเดียว ตัวเลือกส่วนใหญ่ขึ้นต้นด้วย He / She / The man / The woman ให้ฟังกริยาที่บอกการกระทำหรือท่าทาง',
  r=[['is + V-ing บอกสิ่งที่กำลังทำ', 'ดูมือ สายตา และท่าทางของคนในภาพ', [['She\'s <b>eating</b> in a picnic area.', 'เธอกำลังทานอาหารในบริเวณปิกนิก']]],
     ['ท่าทางคงที่ก็เป็น V-ing', 'is standing / is sitting / is leaning against / is looking at', [['The man <b>is standing</b> next to a car.', 'ผู้ชายยืนอยู่ข้างรถ']]],
     ['สิ่งของในภาพก็เป็นคำตอบได้', 'บางครั้งคำตอบพูดถึงของรอบตัวคนแทนตัวคน', [['A bicycle <b>is parked</b> near the door.', 'จักรยานจอดอยู่ใกล้ประตู']]]],
  tips=['ก่อนเสียงเริ่ม ให้ดูภาพแล้วนึกกริยา 2–3 คำที่ตรงกับท่าทาง']),
 dict(id='group', en='Two or more people', th='ภาพหลายคน',
  intro='ภาพมีหลายคน ตัวเลือกพูดถึงทุกคน (They / Some people) หรือบางคน (One of the men / A woman)',
  r=[['ทุกคนทำเหมือนกัน', 'They\'re / Some people are ... ต้องจริงสำหรับทุกคนในภาพ', [['<b>Some people are</b> sitting at a table.', 'ผู้คนนั่งอยู่ที่โต๊ะ']]],
     ['คนใดคนหนึ่ง', 'One of the women is ... / A man is ... ดูแค่คนนั้น', [['<b>One of the men</b> is sweeping a patio.', 'ชายคนหนึ่งกำลังกวาดลานบ้าน']]],
     ['ปฏิสัมพันธ์', 'are having a conversation / are shaking hands / are facing each other', [['Two people <b>are having a conversation</b>.', 'สองคนกำลังคุยกัน']]]],
  tips=['ระวังตัวเลือกที่พูดว่า "ทุกคน" แต่ในภาพมีคนเดียวที่ทำ']),
 dict(id='things', en='Objects & scenery', th='ภาพสิ่งของและทิวทัศน์',
  intro='ภาพไม่มีคน ตัวเลือกบอกตำแหน่งและสภาพของสิ่งของ ใช้รูป passive บอกสภาพ',
  r=[['has / have been + p.p. = ถูกทำไว้แล้ว (สภาพ)', '', [['Potted plants <b>have been placed</b> along a wall.', 'กระถางต้นไม้ถูกวางไว้ริมกำแพง']]],
     ['is / are + p.p. หรือ there is / are', '', [['Some clothes <b>are displayed</b> under a tent.', 'เสื้อผ้าถูกจัดแสดงใต้เต็นท์'], ['<b>There are</b> some chairs on a balcony.', 'มีเก้าอี้อยู่บนระเบียง']]],
     ['is being + p.p. = กำลังถูกทำ', 'ต้องมีคนกำลังทำอยู่ ภาพไม่มีคนจึงมักเป็นตัวลวง (ยกเว้น is being displayed ที่หมายถึงสภาพ)', []],
     ['คำบอกตำแหน่ง', 'on, under, next to, beside, in front of, behind, along, against, above, across, between', [['A ladder is leaning <b>against</b> the wall.', 'บันไดพิงกำแพงอยู่']]]],
  tips=['ดูภาพแล้วถามว่า "ของอะไร อยู่ตรงไหน สภาพเป็นอย่างไร"']),
 dict(id='mix', en='People & things', th='ภาพผสม คน สิ่งของ และทิวทัศน์',
  intro='ภาพมีทั้งคนและสิ่งของ คำตอบอาจพูดถึงคนหรือของก็ได้ ต้องตรวจทุกตัวเลือก',
  r=[['คำตอบไม่จำเป็นต้องพูดถึงคน', 'บ่อยครั้งคำตอบที่ถูกพูดถึงฉากหลังหรือสิ่งของ', [['A door <b>has been taken off</b> its frame.', 'ประตูถูกถอดออกจากวงกบ']]],
     ['ตรวจทั้งประธานและกริยา', 'ประธานมีในภาพไหม กริยาตรงกับสิ่งที่เห็นไหม ผิดข้อใดข้อหนึ่งก็ตัดได้', []]],
  tips=['อย่าสรุปจากคำแรก ฟังให้จบประโยค']),
]

def kind(ex):
    if ex.startswith('ภาพคนเดียว'): return 'one'
    if ex.startswith(('ภาพหลายคน', 'ภาพสองคน', 'ภาพมีคน')): return 'group'
    if ex.startswith('ภาพผสม'): return 'mix'
    if ex.startswith(('ภาพสิ่งของ', 'ภาพทิวทัศน์')): return 'things'
    raise SystemExit('unknown picture type: ' + ex[:40])

def main():
    amap = load('tests')['audio']
    byid = {L['id']: dict(L, items=[]) for L in LESSONS}
    for L in byid.values(): L['tips'] = L['tips'] + TRAPS
    for t in range(1, 11):
        lc = load('lc%02d' % t); tt = '%02d' % t
        for it in lc['parts']['1']:
            ch = next(c for c in lc['audio_chunks'] if it['audio']['start'] >= c['offset'] and (c['end'] is None or it['audio']['start'] < c['end']))
            off = ch['offset']; r2 = lambda x: round(x - off, 2)
            sg = {k: [r2(v['start']), r2(v['end'])] for k, v in it['segments'].items() if k in 'ABCD'}
            byid[kind(it['explain_th'])]['items'].append(dict(id=tt+'-'+str(it['n']), t=tt, n=it['n'], p=1, s='', sth='',
                img='exam/'+it['image'], o=it['options'], oth=it.get('options_th', {}), a=it['answer'], x=it.get('explain_th', ''), v=it.get('vocab', []),
                au=dict(f='exam/'+amap[ch['file']], s=r2(it['audio']['start']), e=r2(it['audio']['end'])), sg=sg))
    out = [byid[L['id']] for L in LESSONS]
    for L in out:
        for it in L['items']:
            assert os.path.exists(os.path.join(D, '..', it['img'][5:])), it['img']
    js = '(window.__X=window.__X||{})["xpart1"]=' + json.dumps({'v': 1, 'lessons': out}, ensure_ascii=False, separators=(',', ':')) + ';\n'
    open(os.path.join(D, 'xpart1.js'), 'w', encoding='utf-8').write(js)
    for L in out: print('%-7s %3d  %s' % (L['id'], len(L['items']), L['th']))
    print('total', sum(len(L['items']) for L in out), 'bytes', len(js.encode()))

if __name__ == '__main__':
    main()
