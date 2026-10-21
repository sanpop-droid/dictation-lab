"""Build exam/data/xmind.js: mind-map lessons (แผนผังคำ).

Four groups of 8 maps + a one-page grammar summary. The app draws every map from `mm` (no HTML stored here):
  mm = { k:'pv'|'fam'|'cmp'|'topic', root, rt (Thai), em (emoji), b:[ {w, t, e, x?, xt?, g?} ] }
    pv    — phrasal verbs: b.w is the particle; the full verb is root + ' ' + w
    fam   — words that end with the same sound: root like '-ed'; the shared ending is highlighted
    cmp   — compound words: the root word is highlighted inside each branch
    topic — words by topic: b.g is the sub-branch (group) name
Each map gets one "fill the missing branch" question per branch: the map is shown with that branch hidden.
Option order comes from a seeded random stream, so the letters stay the same when the file is rebuilt.
Run:  python3 tools/build_mind.py
"""
import json, os, random
from examdata import D

PV = [
 ('take', 'เอา หยิบ', '✋', [
  ('after', 'หน้าตาหรือนิสัยเหมือน (พ่อแม่)', '👨‍👧', 'She takes after her mother.', 'เธอหน้าตาเหมือนแม่'),
  ('off', 'ถอด (เสื้อ รองเท้า) / เครื่องบินขึ้น', '👟', 'Please take off your shoes.', 'กรุณาถอดรองเท้า'),
  ('over', 'รับช่วงต่อ เข้าควบคุม', '🧑‍💼', 'Ken will take over the project next month.', 'เคนจะรับช่วงดูแลโครงการเดือนหน้า'),
  ('up', 'เริ่มทำ (งานอดิเรก)', '🧘', 'I took up yoga last year.', 'ฉันเริ่มเล่นโยคะเมื่อปีที่แล้ว'),
  ('back', 'ถอนคำพูด / คืนของ', '↩️', 'I take back what I said.', 'ฉันขอถอนคำพูด'),
  ('on', 'รับ (งาน หน้าที่) มาทำ', '📋', 'She took on extra work this week.', 'สัปดาห์นี้เธอรับงานเพิ่ม'),
  ('out', 'เอาออกมา / พาไปเที่ยว', '🍽️', 'He took his kids out for dinner.', 'เขาพาลูกไปกินข้าวนอกบ้าน')]),
 ('get', 'ได้ ไป ถึง', '🏃', [
  ('up', 'ตื่นนอน ลุกขึ้น', '⏰', 'I get up at six every day.', 'ฉันตื่นหกโมงทุกวัน'),
  ('on', 'ขึ้น (รถเมล์ รถไฟ เครื่องบิน)', '🚌', 'Get on the bus here.', 'ขึ้นรถเมล์ที่นี่'),
  ('off', 'ลง (จากรถ)', '🚏', 'Get off at the next stop.', 'ลงป้ายหน้า'),
  ('along', 'เข้ากันได้ดี (with ใคร)', '🤝', 'I get along with my coworkers.', 'ฉันเข้ากับเพื่อนร่วมงานได้ดี'),
  ('over', 'หายจาก (ไข้) / ทำใจได้', '💪', 'She got over her cold quickly.', 'เธอหายหวัดเร็ว'),
  ('back', 'กลับมา', '🏠', 'When did you get back?', 'คุณกลับมาเมื่อไร'),
  ('through', 'ติดต่อ (ทางโทรศัพท์) ได้ / ผ่านพ้น', '📞', "I couldn't get through to the office.", 'ฉันโทรติดต่อออฟฟิศไม่ได้')]),
 ('look', 'มอง ดู', '👀', [
  ('for', 'หา', '🔍', "I'm looking for my keys.", 'ฉันกำลังหากุญแจ'),
  ('after', 'ดูแล', '🐶', 'Who looks after your dog?', 'ใครดูแลหมาของคุณ'),
  ('up', 'เปิดหา (คำศัพท์ ข้อมูล)', '📖', 'Look up the word in a dictionary.', 'เปิดหาคำนี้ในพจนานุกรม'),
  ('forward to', 'ตั้งตารอ', '🤩', 'I look forward to meeting you.', 'ฉันตั้งตารอที่จะได้พบคุณ'),
  ('into', 'ตรวจสอบ สืบดู', '🕵️', 'We will look into the problem.', 'เราจะตรวจสอบปัญหานี้'),
  ('out', 'ระวัง!', '⚠️', 'Look out! A car is coming.', 'ระวัง! รถมา'),
  ('over', 'ตรวจดูคร่าวๆ', '📝', 'Please look over this report.', 'ช่วยตรวจดูรายงานนี้หน่อย')]),
 ('put', 'วาง ใส่', '📦', [
  ('on', 'สวมใส่', '🧥', 'Put on your jacket.', 'ใส่แจ็กเก็ตสิ'),
  ('off', 'เลื่อนออกไป', '📅', 'They put off the meeting until Friday.', 'พวกเขาเลื่อนประชุมไปวันศุกร์'),
  ('away', 'เก็บเข้าที่', '🧸', 'Put away your toys.', 'เก็บของเล่นเข้าที่'),
  ('out', 'ดับ (ไฟ)', '🧯', 'Firefighters put out the fire.', 'นักดับเพลิงดับไฟ'),
  ('up with', 'อดทนกับ', '😤', "I can't put up with the noise.", 'ฉันทนเสียงดังไม่ไหว'),
  ('together', 'ประกอบ รวบรวม', '🧩', "Let's put together a plan.", 'มาร่วมกันวางแผนกันเถอะ'),
  ('down', 'วางลง / จดลง', '✍️', 'Put down your pens.', 'วางปากกาลง')]),
 ('turn', 'หมุน เลี้ยว', '🔄', [
  ('on', 'เปิด (ไฟ เครื่อง)', '💡', 'Turn on the light, please.', 'ช่วยเปิดไฟหน่อย'),
  ('off', 'ปิด (ไฟ เครื่อง)', '📴', 'Turn off your phone.', 'ปิดโทรศัพท์ของคุณ'),
  ('up', 'เพิ่ม (เสียง) / โผล่มา', '🔊', 'Turn up the volume.', 'เพิ่มเสียงหน่อย'),
  ('down', 'ลด (เสียง) / ปฏิเสธ', '🙅', 'She turned down the job offer.', 'เธอปฏิเสธข้อเสนองาน'),
  ('into', 'กลายเป็น', '🦋', 'The rain turned into snow.', 'ฝนกลายเป็นหิมะ'),
  ('around', 'หันกลับ', '↪️', 'Turn around and look behind you.', 'หันกลับไปดูข้างหลัง'),
  ('in', 'ส่ง (งาน)', '📤', 'Turn in your report by Friday.', 'ส่งรายงานภายในวันศุกร์')]),
 ('give', 'ให้', '🎁', [
  ('up', 'เลิก ยอมแพ้', '🏳️', "Don't give up!", 'อย่ายอมแพ้'),
  ('back', 'คืน', '🔁', 'Please give back my pen.', 'ช่วยคืนปากกาให้ฉันหน่อย'),
  ('away', 'แจกฟรี', '🆓', 'They gave away free samples.', 'พวกเขาแจกสินค้าตัวอย่างฟรี'),
  ('out', 'แจกจ่าย (ให้ทุกคน)', '📄', 'The teacher gave out the tests.', 'ครูแจกข้อสอบ'),
  ('in', 'ยอมตาม', '🙇', 'He finally gave in.', 'ในที่สุดเขาก็ยอม'),
  ('off', 'ปล่อย (กลิ่น ความร้อน) ออกมา', '🌸', 'The flowers give off a sweet smell.', 'ดอกไม้ส่งกลิ่นหอม')]),
 ('come', 'มา', '🚶', [
  ('back', 'กลับมา', '🔙', 'Come back soon!', 'กลับมาเร็วๆ นะ'),
  ('in', 'เข้ามา', '🚪', 'Please come in.', 'เชิญเข้ามา'),
  ('up with', 'คิด (ไอเดีย) ออก', '💡', 'She came up with a great idea.', 'เธอคิดไอเดียดีๆ ออก'),
  ('across', 'บังเอิญเจอ', '🖼️', 'I came across an old photo.', 'ฉันบังเอิญเจอรูปเก่า'),
  ('from', 'มาจาก (ประเทศ เมือง)', '🌏', 'I come from Thailand.', 'ฉันมาจากประเทศไทย'),
  ('down with', 'ล้มป่วยเป็น', '🤒', 'He came down with a cold.', 'เขาเป็นหวัด'),
  ('over', 'แวะมา (บ้าน)', '🏡', 'Come over for dinner tonight.', 'คืนนี้แวะมากินข้าวที่บ้านสิ')]),
 ('go', 'ไป', '➡️', [
  ('on', 'ทำต่อ / เกิดขึ้น', '▶️', 'Please go on with your story.', 'เล่าต่อเลย'),
  ('out', 'ออกไปข้างนอก / (ไฟ) ดับ', '🌃', "Let's go out tonight.", 'คืนนี้ออกไปข้างนอกกัน'),
  ('back', 'กลับไป', '🏘️', 'I want to go back home.', 'ฉันอยากกลับบ้าน'),
  ('over', 'ทบทวน ตรวจดูอีกรอบ', '🔁', "Let's go over the plan again.", 'มาทบทวนแผนอีกรอบ'),
  ('through', 'ผ่าน (เรื่องยาก) / ตรวจดูละเอียด', '⛰️', 'She went through a hard time.', 'เธอผ่านช่วงเวลาที่ยากลำบาก'),
  ('up', 'ขึ้น เพิ่มขึ้น', '📈', 'Prices went up again.', 'ราคาขึ้นอีกแล้ว'),
  ('down', 'ลดลง', '📉', 'Sales went down last month.', 'ยอดขายลดลงเมื่อเดือนที่แล้ว')]),
]

