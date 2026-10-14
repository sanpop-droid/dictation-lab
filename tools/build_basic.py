"""Build exam/data/xbasic.js (basic grammar) and exam/data/xtips.js (study techniques) — content written by the team.

Questions: [sentence or question, [correct, wrong, wrong, wrong], explanation]; the options are shuffled with a fixed seed.
Run:  python3 tools/build_basic.py
"""
import json, os, random
from examdata import D

BASIC = [
 dict(id='art', en='Articles: a / an / the', th='คำนำหน้านาม a / an / the',
  intro='a / an ใช้กับคำนามนับได้เอกพจน์ที่ยังไม่เจาะจง ส่วน the ใช้เมื่อผู้ฟังรู้ว่าหมายถึงสิ่งไหน',
  r=[['a + เสียงพยัญชนะ / an + เสียงสระ', 'ดูที่ "เสียง" ไม่ใช่ตัวอักษร', [['<b>a</b> book, <b>a</b> university (ยู-)', 'university ขึ้นต้นด้วยเสียง /j/ จึงใช้ a'], ['<b>an</b> apple, <b>an</b> hour', 'hour ไม่ออกเสียง h จึงขึ้นต้นด้วยเสียงสระ']]],
     ['the = สิ่งที่รู้กันแล้ว หรือมีหนึ่งเดียว', 'พูดถึงครั้งที่สอง สิ่งที่มีหนึ่งเดียว หรือสิ่งที่ระบุชัด', [['I bought a laptop. <b>The</b> laptop is fast.', 'ซื้อแล็ปท็อปมาเครื่องหนึ่ง เครื่องนั้นเร็วมาก'], ['<b>The</b> sun rises in the east.', 'พระอาทิตย์ขึ้นทางทิศตะวันออก']]],
     ['ไม่ใส่ article', 'คำนามพหูพจน์หรือนับไม่ได้ที่พูดถึงแบบทั่วไป', [['He drinks coffee every morning.', 'เขาดื่มกาแฟทุกเช้า']]]],
  q=[['She is _____ engineer.', ['an', 'a', 'the', '(ไม่ต้องใส่)'], 'engineer ขึ้นต้นด้วยเสียงสระ จึงใช้ an'],
     ['I need _____ umbrella.', ['an', 'a', 'the', '(ไม่ต้องใส่)'], 'umbrella ขึ้นต้นด้วยเสียงสระ /ʌ/ จึงใช้ an'],
     ['He works at _____ university in Bangkok.', ['a', 'an', 'the', '(ไม่ต้องใส่)'], 'university ขึ้นต้นด้วยเสียง /j/ (ยู) ซึ่งเป็นเสียงพยัญชนะ จึงใช้ a'],
     ["Please close _____ door. It's cold.", ['the', 'a', 'an', '(ไม่ต้องใส่)'], 'ทั้งคนพูดและคนฟังรู้ว่าประตูบานไหน จึงใช้ the'],
     ['We waited for _____ hour.', ['an', 'a', 'the', '(ไม่ต้องใส่)'], 'hour ไม่ออกเสียง h ขึ้นต้นด้วยเสียงสระ จึงใช้ an'],
     ['_____ sun rises in the east.', ['The', 'A', 'An', '(ไม่ต้องใส่)'], 'ดวงอาทิตย์มีหนึ่งเดียว จึงใช้ the'],
     ['I bought a laptop yesterday. _____ laptop is very fast.', ['The', 'A', 'An', '(ไม่ต้องใส่)'], 'พูดถึงแล็ปท็อปเครื่องเดิมเป็นครั้งที่สอง จึงใช้ the'],
     ['He drinks _____ coffee every morning.', ['(ไม่ต้องใส่)', 'a', 'an', 'the'], 'coffee เป็นคำนามนับไม่ได้ที่พูดแบบทั่วไป จึงไม่ต้องใส่ article']]),
 dict(id='count', en='Countable & uncountable nouns', th='คำนามนับได้และนับไม่ได้',
  intro='คำนามนับได้มีรูปพหูพจน์ ส่วนคำนามนับไม่ได้ไม่เติม s และใช้คำบอกจำนวนต่างกัน',
  r=[['คำนามนับไม่ได้ที่ออกสอบบ่อย', 'information, advice, furniture, equipment, luggage, money, water, feedback ไม่เติม s และไม่ใช้ a / an', [['some useful <b>information</b>', 'ข้อมูลที่เป็นประโยชน์'], ['a piece of <b>advice</b>', 'คำแนะนำหนึ่งข้อ']]],
     ['คำบอกจำนวน', 'many / few / a few + นามนับได้พหูพจน์ / much / little / a little + นามนับไม่ได้ / a lot of ใช้ได้ทั้งสองแบบ', [['How <b>many</b> people came?', 'มีคนมากี่คน'], ["We don't have <b>much</b> time.", 'เรามีเวลาไม่มาก']]],
     ['some กับ any', 'some ใช้ในประโยคบอกเล่า (และคำถามที่เสนอหรือขอ) / any ใช้ในประโยคปฏิเสธและคำถาม', [["There isn't <b>any</b> milk.", 'ไม่มีนมเลย']]],
     ['few / little กับ a few / a little', 'few, little = แทบไม่มี (ความหมายเชิงลบ) / a few, a little = มีอยู่บ้าง', []]],
  q=[['How _____ people came to the meeting?', ['many', 'much', 'little', 'a little'], 'people นับได้ พหูพจน์ จึงใช้ many'],
     ["We don't have _____ time.", ['much', 'many', 'few', 'a few'], 'time ในความหมาย "เวลา" นับไม่ได้ จึงใช้ much'],
     ['Could you give me some _____?', ['advice', 'advices', 'an advice', 'advises'], 'advice นับไม่ได้ ไม่เติม s และไม่ใช้ an'],
     ["There isn't _____ milk in the fridge.", ['any', 'some', 'many', 'a few'], 'ประโยคปฏิเสธใช้ any และ milk นับไม่ได้'],
     ['I have _____ questions about the contract.', ['a few', 'a little', 'much', 'a lot'], 'questions นับได้พหูพจน์ จึงใช้ a few (a lot ต้องมี of)'],
     ['The office needs new _____.', ['equipment', 'equipments', 'an equipment', 'equipmentes'], 'equipment นับไม่ได้ ไม่เติม s'],
     ['She gave me _____ useful information.', ['some', 'many', 'a', 'few'], 'information นับไม่ได้ ใช้ some ได้ แต่ใช้ many, a, few ไม่ได้'],
     ['There is _____ sugar left, so please buy more.', ['little', 'few', 'many', 'a few'], 'sugar นับไม่ได้ และประโยคบอกว่าต้องซื้อเพิ่ม จึงใช้ little (แทบไม่มี)']]),
 dict(id='comp', en='Comparatives & superlatives', th='การเปรียบเทียบ ขั้นกว่าและขั้นสุด',
  intro='ขั้นกว่าเปรียบเทียบสองสิ่ง (ตามด้วย than) ขั้นสุดบอกว่ามากที่สุดในกลุ่ม (มี the นำหน้า)',
  r=[['คำสั้น (1 พยางค์)', '+er / the + -est', [['tall → <b>taller</b> → <b>the tallest</b>', '']]],
     ['ลงท้าย y', 'เปลี่ยน y เป็น i แล้วเติม -er / -est', [['easy → <b>easier</b> → <b>the easiest</b>', '']]],
     ['คำยาว (2 พยางค์ขึ้นไป)', 'more / the most', [['expensive → <b>more expensive</b> → <b>the most expensive</b>', '']]],
     ['รูปไม่ปกติ', 'good → better → best / bad → worse → worst / far → farther → farthest / many, much → more → most', []],
     ['as ... as = เท่ากับ', 'ใช้ adj รูปปกติระหว่าง as กับ as', [['Today is <b>as hot as</b> yesterday.', 'วันนี้ร้อนเท่ากับเมื่อวาน']]]],
  q=[['This laptop is _____ than my old one.', ['lighter', 'lightest', 'more light', 'light'], 'คำสั้น + er และมี than จึงใช้ขั้นกว่า'],
     ['This is the _____ hotel in the city.', ['most expensive', 'more expensive', 'expensivest', 'expensive'], 'มี the และหมายถึงที่สุดในเมือง คำยาวใช้ the most'],
     ['Her English is _____ than mine.', ['better', 'gooder', 'best', 'more good'], 'good เป็นรูปไม่ปกติ ขั้นกว่าคือ better'],
     ['The test was _____ than I expected.', ['easier', 'more easy', 'easiest', 'easy'], 'easy ลงท้าย y เปลี่ยนเป็น easier'],
     ['Today is as hot _____ yesterday.', ['as', 'than', 'that', 'so'], 'โครงสร้าง as ... as'],
     ['Of all the applicants, she is the _____ experienced.', ['most', 'more', 'much', 'very'], 'Of all ... = ในกลุ่มทั้งหมด จึงใช้ขั้นสุด the most'],
     ['The traffic is _____ today than last week.', ['worse', 'worst', 'badder', 'more bad'], 'bad เป็นรูปไม่ปกติ ขั้นกว่าคือ worse'],
     ['This route is _____ than the highway.', ['shorter', 'more short', 'shortest', 'the shorter'], 'คำสั้น + er และมี than']]),
 dict(id='cond', en='If-clauses (conditionals)', th='ประโยคเงื่อนไข If',
  intro='รูปของกริยาในประโยค If บอกว่าเรื่องนั้นเป็นจริง เป็นไปได้ หรือเป็นแค่การสมมติ',
  r=[['ความจริงทั่วไป', 'If + present, present', [['If you heat ice, it <b>melts</b>.', 'ถ้าทำให้น้ำแข็งร้อน มันจะละลาย']]],
     ['เป็นไปได้ในอนาคต', 'If + present, will + V1 (ห้ามใช้ will หลัง If)', [['If it <b>rains</b>, we <b>will stay</b> home.', 'ถ้าฝนตก เราจะอยู่บ้าน']]],
     ['สมมติสิ่งที่ไม่จริงตอนนี้', 'If + past, would + V1 (ใช้ were กับทุกประธาน)', [['If I <b>were</b> you, I <b>would</b> ask the manager.', 'ถ้าฉันเป็นคุณ ฉันจะถามผู้จัดการ']]],
     ['สมมติอดีตที่ไม่ได้เกิดขึ้น', 'If + had + p.p., would have + p.p.', [['If I <b>had studied</b>, I <b>would have passed</b>.', 'ถ้าตอนนั้นฉันอ่านหนังสือ ฉันคงสอบผ่านไปแล้ว']]],
     ['unless = if ... not', '', [['We will miss the bus <b>unless</b> we hurry.', 'เราจะตกรถบัส ถ้าไม่รีบ']]]],
  q=[['If it _____ tomorrow, we will cancel the picnic.', ['rains', 'will rain', 'rained', 'would rain'], 'เป็นไปได้ในอนาคต ประโยค If ใช้ present'],
     ['If I _____ rich, I would buy a house by the sea.', ['were', 'am', 'will be', 'have been'], 'สมมติสิ่งที่ไม่จริงตอนนี้ ใช้ were'],
     ['If you heat water to 100°C, it _____.', ['boils', 'will boiled', 'boiled', 'is boil'], 'ความจริงทางวิทยาศาสตร์ ใช้ present ทั้งสองส่วน'],
     ['If she had left earlier, she _____ the train.', ['would have caught', 'will catch', 'would catch', 'caught'], 'สมมติอดีต: had + p.p. คู่กับ would have + p.p.'],
     ['We will miss the bus _____ we hurry.', ['unless', 'if', 'because', 'so'], 'unless = ถ้าไม่ ความหมายคือ ถ้าไม่รีบจะตกรถ'],
     ['If I _____ you, I would talk to the manager.', ['were', 'am', 'will be', 'be'], 'If I were you ใช้ให้คำแนะนำ'],
     ['If you finish the report today, I _____ it tomorrow.', ['will check', 'would have checked', 'checked', 'had checked'], 'เป็นไปได้ในอนาคต ประโยคหลังใช้ will + V1'],
     ['If they _____ the ad, they would have applied.', ['had seen', 'saw', 'have seen', 'see'], 'สมมติอดีต ประโยค If ใช้ had + p.p.']]),
 dict(id='modal', en='Modal verbs', th='กริยาช่วย can, should, must และอื่นๆ',
  intro='กริยาช่วย (modal) บอกความสามารถ คำแนะนำ ความจำเป็น หรือความเป็นไปได้ และตามด้วยกริยารูปเดิม (V1) เสมอ',
  r=[['ความสามารถและการขอ', 'can / could (สุภาพกว่า)', [['<b>Could</b> you help me?', 'ช่วยฉันหน่อยได้ไหม']]],
     ['คำแนะนำ', 'should = ควร', [['You <b>should</b> get some rest.', 'คุณควรพักผ่อน']]],
     ['จำเป็น และ ห้าม', 'must / have to = ต้อง / must not = ห้าม / don\'t have to = ไม่จำเป็นต้อง', [['You <b>must not</b> smoke here.', 'ห้ามสูบบุหรี่ที่นี่'], ['You <b>don\'t have to</b> come.', 'ไม่จำเป็นต้องมาก็ได้']]],
     ['ความเป็นไปได้', 'may / might = อาจจะ', [['It <b>might</b> rain later.', 'ฝนอาจจะตกทีหลัง']]]],
  q=[["You _____ wear a helmet. It's the law.", ['must', 'might', 'could', 'would'], 'กฎหมายบังคับ = ต้อง ใช้ must'],
     ["You _____ come if you're busy. It's optional.", ["don't have to", 'must not', "can't", 'should'], 'optional = ไม่บังคับ จึงใช้ don\'t have to (ไม่จำเป็นต้อง)'],
     ["You _____ smoke here. It's not allowed.", ['must not', "don't have to", 'needn\'t', 'might'], 'not allowed = ห้าม ใช้ must not'],
     ['It _____ rain later, so take an umbrella.', ['might', 'must', 'should to', 'can to'], 'ไม่แน่ใจ = อาจจะ ใช้ might'],
     ['You look tired. You _____ get some rest.', ['should', 'must not', "can't", 'might not'], 'ให้คำแนะนำ ใช้ should'],
     ['_____ you help me carry these boxes?', ['Could', 'Must', 'Should', 'Might'], 'ขอร้องอย่างสุภาพ ใช้ Could you ...?'],
     ['She can _____ three languages.', ['speak', 'speaks', 'speaking', 'to speak'], 'หลัง modal ใช้ V1 เสมอ'],
     ['I _____ swim when I was five.', ['could', 'can', 'must', 'should'], 'ความสามารถในอดีต ใช้ could']]),
 dict(id='quest', en='Making questions', th='การสร้างประโยคคำถาม',
  intro='คำถามภาษาอังกฤษสลับกริยาช่วยขึ้นหน้าประธาน ถ้าไม่มีกริยาช่วยให้ใช้ do / does / did',
  r=[['คำถาม Yes / No', 'กริยาช่วย + ประธาน + กริยา', [['<b>Do</b> you like coffee?', 'คุณชอบกาแฟไหม'], ['<b>Have</b> you finished?', 'ทำเสร็จหรือยัง']]],
     ['คำถาม Wh-', 'Wh- + กริยาช่วย + ประธาน + กริยา', [['Where <b>does</b> she work?', 'เธอทำงานที่ไหน']]],
     ['does / did แล้วกริยาเป็นรูปเดิม', 'Does he <b>like</b> ...? (ไม่ใช่ likes) / Did you <b>go</b> ...? (ไม่ใช่ went)', []],
     ['Who / What เป็นประธาน', 'ไม่ต้องใช้ do / did', [['Who <b>called</b> you?', 'ใครโทรหาคุณ']]]],
  q=[['_____ you finish the report yesterday?', ['Did', 'Do', 'Were', 'Have'], 'yesterday = อดีต ไม่มีกริยาช่วยอื่น จึงใช้ Did + V1'],
     ['Where _____ she work?', ['does', 'do', 'is', 'did she'], 'ประธาน she ปัจจุบัน ใช้ does + V1'],
     ['What time _____ the meeting start?', ['does', 'do', 'is', 'are'], 'the meeting เอกพจน์ ใช้ does'],
     ['Who _____ the window?', ['broke', 'did break', 'does broke', 'broken'], 'Who เป็นประธาน ไม่ต้องใช้ did ใช้กริยาอดีตได้เลย'],
     ['_____ you ever been to Japan?', ['Have', 'Did', 'Do', 'Are'], 'ever + been = present perfect ใช้ Have'],
     ['How long _____ you been waiting?', ['have', 'did', 'do', 'are'], 'been waiting = present perfect continuous ใช้ have'],
     ['Does he _____ coffee?', ['like', 'likes', 'liked', 'liking'], 'หลัง does ใช้กริยารูปเดิม'],
     ['Why _____ the train late this morning?', ['was', 'did', 'does', 'were'], 'late เป็น adj ใช้ be และเป็นอดีต เอกพจน์ จึงใช้ was']]),
]

