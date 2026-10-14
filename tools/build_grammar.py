"""Build exam/data/xgram.js: grammar lessons made from every Part 5 and Part 6 question in the 10 practice tests.

Run:  python3 tools/build_grammar.py
Each question is placed in exactly one lesson (first matching rule wins); the script stops if any category is left over.
"""
import json, os, re, collections
from examdata import load, D

# ---------- lessons: rules written by the team, questions filled in from the tests ----------
# r = rules [heading, body (may hold <b>), [[example EN, example TH], ...]]
LESSONS = [
 dict(id='pron', en='Pronouns', th='เลือกรูปสรรพนาม',
  intro='ตัวเลือกเป็นสรรพนามตัวเดียวกันแต่ต่างรูป เช่น he / his / him / himself ให้ดูว่าช่องว่างทำหน้าที่อะไรในประโยค',
  r=[['รูปประธาน: I, he, she, we, they', 'วางหน้ากริยาแท้ เป็นผู้ทำ', [['<b>She</b> will lead the training session.', 'เธอจะเป็นผู้นำการอบรม']]],
     ['รูปกรรม: me, him, her, us, them', 'วางหลังกริยาหรือหลังบุพบท', [['Please send the invoice to <b>him</b>.', 'กรุณาส่งใบแจ้งหนี้ให้เขา']]],
     ['รูปเจ้าของ + คำนาม: my, his, her, our, their, its', 'ตามด้วยคำนามเสมอ เป็นรูปที่ออกสอบบ่อยที่สุด', [['Ms. Kim spoke about <b>her</b> career.', 'คุณคิมพูดถึงอาชีพการงานของเธอ']]],
     ['รูปเจ้าของแบบไม่มีคำนามตาม: mine, his, hers, ours, theirs', 'ใช้แทน "ของ ... + คำนาม" ทั้งก้อน', [['The blue folder is <b>mine</b>.', 'แฟ้มสีน้ำเงินเป็นของฉัน']]],
     ['สรรพนามสะท้อน: myself, himself, themselves', 'ใช้เมื่อประธานกับกรรมเป็นคนเดียวกัน หรือเน้นว่า "ทำเอง" และ by + -self แปลว่า "ด้วยตัวเอง / คนเดียว" ประโยคครบแล้วก็ยังเติมได้', [['Mr. Lee reviewed the contract <b>himself</b>.', 'คุณลีตรวจสัญญาด้วยตัวเอง']]],
     ['สรรพนามไม่ชี้เฉพาะ: those, anyone, each, others', 'those who + กริยา = "ผู้ที่ ..." (พหูพจน์) / anyone who = "ใครก็ตามที่ ..."', [['<b>Those</b> who register early will get a discount.', 'ผู้ที่ลงทะเบียนก่อนจะได้รับส่วนลด']]]],
  tips=['หลังช่องว่างเป็นคำนาม → my / his / their', 'หลังช่องว่างเป็นกริยา → I / he / they', 'ช่องว่างอยู่หลังกริยาหรือบุพบท → me / him / them', 'ประโยคครบแล้ว → himself / themselves']),
 dict(id='noun', en='Noun position', th='ตำแหน่งคำนาม',
  intro='ตัวเลือกเป็นคำเดียวกันแต่ต่างชนิด (noun / verb / adj / adv) ช่องว่างในตำแหน่งต่อไปนี้ต้องเป็นคำนาม',
  r=[['หลัง a / an / the, my / their, this / those', 'คำนำหน้านาม (determiner) ต้องมีคำนามตาม ถ้ามี adj คั่นก็ยังเป็นคำนามตัวท้าย', [['a detailed <b>proposal</b>', 'ข้อเสนอที่ละเอียด']]],
     ['ประธาน กรรม และหลังบุพบท', 'หน้ากริยาแท้ หลังกริยาที่ต้องมีกรรม และหลังบุพบท (of, for, in ...) ใช้คำนาม', [['The project requires <b>approval</b> from the director.', 'โครงการต้องได้รับการอนุมัติจากผู้อำนวยการ']]],
     ['คำนามประสม (noun + noun)', 'คำนามตัวหน้าทำหน้าที่ขยายคำนามตัวหลัง ตัวหลังเป็นตัวหลักของวลี', [['safety <b>regulations</b>', 'ข้อบังคับด้านความปลอดภัย'], ['customer <b>satisfaction</b>', 'ความพึงพอใจของลูกค้า']]],
     ['คนกับสิ่ง', 'คำนามจากรากเดียวกันอาจหมายถึงคนหรือสิ่ง เลือกตามความหมาย และคำนามนับได้เอกพจน์ต้องมี a / the นำหน้า', [['an <b>applicant</b> (ผู้สมัคร) / an <b>application</b> (ใบสมัคร)', '']]],
     ['คำลงท้ายที่เป็นคำนาม', '-tion, -sion, -ment, -ance, -ence, -ity, -ness, -ship และ -er, -or, -ant, -ee (คน)', [['manage<b>ment</b>, perform<b>ance</b>, reli<b>ability</b>', '']]]],
  tips=['หน้าช่องว่างเป็น a / the / adj และหลังช่องว่างเป็น of / กริยา → คำนาม', 'ถ้ามีทั้งคนและสิ่งในตัวเลือก ให้แปลประโยคเลือกความหมาย']),
 dict(id='adj', en='Adjective position', th='ตำแหน่งคำคุณศัพท์',
  intro='คำคุณศัพท์ (adj) ขยายคำนาม หรือบอกลักษณะของประธานหลัง be',
  r=[['adj + คำนาม', 'วางหน้าคำนามที่ขยาย อาจอยู่หลัง a / the / my', [['a <b>successful</b> product launch', 'การเปิดตัวสินค้าที่ประสบความสำเร็จ']]],
     ['be / become / remain / seem + adj', 'ทำหน้าที่ส่วนเติมเต็มประธาน (subject complement)', [['The survey results were <b>impressive</b>.', 'ผลสำรวจน่าประทับใจ']]],
     ['keep / find / make + กรรม + adj', 'adj บอกสภาพของกรรม', [['Please keep the work area <b>clean</b>.', 'กรุณารักษาพื้นที่ทำงานให้สะอาด']]],
     ['-ing กับ -ed', '-ing = เป็นผู้ทำ หรือทำให้เกิดความรู้สึก / -ed = ถูกกระทำ หรือรู้สึก', [['a <b>connecting</b> flight', 'เที่ยวบินต่อเครื่อง'], ['the <b>revised</b> schedule', 'ตารางที่ถูกแก้ไขแล้ว']]],
     ['ขั้นกว่า ขั้นสุด และคำบอกจำนวน', '-er / more ... than, the -est / the most ... / many, few + นามนับได้พหูพจน์ / much, little + นามนับไม่ได้ / each, every + เอกพจน์', [['the <b>most</b> popular model', 'รุ่นที่ได้รับความนิยมที่สุด']]],
     ['คำลงท้ายที่เป็น adj', '-ful, -ous, -ive, -able, -ible, -al, -ic, -ent, -ant, -ary', [['help<b>ful</b>, effect<b>ive</b>, afford<b>able</b>, addition<b>al</b>', '']]]],
  tips=['ช่องว่างอยู่ระหว่าง a / the กับคำนาม → adj', 'ช่องว่างอยู่หลัง be และไม่มีคำนามตาม → adj']),
 dict(id='adv', en='Adverb position', th='ตำแหน่งคำกริยาวิเศษณ์',
  intro='คำกริยาวิเศษณ์ (adv) ขยายกริยา adj หรือทั้งประโยค ตัดออกแล้วประโยคยังครบ',
  r=[['adv ขยายกริยา', 'วางหน้ากริยาแท้ หลัง have / will / be หรือท้ายประโยค', [['The company has <b>recently</b> expanded.', 'บริษัทเพิ่งขยายกิจการ'], ['Our staff will <b>promptly</b> respond.', 'พนักงานจะตอบกลับทันที']]],
     ['adv ขยาย adj', 'วางหน้า adj', [['an <b>extremely</b> popular café', 'คาเฟ่ที่ได้รับความนิยมอย่างมาก'], ['<b>highly</b> recommended', 'ขอแนะนำอย่างยิ่ง']]],
     ['ระหว่าง be กับ -ing / p.p.', 'ช่องว่างอยู่ตรงกลางกริยาหลายคำ', [['The plan is <b>currently</b> being reviewed.', 'แผนกำลังถูกพิจารณาอยู่ในขณะนี้']]],
     ['ประโยคครบแล้ว', 'มีประธาน กริยา และกรรมครบ ช่องว่างที่เหลือมักเป็น adv ส่วนใหญ่ลงท้าย -ly', [['She completed the task <b>efficiently</b>.', 'เธอทำงานเสร็จอย่างมีประสิทธิภาพ']]]],
  tips=['ลองตัดช่องว่างออก ถ้าประโยคยังสมบูรณ์ → adv', 'ระวังคำลงท้าย -ly ที่เป็น adj เช่น friendly, costly, timely']),
 dict(id='verb', en='Verb forms', th='รูปกริยา: tense, agreement และ modal',
  intro='ตัวเลือกเป็นกริยาตัวเดียวกันหลายรูป ให้ดูว่าประโยคมีกริยาแท้หรือยัง ประธานเป็นเอกพจน์หรือพหูพจน์ และมีคำบอกเวลาหรือไม่',
  r=[['หนึ่งประโยคต้องมีกริยาแท้หนึ่งตัว', 'ถ้าประโยคยังไม่มีกริยาแท้ ช่องว่างคือกริยาแท้ ห้ามเลือก -ing หรือ to V', [['The director <b>approved</b> the budget.', 'ผู้อำนวยการอนุมัติงบประมาณ']]],
     ['คำบอกเวลาคือกุญแจ', 'yesterday, last ~, ago → อดีต / next ~, tomorrow → will / since, for + ช่วงเวลา, recently → has / have + p.p. / every ~, usually → present simple', [['Sales <b>have increased</b> since January.', 'ยอดขายเพิ่มขึ้นตั้งแต่เดือนมกราคม']]],
     ['ประธานกับกริยาต้องสอดคล้องกัน', 'ประธานเอกพจน์ + V-s / ประธานพหูพจน์ + V ให้ข้ามวลีขยาย เช่น of ... หรือ who ... แล้วหาประธานตัวจริง', [['The list of new products <b>is</b> attached.', 'รายการสินค้าใหม่แนบมาด้วย']]],
     ['modal + V1', 'หลัง can, will, should, must, may ใช้กริยารูปเดิม', [['Visitors should <b>sign</b> in at the front desk.', 'ผู้มาเยือนควรลงชื่อที่โต๊ะต้อนรับ']]],
     ['ประโยคคำสั่ง', 'ขึ้นต้นด้วย V1 (อาจมี Please นำหน้า)', [['<b>Submit</b> your form by Friday.', 'ส่งแบบฟอร์มภายในวันศุกร์']]],
     ['If / When พูดถึงอนาคต ใช้ present', 'ประโยคย่อยใช้ present ส่วนประโยคหลักใช้ will', [['When the shipment <b>arrives</b>, we will call you.', 'เมื่อสินค้ามาถึง เราจะโทรหาคุณ']]]],
  tips=['ขั้นที่ 1 มีกริยาแท้แล้วหรือยัง', 'ขั้นที่ 2 ประธานตัวจริงคืออะไร เอกพจน์หรือพหูพจน์', 'ขั้นที่ 3 มีคำบอกเวลาไหม']),
 dict(id='voice', en='Active / Passive', th='Active และ Passive voice',
  intro='ตัวเลือกมีทั้งรูปผู้ทำ (active) และรูปถูกกระทำ (be + p.p.) ให้ดูว่าประธานเป็นผู้ทำหรือผู้ถูกกระทำ',
  r=[['Active: ประธานเป็นผู้ทำ และมีกรรมตาม', '', [['The team <b>completed</b> the project.', 'ทีมทำโครงการเสร็จ']]],
     ['Passive: be + p.p. ประธานถูกกระทำ', 'หลังกริยามักไม่มีกรรม แต่อาจมี by หรือบุพบทอื่นตาม', [['The project <b>was completed</b> on time.', 'โครงการเสร็จทันเวลา']]],
     ['ดูว่าหลังช่องว่างมีกรรมไหม', 'มีคำนามเป็นกรรมตาม → active / ไม่มีกรรม → passive', [['The order <b>will be shipped</b> tomorrow.', 'คำสั่งซื้อจะถูกจัดส่งพรุ่งนี้']]],
     ['passive ผสม tense', 'is being + p.p. / has been + p.p. / will be + p.p.', [['The room <b>has been reserved</b>.', 'ห้องถูกจองไว้แล้ว']]],
     ['กริยาที่ไม่มีกรรม ใช้ passive ไม่ได้', 'arrive, occur, happen, rise, remain, take place', [['Prices <b>rose</b> last month.', 'ราคาสูงขึ้นเมื่อเดือนที่แล้ว']]]],
  tips=['ประธานเป็นสิ่งของ (report, order, room) และไม่มีกรรมตาม → มักเป็น passive']),
 dict(id='inf', en='To-infinitive & Gerund', th='To-infinitive และ Gerund',
  intro='to + V1 และ V-ing ทำหน้าที่เหมือนคำนาม adj หรือ adv ได้ ต้องเลือกให้ถูกตำแหน่ง',
  r=[['to V = "เพื่อ"', 'บอกจุดประสงค์ วางต้นหรือท้ายประโยคได้ (in order to)', [['<b>To register</b>, visit our Web site.', 'หากต้องการลงทะเบียน ให้เข้าเว็บไซต์ของเรา']]],
     ['กริยาที่ตามด้วย to V', 'plan, want, hope, decide, agree, expect, need, intend, aim และ ask / allow / encourage / require + คน + to V', [['We encourage staff <b>to attend</b>.', 'เราสนับสนุนให้พนักงานเข้าร่วม']]],
     ['กริยาที่ตามด้วย V-ing', 'consider, suggest, recommend, avoid, finish, enjoy, mind', [['She suggested <b>moving</b> the meeting.', 'เธอเสนอให้เลื่อนการประชุม']]],
     ['บุพบท + V-ing', 'รวมถึง look forward to + V-ing (to ตรงนี้เป็นบุพบท)', [['Thank you for <b>joining</b> us.', 'ขอบคุณที่มาร่วมกับเรา'], ['We look forward to <b>meeting</b> you.', 'เรารอพบคุณ']]],
     ['V-ing เป็นประธาน', 'ใช้กริยาเอกพจน์ตาม', [['<b>Reviewing</b> contracts takes time.', 'การตรวจสัญญาใช้เวลา']]],
     ['make / let / have + คน + V1', 'ไม่มี to (bare infinitive)', [['Please let us <b>know</b>.', 'กรุณาแจ้งให้เราทราบ']]],
     ['คำนาม + to V', 'to V ขยายคำนาม', [['the best way <b>to reach</b> us', 'วิธีที่ดีที่สุดในการติดต่อเรา']]]],
  tips=['หน้าช่องว่างเป็นบุพบท → V-ing', 'แปลว่า "เพื่อ" ได้ → to V']),
 dict(id='part', en='Participles', th='Participle: -ing / -ed ขยายคำนาม',
  intro='V-ing และ V-ed วางหลังคำนามหรือต้นประโยคเพื่อขยาย ต้องถามว่าคำนามนั้นเป็นผู้ทำหรือถูกทำ',
  r=[['คำนาม + V-ing = เป็นผู้ทำ', '', [['employees <b>working</b> overtime', 'พนักงานที่ทำงานล่วงเวลา']]],
     ['คำนาม + V-ed = ถูกกระทำ', '', [['the documents <b>attached</b> to this e-mail', 'เอกสารที่แนบมากับอีเมลนี้']]],
     ['วลีต้นประโยค', 'ประธานของวลีคือประธานของประโยคหลัง', [['<b>Located</b> near the station, the hotel is convenient.', 'โรงแรมตั้งอยู่ใกล้สถานี จึงสะดวก']]]],
  tips=['ถามว่าคำนามนั้น "ทำ" (-ing) หรือ "ถูกทำ" (-ed)']),
 dict(id='conj', en='Conjunctions', th='คำเชื่อมและอนุประโยค',
  intro='คำเชื่อม (conjunction) ตามด้วยประธาน + กริยา ส่วนบุพบทตามด้วยคำนามเท่านั้น นี่คือจุดที่ข้อสอบชอบหลอก',
  r=[['คำเชื่อม + ประธาน + กริยา', 'because, although, even though, while, when, before, after, until, if, unless, as soon as, once, so that', [['<b>Although</b> it rained, many people came.', 'แม้ฝนตก ก็มีคนมามาก']]],
     ['บุพบท + คำนาม', 'because of, despite, in spite of, during, due to', [['<b>Despite</b> the rain, many people came.', 'แม้จะมีฝน ก็มีคนมามาก']]],
     ['คู่ที่ข้อสอบชอบออก', 'because ↔ because of / although ↔ despite / while ↔ during (ซ้ายตามด้วยประโยค ขวาตามด้วยคำนาม)', []],
     ['คำเชื่อมคู่', 'both A and B / either A or B / neither A nor B / not only A but also B / whether A or B', [['<b>Either</b> Monday <b>or</b> Tuesday is fine.', 'วันจันทร์หรือวันอังคารก็ได้']]],
     ['and / but / or / so', 'เชื่อมสิ่งที่มีหน้าที่เท่ากัน', [['fast <b>and</b> reliable', 'เร็วและเชื่อถือได้']]],
     ['ประโยคกลับ (inversion)', 'Should you have questions = If you should have questions', [['<b>Should</b> you need help, call us.', 'หากต้องการความช่วยเหลือ โทรหาเรา']]]],
  tips=['หลังช่องว่างมีประธาน + กริยา → คำเชื่อม', 'หลังช่องว่างเป็นแค่คำนาม → บุพบท', 'จากนั้นค่อยเลือกตามความหมาย']),
 dict(id='cadv', en='Conjunctive adverbs', th='คำเชื่อมความระหว่างประโยค (Part 6)',
  intro='คำอย่าง However, Therefore อยู่ต้นประโยคและตามด้วย comma ใช้บอกว่าประโยคนี้สัมพันธ์กับประโยคก่อนหน้าอย่างไร',
  r=[['เพิ่มเติม', 'In addition, Moreover, Furthermore, Also, Besides', []],
     ['ขัดแย้ง', 'However, Nevertheless, On the other hand, Instead', []],
     ['ผลลัพธ์', 'Therefore, As a result, Consequently, Accordingly, Thus', []],
     ['ลำดับเวลา', 'Afterward, Meanwhile, In the meantime, Then, Finally, Previously', []],
     ['อื่นๆ', 'For example (ยกตัวอย่าง), Otherwise (มิฉะนั้น), In fact (อันที่จริง), Similarly (ในทำนองเดียวกัน), Even so (ถึงอย่างนั้น)', [['Please confirm by Friday. <b>Otherwise</b>, your seat will be released.', 'กรุณายืนยันภายในวันศุกร์ มิฉะนั้นที่นั่งของคุณจะถูกปล่อย']]]],
  tips=['อ่านประโยคก่อนหน้าและประโยคที่มีช่องว่าง', 'ถามว่าสัมพันธ์กันแบบไหน: เพิ่ม / ค้าน / ผล / ลำดับ']),
 dict(id='rel', en='Relative & noun clauses', th='Relative pronoun และ noun clause',
  intro='who, which, that, whose ขยายคำนามที่อยู่ข้างหน้า ส่วน what, whether, that นำประโยคมาทำหน้าที่เป็นคำนาม',
  r=[['who (คน) / which (สิ่ง) / that (ทั้งคู่) + กริยา', '', [['applicants <b>who</b> have experience', 'ผู้สมัครที่มีประสบการณ์']]],
     ['whose + คำนาม', 'แสดงความเป็นเจ้าของ', [['the client <b>whose</b> order was delayed', 'ลูกค้าที่คำสั่งซื้อล่าช้า']]],
     ['บุพบท + whom / which', '', [['the firm <b>for which</b> she works', 'บริษัทที่เธอทำงานให้']]],
     ['what = the thing that', 'มีคำนามอยู่ในตัว จึงไม่มีคำนามนำหน้า', [['<b>What</b> customers want is quality.', 'สิ่งที่ลูกค้าต้องการคือคุณภาพ']]],
     ['whoever / whichever', 'ใครก็ตามที่ / อันไหนก็ตาม', []],
     ['that / whether / if + ประโยค เป็นกรรม', 'whether = ว่า ... หรือไม่', [['We will decide <b>whether</b> to expand.', 'เราจะตัดสินใจว่าจะขยายหรือไม่']]]],
  tips=['หน้าช่องว่างเป็นคน → who', 'หน้าช่องว่างเป็นสิ่งของ → which', 'หลังช่องว่างเป็นคำนาม → whose']),
 dict(id='prep', en='Prepositions', th='คำบุพบท',
  intro='บุพบทตามด้วยคำนามหรือ V-ing ข้อสอบเน้นความหมายและคำที่ใช้คู่กัน (collocation)',
  r=[['เวลา', 'at + เวลา / on + วัน / in + เดือน ปี / by = ไม่เกิน / until = จนถึง / within = ภายใน / during = ระหว่าง / for + ระยะเวลา / since + จุดเริ่ม', [['Submit it <b>by</b> Friday.', 'ส่งภายในวันศุกร์ (ไม่เกิน)'], ['The store is open <b>until</b> 9 P.M.', 'ร้านเปิดจนถึง 3 ทุ่ม']]],
     ['สถานที่', 'at (จุด) / in (ข้างใน) / on (บนพื้นผิว) / throughout (ทั่ว) / across / along / near / next to / opposite', [['<b>throughout</b> the building', 'ทั่วทั้งอาคาร']]],
     ['คู่คำที่ออกบ่อย', 'responsible for, eligible for, in charge of, in addition to, according to, prior to (ก่อน), regarding / concerning (เกี่ยวกับ), as of (นับตั้งแต่), on behalf of, in response to, along with', [['<b>Prior to</b> the meeting, read the report.', 'ก่อนการประชุม ให้อ่านรายงาน']]]],
  tips=['จำเป็นคู่คำได้ผลกว่าจำทีละคำ', 'ถ้าหลังช่องว่างเป็นประโยค ให้ไปดูบทคำเชื่อมแทน']),
 dict(id='vn', en='Noun vocabulary', th='คำศัพท์: คำนาม',
  intro='ตัวเลือกทั้งสี่เป็นคำนาม ข้อนี้วัดความหมาย อ่านทั้งประโยคแล้วดูคำที่มาคู่กับช่องว่าง',
  r=[['ดูคำที่มาคู่กัน', 'กริยาหรือ adj ข้างๆ มักบอกคำตอบ', [['meet the <b>deadline</b>', 'ทันกำหนดส่ง'], ['make a <b>reservation</b>', 'จอง'], ['a wide <b>selection</b> of', 'ตัวเลือกหลากหลาย'], ['under <b>warranty</b>', 'อยู่ในประกัน']]]],
  tips=['แปลประโยคคร่าวๆ ก่อน แล้วเติมคำที่ความหมายเข้ากัน', 'ตัวลวงมักเป็นคำที่เกี่ยวกับเรื่องเดียวกันแต่ใช้คู่กับคำข้างๆ ไม่ได้']),
 dict(id='vv', en='Verb vocabulary', th='คำศัพท์: คำกริยา',
  intro='ตัวเลือกทั้งสี่เป็นกริยารูปเดียวกัน ข้อนี้วัดความหมายและคำที่ตามหลังกริยา',
  r=[['ดูกรรมและบุพบทที่ตามมา', '', [['<b>conduct</b> a survey', 'ทำแบบสำรวจ'], ['<b>address</b> a concern', 'จัดการข้อกังวล'], ['<b>comply</b> with the rules', 'ปฏิบัติตามกฎ'], ['<b>inform</b> customers of changes', 'แจ้งลูกค้าเรื่องการเปลี่ยนแปลง']]]],
  tips=['กริยาบางตัวต้องมีบุพบทเฉพาะ เช่น comply with, respond to, participate in']),
 dict(id='vadj', en='Adjective vocabulary', th='คำศัพท์: คำคุณศัพท์',
  intro='ตัวเลือกทั้งสี่เป็น adj ดูคำนามที่ขยายและบุพบทที่ตามมา',
  r=[['adj + บุพบทที่มาคู่กัน', '', [['<b>eligible</b> for a discount', 'มีสิทธิ์ได้ส่วนลด'], ['<b>responsible</b> for', 'รับผิดชอบ'], ['<b>comparable</b> to', 'เทียบได้กับ'], ['<b>complimentary</b> breakfast', 'อาหารเช้าฟรี']]]],
  tips=['complimentary = ฟรี (ไม่ใช่ "ชม")', 'ถ้ามีบุพบทตามหลัง ให้ใช้บุพบทนั้นช่วยเลือก']),
 dict(id='vadv', en='Adverb vocabulary', th='คำศัพท์: คำกริยาวิเศษณ์',
  intro='ตัวเลือกทั้งสี่เป็น adv ดูว่าขยายอะไร: ตัวเลข เวลา หรือกริยา',
  r=[['คู่ที่ออกบ่อย', '', [['<b>approximately</b> 30 minutes', 'ประมาณ 30 นาที'], ['<b>shortly</b> after the meeting', 'ไม่นานหลังการประชุม'], ['<b>highly</b> recommended', 'ขอแนะนำอย่างยิ่ง'], ['<b>temporarily</b> closed', 'ปิดชั่วคราว']]]],
  tips=['หน้าตัวเลข → approximately, nearly, almost', 'คู่กับเวลา → shortly, recently, previously']),
 dict(id='ins', en='Sentence insertion', th='เลือกประโยคให้เข้ากับบริบท (Part 6)',
  intro='เลือกประโยคทั้งประโยคมาเติมในช่องว่างของบทความ ต้องอ่านข้อความรอบช่องว่าง',
  r=[['อ่านก่อนและหลังช่องว่าง', 'ประโยคที่ถูกต้องเชื่อมได้ทั้งประโยคก่อนหน้าและประโยคถัดไป', []],
     ['ดูคำอ้างอิง', 'this, these, such, it, they ในตัวเลือก ต้องมีสิ่งที่อ้างถึงอยู่ก่อนหน้า', []],
     ['ดูคำเชื่อมในตัวเลือก', 'Also, However, As a result ต้องสอดคล้องกับความสัมพันธ์ของเนื้อหา', []],
     ['ระวังตัวลวง', 'ตัวลวงมักมีคำซ้ำกับในบทความ แต่เนื้อหาไม่ต่อกัน', []]],
  tips=['เปิด "ดูข้อความทั้งหมด" แล้วอ่านรอบช่องว่างก่อนเลือก']),
]