FAM = [
 ('-at', 'เสียง "แอท"', '🐱', [('cat', 'แมว', '🐱'), ('hat', 'หมวก', '🎩'), ('bat', 'ค้างคาว / ไม้ตี', '🦇'), ('rat', 'หนู', '🐀'), ('chat', 'คุยเล่น', '💬'), ('flat', 'แบน / ห้องชุด', '🏢'), ('that', 'นั่น', '👉')]),
 ('-ed', 'เสียง "เอ็ด"', '🛏️', [('bed', 'เตียง', '🛏️'), ('red', 'สีแดง', '🔴'), ('fed', 'ให้อาหาร (อดีตของ feed)', '🍼'), ('sled', 'เลื่อนหิมะ', '🛷'), ('shed', 'โรงเก็บของ', '🛖'), ('wed', 'แต่งงาน', '💍'), ('led', 'นำ (อดีตของ lead)', '🚩')]),
 ('-ee', 'เสียง "อี" ยาว', '🌳', [('see', 'เห็น', '👀'), ('tree', 'ต้นไม้', '🌳'), ('bee', 'ผึ้ง', '🐝'), ('free', 'ฟรี / อิสระ', '🆓'), ('three', 'สาม', '3️⃣'), ('knee', 'เข่า (k ไม่ออกเสียง)', '🦵'), ('agree', 'เห็นด้วย', '👍')]),
 ('-ay', 'เสียง "เอ"', '☀️', [('day', 'วัน', '☀️'), ('play', 'เล่น', '🎮'), ('pay', 'จ่าย', '💳'), ('say', 'พูด', '🗣️'), ('stay', 'พัก อยู่', '🏨'), ('way', 'ทาง วิธี', '🛣️'), ('tray', 'ถาด', '🍽️')]),
 ('-ight', 'เสียง "ไอท์" (gh ไม่ออกเสียง)', '🌙', [('night', 'กลางคืน', '🌙'), ('light', 'แสง ไฟ', '💡'), ('right', 'ถูก / ขวา', '✅'), ('flight', 'เที่ยวบิน', '✈️'), ('bright', 'สว่าง', '🔆'), ('fight', 'ต่อสู้', '🥊'), ('sight', 'การมองเห็น', '👁️')]),
 ('-ake', 'เสียง "เอค"', '🎂', [('cake', 'เค้ก', '🎂'), ('lake', 'ทะเลสาบ', '🏞️'), ('make', 'ทำ สร้าง', '🛠️'), ('snake', 'งู', '🐍'), ('wake', 'ตื่น', '⏰'), ('bake', 'อบ', '🥖'), ('mistake', 'ข้อผิดพลาด', '❌')]),
 ('-ook', 'เสียง "อุค" สั้น', '📖', [('book', 'หนังสือ', '📖'), ('cook', 'ทำอาหาร', '👨‍🍳'), ('look', 'มอง', '👀'), ('hook', 'ตะขอ', '🪝'), ('took', 'เอาไป (อดีตของ take)', '✋'), ('shook', 'เขย่า (อดีตของ shake)', '🤝'), ('notebook', 'สมุด', '📓')]),
 ('-ing', 'เสียง "อิง"', '💍', [('ring', 'แหวน / เสียงกริ่ง', '💍'), ('king', 'กษัตริย์', '👑'), ('sing', 'ร้องเพลง', '🎤'), ('wing', 'ปีก', '🪽'), ('spring', 'ฤดูใบไม้ผลิ', '🌸'), ('swing', 'ชิงช้า', '🛝'), ('thing', 'สิ่งของ', '📦')]),
]