TIPS = [
 dict(id='mem', en='Remembering words', th='เทคนิคการจำคำศัพท์',
  intro='จำคำศัพท์ให้ได้นานต้องดึงความจำออกมาบ่อยๆ ในเวลาที่เหมาะสม ไม่ใช่อ่านซ้ำหลายรอบในวันเดียว',
  r=[['ทบทวนเว้นระยะ', 'ทบทวนหลังเรียน 1, 3, 7, 14 วัน แผนฝึกวันนี้ในแอปจัดให้อัตโนมัติ', []],
     ['ทดสอบตัวเอง ดีกว่าอ่านซ้ำ', 'ปิดคำแล้วเขียนจากความจำ (active recall) สมองต้องดึงข้อมูลออกมา จึงจำแน่นกว่า', []],
     ['จำเป็นวลี ไม่ใช่คำเดี่ยว', 'จำ "meet the deadline" ทั้งวลี พร้อมตัวอย่างประโยค ช่วยให้ใช้ได้จริง', []],
     ['ไม่ต้องเยอะ แต่ต้องทุกวัน', 'คำใหม่วันละ 5–10 คำ และทบทวนคำเก่าทุกวัน ได้ผลกว่าวันละ 50 คำแล้วหยุดไปหลายวัน', []],
     ['คำดื้อต้องฝึกพิเศษ', 'คำที่ผิดซ้ำ ให้แบ่งเป็นก้อนสี ดู-ปิด-เขียน-ตรวจ หลายรอบ (มีในหน้าวันนี้)', []]],
  q=[['วิธีใดช่วยให้จำคำศัพท์ได้นานที่สุด?', ['ทบทวนเว้นระยะ เช่น 1, 3, 7 วันหลังเรียน', 'อ่านซ้ำ 20 รอบในวันเดียว', 'ฟังเพลงอย่างเดียว', 'จดลงสมุดแล้วไม่เปิดดูอีก'], 'การทบทวนเว้นระยะช่วยให้ความจำย้ายไปอยู่ระยะยาว'],
     ['ถ้าต้องจำคำว่า "deadline" ควรจำแบบไหน?', ['จำทั้งวลี meet the deadline พร้อมตัวอย่าง', 'จำแค่คำแปล', 'จำแค่ตัวสะกด', 'จำแค่เสียง'], 'จำเป็นวลีพร้อมบริบททำให้รู้ว่าใช้กับคำไหน'],
     ['การเขียนจากความจำต่างจากการอ่านซ้ำอย่างไร?', ['ต้องดึงความจำออกมา จึงจำได้นานกว่า', 'อ่านซ้ำจำได้นานกว่า', 'ไม่ต่างกัน', 'เขียนจากความจำทำให้ลืมเร็ว'], 'active recall เป็นวิธีที่งานวิจัยด้านการเรียนรู้ยืนยันว่าได้ผลดี'],
     ['คนทำงานควรเรียนคำใหม่วันละประมาณเท่าไร?', ['5–10 คำ และทบทวนคำเก่าทุกวัน', '100 คำ', '50 คำแต่ไม่ทบทวน', 'เดือนละครั้งครั้งละมากๆ'], 'น้อยแต่สม่ำเสมอดีกว่า และต้องมีเวลาเหลือไว้ทบทวน'],
     ['คำที่สะกดผิดซ้ำหลายครั้งควรทำอย่างไร?', ['แบ่งเป็นก้อน แล้วดู-ปิด-เขียน-ตรวจ หลายรอบ', 'ข้ามไปเลย', 'จำเฉพาะคำแปล', 'เดาทุกครั้ง'], 'การฝึกเจาะคำที่ผิดบ่อยช่วยแก้จุดอ่อนตรงจุด']]),
 dict(id='listen', en='Listening', th='เทคนิคการฟัง',
  intro='การฟังดีขึ้นได้ด้วยการฟังซ้ำแบบตั้งใจ ไม่ใช่เปิดฟังผ่านๆ',
  r=[['ฟังทีละประโยค แล้วเขียนตาม (dictation)', 'ช่วยให้รู้ว่าคำไหนฟังไม่ออก มีในเมนูฝึก "เขียนประโยค" และข้อสอบ "ฟังแล้วเขียน"', []],
     ['พูดตาม (shadowing)', 'ฟังแล้วพูดตามทันที เลียนจังหวะและการเน้นเสียง ช่วยให้หูชินกับคำที่เชื่อมกัน', []],
     ['ไม่ต้องฟังออกทุกคำ', 'จับคำสำคัญ เช่น คำนาม ตัวเลข คำกริยาหลัก ก็เข้าใจเรื่องได้', []],
     ['ข้อสอบ: อ่านคำถามก่อนเสียงเริ่ม', 'รู้ว่าต้องฟังอะไร จะจับคำตอบได้ง่ายขึ้น', []],
     ['ฟังหลายสำเนียง', 'ข้อสอบมีทั้งสำเนียงอเมริกัน อังกฤษ แคนาดา และออสเตรเลีย', []]],
  q=[['วิธีใดช่วยให้รู้ว่าตัวเองฟังคำไหนไม่ออก?', ['ฟังทีละประโยคแล้วเขียนตาม', 'เปิดฟังเป็นพื้นหลังทั้งวัน', 'อ่านคำแปลอย่างเดียว', 'ฟังเร็วขึ้น 2 เท่า'], 'dictation ทำให้เห็นคำที่พลาดชัดเจน'],
     ['shadowing คืออะไร?', ['ฟังแล้วพูดตามทันที เลียนจังหวะและเสียงเน้น', 'ฟังโดยไม่พูดอะไร', 'แปลทุกคำเป็นภาษาไทย', 'อ่านสคริปต์ในใจ'], 'shadowing ฝึกทั้งหูและปากไปพร้อมกัน'],
     ['ถ้าฟังไม่ออกบางคำ ควรทำอย่างไร?', ['จับคำสำคัญแล้วเดาจากบริบท', 'หยุดฟังทันที', 'กังวลจนพลาดประโยคถัดไป', 'ตอบข้อแรกเสมอ'], 'ผู้ฟังที่เก่งใช้คำสำคัญและบริบทช่วยเติมส่วนที่หายไป'],
     ['ใน Part 3–4 ควรทำอะไรก่อนเสียงเริ่ม?', ['อ่านคำถามและตัวเลือก', 'ปิดตาฟัง', 'อ่านคำถามข้อถัดไปของ Part อื่น', 'ไม่ต้องทำอะไร'], 'รู้คำถามล่วงหน้าทำให้รู้ว่าต้องฟังข้อมูลไหน'],
     ['ทำไมควรฟังหลายสำเนียง?', ['ข้อสอบมีผู้พูดหลายสำเนียง', 'ทุกสำเนียงเหมือนกัน', 'เพื่อจำสำเนียงเดียว', 'ไม่จำเป็น'], 'ข้อสอบใช้ผู้พูดสำเนียงอเมริกัน อังกฤษ แคนาดา และออสเตรเลีย']]),
 dict(id='read', en='Reading', th='เทคนิคการอ่าน',
  intro='อ่านให้เร็วและแม่น ต้องรู้ว่ากำลังหาอะไร แล้วเลือกวิธีอ่านให้เหมาะ',
  r=[['skimming = กวาดตาหาใจความ', 'อ่านหัวเรื่อง ประโยคแรกของแต่ละย่อหน้า เพื่อรู้ว่าเรื่องเกี่ยวกับอะไร', []],
     ['scanning = หาข้อมูลเฉพาะ', 'มองหาตัวเลข ชื่อ วันที่ โดยไม่อ่านทุกคำ', []],
     ['อ่านคำถามก่อน', 'รู้ว่าต้องหาอะไร แล้วค่อยกลับไปหาในบทความ', []],
     ['เดาความหมายจากบริบท', 'ดูคำรอบๆ คำที่ไม่รู้ ไม่ต้องหยุดเปิดพจนานุกรมทุกคำ', []],
     ['อย่าแปลทุกคำ', 'การแปลทีละคำทำให้ช้าและหลงประเด็น', []]],
  q=[['ถ้าต้องการรู้ว่าอีเมลนี้เขียนมาเพื่ออะไร ควรอ่านแบบไหน?', ['skimming อ่านหัวเรื่องและประโยคแรก', 'อ่านทุกคำอย่างละเอียด', 'อ่านย่อหน้าสุดท้ายอย่างเดียว', 'ข้ามไปดูตัวเลข'], 'จุดประสงค์มักอยู่ต้นเรื่อง'],
     ['ถ้าคำถามถามราคาของสินค้า ควรอ่านแบบไหน?', ['scanning หาตัวเลขหรือสัญลักษณ์เงิน', 'อ่านทุกคำตั้งแต่ต้น', 'อ่านแค่หัวเรื่อง', 'แปลทุกประโยค'], 'scanning เหมาะกับข้อมูลเฉพาะ เช่น ตัวเลข'],
     ['เจอคำที่ไม่รู้ความหมาย ควรทำอย่างไรก่อน?', ['เดาจากคำรอบๆ และบริบท', 'หยุดอ่านทันที', 'ข้ามทั้งย่อหน้า', 'เลือกตอบ A'], 'บริบทมักบอกความหมายคร่าวๆ ได้'],
     ['ทำไมจึงควรอ่านคำถามก่อนอ่านบทความ?', ['รู้ว่าต้องหาข้อมูลอะไร ประหยัดเวลา', 'เพื่อจำคำถามทั้งหมด', 'ไม่จำเป็นต้องอ่านบทความ', 'เพื่อเดาคำตอบ'], 'อ่านอย่างมีเป้าหมายเร็วกว่าอ่านทั้งหมดแล้วค่อยหา'],
     ['ข้อเสียของการแปลทุกคำคืออะไร?', ['ช้า และอาจไม่เข้าใจภาพรวม', 'ทำให้อ่านเร็วขึ้น', 'ทำให้ได้คะแนนเต็ม', 'ไม่มีข้อเสีย'], 'ภาษาอังกฤษควรเข้าใจเป็นวลีและประโยค']]),
 dict(id='write', en='Writing & spelling', th='เทคนิคการเขียนและการสะกด',
  intro='สะกดได้แม่นต้องใช้ทั้งตา หู และมือ ไม่ใช่จำจากเสียงอย่างเดียว',
  r=[['แบ่งคำเป็นก้อน', 'ดูก้อนตัวสะกดสีต่างๆ ในหน้าฝึกสะกด เช่น in-for-ma-tion', []],
     ['รู้กฎที่ช่วยได้', 'Magic E (hop → hope), เติม -ed, -s, เปลี่ยน y เป็น i (easy → easier)', []],
     ['พิมพ์ตามเมื่อสะกดผิด', 'มือจะจำตัวสะกดที่ถูก (เปิดได้ในตั้งค่า)', []],
     ['เขียนประโยคของตัวเอง', 'ใช้คำใหม่ในประโยคที่เกี่ยวกับชีวิตตัวเอง 1–2 ประโยค ช่วยให้จำและใช้เป็น', []],
     ['จดคำที่ชอบผิด', 'เช่น receive (e ก่อน i หลัง c), necessary (c ตัวเดียว s สองตัว) แล้วทบทวนบ่อยๆ', []]],
  q=[['วิธีใดช่วยสะกดคำยาวๆ ได้ง่ายขึ้น?', ['แบ่งคำเป็นก้อน เช่น in-for-ma-tion', 'จำทั้งคำในครั้งเดียว', 'ฟังเสียงอย่างเดียว', 'ดูคำแปลอย่างเดียว'], 'ก้อนเล็กจำง่ายกว่าทั้งคำ'],
     ['คำว่า hop เติม e เป็น hope เพราะกฎอะไร?', ['Magic E ทำให้สระข้างหน้าออกเสียงยาว', 'กฎการเติม -ed', 'กฎพหูพจน์', 'ไม่มีกฎ'], 'e ท้ายคำทำให้ o ออกเสียงยาว'],
     ['easy เปลี่ยนเป็นขั้นกว่าอย่างไร?', ['easier', 'easyer', 'more easy', 'easyier'], 'ลงท้ายพยัญชนะ + y ให้เปลี่ยน y เป็น i แล้วเติม -er'],
     ['ข้อใดสะกดถูก?', ['necessary', 'neccessary', 'necesary', 'neccesary'], 'necessary: c ตัวเดียว s สองตัว'],
     ['ข้อใดสะกดถูก?', ['receive', 'recieve', 'receeve', 'recive'], 'receive: หลัง c ใช้ ei']]),
 dict(id='exam', en='Test strategy', th='เทคนิคการทำข้อสอบ',
  intro='คะแนนไม่ได้ขึ้นกับความรู้อย่างเดียว การใช้เวลาและการเลือกข้อที่จะทำก่อนก็สำคัญ',
  r=[['ไม่มีการหักคะแนนเมื่อตอบผิด', 'ถ้าไม่แน่ใจ ให้ตัดตัวเลือกที่ผิดแล้วเดา ห้ามเว้นว่าง', []],
     ['พาร์ตอ่านมีเวลาจำกัด', 'Part 5 ควรใช้ราว 20–30 วินาทีต่อข้อ เพื่อเหลือเวลาให้ Part 7 ที่ยาวที่สุด', []],
     ['Part 3–4 อ่านคำถามล่วงหน้า', 'ระหว่างที่เสียงอ่านคำถามชุดก่อน ให้อ่านคำถามชุดถัดไป', []],
     ['ข้อที่ใช้เวลามาก ทำทีหลัง', 'เช่น คำถาม NOT ใน Part 7 ต้องตรวจทุกตัวเลือก', []],
     ['ฝึกจับเวลาจริง', 'ใช้โหมดสอบในเมนูข้อสอบ เพื่อให้ชินกับเวลาจริง', []]],
  q=[['ถ้าไม่รู้คำตอบเลย ควรทำอย่างไร?', ['ตัดตัวเลือกที่ผิดแล้วเดา ไม่เว้นว่าง', 'เว้นว่างไว้', 'เลือก A ทุกข้อ', 'ใช้เวลาคิดจนกว่าจะรู้'], 'ข้อสอบไม่หักคะแนนเมื่อตอบผิด การเดาจึงมีแต่ได้'],
     ['Part 5 ควรใช้เวลาต่อข้อประมาณเท่าไร?', ['20–30 วินาที', '3 นาที', '5 วินาที', '1 นาทีครึ่ง'], 'เพื่อเหลือเวลาให้ Part 7'],
     ['ระหว่างที่เสียงอ่านคำถาม Part 3 ชุดก่อน ควรทำอะไร?', ['อ่านคำถามของชุดถัดไป', 'ฟังคำถามซ้ำ', 'แก้คำตอบข้อเก่า', 'พักสายตา'], 'ทำให้รู้ล่วงหน้าว่าชุดต่อไปต้องฟังอะไร'],
     ['คำถาม NOT ใน Part 7 ควรทำเมื่อไร?', ['ทำทีหลัง เพราะต้องตรวจทุกตัวเลือก', 'ทำก่อนเสมอ', 'ข้ามไม่ต้องทำ', 'ทำพร้อมฟังเสียง'], 'ข้อที่ใช้เวลามากควรเก็บไว้ทำหลังข้อที่ทำได้เร็ว'],
     ['วิธีใดช่วยให้ชินกับเวลาสอบจริง?', ['ฝึกด้วยโหมดจับเวลา', 'ทำทีละข้อแบบไม่จำกัดเวลาเท่านั้น', 'อ่านเฉลยอย่างเดียว', 'ไม่ต้องฝึก'], 'การจับเวลาทำให้รู้จังหวะของตัวเอง']]),
]

