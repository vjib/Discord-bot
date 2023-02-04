difficulty_to_num={}
difficulty_to_num['effortless']=0
difficulty_to_num['easy']=1
difficulty_to_num['medium']=2
difficulty_to_num['hard']=3
difficulty_to_num['difficult']=4
difficulty_to_num['challenging']=5
difficulty_to_num['intense']=6
difficulty_to_num['remorseless']=7
difficulty_to_num['insane']=8
difficulty_to_num['extreme']=9
difficulty_to_num['terrifying']=10
difficulty_to_num['catastrophic']=11
difficulty_to_num['horrific']=12
difficulty_to_num['unreal']=13
difficulty_to_num['nil']=14

num_to_difficulty=['effortless','easy','medium','hard','difficult','challenging','intense','remorseless','insane','extreme','terrifying','catastrophic','horrific','unreal','nil']

subdifficulty_to_num={}
subdifficulty_to_num['bottom']=0.0
subdifficulty_to_num['bottom-low']=0.11
subdifficulty_to_num['low']=0.22
subdifficulty_to_num['low-mid']=0.33
subdifficulty_to_num['mid']=0.45
subdifficulty_to_num['mid-high']=0.56
subdifficulty_to_num['high']=0.67
subdifficulty_to_num['high-peak']=0.78
subdifficulty_to_num['peak']=0.89

difficulty_color={
    "easy":"#76f447",
    "medium":"#fffe00",
    "hard":"#fe7c00",
    "difficult":"#ff0c03",
    "challenging":"#880015",
    "intense":"#19222d",
    "remorseless":"#ca00ca",
    "insane":"#0000ff",
    "extreme":"#028aff",
    "terrifying":"#01ffff",
    "catastrophic":"#dddddd"
}

difficulty_color_hex = {}
difficulty_color_hex['effortless'] = 0x00CE01
difficulty_color_hex['easy'] = 0x76F447
difficulty_color_hex['medium'] = 0xFFFE02
difficulty_color_hex['hard'] = 0xFE7C00
difficulty_color_hex['difficult'] = 0xFF0C04
difficulty_color_hex['challenging'] = 0xC10000
difficulty_color_hex['intense'] = 0x192832
difficulty_color_hex['remorseless'] = 0xC901C9
difficulty_color_hex['insane'] = 0x0000FF
difficulty_color_hex['extreme'] = 0x0389FF
difficulty_color_hex['terrifying'] = 0x1FFFF
difficulty_color_hex['catastrophic'] = 0xFFFFFF
difficulty_color_hex['horrific'] = 0x9691FF
difficulty_color_hex['unreal'] = 0x4B00C8
difficulty_color_hex['nil'] = 0x797981

subdifficulty_list=['bottom','bottom-low','low','low-mid','mid','mid-high','high','high-peak','peak']
NonSC_difficulty=['easy','medium','hard','difficult','challenging','intense','remorseless']
SC_difficulty=['insane','extreme','terrifying','catastrophic']
SC_nonofficial_difficulty=['horrific','unreal','nil']

def correctSubdifficulty(s):
  if str(s)=='nan':
    return s
  s=s.lower()
  s=s.replace("(baseline)","").strip()
  return s

def correctDifficulty(d):
  if str(d)=='nan':
    return d
  d = d.lower()
  if (d == 'eff'):
    d = 'effortless'
  elif (d == 'eas'):
    d = 'easy'
  elif (d == 'med'):
    d = 'medium'
  elif (d == 'har'):
    d = 'hard'
  elif (d == 'diff' or d == 'dif'):
    d = 'difficult'
  elif (d == 'cha'):
    d = 'challenging'
  elif (d == 'int'):
    d = 'intense'
  elif (d == 'rem'):
    d = 'remorseless'
  elif (d == 'ins'):
    d = 'insane'
  elif (d == 'ext'):
    d = 'extreme'
  elif (d == 'ter' or d == 'terri'):
    d = 'terrifying'
  elif (d == 'cata' or d == 'cat'):
    d = 'catastrophic'
  elif (d == 'hor'):
    d = 'horrific'
  elif (d == 'unr'):
    d = 'unreal'
  return d