CMP = [
 ('fire', 'ไฟ', '🔥', [('fireman', 'พนักงานดับเพลิง', '🧑‍🚒'), ('firework', 'ดอกไม้ไฟ', '🎆'), ('fireplace', 'เตาผิง', '🏠'), ('campfire', 'กองไฟ', '🏕️'), ('firefly', 'หิ่งห้อย', '✨'), ('fire alarm', 'สัญญาณเตือนไฟไหม้', '🚨'), ('fire exit', 'ทางหนีไฟ', '🚪')]),
 ('foot', 'เท้า', '🦶', [('football', 'ฟุตบอล', '⚽'), ('footprint', 'รอยเท้า', '👣'), ('footpath', 'ทางเดินเท้า', '🚶'), ('footstep', 'ก้าวเท้า เสียงฝีเท้า', '👞'), ('barefoot', 'เท้าเปล่า', '🦶'), ('footnote', 'เชิงอรรถ (หมายเหตุท้ายหน้า)', '📝')]),
 ('sun', 'ดวงอาทิตย์', '☀️', [('sunlight', 'แสงแดด', '🌞'), ('sunglasses', 'แว่นกันแดด', '🕶️'), ('sunrise', 'พระอาทิตย์ขึ้น', '🌅'), ('sunset', 'พระอาทิตย์ตก', '🌇'), ('sunflower', 'ดอกทานตะวัน', '🌻'), ('sunscreen', 'ครีมกันแดด', '🧴'), ('sunburn', 'ผิวไหม้แดด', '🥵')]),
 ('book', 'หนังสือ', '📚', [('bookshelf', 'ชั้นวางหนังสือ', '📚'), ('bookstore', 'ร้านหนังสือ', '🏪'), ('notebook', 'สมุด', '📓'), ('textbook', 'หนังสือเรียน', '📘'), ('guidebook', 'หนังสือนำเที่ยว', '🗺️'), ('bookmark', 'ที่คั่นหนังสือ', '🔖')]),
 ('home', 'บ้าน', '🏡', [('homework', 'การบ้าน', '📝'), ('homepage', 'หน้าแรกของเว็บไซต์', '🌐'), ('hometown', 'บ้านเกิด', '🏘️'), ('homemade', 'ทำเองที่บ้าน', '🍪'), ('homesick', 'คิดถึงบ้าน', '😢'), ('homeless', 'ไร้บ้าน', '🥺')]),
 ('rain', 'ฝน', '🌧️', [('rainbow', 'รุ้ง', '🌈'), ('raincoat', 'เสื้อกันฝน', '🧥'), ('raindrop', 'หยดฝน', '💧'), ('rainfall', 'ปริมาณฝน', '🌧️'), ('rainforest', 'ป่าฝน', '🌳'), ('rainy season', 'ฤดูฝน', '☔')]),
 ('water', 'น้ำ', '💧', [('waterfall', 'น้ำตก', '🏞️'), ('watermelon', 'แตงโม', '🍉'), ('waterproof', 'กันน้ำ', '☂️'), ('underwater', 'ใต้น้ำ', '🤿'), ('saltwater', 'น้ำเค็ม', '🌊'), ('water bottle', 'ขวดน้ำ', '🍶')]),
 ('air', 'อากาศ', '💨', [('airport', 'สนามบิน', '🛫'), ('airplane', 'เครื่องบิน', '✈️'), ('airline', 'สายการบิน', '🛩️'), ('air conditioner', 'เครื่องปรับอากาศ', '❄️'), ('airmail', 'ไปรษณีย์ทางอากาศ', '📮'), ('aircraft', 'อากาศยาน', '🚁')]),
]