def lesson_of(cat):
    c = cat.lower()
    if 'sentence insertion' in c or 'choosing a sentence' in c: return 'ins'
    if 'conjunctive adverb' in c: return 'cadv'
    if 'relative' in c or 'noun clause' in c or 'noun-clause' in c: return 'rel'
    if c.startswith('noun position') or 'determiner' in c: return 'noun'
    if c.startswith('adjective position') or 'quantity adjective' in c: return 'adj'
    if c.startswith('adverb position'): return 'adv'
    if 'pronoun' in c: return 'pron'
    if 'conjunction' in c or 'conditional inversion' in c: return 'conj'
    if 'voice' in c or 'active vs. passive' in c: return 'voice'
    if 'infinitive' in c or 'gerund' in c or 'object complement' in c: return 'inf'
    if 'participle' in c: return 'part'
    if 'preposition' in c: return 'prep'
    if c.startswith('verb') : return 'verb' if 'vocabulary' not in c else 'vv'
    if c.startswith('noun vocabulary'): return 'vn'
    if c.startswith('adjective vocabulary'): return 'vadj'
    if c.startswith('adverb vocabulary'): return 'vadv'
    return None

def sentence_with(text, n):
    """the sentence of a Part 6 passage that holds blank [n]; other blanks shown as [...]"""
    parts = re.split(r'(?<=[.!?])\s+(?=[A-Z\[])', text.replace('\n', ' '))
    for p in parts:
        if '[%d]' % n in p:
            return re.sub(r'\[(\d{3})\]', lambda m: '_____' if int(m.group(1)) == n else '[...]', p).strip()
    return '_____'