def isSC(difficulty):
  return difficulty in SC_difficulty+SC_nonofficial_difficulty

def getNonSCDifficulty():
  return NonSC_difficulty

def getSCDifficulty():
  return SC_difficulty

def getAllDifficulty():
  return NonSC_difficulty+SC_difficulty

def getAllSubDifficulty():
  return subdifficulty_list

def increaseDifficultyLabel(difficulty,step=1):
  dif=correctDifficulty(difficulty)
  if dif not in difficulty_to_num:
    return difficulty

  if not str(step).isnumeric():
    return difficulty

  num=difficulty_to_num[dif]+int(step)
  if num>=len(difficulty_to_num):
    num=len(difficulty_to_num)-1

  return num_to_difficulty[num]

def decreaseDifficultyLabel(difficulty,step=1):
  dif=correctDifficulty(difficulty)
  if dif not in difficulty_to_num:
    return difficulty

  if not str(step).isnumeric():
    return difficulty

  num=difficulty_to_num[dif]-int(step)
  if num<0:
    num=0

  return num_to_difficulty[num]

def getDifficultyLabelByNumber(number):

  try:
    number=float(number)
    
    difficulty_num=int(number)
    subdifficulty_num=number-difficulty_num
  
    difficulty=num_to_difficulty[difficulty_num]
    sorted_dif=list({k: v for k, v in sorted(subdifficulty_to_num.items(), key=lambda item: item[1])}.keys())
  
    subdifficulty=sorted_dif[0]
  
    for sub in sorted_dif:
      if subdifficulty_num>=subdifficulty_to_num[sub]:
      	subdifficulty=sub
     
    return difficulty,subdifficulty
  except Exception as e:
    return None,None

def increaseDifficultyByOne(difficulty,subdifficulty):
  cur_dif=correctDifficulty(difficulty)
  cur_sub_dif=correctSubdifficulty(subdifficulty)

  try:
    point=difficulty_to_num[cur_dif]+subdifficulty_to_num[cur_sub_dif]
    point=point+0.13

    return getDifficultyLabelByNumber(point)
  
  except Exception as e:
    print(e)
    return difficulty,subdifficulty

def decreaseDifficultyByOne(difficulty,subdifficulty):
  cur_dif=correctDifficulty(difficulty)
  cur_sub_dif=correctSubdifficulty(subdifficulty)

  try:
    point=difficulty_to_num[cur_dif]+subdifficulty_to_num[cur_sub_dif]
    point=point-0.01

    return getDifficultyLabelByNumber(point)
  
  except Exception as e:
    return difficulty,subdifficulty

def increaseDifficulty(difficulty,subdifficulty,step=1):
  cur_dif=correctDifficulty(difficulty)
  cur_sub_dif=correctSubdifficulty(subdifficulty)

  try:
    for k in range(int(step)):
      cur_dif,cur_sub_dif=increaseDifficultyByOne(cur_dif,cur_sub_dif)
    return cur_dif,cur_sub_dif
  
  except Exception as e:
    return difficulty,subdifficulty

def decreaseDifficulty(difficulty,subdifficulty,step=1):
  cur_dif=correctDifficulty(difficulty)
  cur_sub_dif=correctSubdifficulty(subdifficulty)

  try:
    for k in range(int(step)):
      cur_dif,cur_sub_dif=decreaseDifficultyByOne(cur_dif,cur_sub_dif)
    return cur_dif,cur_sub_dif
  
  except Exception as e:
    return difficulty,subdifficulty

def getColor(difficulty):
  dif=correctDifficulty(difficulty)
  if dif not in difficulty_color:
    return "#000000"

  return difficulty_color[dif]

def getColorHex(difficulty):
  dif=correctDifficulty(difficulty)
  if dif not in difficulty_color_hex:
    return 0x000000

  return difficulty_color_hex[dif]


  
  