TOPIC = [
 ('Office', 'ที่ทำงาน', '🏢', [
  ('คน', [('manager', 'ผู้จัดการ', '👔'), ('colleague', 'เพื่อนร่วมงาน', '🧑‍🤝‍🧑'), ('receptionist', 'พนักงานต้อนรับ', '🛎️')]),
  ('ของ', [('printer', 'เครื่องพิมพ์', '🖨️'), ('folder', 'แฟ้ม', '📁'), ('stapler', 'ที่เย็บกระดาษ', '📎')]),
  ('งาน', [('schedule', 'ตารางงาน', '🗓️'), ('deadline', 'กำหนดส่ง', '⏳'), ('report', 'รายงาน', '📊')])]),
 ('Airport', 'สนามบิน', '🛫', [
  ('สถานที่', [('gate', 'ประตูขึ้นเครื่อง', '🚪'), ('terminal', 'อาคารผู้โดยสาร', '🏢'), ('runway', 'ทางวิ่งเครื่องบิน', '🛬')]),
  ('เอกสาร', [('passport', 'หนังสือเดินทาง', '🛂'), ('boarding pass', 'บัตรขึ้นเครื่อง', '🎫'), ('ticket', 'ตั๋ว', '🎟️')]),
  ('การเดินทาง', [('luggage', 'กระเป๋าเดินทาง', '🧳'), ('flight', 'เที่ยวบิน', '✈️'), ('delay', 'ความล่าช้า', '⏱️')])]),
 ('Hotel', 'โรงแรม', '🏨', [
  ('จุดบริการ', [('front desk', 'แผนกต้อนรับ', '🛎️'), ('lobby', 'ล็อบบี้', '🛋️'), ('reservation', 'การจอง', '📝')]),
  ('ห้องพัก', [('single room', 'ห้องเตียงเดี่ยว', '🛏️'), ('room service', 'บริการส่งอาหารถึงห้อง', '🍽️'), ('key card', 'คีย์การ์ด', '🔑')]),
  ('การเข้าพัก', [('check in', 'ลงทะเบียนเข้าพัก', '✅'), ('check out', 'แจ้งออกจากที่พัก', '🧳'), ('guest', 'แขก', '🧑')])]),
 ('Restaurant', 'ร้านอาหาร', '🍽️', [
  ('คน', [('waiter', 'พนักงานเสิร์ฟ', '🤵'), ('chef', 'พ่อครัว', '👨‍🍳'), ('customer', 'ลูกค้า', '🧑')]),
  ('อาหาร', [('appetizer', 'อาหารเรียกน้ำย่อย', '🥗'), ('main course', 'อาหารจานหลัก', '🍝'), ('dessert', 'ของหวาน', '🍰')]),
  ('การจ่าย', [('menu', 'เมนู', '📋'), ('bill', 'บิลค่าอาหาร', '🧾'), ('tip', 'ทิป', '💵')])]),
 ('School', 'โรงเรียน', '🏫', [
  ('คน', [('teacher', 'ครู', '👩‍🏫'), ('student', 'นักเรียน', '🧑‍🎓'), ('principal', 'ครูใหญ่', '👨‍💼')]),
  ('วิชา', [('math', 'คณิตศาสตร์', '➗'), ('science', 'วิทยาศาสตร์', '🔬'), ('history', 'ประวัติศาสตร์', '📜')]),
  ('ในห้องเรียน', [('classroom', 'ห้องเรียน', '🏫'), ('homework', 'การบ้าน', '📝'), ('exam', 'การสอบ', '✏️')])]),
 ('Beach', 'ชายหาด', '🏖️', [
  ('ธรรมชาติ', [('sand', 'ทราย', '🏝️'), ('wave', 'คลื่น', '🌊'), ('shell', 'เปลือกหอย', '🐚')]),
  ('กิจกรรม', [('swimming', 'ว่ายน้ำ', '🏊'), ('surfing', 'โต้คลื่น', '🏄'), ('sunbathing', 'อาบแดด', '🌞')]),
  ('ของที่พกไป', [('sunscreen', 'ครีมกันแดด', '🧴'), ('umbrella', 'ร่ม', '⛱️'), ('flip-flops', 'รองเท้าแตะ', '🩴')])]),
 ('Hospital', 'โรงพยาบาล', '🏥', [
  ('คน', [('doctor', 'หมอ', '🧑‍⚕️'), ('nurse', 'พยาบาล', '👩‍⚕️'), ('patient', 'ผู้ป่วย', '🛌')]),
  ('สถานที่', [('emergency room', 'ห้องฉุกเฉิน', '🚑'), ('pharmacy', 'ร้านขายยา ห้องยา', '💊'), ('waiting room', 'ห้องรอ', '🪑')]),
  ('เอกสารและยา', [('appointment', 'การนัดหมาย', '📅'), ('prescription', 'ใบสั่งยา', '📄'), ('medicine', 'ยา', '💊')])]),
 ('Shopping', 'การซื้อของ', '🛍️', [
  ('สถานที่', [('mall', 'ห้างสรรพสินค้า', '🏬'), ('supermarket', 'ซูเปอร์มาร์เก็ต', '🛒'), ('market', 'ตลาด', '🧺')]),
  ('เงิน', [('price', 'ราคา', '🏷️'), ('discount', 'ส่วนลด', '🔖'), ('receipt', 'ใบเสร็จ', '🧾')]),
  ('บริการ', [('cashier', 'พนักงานเก็บเงิน', '💁'), ('refund', 'การคืนเงิน', '💸'), ('delivery', 'การจัดส่ง', '🚚')])]),
]