CTX = {}

def main():
    byid = {L['id']: dict(L, items=[]) for L in LESSONS}
    left = collections.Counter()
    for t in range(1, 11):
        rc = load('rc%02d' % t); tt = '%02d' % t
        for it in rc['parts']['5']:
            lid = lesson_of(it['category'])
            if not lid: left[it['category']] += 1; continue
            byid[lid]['items'].append(dict(id=tt+'-'+str(it['n']), t=tt, n=it['n'], p=5, s=it['sentence'], sth=it.get('sentence_th',''),
                o=it['options'], oth=it.get('options_th',{}), a=it['answer'], c=it.get('category_th',''), x=it.get('explain_th',''), v=it.get('vocab',[])))
        for st in rc['parts']['6']:
            text = '\n\n'.join(p['text'] for p in st['passages']); text_th = '\n\n'.join(p.get('text_th','') for p in st['passages'])
            for q in st['questions']:
                lid = lesson_of(q.get('category',''))
                if not lid: left[q.get('category','')] += 1; continue
                item = dict(id=tt+'-'+str(q['n']), t=tt, n=q['n'], p=6, s=sentence_with(text, q['n']), sth='',
                    o=q['options'], oth=q.get('options_th',{}), a=q['answer'], c=q.get('category_th',''), x=q.get('explain_th',''), v=[])
                item['cx'] = tt + '-' + st['set']   # Part 6 answers often depend on the passage: point to it
                CTX[item['cx']] = {'en': text, 'th': text_th}
                byid[lid]['items'].append(item)
    if left:
        raise SystemExit('categories without a lesson: %r' % left)
    out = [byid[L['id']] for L in LESSONS]
    total = sum(len(L['items']) for L in out)
    js = '(window.__X=window.__X||{})["xgram"]=' + json.dumps({'v': 1, 'lessons': out, 'ctx': CTX}, ensure_ascii=False, separators=(',', ':')) + ';\n'
    open(os.path.join(D, 'xgram.js'), 'w', encoding='utf-8').write(js)
    for L in out: print('%-5s %3d  %s' % (L['id'], len(L['items']), L['th']))
    print('total', total, 'bytes', len(js.encode()))

if __name__ == '__main__':
    main()
