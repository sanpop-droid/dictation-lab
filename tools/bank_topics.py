"""Topic map for every word in the word bank (คลังคำ): used by tools/build_bank.py.

TOPICS: topic id -> (Thai name, emoji, [(group code, Thai group name), ...])
L: one string per batch, lines of  "code: word|word|word"  (words matched without case)
"""

TOPICS = {
 'fam':  ('คนและครอบครัว', '👨‍👩‍👧', [('fam', 'ครอบครัว'), ('ppl', 'คน วัย และเพศ'), ('rel', 'เพื่อนและความสัมพันธ์')]),
 'bod':  ('ร่างกาย', '🧍', [('bod', 'อวัยวะ'), ('look', 'รูปร่างหน้าตา'), ('bact', 'กิริยาของร่างกาย')]),
 'hlt':  ('สุขภาพ', '🩺', [('ill', 'อาการและโรค'), ('med', 'การรักษาและยา'), ('fit', 'สุขภาพดีและการออกกำลังกาย')]),
 'food': ('อาหารและเครื่องดื่ม', '🍲', [('dish', 'อาหารและของกิน'), ('fv', 'ผักและผลไม้'), ('drk', 'เครื่องดื่ม'), ('cook', 'การทำอาหารและรสชาติ'), ('eat', 'มื้ออาหารและร้านอาหาร')]),
 'home': ('บ้าน', '🏠', [('room', 'บ้านและห้อง'), ('furn', 'ของใช้ในบ้าน'), ('chore', 'งานบ้านและการซ่อม')]),
 'clo':  ('เสื้อผ้า', '👕', [('clo', 'เสื้อผ้าและรองเท้า'), ('acc', 'เครื่องประดับและกระเป๋า')]),
 'nat':  ('ธรรมชาติ', '🌳', [('wea', 'อากาศและฤดู'), ('land', 'ภูมิประเทศและน้ำ'), ('plant', 'พืช'), ('env', 'สิ่งแวดล้อมและพลังงาน'), ('sky', 'ท้องฟ้าและอวกาศ')]),
 'ani':  ('สัตว์', '🐾', [('ani', 'สัตว์')]),
 'plc':  ('สถานที่', '🏙️', [('town', 'สถานที่ในเมือง'), ('bld', 'อาคารและส่วนของอาคาร'), ('geo', 'ประเทศ ภูมิภาค และทิศ')]),
 'trv':  ('การเดินทาง', '✈️', [('veh', 'ยานพาหนะ'), ('road', 'ถนนและการจราจร'), ('trip', 'ท่องเที่ยวและที่พัก'), ('fly', 'สนามบินและตั๋ว')]),
 'edu':  ('การศึกษา', '🎓', [('subj', 'วิชา'), ('study', 'การเรียนและการสอบ'), ('stat', 'เครื่องเขียนและอุปกรณ์')]),
 'job':  ('งานและอาชีพ', '💼', [('occ', 'อาชีพ'), ('hr', 'สมัครงาน จ้างงาน และสวัสดิการ'), ('off', 'สำนักงานและเอกสาร'), ('meet', 'ประชุมและนำเสนอ')]),
 'biz':  ('ธุรกิจ', '🏭', [('co', 'บริษัทและการบริหาร'), ('mkt', 'การตลาดและการขาย'), ('prod', 'การผลิตและคุณภาพ'), ('deal', 'สัญญาและข้อตกลง'), ('ship', 'การสั่งซื้อ ส่งของ และคลังสินค้า')]),
 'mon':  ('เงิน', '💰', [('pay', 'ราคาและการจ่าย'), ('fin', 'ธนาคาร บัญชี และการลงทุน'), ('shop', 'การซื้อของและร้านค้า')]),
 'tec':  ('เทคโนโลยี', '💻', [('dev', 'อุปกรณ์และเครื่องจักร'), ('net', 'อินเทอร์เน็ตและข้อมูล'), ('sci', 'วิทยาศาสตร์และวิศวกรรม')]),
 'com':  ('การสื่อสาร', '📣', [('talk', 'พูด คุย ถาม ตอบ'), ('msg', 'จดหมาย โทรศัพท์ และข้อความ'), ('news', 'ข่าวและสื่อ'), ('lang', 'ภาษา การอ่าน และการเขียน')]),
 'art':  ('บันเทิงและงานอดิเรก', '🎭', [('art', 'ศิลปะ ดนตรี และภาพยนตร์'), ('spt', 'กีฬา'), ('fun', 'งานอดิเรกและการพักผ่อน'), ('evt', 'งานและเทศกาล')]),
 'soc':  ('สังคม', '🏛️', [('gov', 'รัฐ กฎหมาย และการเมือง'), ('crime', 'อาชญากรรมและความปลอดภัย'), ('cult', 'ศาสนา วัฒนธรรม และประวัติศาสตร์'), ('socp', 'ชุมชนและปัญหาสังคม')]),
 'emo':  ('อารมณ์ความรู้สึก', '😊', [('pos', 'ความรู้สึกดี'), ('neg', 'ความรู้สึกไม่ดี')]),
 'chr':  ('นิสัยและบุคลิก', '🧑‍🎤', [('chr', 'นิสัยและบุคลิก')]),
 'mind': ('ความคิดและการรับรู้', '💭', [('think', 'คิด รู้ และเข้าใจ'), ('want', 'ต้องการ ชอบ และตัดสินใจ'), ('sense', 'การมอง ฟัง และรับรู้')]),
 'tim':  ('เวลา', '⏰', [('unit', 'วัน เดือน และหน่วยเวลา'), ('when', 'คำบอกเวลา'), ('freq', 'ความถี่และลำดับ')]),
 'num':  ('จำนวนและการวัด', '🔢', [('num', 'ตัวเลข'), ('qty', 'ปริมาณ'), ('meas', 'การวัดและหน่วย')]),
 'desc': ('คำบอกลักษณะ', '🎨', [('col', 'สี'), ('shp', 'รูปร่างและขนาด'), ('qual', 'ดี แย่ ง่าย ยาก'), ('state', 'สภาพและคุณสมบัติ')]),
 'act':  ('การกระทำทั่วไป', '🏃', [('move', 'การเคลื่อนที่'), ('hand', 'การใช้มือ'), ('get', 'ได้ ให้ เก็บ และใช้'), ('make', 'สร้าง ทำ และเปลี่ยน'), ('do', 'เริ่ม หยุด ลอง และช่วย')]),
 'abs':  ('คำนามนามธรรม', '🧩', [('abs', 'ความคิด เรื่องราว และสถานการณ์')]),
 'fn':   ('คำเล็กที่ใช้บ่อย', '🔗', [('pron', 'สรรพนามและคำชี้'), ('prep', 'บุพบทและตำแหน่ง'), ('conj', 'คำเชื่อม'), ('wh', 'คำถาม'), ('aux', 'กริยาช่วย'), ('adv', 'คำขยายที่ใช้บ่อย'), ('exc', 'คำทักทายและคำอุทาน')]),
}