GROUPS = {
 'pv': ('ก. ต้นไม้ phrasal verb',
        ('กริยาตัวเดียว เช่น take พอมีคำเล็กๆ (after, off, up…) มาต่อท้าย ความหมายจะเปลี่ยนไปเลย แผนผังนี้วาง take ไว้ตรงกลาง แล้วแตกกิ่งออกไปทีละคำ เห็นภาพรวมทีเดียวทั้งต้น จำง่ายกว่าท่องทีละคำ',
         ('Please <b>take off</b> your shoes.', 'กรุณาถอดรองเท้า'), 'กริยาตรงกลาง + คำเล็กที่กิ่ง = ความหมายใหม่ จำเป็นคู่')),
 'fam': ('ข. วงล้อเสียงท้ายเหมือนกัน',
         ('คำในวงเดียวกันลงท้ายด้วยเสียงเดียวกัน เปลี่ยนแค่เสียงข้างหน้า ถ้าอ่านคำหนึ่งออก ก็อ่านคำที่เหลือในวงออกได้เอง ไม่ต้องจำคำอ่านทีละคำ',
          ('c<b>at</b> · h<b>at</b> · b<b>at</b>', 'เสียงท้าย -at เหมือนกัน เปลี่ยนแค่เสียงหน้า'), 'อ่านส่วนท้ายให้ได้ 1 ครั้ง แล้วเปลี่ยนแค่เสียงหน้า')),
 'cmp': ('ค. วงล้อคำประสม',
         ('คำยาวๆ หลายคำเกิดจากคำสั้นสองคำมาต่อกัน เช่น fire (ไฟ) + man (คน) = fireman (พนักงานดับเพลิง) ถ้ารู้คำตรงกลางวง ก็เดาความหมายคำยาวได้',
          ('<b>fire</b>man · camp<b>fire</b> · <b>fire</b>work', 'คนดับไฟ · กองไฟ · ดอกไม้ไฟ'), 'แยกคำยาวเป็น 2 คำสั้น แล้วรวมความหมาย')),
 'topic': ('ง. แผนผังคำตามหัวข้อ',
           ('จัดคำศัพท์ที่อยู่ในสถานที่เดียวกันไว้ด้วยกัน แบ่งเป็นกิ่งย่อย เช่น คน ของ และสิ่งที่ทำ เวลาเจอสถานการณ์จริง สมองจะดึงคำทั้งกลุ่มออกมาพร้อมกัน หัวข้อเหล่านี้ออกสอบ TOEIC บ่อย',
            ('At the <b>airport</b>: <b>gate</b>, <b>passport</b>, <b>luggage</b>', 'ที่สนามบิน: ประตูขึ้นเครื่อง หนังสือเดินทาง กระเป๋า'), 'นึกถึงสถานที่ → แตกกิ่ง คน / ของ / สิ่งที่ทำ')),
}