def build(lessons, prefix, seed, extra=None, more=None, groups=None):
    """Option order comes from one seeded stream in a fixed order (first lessons, then added questions, then new lessons),
    so questions that already existed keep their letters and saved answers stay valid."""
    rnd = random.Random(seed); K = 'ABCD'; byid = {}
    def make(L, qs, start):
        items = []
        for i, (s, opts, x) in enumerate(qs, start):
            order = list(range(4)); rnd.shuffle(order)
            o = {K[j]: opts[k] for j, k in enumerate(order)}
            items.append(dict(id='%s-%s-%d' % (prefix, L['id'], i), p=0, s=s, gap=1 if '_____' in s else 0, o=o, oth={}, a=K[order.index(0)], x=x, v=[]))
        return items
    for L in lessons: byid[L['id']] = dict(id=L['id'], en=L['en'], th=L['th'], intro=L['intro'], r=L['r'], tips=[], items=make(L, L['q'], 0))
    for lid, qs in (extra or {}).items(): byid[lid]['items'] += make(byid[lid], qs, len(byid[lid]['items']))
    for L in (more or []): byid[L['id']] = dict(id=L['id'], en=L['en'], th=L['th'], intro=L['intro'], r=L['r'], tips=[], items=make(L, L['q'], 0))
    if not groups: return list(byid.values())
    out = []
    for g, ids in groups:
        for lid in ids: L = byid.pop(lid); L['grp'] = g; out.append(L)
    assert not byid, 'lessons left out of the groups: %r' % list(byid)
    return out

def write(key, lessons):
    js = '(window.__X=window.__X||{})["%s"]=' % key + json.dumps({'v': 1, 'lessons': lessons}, ensure_ascii=False, separators=(',', ':')) + ';\n'
    open(os.path.join(D, key + '.js'), 'w', encoding='utf-8').write(js)
    print(key, len(lessons), 'lessons', sum(len(L['items']) for L in lessons), 'questions')

if __name__ == '__main__':
    import basic_more as M
    write('xbasic', build(BASIC, 'bg', 7, M.EXTRA, M.NEW, M.GROUPS))
    write('xtips', build(TIPS, 'tp', 8))