L = []
L.append('''
prep: about|above|across|around|at|behind|below|between|by|during|in|into|near|down|front|away|back|after|before|left
pron: all|another|any|anyone|anything|both|each|else|he|her|him|his|I|it|its|me|my|nobody|nothing
conj: and|as|because|but|however|if
adv: also|again|just|not|maybe|here
exc: bye|goodbye|hello|hey|hi|no
aux: May|be
when: ago|now|later|early|late|future|moment|next|last
freq: always|never
unit: afternoon|April|August|century|date|day|December|hour|January|July|June|March|minute|Monday|month|morning|night|November|midnight
fam: aunt|brother|cousin|dad|daughter|grandfather|grandmother|grandparent|husband|mother|mum
ppl: adult|baby|boy|child|girl|man|age|name
rel: boyfriend|girlfriend|dear|neighbour|married|member|meet|miss
bod: arm|body|ear|hair|hand|head|leg|mouth|nose
look: beautiful|blonde
bact: born|die|laugh|hungry|lie
fit: health|healthy|gym|diet
med: hospital
fv: apple|banana|carrot|fruit
dish: bread|butter|cake|cheese|chicken|chocolate|cream|egg|meat|ice
drk: beer|coffee|juice|milk
cook: cook|cooking|delicious
eat: breakfast|dinner|lunch|meal|menu|cafe|dish
room: apartment|bathroom|bedroom|door|garden|house|home|kitchen
furn: bed|chair|clock|desk|box|cup|bottle|glass
chore: clean|bath
clo: boot|clothes|coat|dress|hat|jacket|jeans
acc: bag
wea: air|autumn
land: land|island|mountain|beach
env: natural
sky: light
ani: animal|bird|cat|cow|dog|elephant|horse|lion|mouse
town: cinema|library|museum|club|centre|address|local|area
geo: capital|city|country|north|east
fly: airport
veh: bicycle|bike|boat|bus|car
road: drive
trip: journey|holiday|hotel|map
subj: geography|history
study: classroom|college|course|dictionary|homework|lesson|learn|class
occ: actor|actress|artist|dancer|doctor|driver|nurse
hr: career|job|interview
meet: meeting
co: business|company
mkt: customer
pay: bill|cheap|cost|dollar|euro|money|cent
shop: buy|market
fin: bank
dev: camera|computer|machine
net: blog|email|internet|information
talk: answer|ask|call|conversation|describe|description|dialogue|discuss|introduce
msg: message|letter|card
news: article|magazine|news|newspaper
lang: language|meaning|note|list
off: chart
art: band|concert|dance|dancing|draw|guitar|movie|music|art|design
spt: ball|match
fun: game|hobby|fun
evt: birthday
cult: culture
neg: afraid|angry|bored|hate
pos: happy|enjoy|love|hope|interested
chr: kind|funny
think: agree|believe|guess|imagine|know|mean
want: decide|choose|like|need|interest
sense: hear|listen|look
col: black|blue|brown|green|grey|colour
shp: big|large|little|long|high|line
qual: bad|best|better|good|great|amazing|easy|difficult|important|interesting|boring|nice|correct|dangerous|common|different|main|key|modern|negative|complete
state: cold|cool|dark|dirty|full|hard|hot|new|busy|live
move: arrive|come|go|leave|move|climb
hand: bring|carry|cut
get: give|get|have|keep|lose|include|add
make: build|create|change|make|do|improve|grow
do: begin|end|break|help|check|compare|join|happen|let
abs: action|activity|advice|beginning|detail|difference|idea|life|mistake|model
num: eight|eighteen|eighty|eleven|hundred|million|nine|nineteen|ninety|number
qty: half|lot|many|more|most|much|enough|group
meas: kilometre|mile|metre
bld: building|downstairs
''')
L.append('''
make: become|turn|combine|arrange
lang: book|page|paragraph|phrase|sentence|spell|spelling|text|title|word|write|writing|story|topic|character
move: close|open|out|over|stand|sit|walk|stay|visit|wait|appear|attend|abroad
drk: drink|tea|water|wine
eat: eat|thirsty|bar|bowl
wh: how|what|when|where|which|who|why
abs: object|opinion|part|piece|situation|thing|way|type|style|subject|success|case|cause|chance|choice|consequence|advantage|benefit|ability|alternative|background|behaviour|attention|argument|comparison|arrangement|collection|connection|conclusion|amount|average|bit
unit: October|Saturday|September|Sunday|Thursday|Tuesday|Wednesday|week|weekend|year|time|period|past|summer|spring|winter|second
prep: of|off|on|outside|opposite|through|to|under|until|up|upstairs|with|without|against|along|among|according to|bottom|there|together
freq: often|once|sometimes|twice|usually|third|then|already
exc: oh|sorry|thank|thanks|welcome|yeah|yes|ah|all right
num: one|seven|seventeen|seventy|six|sixteen|sixty|ten|thirteen|thirty|thousand|three|twelve|twenty|two|billion
fv: onion|orange|tomato|vegetable|bean|pepper
qty: only|some|pair|too|very|almost|still|enough
conj: or|so|than|although|anyway
pron: other|our|she|somebody|someone|something|that|the|their|them|they|this|us|we|you|your|yourself|anybody|anywhere|anymore
get: own|share|take|use|spend|accept|allow|borrow|belong|available|catch|win
art: paint|painting|photo|photograph|piano|picture|sing|singer|song|sound|video|cartoon|classical|audience|celebrity|architecture|background
stat: paper|pen|pencil|board|button
fam: parent|sister|son|uncle|wife|birth
town: park|school|station|street|town|village|supermarket|theatre|church|castle|bridge
rel: partner|people|person|personal|visitor|welcome
evt: party|celebrate|award
fly: passport|ticket|airline
pay: pay|cash|coin
bact: sleep|shower|wake|asleep|alive|blow
ani: pig|sheep|snake|bear
col: pink|white|yellow|coloured|bright
qual: perfect|similar|special|sure|strong|terrible|useful|wonderful|wrong|well|awful|brilliant|clear|clearly|certain|certainly|complex|competitive|commercial|based|badly|blank|attractive|average
subj: science|chemistry|biology
occ: scientist|teacher|waiter|worker|writer|architect|assistant|athlete|author|boss|businessman|chef|coach|student
land: sea|water|tree
mkt: sell|advertise|advertisement|advertising|competitor|complaint
msg: send|phone|telephone|text|chat|comment|communication
shop: shop|shopping|supermarket
shp: short|small|tall|circle
ill: sick|tired|blood|accident
neg: tired|confused|confuse
pos: confident
spt: sport|swim|swimming|team|tennis|baseball|basketball|beat|win
sky: star|sun|cloud
wea: snow|weather|warm|climate
geo: south|west|world
state: slow|still|old|young|broken|closed|alive|alone|active
talk: say|speak|talk|tell|show|statement|argue|thank|conclude|confirm|commit
do: start|stop|try|act|achieve|apply|avoid|care|concentrate|behave|test|work|attack
study: student|study|teach|test|university|skill
clo: shirt|shoe|skirt|sweater|trousers|T-shirt|wear|belt|clothing
dish: soup|sugar|beef|biscuit|chip|ice
furn: table|umbrella|wall|window|bin|carpet|brush
when: soon|today|tomorrow|tonight|yesterday|already
trip: tourist|travel|trip|vacation|camp|camping|adventure
veh: taxi|train
road: traffic|way
sense: see|watch|look
think: think|understand|know|certain
want: want
dev: television|app
net: website|online|cloud
bod: tooth|ankle|bone|brain
room: toilet
chore: wash
make: affect
''')
L.append('''
off: office|order|section|mark|item|entry|print|printer|diagram|reference
ppl: teenager|woman|female|male|guy|kid|lady|human|individual|hero|king
qual: able|ancient|careful|carefully|clever|convenient|cruel|definite|direct|directly|effective|effectively|equal|equally|exact|exactly|excellent|extreme|extremely|fair|formal|general|ideal|impossible|incredible|independent|informal|intelligent|lovely|necessary|normal|normally|ordinary|original|particular|proper|properly|rare|reliable|remote|perfect|helpful|likely|lucky|polite|private|continuous|current|daily|everyday|custom|double|free|fresh|deep|due|happily|foreign|international|national|cultural|economic|educational|environmental|physical|medical|musical|religious|related|repeated|included|including|covered|engaged|missing|lost|express
adv: actually|especially|immediately|instead|mostly|nearly|perhaps|currently|finally|firstly|fortunately|rarely|regularly|anyway
abs: appearance|space|content|contrast|difficulty|disadvantage|effort|element|evidence|experience|factor|feature|focus|gap|goal|habit|knowledge|level|lifestyle|luck|manner|material|matter|method|mind|memory|movement|nature|opportunity|option|pattern|peace|possibility|power|position|quality|range|reality|reaction|relation|possession|permission|property|duty|emergency|error|figure|image|expression|explanation|definition|introduction|instruction|recommendation|damage
gov: army|court|election|government|law|lawyer|president|protest|enemy|national|economy|economic
cook: boil|burn|fresh|knife|fork|oven|jam|plate
ill: cigarette|drunk|flu|headache|hurt|ill|illness|injury|pain
socp: charity|donate|population|pollution
env: coal|gas|oil|petrol|pollution|environmental|nature|plastic|metal|gold|diamond|material|cotton|heat|power
get: consist|consume|deliver|feed|hold|lend|offer|pick|pass|remain|release|rent|possession|include
mkt: consumer|discount|promote|commercial
furn: container|curtain|fan|fridge|furniture|lamp|mirror|lock|pack|bin
msg: contact|mail|link|network|mobile|invitation|invite|greet|remind
talk: convince|mention|quote|quotation|recommendation|joke|comment|reject|protest|define|explanation
clo: costume|dressed|jewellery|pants|pocket|fashion|cotton
room: cottage|hall|gate|entrance|parking|lab
land: countryside|lake|forest|hill|ocean|field|grass|ground|nature|farm|farming
do: count|cover|decorate|determine|divide|fail|finish|fix|identify|increase|involve|manage|organize|perform|prevent|repair|repeat|prove|predict|quit|exist|qualify|focus|relate
crime: criminal|gun|kill|prison|punish|punishment|fight|hide|steal
fin: currency|penny|percent|profit|receipt|per
pay: receipt
deal: deal
unit: decade
art: documentary|drum|episode|fiction|film|gallery|image|jazz|novel|painter|musician|poster|pop|entertain|entertainment|musical|perform
trip: departure|destination|guest|guide|passenger|palace|queue
neg: disappointed|disappointing|dislike|embarrassed|embarrassing|fear|nervous|pain
think: doubt|expect|knowledge|mind|memory|notice|define|predict|reflect|determined|identify
want: dislike|encourage|expect
move: drop|fall|fly|flying|jump|lift|forward|pass|onto|pop|race
state: dirt|dust|empty|fat|flat|heavy|loud|loudly|low|narrow|noise|noisy|broken
geo: eastern|international|foreign
fit: fit|fat|heavy
study: educate|educated|essay|lecture|learning|instructor|major|qualification|qualified|knowledge
subj: mathematics|maths|physics
news: editor|journalist|media|listener|platform
hr: employment|instructor
abs: emotion
sci: engineering|experiment|invention|invent|lab|planet|element
conj: despite|except|neither|unless
pron: everywhere|hers|herself|himself|itself|mine|myself|none|nowhere|ourselves|neither
occ: expert|farmer|lawyer|leader|manager|officer|owner|painter|pilot|producer|profession|journalist|editor|instructor|president
prod: factory|industry|production|producer|material|plastic
ani: farm|fish|frog|insect|monkey|pet|fishing
spt: fishing|golf|hockey|goal|racing|race|field|hit
evt: gift|celebrate|invitation|invite
cult: god|religion|religious|cultural|king|palace
bod: finger|heart|knee|neck|blood|human
shp: huge|height|edge|middle|hole|narrow
pos: happily|laughter|pleased|proud|relaxed|relaxing|lucky
bact: hurt|laughter
chr: lazy|patient|personality|polite|intelligent|clever|cruel|helpful
dev: instrument|laptop|printer|program|platform|mobile
hand: hit|hold|knock|lift|pull|push|lock|pick|fix
co: leader|organization|manage|manager|owner
rel: marry|relative|relation|guest
meas: least|less|per|percent|height
qty: least|less|most|mostly|nearly|double
aux: might
sky: moon|planet
veh: lorry|motorcycle|petrol|parking|passenger
exc: please
mkt: promote
fin: profit
net: link|network|program|online
''')
L.append('''
abs: development|final|result|risk|responsibility|resource|rule|sample|set|setting|sort|spirit|spot|standard|state|strength|stuff|substance|theme|theory|trend|trick|truth|value|version|wonder|worth|aspect|being|bond|challenge|characteristic|circumstance|combination|component|concept|consideration|core|creation|crisis|criterion|emphasis|existence|expectation|extent|fault|favour|finding|affair|similarity|talent|tip|approach|access|advance|barrier|failure|conflict|confidence|commitment|courage|comfort|enthusiasm|faith|evil|desire|demand|delight|anger|concern|aid
land: earthquake
freq: first|following|further|afterwards|throughout|whenever|constantly|constant
prep: inside|within|beyond|upon|till|throughout|downwards|elsewhere|unlike|since
co: lead|leader|administration|agency|association|chairman|chief|commission|committee|corporate|council|division|executive|firm|crew|staff|union|manage
fv: lemon|nut|seed|plant|crop|bush
plant: plant|seed|crop|bush|grass|tree|forest|wing
med: medicine|treat|treatment|cure|symptom|cancer|blind|bacteria|cell
ill: symptom|cancer|blind|throat
when: present|current|currently|annual|anniversary|sudden|while|youth
get: request|require|store|supply|acquire|adopt|deserve|access|enable|capture|bet|beg
hr: retire|retired|unemployed|unemployment|shift|staff|volunteer|talented|talent|qualified|commitment
talk: represent|respect|summarize|summary|warn|warning|accuse|acknowledge|appeal|blame|cite|command|criticism|criticize|critic|debate|declare|decline|deny|excuse|emphasize|enquiry|feedback|request|vote
trip: reservation|tour|tent|accommodation|sail|sailor
do: revise|separate|scan|survive|suffer|tend|update|attempt|adapt|alter|assess|assessment|associate|calculate|cancel|conduct|contribute|contribution|convert|ensure|establish|estimate|evaluate|enhance|engage|encounter|emerge|dominate|detect|demonstrate|defend|delay|edit|draft|examination|extend|expose|exploration|crash|collapse|arise|approve|approval|display|distribute|distribution|dismiss|elect|deliberate|deliberately|concentration
acc: ring
move: rise|roll|row|sink|shake|stick|spread|float|fold|drag|dig|approach|emerge|bent
dev: robot|switch|software|tape|tube|tyre|cable|chain|disc|alarm|aircraft|file
chr: romantic|shy|silly|smart|sensible|aggressive|ashamed|capable|conservative|dishonest|enthusiastic|ethical|flexible|honest
furn: rope|shelf|string|tin|yard|chain
state: rough|sharp|shiny|silent|smooth|solid|tight|bent|bitter|broad|curved|even|flat|valuable|used|worse|worst|deep|deeply|whole|entire|entirely|total|totally
cult: royal|spirit|statue|sculpture|faith|god|civil|citizen|ethical
spt: rugby|stadium|supporter|contest|defeat|battle
crime: safety|security|shoot|victim|violent|weapon|bullet|armed|arms|evil|discipline|accuse
qual: scientific|secondary|seriously|similarly|simply|slightly|specifically|standard|strongly|successfully|suitable|surely|technical|typically|unable|uncomfortable|unfair|unlikely|unnecessary|unpleasant|various|absolutely|academic|accurate|actual|additional|apparent|apparently|appropriate|artificial|basically|brief|capable|classic|closely|commonly|complicated|confusing|conscious|consistent|contemporary|critical|crucial|decent|detailed|domestic|dramatic|efficient|external|extraordinary|flexible|similarly
land: sand|soil|wave|desert|surface|shell
sci: scientific|bacteria|cell|experiment|theory|technique|statistic|creature
art: script|sculpture|studio|statue|viewer|broadcast|cast|artistic|edition|classic|dramatic|draft
ppl: servant|sex|stranger|youth|elderly|fellow|citizen|being
bact: sexual|cry|touch|feel|dig|survive
sky: shine|flame|flash|light
sense: sight|view|signal|touch|feel|detect|flash
pron: theirs|whatever|whether
conj: therefore|though|unless|whether|while|since|despite
num: dozen
meas: weigh|tail|depth|angle|curve|capacity|tiny|slice
shp: tiny|slice|curve|curved|angle|depth|broad|row
fin: tax|trade|account|budget|credit|debt|bond|estate|expense|fee|finance|value|spending
pay: spending|expense|fee
lang: translate|translation|written|spoken|document|edition|edit
msg: signal|update
geo: southern|western|worldwide|border|county|district|domestic
veh: transport|aircraft|crash
cook: spicy|bitter|slice
clo: suit|underwear|wool|feather
bod: throat|toe|tongue|breast|tail|wing|feather
ani: creature|tail|feather|wing
neg: upset|worry|anxious|anger|concerned|depressed|depressing|desperate|ashamed|concern
pos: delight|delighted|enthusiasm|enthusiastic|comfort|convinced|confidence
aux: will
env: waste|bush|soil
socp: volunteer|charity|aid|union|vote
gov: vote|civil|council|commission|defence|defend|declare|election|elect|armed|battle|citizen|administration|domestic
think: assume|consideration|conscious|expectation|expect|wonder|believe|knowledge
want: desire|demand|approve|deserve|favour
deal: contract|deal|agenda|commitment
meet: agenda|debate|feedback
mkt: delivery
ship: delivery|distribute|distribution|supply
off: document|file|draft
fun: tent|sail
evt: anniversary|decoration
chore: decoration
hand: shake|roll|fold|drag|switch
rel: fellow|associate
''')
L.append('''
chr: responsible|humorous|humour|impatient|lively|logical|mysterious|neat|sincere|sensitive|strict|tough|wise|willing|offensive|honour
look: ugly|pose
qual: associated|fundamental|grand|harmful|intended|intense|internal|initial|initially|largely|latest|limited|long-term|loose|lower|massive|maximum|medium|minimum|minor|mixed|multiple|numerous|official|outer|overall|partly|permanent|plain|positive|potential|prime|pure|rapid|rapidly|raw|realistic|reasonable|relatively|relevant|severe|significant|significantly|slight|somewhat|stable|steady|temporary|tough|truly|ultimately|unexpected|unique|unknown|upper|vast|virtual|visual|vital|widely|absolute|acceptable|enjoyable|fully|gradually|increasingly|former|inner|secure|pointed|matching|regional|rural|urban|industrial|tropical|solar|spiritual|moral|holy|professional|senior|junior
qty: bunch|plus|majority|minority|sum|volume|scale|pile|stack|mass|numerous
make: construct|construction|generate|modify|transform|transition|produce|preserve|install|set up|rearrange|replace|turn out|found
meas: decrease|reduction|inch|measurement|speed|pace|frequency|rate|rank|grade|maximum|minimum

neg: emotional|regret|shame|shock|shocked|nightmare|impatient|scream|harm
town: facility|institute|institution|venue|cafeteria|resort|housing
pos: forgive|fortune|joy|relief|satisfied|satisfy|praise|impress|impressed|sympathy|trust|reward|inspire
hand: folding|grab|handle|rub|wrap|sweep|split|tear|wipe off|brush off|throw away|shovel|stack|roll up|pitch|load
gov: freedom|govern|justice|minister|parliament|military|opposition|regulation|revolution|licence|permit|official|council|military
env: fuel|mineral|steel|rubber|silk|wire|solar|preserve|wildlife|species
dev: function|motor|monitor|panel|screen|satellite|tank|install|virtual|light fixture
fin: fund|funding|income|investment|insurance|loan|owe|pension|saving|wealth|wealthy|wage|budget
freq: furthermore|nevertheless|occasionally|otherwise|thus|whereas|wherever|yet|latest
get: gain|grant|obtain|possess|reach|retain|rid|seek|select|selection|accompany|abandon|reserve|pursue|transfer|submit
crime: gang|harm|offence|offend|investigation|witness|violence|threat|threaten|shooting|shot|rescue|protection|secure|suspect|swear
art: genre|illustrate|illustration|plot|rhythm|stage|tale|tone|tune|performance|popularity|imagination|sponsor|host
hr: hire|hiring|labour|wage|pension|leadership|master|specialist|employee|personnel|assignment|do for a living|senior|junior|professional|reputation
sense: hearing|observation|observe|stare|monitor|sense|track
cult: heaven|hell|holy|lord|soul|spiritual|moral|philosophy|slave
bod: heel|lung|nerve|organ|wound|self
think: hesitate|imagination|imply|insight|interpret|judgement|notion|perspective|recall|regard|suspect|realistic|reasonable|logical|principle|vision
evt: host|opening|launch|session
room: household|housing|seat|corridor|entryway|walkway|flooring|frame|shelter|tunnel
abs: incident|initiative|instance|issue|means|mission|objective|obligation|origin|outcome|outline|phase|phenomenon|potential|presence|principle|priority|privacy|procedure|process|progress|proof|prospect|requirement|routine|sequence|status|step|structure|struggle|target|term|trouble|weakness|zone|preparation|protection|success|victory|silence|shade|shadow|load
talk: inform|insist|interrupt|justify|oppose|opposed|propose|proposal|remark|whisper|urge|have a conversation|obey
do: impose|launch|maintain|operate|recover|register|rely|resist|resolve|rush|settle|survey|trial|vary|melt|mount|multiply|transfer|maintenance|make a decision|maintain|hesitate
ill: infection|pregnant|surgery|therapy|unconscious|wound|severe|vitamin|recover
med: surgery|therapy|vitamin|psychologist|psychology|infection
subj: psychology|philosophy
study: pupil|grade|term|rank|session
news: publication|reveal|interrupt
spt: league|opponent|victory|pitch|strike|defeat
land: landscape|root|slope|steep|stream|shallow|tropical|stone
move: lean|slip|slide|stretch|surround|surrounding|upwards|via|launch
shp: hollow|round|shape|shallow|steep|round
state: hollow|sticky|stiff|loose|neat|silence
sci: mass|mineral|scale|phenomenon|universe|satellite|solar
sky: universe|satellite|solar
deal: guarantee|obligation|regulation|permit|licence|proposal|propose|agenda
co: institute|management|department|sector|scheme|project|representative|leadership|personnel
off: schedule|project|scheme|work order|forecast|assignment
plant: root|potted plant
pron: whom|self
wh: whom
wea: shade|forecast
veh: ship|vehicle|parking garage|tunnel
road: rush|parking garage
mkt: popularity|purchase|price|sponsor|vendor|sales target|sold out
shop: purchase|price|sold out
ship: package|stock|vendor
pay: price|wage
prep: beside|via|upon
furn: rack|tank|frame|light fixture|potted plant
ppl: resident|participant|tenant|representative|slave|master
rel: participant|tenant|witness
trip: resort|reserve|make a reservation|seat|venue
eat: take an order|cafeteria|wait in line
ani: hunt|hunting|wildlife|species
state: be scattered|be suspended from
chore: repair|maintenance|sweep|wipe off|rearrange|clean
''')
L.append('''
room: passage|patio|interior|exterior|aisle|break room|main entrance|cathedral ceiling|garage|handrail|room|on-site|site
wea: wind|fog|stormy|rainfall|atmosphere
cook: blender|recipe|ingredient|utensil|lid|straw|filling|flavour|culinary|blend|delectable|aromatic|bite|pastry chef|dietary|serve|catering|cater|refreshments
prod: prototype|manufacturing|textile|machinery|inspection|inspect|assembly|assemble|specification|handcrafted|custom-made|quality|innovative|reinforcement|screw|overtighten|cushioning|flattened|unpack
ship: pick up|come in|merchandise|cargo ship|harbor|port authority|freight|courier|transit|drop off|drop-off|dock|ferry|supply chain|packet|loss|tow
plant: bouquet|orchid|shrub|orchard|vegetable garden|botanical garden|sunken garden|horticulture|conservatory|harvest|yield|landscaping|potted plant|branch
evt: nominate|announcement|make a speech|gala|celebration|commemorate|benefit concert|fund-raising|gathering|auction|be honored|honored|concession stand|exhibit|dress rehearsal|staging
want: be interested in|preference|favorite|intend to|opt out of|take pride in|in need of
med: prescription
sense: look for|glance|overlook|browse|highlight|lit|dim|vivid|sparkling|stunning|vibrant
do: walk through|delete|authorize|participate|participate in|concentrate on|focus on|negotiate|oversee|go ahead with|merge|relocate|pull up|remove|assign|consult|develop|proceed|explore|renovate|reorganization|renovation|repave|inspect|reduce|recreate|customize|verify|incorporate|expedite|finalize|equip|hone|excel|occur|adjust|coordinate|accommodate|revolutionize|result in|refrain from|adhere to|follow|seal|crack|drain|filter|installation|do research|research|demonstration|completion|planning|plan
mkt: review|sales representative|retail|dealership|a selection of|marketplace|public relations|publicist|ad|competition|patron|premier|superior|stand out|of its kind|profile|subscribe|subscriber|offer a refund|pricey
off: expense report|policy|invoice|interoffice|underlined|booklet|brochure|informational|deadline|timeline|tight schedule|behind schedule|be on track|scheduling conflict|schedule|administrative|head office|staffing|work order
fin: reimbursement|invest|proceeds|real estate|audit|surplus|fraction|quarter|overtime pay|compensation|at one's expense|fine
deal: approved|terms|condition|warranty|coverage|expiration|expire|renew|renewal|privilege|certification|certificate|confirmation|issuance|authority|coalition|merger|guild
hr: supervisor|absent|retirement|career path|job offer|work one's way up|new hire|applicant|employ|perk|upward mobility|paid vacation|job seeker|skill set|skilled|veteran|colleague|vice president|cofounder|tailor|electrician|botanist|archaeologist|professor|performer|attendant|guest speaker|attendee|recipient
occ: supervisor|tailor|electrician|botanist|archaeologist|professor|performer|attendant|cashier|pastry chef|mayor|cofounder|vice president|publicist|veteran
dev: electronic|electronics|equipment|device|appliance|tool|ringtone|machinery|trowel|crowbar|screw
veh: deck|cargo ship|ferry|vehicle|get a flat tire|wheel alignment|lane|northbound
trip: uneventful|ordeal|baggage|luggage|fully booked|in advance|historical site|ruins|remains|trail|explore
qual: incorrectly|compact|wide-mouthed|world-renowned|renowned|designated|alternate|introductory|efficiently|intricate|defensive|protective|internally|immediate|regular|emerging|unimaginable|eco-friendly|beneficial|easy-to-acquire|expansive|sweeping|adjacent|charitable|substantial|solely|vetted|distracting|multilayer|feasible|specific|individualized|recognized|respective|practical|time-consuming|inattentive|simplified|worthwhile|smoothly|with ease|laid-back|bustling|generous|participating|approved|upcoming|previously|frequently|annually|in a row|going forward|recently|eventually|unfortunately
msg: place a call|stamp|contact information|reply|notify|keep someone posted|reach out to|stay informed of|post|press conference|follow-up
room: under construction
news: publishing|press conference|recording|scene
think: thought|realize|express doubt|assuming|findings|judge|key factor
socp: public|donation|charity|charitable|native|inhabitant|heritage|patron
abs: lack|mix-up|addition|guidance|assistance|support|cooperation|collaboration|flexibility|expansion|infusion|jewel|cluster|region|key factor
co: merger|operation|expansion|reorganization|closure|head office|branch|internally
meet: conference|presentation|give a lecture|guest speaker|attendee|introductory|fill out a questionnaire|make a request|express concern
art: drawing|modern art|exhibit|mosaic|performer|clay|marble
crime: protect|protective|defensive
land: coast|shore|clay|marble|Great Plains|drainage|drain
env: offshore wind|greenhouse gas|emission|pollutant|conservation|eco-friendly
geo: region|northbound
gov: mayor|ballot|authority|coalition
when: no longer|quite a while|upcoming|in advance|no later than|time zone|immediate
prep: in addition to|related to|adjacent to|regardless of|amid|no matter how
aux: be supposed to
study: enroll|tuition|completion|certificate|guidance|introductory
get: collect|raise|abound|stop by|take a break|hold on to|reply|equip
hand: hold on to|unpack|screw|seal|tow
neg: distracting
pos: be honored|honored|take pride in
''')
L.append('''
hr: registration|job posting|fill the position|be promoted|apply for|open position|recruit|application|time sheet|payroll department|workforce|candidate|cover letter|credentials|advanced degree|performance review|coworker|fill in for|be involved|entrepreneur|graduate|team building|engagement|on vacation|recruit
co: expand|executive team|headquarters|main branch|incorporated|stakeholder|strategy|implement|society|facilitator|chairperson|organizer|financial management|based in|directive|work with|collaborate|asset
ship: out of service|transportation|deliverable|shipment|shipping container|back-ordered|back order|distributor|storage|storage closet|warehouse|inventory|cargo|crate|breakage|in transit|expedited shipping|port|exporter|supplier|wholesale|packaging|place an order|out of stock|discontinue|preorder|shortage|availability|disruption|household goods|raw material|finished product
deal: promise|negotiation|agreement|lease|rental application|restriction|mandatory|licensed|certified|penalty fee|enact|extension|in place
room: shingle|shutter|canopy|wallpaper|air duct|railing|ladder|heating system|residential|residence|suburb|clubhouse|showroom|outlet|reside
talk: refer to|apology|apologize|suggestion|voice|inquiry|query|refer|rest assured that|in apology for|gladly
study: uncover|education|laboratory|marine biology|graduate|advanced degree
do: sign up for|turn off|trial run|try out|investigate|allocate|figure out|keep track of|fill out|fill in|enter|maximize|modernize|complicate|outpace|trigger|overcome|break ground|itemize|insert|discard|scatter|reschedule|limit|compete|anticipate|render|take on|take measurements|take a measurement|marinate|transplant|watering|irrigation|arrange flowers
net: connectivity|webinar|analytics|networking|alert|voicemail|subscription|automatically|remotely|printable
qty: a range of|plenty|dozens of|approximately|extra|left over|variety|portion|quantity|subtotal|unit|fraction
art: compose|opening act|landscape painting|restoration|restorer|unveil|segment|keynote speech|showcase
chr: spare no effort|undeterred|passionate|knowledgeable|dependable|loyal|be eager to|motivational
geo: Filipino|metropolitan|locally|nearby|walking distance|suburb
eat: eatery|diner|luncheon|dining table|executive chef|vegetarian|chocolatier|grocer
dish: curried|oxtail|red snapper|jerk|stewed|eggplant|flour|brittle|swirl|food coloring|spice|nutrition
cook: marinate|smoky|crushed|delightful|flavor|texture|sour|deep fryer|cookware|kitchen supply|freezer|prep|pour|spill
qual: extensive|outstanding|glowing|last-minute|decorative|valued|long-standing|frequent|on a regular basis|double-sided|unavailable|incorrect|positively|casual|state-of-the-art|preliminary|suited for|seasonal|oversized|indirectly|well-attended|durable|adjustable|fabulous|underway|handheld|unclear|weighty|professionally|cost-efficient|up-to-date|ongoing|energy-efficient|rising|exceptionalism|exclusively|adequate|memorable|organized|far-reaching|weeklong|reduced|completely|underused|at no cost|automotive|custom-built|substantially|affected|attached|diverse|fast-paced|prospective|sustainable|separately|previous|identical|recurring|in-store|mistakenly|brick-and-mortar|machine-washable|reusable|highly|predetermined|cluttered|messy|enclosed|tired of|acquired|quality|details
pos: live up to|delightful|gift certificate|look forward to|care for|relaxation|memorable
neg: dissatisfaction|inconvenience|downside|tired of
dev: malfunction|charger|electrical failure|electric|electrify|fully charged|solar powered|instruction manual|welding|handheld|fitness tracker|lawn mower|engine room
fin: billing|invoicing|account number|payment|payment method|travel expense|refund|charge|operating cost|investor|profits|pricing|ring up|reduced
mkt: incentive|rollout|promotion|preferred customer|loyal customer|rave review|target audience|boost|promotional|publicize|publicity|draw attention|limited-time offer|advertiser|attract|retailer|response rate|rating|score|wholesale|shelf space|prospective
abs: impact|aim|decision|adjustment|time frame|category|signature|problem-solving|strategy|usage|revision|amenity
evt: appointment|convention|special occasion|fund-raiser|scavenger hunt|luncheon|opening act
off: handout|reminder|time sheet|directions|enclosure|office supplies|newsletter|detail|details
med: pharmaceutical|physical therapy|stimulation|health-care|dentist|checkup|optician
occ: dentist|optician|contractor|inspector|politician|spokesperson|government official|finisher|executive chef|restorer
prod: manufacturer|manufacture|workmanship|quality|custom-built|finished product
land: seashore|aquatic|ecosystem|gravel|grove|bamboo|oak|magnolia|seedling
plant: magnolia|grove|seedling|oak|bamboo|planter|watering|irrigation|transplant|arrange flowers
env: ecosystem|public awareness|sustainable|energy-efficient|trash|trash bin|reusable
meas: cubic meter|metric ton|take a measurement|take measurements
road: paving|highway|sidewalk|roadwork|monthly pass|public transportation
trip: itinerary|site tour|historic site|attraction|overnight
socp: public awareness|society
when: on time|make it|ahead of time|be scheduled to|be on schedule|as of|the whole way|on hold|in the event of|in case of|overnight
prep: belong to|be associated with|in contrast to|in a circle
hand: grip|tack|chop|insert|hang up|lay out|pour|spill|take off|discard|wooden board|rolling chair
furn: rolling chair|trash bin|blanket|pillow|planter|dining table|shelving unit|wooden board|storage closet
prod: factory floor
shop: department store|grocer|cosmetics|in person|in-store|retailer
clo: jewelry|fabric|eyeglass frame|athletic apparel|take off
acc: jewelry|eyeglass frame
move: proceed to|face|gather|vacate|take a walk|reside
gov: government official|politician|city hall
town: city hall|car dealership|showroom|clubhouse
veh: car dealership|automotive
sense: sign
msg: sign|signature|voicemail
wea: weather forecast|forecasting
think: there is no point|figure out|anticipate|unclear
spt: compete|score|rating
''')
L.append('''
deal: cancellation|sign a contract|valid|entitle|lock into|annual fee|e-signature|sign off|claim|undisclosed
evt: in attendance|honor|take place|be scheduled for|medical trade show|turnout|win an award|open house|opening ceremony|exhibition|exposition|award ceremony|award-winning|reception|job fair|retreat|centerpiece|ballroom|floral arrangement|esteemed
news: publish|breaking news|press|reporter|reportedly|editorial|published|nonfiction|billboard
get: take advantage of|return|provide|spare|save|contain|incur|attach|afford to|raise money|run out of|be stocked with|be filled with|on hand|sacrifice|unload|fill up
mkt: boast|client|product placement|customer base|customer loyalty|loyalty|referral|patronage|on sale|mark down|for a limited time|price quote|bidder|sales associate|shop assistant|affordable|inexpensive|expensive|reasonably|priced|top-quality|high-quality|top-notch
meet: conference presentation|conference room|video conference|focus group|brainstorm|takeaway|one-on-one|in pairs|input|consultation|consultant|go over|look over|wrap up
off: recorded|record|keep records|save|password|scheduled|handbook|photocopy|flier|registration form|layout|paperwork|order form|calendar|time slot|formatting|task|instructions|copy down|specify|log|name tag|information packet|business day|after-hours|overdue|office supply|be pushed to|postpone|reservable
crime: safety inspection|claim
art: art museum|camera operator|craft|carpentry|handmade|treasure|kingdom|authenticity|authenticate
veh: electric car|be stuck in traffic|traffic congestion|rideshare|muffler|take a ride|aboard|boarding|departure board|concourse|rough water|lighthouse|route|roaming
road: route|traffic congestion|be stuck in traffic|underground
co: be closed down|foundation|director|staffer|enterprise|alliance|shareholder|bankruptcy|viability|profitability|company-wide|business transformation|under the direction of|direction|operational|operating|productivity|streamline|morale|struggling
occ: speech therapist|accountant|mechanic|receptionist|reporter|server|agent|librarian|concierge|consultant|camera operator|grower|mentor
want: prefer|favor|taste|be concerned about|eager|appreciate|feel free to|consider
qual: officially|impressive|space-saving|indoor|lightweight|low-light|possible|possibly|probably|urgent|fully equipped|dental|recent|framed|abandoned|underground|generously|sluggish|clogged|profitable|nutritional|unhealthy|nuanced|extended|continued|fragile|ambitiously|partial|particularly|hard-earned|informed|sugary|cost-effective|supportive|discontinued|selected|exceptional|straightforward|responsive|inflexible|monetary|existing|satisfying|sourced|viable|uncertain|open-air|bulky|clunky|packed|lengthy|unfamiliar|inaccurate|originally|considerable|disposable|projected|comfortable|continental|specialized|brand-new|incomplete|expedited|thorough|structural|intact|gratifying|top-quality|valid|in use|familiar with|mindful|mindful of|dedicated to
abs: product|location|capability|novelty|limitation|improvement|replacement|purpose|needs|solution|achievement|dedication|foresight|distraction|convenience|absence|timing|response|cost-savings|surge|politeness|gratitude|viability
room: redevelop|remodel|construction site|makeover|dining room|waiting room|workplace|floor|locker room|reception desk|circulation desk|leasing office|support beam|fencing|roofing|fireplace|couch|coat-check
fin: cost estimate|revenue|open an account|calculation|issue a refund|accounting practice|banking|savings|checking account|checking|account holder|deposit|payroll|bookkeeping|tax law|in total|profitable|monetary
do: make a change|register for|take care of|come along|look into|take a look at|take a look|sign up|discover|go on|move forward|deal with|simplify|juggle|prioritize|roll out|accomplish|embark on|analyze|examine|sort out|revive|suspend|prepare|deepen|accelerate|catch up|place a limit on|in the process of|take part in|break down|give way to|specialize in|specialise in|stress
talk: misunderstand|misunderstanding|file a complaint|persuade|explain|respond|respond to|complain|disagree|acknowledge receipt|wish someone well|express|in response to|regarding|concerning|when it comes to|to this end
move: depart|head over to|wander|on one's way to|push against|hang|glance at|blow away|gently
neg: ruin|frustrating|frustrated|wear off|be concerned about|struggling
pos: grateful|stress reliever|brighten up|relieved|inspiring
dev: notification|glitch|vending machine|electricity|liquid|iron|hook
sky: outer space
fit: health care|wellness|hydration|weight loss|exercise|nutritional|serving|gluten-free|vegan
hr: job candidate|human resources department|talent development|professional development|job opening|available position|get promoted|earn a degree|understaffed|orientation|mentor|dedication|morale
eat: beverage|serving|server|vegan|gluten-free|sugary|dining room|vending machine
med: medical practice|dental
furn: housewares|stem|couch|hook|drop cloth|stain|in a pile|disposable
plant: stem|grower|log
clo: footwear|athletic footwear|vest|iron
cook: peel
socp: community|town council
gov: town council|tax law|territory|kingdom
trip: travel arrangement|retreat|hospitality|concierge|rental
ship: bulk|expedited delivery|put in an order|processing
prep: instead of|versus|prior to|in the distance|around the corner|for instance|alternatively
when: at the last minute|in time|as soon as possible|so far|right away|in the long run|more than once|infrequently|before one's time|in anticipation of|before one's time
qty: a variety of|at least|in total|considerable
wea: inclement weather
ppl: childhood
think: correspond with
''')
L.append('''
env: environment|surroundings|environmentally friendly|recycling|landfill|dispose of|reuse|energy-saving|wind turbine|debris|insulation|waterproofing|fiber|cloth|repurpose|usable
abs: service|customisation|offering|growth|awareness|source|quest|substitute|complexity|track record|expertise|appreciation|involvement|efficiency|effectiveness|avoidance|generosity|reassurance|imitation|distance|balance|setup|form|measure|flow|practice
hr: portfolio|work sample|full-time position|intern|entry-level job|management position|job description|resignation|day off|be compensated for|experienced|degree|be skilled at|liaison|coordinator|founder|cofound|get ahead|mate|alumni|employee badge|vacation policy|go on vacation|take a vacation|fill|be in charge of|in charge of
prep: on behalf of|on one's behalf|at the request of|contingent upon|by means of|based on|such A as B|given|farther|back and forth|clockwise
road: commute|rapid-transit|transit agency|motorway|detour road|run late|resurface|cut over|driveway|path|trailhead|infrastructure|slow down|widen
qual: horrendous|mistaken|involved|involved in|inaccessible|complimentary|leading|continually|exclusive|behind-the-scenes|successful|historic|elaborate|economical|technologically|advanced|eligible|be eligible for|virtuosic|periodic|accessible|cracked|brand new|traditional|ordinarily|resulting|inclusive|lesser-known|qualifying|aesthetic|rewarding|do-it-yourself|preferable|optional|paperless|as-needed|comprehensive|remaining|trustworthy|promptly|unpredictable|scenic|cordially|keen|pending|hands-on|foundational|prestigious|regarded|outdoor|awfully|high-rise|informative|permitted|step-by-step|unsuccessful|popular|upholstered|mild|crowded|fairly|challenging|out of the ordinary|stuck|inconvenient|leftover|forested|required|pre-owned|prefabricated|political|soothing|instrumental|revised|imitative|prior|yearly|celebratory|commemorative|open-ended|custodial|devoted|literary|financial|agricultural|in particular
think: be aware of|assumption|have in mind|be worth|recognize|clarify|clarification|come up with|intend|have one's eyes on|nothing but|ignore|familiarize oneself with|point out|tend to|seek to|have yet to
co: consultancy|takeover|rival|acquisition|business venture|chamber of commerce|business administration|branch office|in business|trustee|developer|compliance|logistics|chapter|dues|relocation
mkt: clientele|potential client|rewards card|redeem|testimonial|end-of-season sale|price tag|gift card|rebate|shout-out|exclusive|sales report|in stock|have in stock|same-day pickup
neg: disappointment|horrendous|scam|cyberattack
talk: give directions|follow up|get back to|get in touch with|put someone in touch|reach out|reconnect|compliment|give attention|reword|RSVP|consent|admit|cordially
art: footlight|playwright|footage|video footage|mural|artwork|piccolo|recording artist|number one hit|recital|rehearse|acoustics|playlist|instrumental|manuscript|excerpt|copy editor|reviewer|installment|wit|suspense|science fiction|detective|captivate|autograph|lighting|virtuosic|literary|publisher
cult: dig site|pottery|unearth|excavation|historic|traditional|heritage
wea: thunderstorm|electrical outage
dev: technician|utility|manual|shut down|refrigerator|activate|freeze|refill|recharge|charging station|control panel|plug|plug in|wall outlet|shut off|overheating|connect|reset|upgrade|dishwasher|pitcher|filtration|clog|tap water|gear|accessories|intranet|spreadsheet|log on to|tracking|in real time|layer|identification|employee badge
fin: financial|VAT|transaction|low-interest|premium|financing|payment plan|balance|postage|authorization
when: business hours|afterward|to date|beforehand|suddenly|on the rise|in effect|at hand|in preparation for|in one's haste|lag time|come a long way|be poised to
evt: grand opening|banquet|awards ceremony|celebratory|enter a contest|plaque|commemorative
fit: relax|kneel down
move: await|occupy|go on to|end up in|settle into|out of town|outside the city limits|leave off|lay|kneel down|take down|pile up|tie|trim|polish
ani: owl
fv: citrus|grapefruit
dish: crisps
plant: agriculture|agricultural|cultivate|agritourism|forested|ridge
land: ridge
trip: tourist destination|vacation destination|theme park|lodging|scenic|agritourism|suitcase|overnight bag|go on vacation
study: graduation|admission|enrollment|admit|satellite campus|Bachelor of Arts|cosmetology|board of education|school district|capital letter|take notes|degree|alumni
occ: technician|developer|industrial engineer|copy editor|janitor|legislator|clerk|housekeeper|barber|conductor|coordinator|analyst|detective|presenter|playwright|reviewer
gov: legislator|political|security measure|building permit|permitted|board of education|school district|compliance
crime: security measure|protective clothing|scam|cyberattack
meet: give a presentation|board meeting|presenter|questionnaire|respondent|open-ended|at the request of
eat: dining|directness
chr: directness|ambitious|trustworthy|keen|devoted|be willing to|be committed to|make every effort to|pride oneself on|experienced
ship: logistics|same-day pickup|goods|package insert|postage|in stock|have in stock|refill
off: annual report|filing cabinet|registration packet|expiration date|blueprint|sales report|envelope|binder|supply closet|stationery|questionnaire|spreadsheet|take notes|press release
news: press release|outreach
socp: neighbor|newcomer|outreach|awareness
fam: nephew
room: ceiling|closet|cupboard|hallway|pullout sofa|high-rise|household belongings|driveway|lumber|janitorial service|custodial staff|cleaning supplies|setup
chore: janitorial service|custodial staff|cleaning supplies|polish|trim
clo: apparel|protective clothing|tie
qty: plenty of|a couple dozen|weight|measure
meas: weight|distance|quadrant
do: restore|follow up|exceed|motivate|evolve|surpass|carry out|come across|fill|locate|assist|retrieve|set aside|redesign|run|contract with|meet one's demand|take up|cut out|seek to|influence|check out|have an opening|subscribe to|be involved with|qualify for|be equipped with
shop: grocery|check out|goods|accessories
want: be willing to|be committed to
''')
L.append('''
sense: flicker|visible|brighten|indicate|get a sense of|illuminate|moonbeam
msg: heads-up|cc|attn|address to|send in|mobile phone|mail carrier|postal|flyer|bulletin board|banner|telecommunications|prepaid|unlimited|interact
deal: lease agreement|waiver|take effect|go into effect|lifetime warranty|license|nonrefundable|conditions|in compliance|preapproval|bid|bidding|sign off on|flat fee
qty: low on|altogether|an assortment of|the majority of|insufficient|in bulk|grand total|plus tax
qual: off-site|applicable|inexperienced|dedicated|rather|burdensome|consequently|oriented|nonfood|unrefrigerated|approximate|modest|primarily|personalized|family-run|surprisingly|hopefully|mechanical|elected|architectural|walk-in|galvanized|alternately|refurbished|wall-mounted|temporarily|damaged|fast-freeze|fast-setting|as is|compelling|electrical|committed to|luxurious|featured|established|giant|up-and-coming|distinctive|trendsetting|restrictive|work-related|declining|jointly|unoccupied|wooden|customized|uniform|unforeseen|athletic|iconic|securely|unable to|visible|productively|functional|familiar|typical|furnished|timely|verified|entry-level|interactive|mock|low-cost|free of charge|odd|obviously|desirable|self-employed|detail-oriented|archival|diplomatic|engaging|blissful|occasional|equine|grassy|edible|potted|uncommon|cautious|market ready|faithful|anxiously|urgently|in-house|thoroughly|whatsoever|latter|floral|budgetary|organic|faulty|aspiring|densely populated|quarterly
fin: chequing|debit card|direct deposit|paycheck|pay stub|voided check|accounting|reimburse|grand total|plus tax|open a savings account|close an account|labor charge|labour cost|asking price|membership fee|admission fee|treasurer|bookkeeper|award a grant|commerce|budgetary|projection
hr: superintendent|willingness|successful job applicant|reference letter|employer|workload|help-wanted|recruiter|search committee|resign|homemaker|self-employed|diploma|be qualified for|general manager|leave for the day|labor|promotion letter|employee handbook|per company policy|educator|readiness
meas: radius|pressure|temperature|thermometer|acre|duration|oval
prep: ahead of|followed by|as well as|next to each other|close by|underneath|rear|as for|to begin with|now that|what's more|in the meantime|throughout the year|for a while|be about to|at all times|on the horizon|short notice|rain or shine
dev: kitchen appliance|mechanism|drivetrain|pop-up bubble|remote control|refrigeration|solar panel|technical support|circuit|operating system|kit|trolley|thermometer|mobile phone
cook: roaster|brew|baker|tartlet|caterer|pastry|undercooked|protein|potassium|standing cake|takeout|kitchen appliance
chr: enthusiast|dedicated|willingness|cautious|faithful
talk: follow up with|keep in mind|disturb|remarks|announce|inquire|keynote address|give a speech|make a suggestion|suggest|assure|discourage|discourage from|follow up on|neglect
room: floor covering|decorating|dress up|mezzanine|stairway|security office|home decor|retaining wall|drainpipe|storage shed|water pipe|plumbing|wall-to-wall|refinish|boardroom|supply room|loading dock|grounds|furnished|brick
chore: scrub|wipe down|refinish|decorating
furn: tray|bucket|tablecloth|stool|drawer|file cabinet|pallet|walking stick|planter box|bike rack|kit
cult: historian|pirate|dinosaur|symbol|iconic|identity|biography|memoir|charm
evt: ceremony|social|information session|book signing|trade show|exhibitor|get-together|be held|keynote address|have a run|casting
meet: information session|search committee|board of directors|boardroom
co: board of directors|chief executive officer|powerhouse|general manager|publishing firm|rental agency|customer-care|innovation|governance|family-run|trade commissioner|in-house
off: scheduling|archive|submission|schedule conflict|wall-to-wall|shred|print out|purchase order|employee handbook|file cabinet|compile|transcribe|breakdown|mislabel
trip: boardwalk|waterfront|fountain|square|inn|take a reservation|be seated|walking trail|on foot|show around|catch the train|moving van|be booked up|overseas|party of|close by|bowling alley|admission fee|box office|wait list|flight|boarding pass
road: pedestrian bridge|walking trail|on foot|navigate|block|have a flat tire|fleet|moving van|be located
art: videographer|casting|chord|riff|journal|paperback|hardcover|flashback|narrative|lead story|go on the air|sculpt|highs and lows|book signing|box office|have a run|engaging
gov: City Council|run for election|politics|voter|diplomatic|trade commissioner|governance|public land|elected
mkt: supplement|fragrance|keep up with|go with|trendsetting|floor model|restock|customer-care|bidding|be sold out|checkout|kiosk|compelling|distinctive|set apart
do: execute|entail|allow for|shorten|compile|get done|fulfill a request|have trouble -ing|devise|elevate|integrate|resume|make up for|undergo|fine-tune|initiate|conserve|compensate|exclude|enroll in|turn into|instruct|do a search|put together|tear down|lay down|take out|call for|recovery|place|arrange a time|make an appointment|be allowed|be based on|afford|precaution
env: renewable|solar panel|propane|garbage|conserve|habitat|organic|fertilizer
wea: elements|inclement|warmth|weather report|rain or shine
plant: weedy|fertilizer|fish pond|fern|vine|gardening|sapling|lawn|florist|floral|potted|grazing|pasture|grassy|edible
ani: horse-boarding|groom|grazing|equine|veterinarian|dinosaur
occ: baker|caterer|recruiter|historian|real estate broker|videographer|landlord|physician|veterinarian|luthier|bookkeeper|educator|florist|mail carrier|treasurer|handler|carrier
ship: express delivery|carrier|handler|loading dock|pallet|restock|cannery|export|in bulk
prod: cannery|innovation|scuff|dent|faulty|burst|galvanized
med: medical appointment|physician|disease|sprain|feel pain|on call
ill: disease|sprain|feel pain
pos: satisfaction|feel included|blissful
neg: feel excluded|discourage|anxiously
socp: family obligation|homemaker
fam: family obligation
abs: willingness|innovation|satisfaction|symbol|identity|recovery|verification|precaution|charm|narrative|projection|readiness
study: diploma|educator|instruct|biochemistry|journal
sci: biochemistry|potassium|protein|circuit|mechanism
spt: athletic|finish line|bowling alley
when: hopefully|temporarily|throughout the year|on the horizon|for a while|short notice|at all times|in the meantime|now that|be about to
crime: precaution|security office|badge|securely|verification|pirate
move: rest|be seated|navigate|block|place
''')
L.append('''
geo: Aussie|Grecian|gulf|nationwide|citywide|seaside|historic district|neighborhood|next door
furn: supplies|essentials|cardboard|shelving|fixture|chest|pad|toolbox|lightbulb|doorknob|linen|magnet|rollaway bed|crib|briefcase|wheelbarrow|pole|hanging|wheeled|fold up
when: long overdue|midday|semiannual|on a weekly basis|on a monthly basis|weekday|nowadays|sooner than expected|in progress|repeatedly|respectively|generally|usual
msg: callout|receiver|satellite dish|express mail|direct mail|distribution list|business card|wireless|hardwired|FAQ|forum|drop-down menu
ill: sore|overwhelmed|worried|be concerned
hr: job interview|job listing|assistant manager|pay rate|a great fit|semiretired|recruitment|role|professional certification|senior partner|work from home|leave work|work extra hours|be paid overtime|onboarding|employment contract|take on a role|competent|be capable of|childcare|affiliation|cubicle|assigned
med: medical record|medical equipment|medical clinic|exam|optical|nutritionist|stay hydrated|sunscreen|sore|microscope
qual: at one's convenience|generally|combined|much-anticipated|usual|redesigned|people-centered|repetitiously|guided|publicly|finest|remodeled|unusual|primary|exceptionally|long-lasting|human-made|processed|dramatically|beloved|of no use|unsatisfied|misleading|compatible|stand-alone|in order|open-plan|fixed|agreed-upon|expanded|in-office|identified|stringent|illustrated|anonymously|by far|incredulous|individually|carbonated|nonrefrigerated|electronically|overpriced|occupied|hybrid|botanical|resistant|strange|handblown|spacious|moderate|antique|unfailing|defective|essential|locked|surprising|phenomenal|definitely|restricted|photographic|proprietary|automatic|strategic|picturesque|gourmet|first-rate|chemical|waterproof|historical|aging|low-tech|sole|expertly|strategically|notably|minimal|spontaneous|proposed|estimated|on file|corresponding to|Earth-friendly|perfectly|reclaimed|torn down|justified|environmentally|unpopular|calm|energy efficient|jewel-toned|mineral-rich|joint
mkt: endcap|great deals|special deal|throw in|selling point|storefront|alternate product|special offer|presale|going-out-of-business sale|rewards|foot traffic|final offer|secure a deal|checkout station|vending|give away|hand out
meet: debrief|keynote speaker|briefing|adjournment|advisory board|attendance sheet|attendance|on the same page|overview|read through|rating scale|administer|fill out a survey|evaluation form|sign-up sheet|sign-up
do: disrupt|fill out a form|fasten|counsel|broaden|move ahead with|advise|fulfill|supervise|make arrangements|remake|align|reframe|be tailored to|end up|squeeze|take inventory|steer|misplace|go through|label|reinstall|have an effect on|fit into|furnish|unfold|skip ahead|take apart|overhaul|reassure|congratulate|back out|exchange|serve as|ready|seal up|reorganize|stabilize|seek out|complement|sandwich|prevent from|search for|look up|turn on|facilitate|reinforce|free up|unlock|get used to|strive|meet the needs of|take over|make sense|make a difference|have access to|advocate|lead to|get to|mass-produce|grind|temper|stir|scorch|roast|bloom|rename|be subject to|be required to|be aware|spotlight|be connected to
chore: household task|cleanup|laundry|recyclables|groundskeeping
wea: weather condition|snowfall|room temperature
prod: production facility|engineer|workshop|artisan|crafter|woodcraft|cabinetry|mass-produce|batch|output|production cost|mixture|compound|defective|handblown|hardwood|microfiber|reclaimed|specifications|documentation
dev: electronic device|electricity cost|charging|furnace|automatic|wireless|hardwired|toolbox|water main|utility rate|power plant|fire extinguisher|safety equipment|toolshed|magnet
env: energy efficient|carbon footprint|recyclables|waste-to-energy|power plant|nature preserve|Earth-friendly|environmentally|fuel price
veh: car carrier|restraint|carry-on luggage|round-trip|transporter|stuck in traffic|congestion
road: intersection|pedestrian|pavement|telephone pole|lamppost|foot traffic|congestion|stuck in traffic
meas: length
evt: parade|reading|present an award|banquet hall|throw a party|bonding|inception
news: stay tuned|commercial break|spotlight
trip: business travel|tourism|guided|suite|planetarium|hiking|site visit|cabin|round-trip|carry-on luggage|guidebook|seaside
prep: in case|such as|as well|rather than|in terms of|having said that|other than|as follows|one another|given that|by the way|in addition|out of sight|in the know
abs: misconception|interruption|generation|instability|volatility|bottom line|fact-finding|format|guideline|coordination|essentials|implementation|enhancement|prerequisite|modification|dispute|wisdom|nugget|optimism|calmness|interaction|metric|base|belongings|role
plant: leafy|herb|hybrid|bloom|botanical|lily|barn|whole grain|sapling
art: dramatize|permanent collection|needlework|musical instrument|on display|take a photograph|photographic|framing
sky: dome|galaxy|planetarium
eat: cuisine|platter|banquet hall|gourmet|pantry|whole grain
ship: rush shipping|in transport|import|packing slip|shipping|transporter|car carrier|take inventory
fin: tax revenue|fair market value|accountancy|pay in advance|insurance claim|price estimate|leasing|bottom line|Chief Financial Officer|base
clo: eyewear|wristwatch|gemstone
acc: eyewear|wristwatch|gemstone
co: corporate office|work space|law firm|corporation|Chief Financial Officer|chief technology officer|consulting|family-run business|administrator|advisory board|strategic
room: stairwell|basement|fence|emergency exit|work space|cubicle|doorknob|column|skyscraper|demolition|toolshed|barn|cabin|open-plan
crime: use caution|safety equipment|fire extinguisher|emergency exit|protector|repair ticket
chore: repair ticket
neg: overwhelmed|worried|be concerned|unsatisfied|incredulous
ppl: usher|the public|beloved|generation
occ: usher|engineer|artisan|crafter|nutritionist|administrator|transporter|senior partner
move: lean over|look up at|prop against|pin|lean against|unfold|fold up
think: give a thought to|in the know|be aware|make sense|wisdom
deal: agreed-upon|final offer|employment contract|be subject to|secure a deal
''')
L.append('''
qty: run low on|out of|a number of|a sequence of|percentage|excess|abundant|remainder|sufficiently|turnover
room: amenities|ventilation|faucet|awning|prop open|flush|leaking|leak|lodge|lobby|window treatment|drape|valance|redecorate|furnishings|decorated|tastefully|decorator|stall|trailer|erect|demolish|renovated
off: detailed information|fact sheet|request form|serial number|due date|hours of operation|database|catalog|directory|code|duplicate|search|disk|registered mail|overnight mail
ship: logistical|airfreight|charter|seaport|purveyor|merchant|provider|building supplies|bulk discount|subcontract
art: play|folk story|programming|lineup|computer-generated|poem|anthology|stitch|seamstress|soapmaking|representation|creative|elegance
med: clinic|nursing|surgical|dental hygienist|general hospital|MD|diagnostic|primary care|internist|pharmaceuticals|diagnose|protective gear
qual: isolated|central to|weekly|off-season|specialised|independently|commendable|electrified|enhanced|reclinable|renovated|high-profile|commonplace|one-size-fits-all|selective|hardy|personable|easygoing|pleasant-looking|quaint|cloudy|unlocked|outdated|portable|top-of-the-line|costly|added|ideally|open-door|technically|farthest|accidentally|understandable|voided|sturdy|padded|regionally|high-end|imposing|influential|corrupted|failed|inviting|desired|demanding|quoted|respected|forthcoming|headquartered|automated|anticipated|technological|ultramodern|lifelong|charming|superb|mainly|mutually|personally|overcrowded|physically|casually|verbally|commensurate|hesitant|weakly|delicately|flexibly|vested|strictly|essentially|accurately|integral|tedious|cautiously|profitably|aggressively|wisely|conducive|inconsiderately|perceptive|uniformly|systematically|subjective|basic|randomly|disparate|equivalent|deluxe|successive|in-depth|serious|evident|pertinent|productive|enthusiastically|steadily|be suited for|vulnerable to|free of|unfamiliar with|vocational|departmental|recycled|be made of
when: additionally|lately|momentarily|subsequently|long before|at the latest|every other|than usual|on schedule|on-time|on target|on track|fiscal year|advance notice|day shift|on leave|periodically|punctually|lead time|coincide
prep: result from|in turn|for the purpose of|except for|aside from|in fact|first of all|besides|depending on|by contrast|in appreciation of|due to|subject to|regardless|it so happens that|by necessity|apply to|proximity
trip: flock to|flock|make a stop|amusement park|tourist attraction|recreation|excursion|embarkation|check in|escort|fare|have a view of|outdoors|nestle
co: start-up|strategize|headquarter|business-to-business|research and development|legal department|department head|pool|best practice|buy-in|scope|summit|e-commerce|liability|system|tier|protocol
abs: resources|relations|personalisation|customization|familiarity|precision|usefulness|significance|occasion|impression|patience|recognition|preservation|momentum|removal|reinstallation|assurance|provision|fad|inspiration|persuasion|substitution|complication|accomplishment|basis|merit|behavior|discrepancy|reflection|attitude|burden|indicator|compromise|influx|dimension|confusion|thrill|attainment|spectrum|instinct|reason|encouragement|reform|scrutiny|velocity
hr: flight attendant|machinist|CV|on leave|benefits package|recruiting|custodian|auto technician|bachelor|qualifications|training|novice|apprentice|salary|take one's place|take over for|day shift|make a name
geo: continent|province|regionally|seaport
env: megawatt|gigawatt|carbon-reduction|turbine|power grid|diesel|hydrogen-powered|preservation|water supply|sediment|discoloration|water analysis
dev: transformer|outage|artificial intelligence|simulate|serial number|vacuum cleaner|mower|fluid|steering|rotation|navigation|automated|checkout kiosk|database|portable|disk|code
fv: lettuce|spinach|wheat|turkey
dish: sourdough|hummus|turkey|appetizer|refreshment
cook: grill|dip|mix
fit: pool-based|workout|spare time|leisure
pos: admire|be impressed by|thrilled|thrill|excite|look up to
neg: tire|disappoint|irritate|apprehensive|nervously|tempt
do: do a favor|pass on to|fabrication|fabricate|preregistration|familiarize|restrict|fail to|lean toward|opt for|opt to|opt|take a step|reassemble|skip|sanitize|designate|make improvements|minimize|be intended to|take seriously|flourish|look to|set to|slate|can't afford to|pass up|refinance|foster|manage to|stay on top of|bring in|bring together|call in|bargain|diversify|rectify|subtract|deduct|accumulate|build up|reconcile|pull out|give up|withhold|hamper|move up|open to|bring up|go ahead|conform|repel|take back|throw out|ascertain|solve|fluctuate|get out of|accustom to|relinquish|regulate|distinguish|economize|offset|preclude|disperse|constitute|disseminate|specialize|control|continue|abide by|obligate|recur|back up|be ready for|mix|daringly
sense: pay attention to|be mindful of|glimpse|remember|forget|aware
think: remember|forget|aware|be mindful of|aware
rel: socialize with|goer|spouse|mutually
evt: put on|raffle|festivity|banquet room|occasion|summit
hand: rake|line up|crouch down|try on|pass out|stitch|dip
clo: try on|garment|wrinkle|brand|toiletries|pillowcase
furn: pillowcase|toiletries
fly: in-flight|baggage claim|flight attendant|aviation|embarkation
fin: pay a bill|value-added tax|line of credit|venture capital|voucher|dividend|down payment|mortgage|liability|penalty|quart
mkt: market share|price point|sales promotion|bulk discount|retail store|grocery store|promoter|preach|brand|voucher
road: speed limit|passing lane|traffic volume|shoulder|travel lane|barricade
talk: deliver a speech|give a talk|ask for|solicit|petition|verbally|give a ride|preach
gov: authorities|lawmaker|enter into a contract|prohibit|trespass|reform|petition|regulate
deal: enter into a contract|trial period|unsubscribe|at no charge|voided|abide by|obligate|provision|assurance
chr: responsible for|easygoing|personable|patience|creative
crime: trespass|protective gear|penalty
prod: precision|fabrication|fabricate|defect|statistics
sci: statistics|artificial intelligence|velocity
meas: square-metre|megawatt|gigawatt|quart|dimension
plant: flower bed|replant|herb
wea: rainstorm|cloudy
eat: water station|refreshment|appetizer
study: textbook|bachelor|vocational|training|novice|apprentice|instruct
''')
# final corrections (later lines win)
L.append('''
make: consist of
occ: general contractor
furn: walk-in refrigerator|sleeve
socp: make a donation
do: meet the need|turn in|fall to
geo: neighbourhood
fin: boom
get: be sourced
msg: get in touch
when: as needed
shop: sell out
state: heavy
ill: pain
ppl: human
wea: heat
dev: flash
fly: flight|airport|boarding pass|passport|ticket|airline|aircraft
mkt: rating
''')