def opts(rnd, right, pool):
    others = [x for x in pool if x != right]
    o = [right] + rnd.sample(others, 3); rnd.shuffle(o)
    K = 'ABCD'; return {K[i]: v for i, v in enumerate(o)}, K[o.index(right)]

def lesson(k, slug, root, rt, em, branches, rnd, en, th):
    gname, (say, eg, rule) = GROUPS[k]
    words = [b['w'] for b in branches]
    items = []
    for i, b in enumerate(branches):
        o, a = opts(rnd, b['w'], words)
        if k == 'pv':
            s = 'กิ่งที่หายไปคือคำไหน: %s ___ = %s' % (root, b['t']); summ = '%s %s = %s' % (root, b['w'], b['t'])
            x = '%s %s แปลว่า %s เช่น %s (%s)' % (root, b['w'], b['t'], b['x'], b['xt'])
        elif k == 'fam':
            s = 'กิ่งที่หายไปคือคำไหน: %s %s (ลงท้าย %s)' % (b['e'], b['t'], root); summ = '%s = %s' % (b['w'], b['t'])
            x = '%s แปลว่า %s ลงท้ายด้วย %s เหมือนทุกคำในวง' % (b['w'], b['t'], root)
        elif k == 'cmp':
            s = 'กิ่งที่หายไปคือคำไหน: %s %s' % (b['e'], b['t']); summ = '%s = %s' % (b['w'], b['t'])
            x = '%s แปลว่า %s มีคำว่า %s (%s) อยู่ในคำ' % (b['w'], b['t'], root, rt)
        else:
            s = 'กิ่งที่หายไปคือคำไหน: %s %s (กิ่ง %s)' % (b['e'], b['t'], b['g']); summ = '%s = %s' % (b['w'], b['t'])
            x = '%s แปลว่า %s อยู่ในกิ่ง "%s" ของหัวข้อ %s' % (b['w'], b['t'], b['g'], root)
        items.append(dict(id='mm-%s-%d' % (slug, i), p=0, mm=i, s=s, o=o, oth={}, a=a, x=x, v=[], sum=summ))
    return dict(id='mm-' + slug, en=en, th=th, grp=gname, intro='', html='', r=[], tips=[],
                mm=dict(k=k, root=root, rt=rt, em=em, b=branches), easy=dict(say=say, eg=list(eg), rule=rule), items=items)

