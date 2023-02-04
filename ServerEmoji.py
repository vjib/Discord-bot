emoji_code = {}
emoji_code['easy'] = '<:Easy:899486900824465409>'
emoji_code['medium'] = '<:Medium:899486901139017779>'
emoji_code['hard'] = '<:Hard:899486901034164225>'
emoji_code['difficult'] = '<:Difficult:899486901134831626>'
emoji_code['challenging'] = '<:Challenging:899486901160013855>'
emoji_code['intense'] = '<:Intense:975655931734032404>'
emoji_code['remorseless'] = '<:Remorseless:899486901147422780>'
emoji_code['insane'] = '<:Insane:899486901159993364>'
emoji_code['extreme'] = '<:Extreme:899486901206130708>'
emoji_code['terrifying'] = '<:Terrifying:899486901164191764>'
emoji_code['catastrophic'] = '<:Catastrophic:899486901168394300>'
emoji_code['horrific'] = '<:Horrific:977816930230607903>'
emoji_code['unreal'] = '<:Unreal:977816943740465212>'
emoji_code['nil']='<:Nil:1046248521524854815>'
#1023981436056899665
emoji_code['tower rush'] = '<a:Difficultyrainbow:1023981436056899665>'
#emoji_code['tower rush'] = '<a:Difficultyrainbow:1024000863825575956>'
emoji_code['gameplaystar'] = '<:GameplayStar:1009624550000042045>'
emoji_code['goldstar'] = '<:GoldStar:1009624833220423711>'
emoji_code['designstar'] = '<:DesignStar:1009624565812564088>'
emoji_code['creativitystar'] = '<:CreativityStar:1009624820759150663>'
emoji_code['emptystar'] = '<:EmptyStar:1031831101875945502>'
emoji_code['0'] = '0️⃣'
emoji_code['1'] = '1️⃣'
emoji_code['2'] = '2️⃣'
emoji_code['3'] = '3️⃣'
emoji_code['4'] = '4️⃣'
emoji_code['5'] = '5️⃣'
emoji_code['6'] = '6️⃣'
emoji_code['7'] = '7️⃣'
emoji_code['8'] = '8️⃣'
emoji_code['9'] = '9️⃣'
emoji_code['10'] = '🔟'

emoji_code['pass']="<:Pass:1024163702783619194>"
emoji_code['fail']="<:Fail:1024163700619345922>"

emoji_code['0_g'] = "<:0_g:1024150466420027472>"
emoji_code['1_g'] = "<:1_g:1024150468374564934>"
emoji_code['2_g'] = "<:2_g:1024150470207479859>"
emoji_code['3_g'] = "<:3_g:1024150472224935969>"
emoji_code['4_g'] = "<:4_g:1024150474066235422>"
emoji_code['5_g'] = "<:5_g:1024150476163403948>"
emoji_code['6_g'] = "<:6_g:1024150478302494802>"
emoji_code['7_g'] = "<:7_g:1024150480563228742>"
emoji_code['8_g'] = "<:8_g:1024150482463227944>"
emoji_code['9_g'] = "<:9_g:1024150484375838823>"
emoji_code['10_g'] = "<:10_g:1024150486321987657>"
emoji_code['11_g'] = "<:11_g:1024152242091196556>"
emoji_code['12_g'] = "<:12_g:1024152244305793074>"
emoji_code['13_g'] = "<:13_g:1024152246545555577>"
emoji_code['14_g'] = "<:14_g:1024152248806285352>"
emoji_code['15_g'] = "<:15_g:1024152250815361034>"
emoji_code['16_g'] = "<:16_g:1024152253231284314>"
emoji_code['17_g'] = "<:17_g:1024152255391354911>"
emoji_code['18_g'] = "<:18_g:1024152257681428530>"
emoji_code['19_g'] = "<:19_g:1024152259728248892>"
emoji_code['20_g'] = "<:20_g:1024152261959634974>"
emoji_code['21_g'] = "<:21_g:1024152264207769690>"
emoji_code['22_g'] = "<:22_g:1024152266141335563>"
emoji_code['23_g'] = "<:23_g:1024152268129447956>"
emoji_code['24_g'] = "<:24_g:1024152270679593001>"
emoji_code['25_g'] = "<:25_g:1024152272898367508>"

emoji_code['a'] = '🇦'
emoji_code['b'] = '🇧'
emoji_code['c'] = '🇨'
emoji_code['d'] = '🇩'
emoji_code['e'] = '🇪'
emoji_code['f'] = '🇫'
emoji_code['g'] = '🇬'
emoji_code['h'] = '🇭'
emoji_code['i'] = '🇮'
emoji_code['j'] = '🇯'
emoji_code['k'] = '🇰'
emoji_code['l'] = '🇱'
emoji_code['m'] = '🇲'
emoji_code['n'] = '🇳'
emoji_code['o'] = '🇴'
emoji_code['p'] = '🇵'
emoji_code['q'] = '🇶'
emoji_code['r'] = '🇷'
emoji_code['s'] = '🇸'
emoji_code['t'] = '🇹'
emoji_code['u'] = '🇺'
emoji_code['v'] = '🇻'
emoji_code['w'] = '🇼'
emoji_code['x'] = '🇽'
emoji_code['y'] = '🇾'
emoji_code['z'] = '🇿'
emoji_code[' ']='⠀'

#🇦 🇧 🇨 🇩 🇪 🇫 🇬 🇭 🇮 🇯 🇰 🇱 🇲 🇳 🇴 🇵 🇶 🇷 🇸 🇹 🇺 🇻 🇼 🇽 🇾 🇿

def getEmoji(emoji):
  if str(emoji)=='nan':
    return ":grey_question:"
  emoji=emoji.lower()
  if emoji in emoji_code:
    return emoji_code[emoji]
  return emoji

def textToEmoji(text):
  emoji_text=""
  for t in text:
    if t in emoji_code:
      emoji_text+=emoji_code[t]+" "
    else:
      emoji_text+=emoji_code[' ']+" "
  return emoji_text