def grammar_page(rnd):
    T = [('ปัจจุบัน (ทำเป็นประจำ)', 'Present Simple', 'always, usually, often, sometimes, never, every day, once a week'),
         ('กำลังทำอยู่ตอนนี้', 'Present Continuous', 'now, right now, at the moment, Look! / Listen!'),
         ('อดีต (จบแล้ว)', 'Past Simple', 'yesterday, last night, last week, two days ago, in 2020'),
         ('ทำมาจนถึงตอนนี้', 'Present Perfect', 'already, yet, just, ever, since 2020, for three years'),
         ('อนาคต', 'Future (will / be going to)', 'tomorrow, next week, soon, in two days, later')]
    P = [('I', 'me', 'my', 'mine', 'myself', 'ฉัน'), ('you', 'you', 'your', 'yours', 'yourself', 'คุณ'), ('he', 'him', 'his', 'his', 'himself', 'เขา (ชาย)'),
         ('she', 'her', 'her', 'hers', 'herself', 'เธอ'), ('it', 'it', 'its', '–', 'itself', 'มัน'), ('we', 'us', 'our', 'ours', 'ourselves', 'เรา'), ('they', 'them', 'their', 'theirs', 'themselves', 'พวกเขา')]
    Q = [('who', 'ใคร'), ('whom', 'ใคร (เป็นผู้ถูกกระทำ)'), ('whose', 'ของใคร'), ('what', 'อะไร'), ('which', 'อันไหน'), ('where', 'ที่ไหน'),
         ('when', 'เมื่อไร'), ('why', 'ทำไม'), ('how', 'อย่างไร'), ('how many', 'กี่ (ของนับได้)'), ('how much', 'เท่าไร (ราคา ของนับไม่ได้)'), ('how long', 'นานเท่าไร ยาวเท่าไร'),
         ('how often', 'บ่อยแค่ไหน'), ('how far', 'ไกลแค่ไหน'), ('how old', 'อายุเท่าไร'), ('what time', 'กี่โมง'), ('what kind of', 'แบบไหน ประเภทไหน'), ('how about', '…ล่ะ (ชวน เสนอ)')]
    h = ['<h3 class="bv-h">1. คำบอกเวลา → ใช้ tense ไหน</h3><div class="mm-sheet"><table class="mm-tbl"><tr><th>เวลา</th><th>tense</th><th>คำที่เห็นแล้วนึกถึง</th></tr>']
    h += ['<tr><td>%s</td><td>%s</td><td lang="en">%s</td></tr>' % r for r in T]
    h.append('</table></div><h3 class="bv-h">2. สรรพนาม 5 รูป</h3><div class="mm-sheet"><table class="mm-tbl"><tr><th>หน้ากริยา</th><th>หลังกริยา</th><th>ของ… + คำนาม</th><th>ของ… (ไม่มีคำนามตาม)</th><th>ตัว…เอง</th><th>แปล</th></tr>')
    h += ['<tr>%s<td>%s</td></tr>' % (''.join('<td lang="en">%s</td>' % c for c in r[:5]), r[5]) for r in P]
    h.append('</table></div><p class="mm-note">ตัวอย่าง: <b>She</b> called <b>me</b>. This is <b>my</b> bag. The bag is <b>mine</b>. I did it <b>myself</b>.</p>')
    h.append('<h3 class="bv-h">3. คำถาม 18 คำ</h3><div class="mm-qgrid">' + ''.join('<span><b lang="en">%s</b>%s</span>' % q for q in Q) + '</div>')
    raw = [('yesterday บอกว่าควรใช้ tense ไหน', 'Past Simple', ['Present Simple', 'Future (will)', 'Present Perfect'], 'yesterday = เมื่อวาน เป็นอดีตที่จบแล้ว ใช้ Past Simple'),
           ('every day บอกว่าควรใช้ tense ไหน', 'Present Simple', ['Past Simple', 'Present Continuous', 'Future (will)'], 'every day = ทุกวัน เป็นเรื่องที่ทำประจำ ใช้ Present Simple'),
           ('right now บอกว่าควรใช้ tense ไหน', 'Present Continuous', ['Present Simple', 'Past Simple', 'Present Perfect'], 'right now = ตอนนี้เลย กำลังทำอยู่ ใช้ Present Continuous'),
           ('since 2020 บอกว่าควรใช้ tense ไหน', 'Present Perfect', ['Past Simple', 'Present Simple', 'Future (will)'], 'since = ตั้งแต่ ทำมาจนถึงตอนนี้ ใช้ Present Perfect'),
           ('next week บอกว่าควรใช้ tense ไหน', 'Future (will)', ['Past Simple', 'Present Perfect', 'Present Continuous'], 'next week = สัปดาห์หน้า เป็นอนาคต'),
           ('He called ___ yesterday. (ฉัน, หลังกริยา)', 'me', ['I', 'my', 'mine'], 'หลังกริยาใช้รูป me'),
           ('This is ___ car. (ของเธอ + คำนาม)', 'her', ['she', 'hers', 'herself'], 'มีคำนาม car ตามหลัง ใช้ her'),
           ('The phone is ___. (ของพวกเขา ไม่มีคำนามตาม)', 'theirs', ['their', 'them', 'they'], 'ไม่มีคำนามตามหลัง ใช้ theirs'),
           ('___ is your birthday? (เมื่อไร)', 'When', ['Where', 'Who', 'Why'], 'when = เมื่อไร'),
           ('___ does this bag cost? (ราคาเท่าไร)', 'How much', ['How many', 'How long', 'How often'], 'ถามราคาใช้ how much'),
           ('___ do you go to the gym? (บ่อยแค่ไหน)', 'How often', ['How long', 'How far', 'How much'], 'how often = บ่อยแค่ไหน'),
           ('___ pen is this? (ของใคร)', 'Whose', ['Who', 'Which', 'Whom'], 'whose = ของใคร')]
    items = []
    for i, (s, right, wrong, x) in enumerate(raw):
        o = [right] + wrong; rnd.shuffle(o); K = 'ABCD'
        items.append(dict(id='mm-gram-%d' % i, p=0, s=s, o={K[j]: v for j, v in enumerate(o)}, oth={}, a=K[o.index(right)], x=x, v=[]))
    return dict(id='mm-gram', en='Grammar on one page', th='สรุปไวยากรณ์ 1 หน้า', grp='จ. สรุปไวยากรณ์ 1 หน้า', intro='เปิดดูก่อนสอบหรือก่อนทำแบบฝึก',
                html=''.join(h), r=[], tips=[], easy=dict(say='หน้านี้รวม 3 อย่างที่ใช้บ่อยที่สุดไว้ในที่เดียว: คำบอกเวลาที่บอกว่าต้องใช้ tense ไหน, สรรพนาม 5 รูป และคำถาม 18 คำ ไม่ต้องจำทั้งหมดในครั้งเดียว ใช้เปิดดูเวลาทำข้อสอบแล้วไม่แน่ใจ',
                eg=['<b>Yesterday</b> I <b>went</b> to work.', 'เห็น yesterday → ใช้กริยาอดีต'], rule='เห็นคำบอกเวลา → รู้ tense · ดูตำแหน่ง → รู้รูปสรรพนาม'), items=items)

def main():
    rnd = random.Random(35); out = []
    for root, rt, em, bs in PV:
        out.append(lesson('pv', 'pv-' + root, root, rt, em, [dict(w=w, t=t, e=e, x=x, xt=xt) for w, t, e, x, xt in bs], rnd, root + ' + …', root + ' (' + rt + ')'))
    for root, rt, em, bs in FAM:
        out.append(lesson('fam', 'fam-' + root.strip('-'), root, rt, em, [dict(w=w, t=t, e=e) for w, t, e in bs], rnd, 'Words ending in ' + root, 'คำลงท้าย ' + root))
    for root, rt, em, bs in CMP:
        out.append(lesson('cmp', 'cmp-' + root, root, rt, em, [dict(w=w, t=t, e=e) for w, t, e in bs], rnd, root + ' + …', 'คำประสมกับ ' + root + ' (' + rt + ')'))
    for root, rt, em, gs in TOPIC:
        out.append(lesson('topic', 'topic-' + root.lower(), root, rt, em, [dict(w=w, t=t, e=e, g=g) for g, ws in gs for w, t, e in ws], rnd, root, rt))
    out.append(grammar_page(rnd))
    ids = [it['id'] for L in out for it in L['items']]; assert len(ids) == len(set(ids))
    for L in out:
        for it in L['items']: assert len(set(it['o'].values())) == len(it['o']), it['id']
    js = '(window.__X=window.__X||{})["xmind"]=' + json.dumps({'v': 1, 'lessons': out}, ensure_ascii=False, separators=(',', ':')) + ';\n'
    open(os.path.join(D, 'xmind.js'), 'w', encoding='utf-8').write(js)
    print(len(out), 'lessons', len(ids), 'questions', len(js.encode()), 'bytes')

if __name__ == '__main__':
    main()
