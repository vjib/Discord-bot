import discord
import asyncio

from discord.ext import commands, tasks
from discord.ext.commands import has_permissions, MissingPermissions
from discord.utils import get

#from webserver import keep_alive

import urllib.parse
from urllib.request import urlopen

import matplotlib
import matplotlib.pyplot as plt

from PIL import Image, ImageOps, ImageFilter, ImageDraw, ImageFont, ImageColor

from googleapiclient.discovery import build

import re

import os
import json
import csv

import operator

import requests
import io
from io import BytesIO
from bs4 import BeautifulSoup

import pandas as pd
import numpy as np
import math
import random

import time
from datetime import date, datetime, timedelta
import dateutil.parser
import textwrap

import string
from string import ascii_letters

#import nltk
#from nltk.corpus import stopwords
#nltk.download('stopwords')
#nltk.download('punkt')
#from nltk.corpus import stopwords
#from nltk.tokenize import word_tokenize

#from keras.layers import LSTM

#import bot_commands.test

import database_handler as db_handler

import JToHDifficulties
import ServerEmoji as emoji
import ServerNNModel as NNModel

from wonderwords import RandomWord

bot_id = os.environ['BOT_ID']
bot_channel_id = os.environ['BOT_CHANNEL_ID']
bot_channel_alt_id = os.environ['BOT_CHANNEL_ALT_ID']
bot_channel_premium_id = os.environ['BOT_CHANNEL_PREMIUM_ID']
document_channel_id = os.environ['DOCUMENT_CHANNEL_ID']
guide_channel_id = os.environ['GUIDE_CHANNEL_ID']
bot_status_channel_id = os.environ['BOT_STATUS_CHANNEL_ID']
leaderboard_channel_id = os.environ['LEADERBOARD_CHANNEL_ID']
jtoh_leaderboard_channel_id = os.environ['JTOH_LEADERBOARD_CHANNEL_ID']
guessing_leaderboard_channel_id = os.environ['GUESSING_LEADERBOARD_CHANNEL_ID']
update_log_channel_id = os.environ['UPDATE_LOG_CHANNEL_ID']
server_id = os.environ['SERVER_ID']
owner_id = os.environ['OWNER_ID']
tower_info_url = os.environ['TOWER_INFO_URL']
tower_color_url = os.environ['TOWER_COLOR_URL']
tower_area_code_url = os.environ['TOWER_AREA_CODE_URL']
tower_detail_url = os.environ['TOWER_DETAIL_URL']
badge_info_url = os.environ['BADGE_INFO_URL']
official_difficulty_url = os.environ['JTOH_OFFICIAL_DIFFICULTY_URL']
jtoh_real_time_role_id = os.environ['JTOH_REAL_TIME_ROLE_ID']

youtube_api_key = os.environ['YOUTUBE_API_KEY']
youtube_channel_id = os.environ['YOUTUBE_CHANNEL_ID']
youtube_sub_channel_id = os.environ['YOUTUBE_SUB_CHANNEL_ID']
youtube_view_channel_id = os.environ['YOUTUBE_VIEW_CHANNEL_ID']
youtube_api = build('youtube', 'v3', developerKey=youtube_api_key)

level_1_role_id = os.environ['LEVEL_1_ROLE_ID']

root_tmp_path = "image/temp/"
"""
password_input = input("Password: ")
if password_input!=os.environ['PASSWORD']:
  exit()
"""

active_mode = 1

is_drawing = 0

prefix = '?crp?'

#bot = commands.Bot(command_prefix=prefix)  #Define Prefix

intents = discord.Intents.all()
intents.message_content = True

#client = discord.Client(intents=intents)
bot = discord.Bot(intents=intents, help_command=commands.DefaultHelpCommand())

tower_re = '((T|C|S)o[a-zA-Z][a-zA-Z]?[a-zA-Z]?[a-zA-Z]?|[a-zA-Z]+AT|TT)'
subdifficulty_re = '(baseline|bottom|baseline-low|bottom-low|low|low-mid|mid|mid-high|high|high-peak|peak)'
difficulty_re = '(effortless|easy|medium|hard|difficult|diff|challenging|intense|remorseless|rem|insane|extreme|terri|terrifying|cata|catastrophic|horrific|unreal|nil)'

df_info = pd.read_csv(tower_info_url)
df_area = pd.read_csv(tower_area_code_url)
df_badge = pd.read_csv(badge_info_url)
df_progress = pd.read_csv(tower_detail_url + "Progression%20route")
df_feature = pd.read_csv(tower_detail_url + "Features")
df_perdif = pd.read_csv(tower_detail_url + "Personal%20raw%20difficulty")
df_feature_code = pd.read_csv(tower_detail_url + "Features%20raw%20info")
df_color_label = pd.read_csv(tower_color_url + "Label")
df_color_colors = pd.read_csv(tower_color_url + "Colors")

feature_code = {}


async def refreshData():

    global df_info
    global df_area
    global df_badge
    global df_progress
    global df_feature
    global df_perdif
    global df_feature_code
    df_info = pd.read_csv(tower_info_url)
    df_area = pd.read_csv(tower_area_code_url)
    df_badge = pd.read_csv(badge_info_url)
    df_progress = pd.read_csv(tower_detail_url + "Progression%20route")
    df_feature = pd.read_csv(tower_detail_url + "Features")
    df_perdif = pd.read_csv(tower_detail_url + "Personal%20raw%20difficulty")
    df_feature_code = pd.read_csv(tower_detail_url + "Features%20raw%20info")


async def checkAdmin(message):
    user_id = message.author.id
    if (str(user_id) == str(owner_id)):
        return True
    return False


async def checkAuthen(message):
    user_id = message.author.id
    guild = message.guild.id

    if str(guild) != str(server_id):
        return False

    if active_mode == 0:
        return False
    elif str(user_id) == str(bot_id):
        return False

    return True


async def isBotChannel(message):
    channel_id = message.channel.id
    #print(channel_id)
    #print(message.channel.type)
    #print(message.channel.parent_id)
    #print(str(bot_channel_premium_id))

    if str(channel_id) == str(bot_channel_id) or str(channel_id) == str(
            bot_channel_alt_id
    ) or str(channel_id) == str(bot_channel_premium_id) or (
            str(message.channel.type) == 'public_thread'
            and str(message.channel.parent_id) == str(bot_channel_premium_id)):
        return True
    return False


async def hacking_handler(ctx):
    user_id = ctx.author.id
    print(user_id + " is trying to hack me!!!")


async def filtering_input(ctx, input):

    #if input.index("@")>=0:
    #await hacking_handler(ctx)
    #await ctx.send("c!warns <@" + str(user_id) + ">")

    if not re.match("^[a-zA-Z0-9_-]*$", input):
        #input = ""
        input = re.sub("[^a-zA-Z0-9_-]", "", input)
    return input[0:30]


async def filtering_input_with_space(ctx, input):

    #if input.index("@")>=0:
    #await hacking_handler(ctx)
    #await ctx.send("c!warns <@" + str(user_id) + ">")

    if not re.match("^[a-zA-Z0-9_ ]*$", input):
        input = re.sub("[^a-zA-Z0-9_]", "", input)
    return input[0:50]


async def filtering_message(message):
    new_message = message.translate(
        message.maketrans('', '', string.punctuation.replace(",", "")))
    """
  text_tokens = word_tokenize(new_message)

  tokens_without_sw = [word for word in text_tokens if not word in stopwords.words('english')]

  new_message=' '.join(tokens_without_sw)
  """

    return new_message.replace("@", "").replace("?", "").replace(
        "!", "").replace("I think", "").replace("i think", "").replace(
            "For me",
            "").replace("for me",
                        "").replace("imo", "").replace("everyone",
                                                       "").replace("Crp",
                                                                   "").strip()


async def noUsernameFound(username):
    error_list = [
        "Who is **{}**? eo who thinks ToBK is insane but ToPP is cata?",
        "Who is **{}**? eo who thinks ToTL is rem but ToFaCT is extreme?",
        "Who is **{}**? eo who thinks ToSO is really harder than ToEI?",
        "Who is **{}**? eo who thinks ToSM is really harder than ToBK?",
        "Who is **{}**? eo who cried when ToEI was terrifying?",
        "Who is **{}**? eo who can't beat ToIB because it has COs?"
    ]
    error = random.choice(error_list)
    return error.format(username)


async def correctTowerCaseSensitive(tower):
    new_tower = tower[0].upper() + tower[1].lower() + tower[2:len(tower
                                                                  )].upper()
    return new_tower


async def noTowerFound(tower):
    error_list = [
        "What is **" + tower +
        "**? A new JToH building that curators said it is bland without playing it?",
        "What is **" + tower +
        "**? A new JToH building that curators hardfailed after seeing 1 misalignment?",
        "What is **" + tower +
        "**? A new JToH building that curators like because it has good design, but has bad gameplay?",
        "What is **" + tower +
        "**? A new JToH building that curators failed it because they were too lazy to playtest?",
        "What is **" + tower +
        "**? A new JToH building that curators love because it is unsightreadable?",
        "What is **" + tower +
        "**? A new JToH building that curators stole it from AToS?"
    ]
    error = random.choice(error_list)
    return error.format(tower)


async def hasTowerInMessage(message):
    RE_checker = re.compile('.*' + tower_re + '.*')

    match_checker = RE_checker.search(message)
    if match_checker:
        return True
    return False


"""
async def provideTowerGuide(ctx,filtered_message):

  user_id = ctx.author.id
  
  RE_checker = re.compile('[a-zA-Z0-9]*(h|H)ow to beat ' + tower_re + '(\?)?$')

  match_checker = RE_checker.search(filtered_message)

  words = str(filtered_message).split(" ")
  
  if match_checker and words[-1] in df_info['Acronym'].values:
    try:
      url = df_info[df_info['Acronym'] == words[-1]]['Video URL'].values[0]
      await ctx.channel.send(
                '<@' + str(user_id) + '>, you can check guide on ' +
                words[-1] + ' via this link -> ' + url
        )  #Respond message
      return True
    except:
      await ctx.channel.send(
                '<@' + str(user_id) +
                '>, NOOOOOO!!!!!! I don\'t have a guide on ' +
                words[-1])
      return True
  return False

async def provideTowerDifficulty(ctx,filtered_message):


  RE_checker = re.compile(
        '[a-zA-Z0-9_ ]*((d|D)ifficulty) (of) ' +
        tower_re + '$')
  match_checker = RE_checker.search(filtered_message)

  user_id = ctx.author.id
  words = str(filtered_message).split(" ")
  
  if match_checker and words[-1] in df_info['Acronym'].values:
    try:
      cur_subdif = df_info[df_info['Acronym'] == words[-1]]['Sub difficulty'].values[0]
      cur_dif = df_info[df_info['Acronym'] == words[-1]]['Difficulty'].values[0]
      await ctx.channel.send('<@' + str(user_id) + '> Current difficulty of ' +
                                       words[-1] + ' is ' +
                                       cur_subdif + ' ' + emoji_code[cur_dif]
                                       )  #Respond message
    except:
      await ctx.channel.send(
                '<@' + str(user_id) +
                '> I don\'t know the difficulty of ' +
                words[-1])
    try:          
      dif = df_info[df_info['Acronym'] == words[-1]]['Personal difficulty'].values[0]
      sub_dif = df_info[df_info['Acronym'] == words[-1]]['Personal sub difficulty'].values[0]
      await ctx.channel.send('I think ' +
                                       words[-1] + ' is ' +
                                       sub_dif + ' ' + emoji_code[dif]
                                       )  #Respond message
    except:
      await ctx.channel.send(
                'I have no opinion about the difficulty on ' +
                words[-1])
    try:
      com_dif = df_info[df_info['Acronym'] == words[-1]]['Communal difficulty'].values[0]
      com_sub_dif = df_info[df_info['Acronym'] == words[-1]]['Communal sub difficulty'].values[0]
      await ctx.channel.send(
                'Most people think ' + words[-1] + ' is ' +
                com_sub_dif + ' ' + emoji_code[com_dif])  #Respond message
    except:
      await ctx.channel.send(
                'and I don\'t know what people think about ' +
                words[-1])
    return True
  else:
    return False

async def provideTowerFullName(ctx,filtered_message):

  user_id = ctx.author.id
  words = str(filtered_message).split(" ")
  
  RE_checker = re.compile(
        '[a-zA-Z0-9_ ]*(W|w)hat[a-zA-Z0-9_ ]*(is |s )' + tower_re + '(\?)?$')
  match_checker = RE_checker.search(filtered_message)
  if match_checker and words[-1] in df_info['Acronym'].values:
    tower_full_name = df_info[df_info['Acronym'] == words[-1]]['Tower'].values[0]
    await ctx.channel.send('<@' + str(user_id) + '> ' + tower_full_name
                                   )  #Respond message
    return True
  return False

async def provideTowerPlaytime(ctx,filtered_message):

  user_id = ctx.author.id
  words = str(filtered_message).split(" ")
  
  RE_checker = re.compile(
        '[a-zA-Z0-9_ ]*((h|H)ow long)[a-zA-Z0-9_ ]*(beat)[a-zA-Z0-9_ ]*' +
        tower_re + '(\?)?$')
  match_checker = RE_checker.search(filtered_message)
  if match_checker and words[-1] in df_info['Acronym'].values:
    try:
      normal_playtime = df_info[df_info['Acronym'] == words[-1]]['Average normal playtime (minute)'].values[0]
      speedrun_playtime = df_info[
                df_info['Acronym'] == words[-1]]['Average speedrun playtime (minute)'].values[0]
      await ctx.channel.send(
                '<@' + str(user_id) + '> Most people should beat ' +
                words[-1] + ' in **' +
                str(int(normal_playtime)) + '** minutes')  #Respond message
      await ctx.channel.send(
                'unless you try to speedrun ' + words[-1] +
                ' you should take **' + str(int(speedrun_playtime)) +
                '** minutes to beat it')  #Respond message
    except:
      await ctx.channel.send('<@' + str(user_id) +
                                       '> I have no information about ' +
                                       words[-1])
    return True
  return False

async def provideTowerLocation(ctx,filtered_message):

  user_id = ctx.author.id
  words = str(filtered_message).split(" ")
  
  RE_checker = re.compile(
        '[a-zA-Z0-9_ ]*(W|w)here[a-zA-Z0-9_ ]*' + tower_re + '(\?)?$')
  match_checker = RE_checker.search(filtered_message)
  if match_checker and words[-1] in df_info['Acronym'].values:
    tower_location = df_info[df_info['Acronym'] == words[-1]]['Location'].values[0]
    tower_location_number = df_info[
            df_info['Acronym'] == words[-1]]['Location number'].values[0]
    tower_location_type = df_info[df_info['Acronym'] == words[-1]]['Location type'].values[0]
    if (df_info[df_info['Acronym'] == words[-1]]['Accessible'].values[0]=='y'):
      return
    if (tower_location == 'ring' or tower_location == 'zone'):
      subrealm_text = ''
    if (tower_location_type == 'subrealm'):
      subrealm_text = 'subrealm of '
    await ctx.channel.send(
                '<@' + str(user_id) + '> ' + words[-1].replace('?', '') +
                ' is in ' + subrealm_text + tower_location + ' ' +
                str(int(tower_location_number)))  #Respond message
    return True
  return False

"""


async def checkUnderrating(ctx, filtered_message):

    user_id = ctx.author.id
    words = str(filtered_message).split(" ")

    RE_checker = re.compile(tower_re + ' (is )?' + subdifficulty_re + '?( )?' +
                            difficulty_re + '( [a-zA-Z]*)?$')
    match_checker = RE_checker.search(filtered_message)
    if match_checker and words[0] in df_info['Acronym'].values:
        try:
            mem_difficulty = JToHDifficulties.correctDifficulty(words[-1])

            mem_difficulty_code = JToHDifficulties.difficulty_to_num[
                mem_difficulty]
            current_difficulty = df_info[df_info['Acronym'] ==
                                         words[0]]['Difficulty'].values[0]
            current_difficulty_code = JToHDifficulties.difficulty_to_num[
                current_difficulty]

            if mem_difficulty_code < current_difficulty_code:
                respond_list = [
                    "eo", "based", "Stop underrating " + words[0] + "!"
                ]
                respond = random.choice(respond_list)
                await ctx.channel.send('<@' + str(user_id) + '> ' + respond
                                       )  #Respond message
            elif mem_difficulty_code >= current_difficulty_code + 2:
                respond_list = [
                    "reverse eo", "based", "Stop overrating " + words[0] + "!"
                ]
                respond = random.choice(respond_list)
                await ctx.channel.send('<@' + str(user_id) + '> ' + respond
                                       )  #Respond message
        except:
            return False
        return True
    else:
        return False


async def checkTowerComment(ctx, filtered_message):
    user_id = ctx.author.id
    words = str(filtered_message).split(" ")

    RE_checker = re.compile(tower_re + ' ((is )?(([a-zA-Z])* )?)?(bad|sucks)$')
    match_checker = RE_checker.search(filtered_message)
    if match_checker and words[0] in df_info['Acronym'].values:
        try:
            dialogue_list = [
                "Skill issues", "No you bad",
                "Quit JToH and play Mega Fun Obby"
            ]
            dialogue = random.choice(dialogue_list)
            await ctx.channel.send('<@' + str(user_id) + '> ' + dialogue
                                   )  #Respond message
        except:
            return False
        return True
    else:
        return False


async def printTowerImage(tower):
    #tower=await correctTowerCaseSensitive(tower)

    info = df_info[df_info['Acronym'].str.lower() == tower.lower()]

    if info.shape[0] > 0:
        full_name = info.iloc[0]['Tower']

        tower_url = full_name.title().replace(" ", "_").replace(
            "Of", "of").replace("And", "and").replace("\'S", "\'s")

        URL = "https://jtoh.fandom.com/wiki/" + tower_url
        URL = URL.replace("?", "%3F")

        page = requests.get(URL, timeout=5)

        if (page.status_code != 200):
            return 1, root_tmp_path + "question.jpg"
        else:
            soup = BeautifulSoup(page.content, "html.parser")
            image = soup.find_all('img', {'class': 'pi-image-thumbnail'})
            img_url = image[0].get('src')
            #img_url=image[0].get('src').split(".png",1)[0]+".png"
            #print(img_url)
            return -1, img_url

    else:
        return 0, None


async def getTowerColorsFromURL(tower):

    floor_list = []

    info = df_info[df_info['Acronym'].str.lower() == tower.lower()]

    if info.shape[0] > 0:
        full_name = info.iloc[0]['Tower']
        tower_url = full_name.title().replace(" ", "_").replace(
            "Of", "of").replace("And", "and").replace("\'S", "\'s")

        URL = "https://jtoh.fandom.com/wiki/" + tower_url

        page = requests.get(URL, timeout=5)

        if (page.status_code != 200):
            return floor_list
        else:
            soup = BeautifulSoup(page.content, "html.parser")
            try:

                floor_table = soup.findAll(
                    'span', id=['Floor_Colors', 'Floor_Colours'])

                floor_table = floor_table[0].parent.findNext(
                    'table', {'class': 'wikitable'})

                #print(floor_table)

                for element in floor_table.findAll('th'):
                    if (element.has_attr('style')):
                        label = element.getText().replace("\n", "")
                        style_tag = element['style']

                        if (str(style_tag).find('background') != -1):
                            color_pivot = str(style_tag).index('#')
                            color = str(style_tag)[color_pivot +
                                                   1:color_pivot + 7]

                            #floor_list.append((label,color))
                            floor_list.append(color)

                total_floor = int(info.iloc[0]['Floors'])

                if (len(floor_list) == 1 and total_floor > len(floor_list)):
                    pivot_color = floor_list[0]
                    floor_list = []
                    for k in range(total_floor):
                        floor_list.append(pivot_color)

            except:
                return floor_list

    return floor_list


async def getTowerColors(tower):

    floor_list = []

    colors = df_color_colors[df_color_colors['Acronym'].str.lower() ==
                             tower.lower()]

    if colors.shape[0] > 0:
        raw_list = colors.values.tolist()[0]
        raw_list.pop(0)

        for color in raw_list:
            if str(color) != 'nan':
                floor_list.append(color[1:7])
    else:
        return await getTowerColorsFromURL(tower)

    return floor_list


def get_concat_v(im1, im2):
    dst = Image.new('RGB', (im1.width, im1.height + im2.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (0, im1.height))
    return dst


def generatetowerfromcolors(floor_list):
    tower_img_template = None
    for floor in floor_list:
        color_url = "https://singlecolorimage.com/get/" + floor + "/25x25"

        img = Image.open(requests.get(color_url, stream=True).raw)
        if not tower_img_template:
            tower_img_template = img
        else:
            tower_img_template = get_concat_v(tower_img_template, img)
    return tower_img_template


async def printTowerColors(ctx, tower, difficulty='e'):

    #tower=await correctTowerCaseSensitive(tower)
    """
    global is_drawing
    is_drawing = 1
    """
    floor_list = await getTowerColors(tower)

    if len(floor_list) > 0:
        if difficulty == 'h':
            random.shuffle(floor_list)

        tempfilename = root_tmp_path + "tempimagecolors" + tower + ".png"
        tower_img_template = generatetowerfromcolors(reversed(floor_list))

        #await ctx.send(color_url)
        #time.sleep(0.75)
        """
    img = Image.open(requests.get(img_url, stream=True).raw)
      tempfilename="tempimage"+tower+".png"
      #img = img.filter(ImageFilter.GaussianBlur(5))
      width, height = img.size
      small_img=img.resize((25,25),Image.BILINEAR)
      img=small_img.resize((width, height),Image.NEAREST)
      img = img.save(tempfilename)
      await ctx.respond("<@"+str(user_id)+"> OK pls tell me the acronym       of the tower in image",file=discord.File(tempfilename))
      os.remove(tempfilename)
    """
        tower_img_template = tower_img_template.save(tempfilename)
        await ctx.send(
            file=discord.File(fp=tempfilename, filename="towercolors.png"))

        #print(tempfilename)

        os.remove(tempfilename)

        is_drawing = 0
        return -1

    is_drawing = 0
    return -99


async def getTowerPlaylist(ctx, tower):

    music_list = []

    info = df_info[df_info['Acronym'].str.lower() == tower.lower()]

    if info.shape[0] > 0:
        full_name = info.iloc[0]['Tower']
        tower_url = full_name.title().replace(" ", "_").replace(
            "Of", "of").replace("And", "and").replace("\'S", "\'s")

        URL = "https://jtoh.fandom.com/wiki/" + tower_url
        URL = URL.replace("?", "%3F")

        page = requests.get(URL, timeout=5)

        if (page.status_code != 200):
            return music_list
        else:
            soup = BeautifulSoup(page.content, "html.parser")
            #print(soup)
            try:

                floor_table = soup.findAll('span', id=['Music'])

                floor_table = floor_table[0].parent.findNext(
                    'table', {'class': 'wikitable'})

                #print(floor_table)

                for element in floor_table.findAll('a'):
                    music_name = element.text
                    music_url = element['href']
                    #print(music_name,music_url)
                    music_list.append((music_name, music_url))

            except:
                return music_list

    return music_list


async def beating_message(message):

    filtered_message = message.content.replace("?", "").replace(
        "!", "").replace("I think", "").replace("i think", "").replace(
            "For me", "").replace("for me",
                                  "").replace("everyone",
                                              "").replace("Crp", "").strip()

    user_id = message.author.id

    words = str(filtered_message).split(" ")

    RE_beat = re.compile('(i|I) (finally )?beat ' + tower_re + '(!)*$')
    match_beat = RE_beat.search(filtered_message)
    if match_beat and words[-1] in df_info['Acronym'].values:

        info = df_info[df_info['Acronym'] == words[-1]].iloc[0]
        difficulty = info['Difficulty']

        if difficulty != 'unreal' and difficulty != 'horrific' and difficulty != 'nil' and difficulty != 'toohard':
            await message.channel.send('<@' + str(user_id) + '> GG!'
                                       )  #Respond message
            await asyncio.sleep(2)
            await message.channel.send('Finally you beat ' + words[-1] +
                                       ' :smile:')  #Respond message
        else:
            await message.channel.send('<@' + str(user_id) +
                                       '> I don\'t believe you!'
                                       )  #Respond message
            await asyncio.sleep(2)
            await message.channel.send('You didn\'t really beat ' + words[-1] +
                                       ' :rage:')


@bot.event
async def on_ready():  #Ready State
    print("Bot Started!")  #Show in CMD
    updateserverclock.start()
    checkforupdate.start()
    updateYoutubeStat.start()
    updatejtohleaderboard.start()
    updateleaderboard.start()
    updateguessingleaderboard.start()


@bot.event
async def on_message(ctx):  #Detect Chat messages

    role = discord.utils.get(ctx.guild.roles, name="Muted")
    if role and ctx and ctx.author and ctx.author.roles and role in ctx.author.roles:
        await ctx.delete()
        #await ctx.channel.send("<@" + str(user_id) + "> You are muted. You have no power here!")
        return

    if (not await checkAdmin(ctx) and not await checkAuthen(ctx)):
        return

    user_id = ctx.author.id
    guild = ctx.guild.id
    """ 
    if (message.content.startswith(prefix) and (await checkAdmin(message) or await isBotChannel(message))):
      print("test2")
      await bot.process_commands(message)
      return
    """

    filtered_message = await filtering_message(ctx.content)

    words = str(filtered_message).split(" ")

    await beating_message(ctx)

    checker_flag = 0

    #print(message.content)

    if (await hasTowerInMessage(filtered_message)):
        """
      if (checker_flag ==0 and await provideTowerGuide(message,filtered_message)):
        checker_flag=1
      elif (checker_flag ==0 and await provideTowerDifficulty(message,filtered_message)):
        checker_flag=1
      elif (checker_flag ==0 and await provideTowerFullName(message,filtered_message)):
        checker_flag=1
      elif (checker_flag ==0 and await provideTowerPlaytime(message,filtered_message)):
        checker_flag=1
      elif (checker_flag ==0 and await provideTowerLocation(message,filtered_message)):
        checker_flag=1
      """
        if (checker_flag == 0
                and await checkUnderrating(ctx, filtered_message)):
            checker_flag = 1
        elif (checker_flag == 0
              and await checkTowerComment(ctx, filtered_message)):
            checker_flag = 1
        else:
            RE_fell = re.compile(
                '[a-zA-Z0-9_ ]*(i|I) (fell|failed)[a-zA-Z0-9_ ]*(floor )?[0-9][0-9]?(a|b|c|A|B|C)?( of)?( )?[a-zA-Z0-9_ ]*'
            )

            match_fell = RE_fell.search(filtered_message)
            if match_fell:
                await ctx.channel.send('<@' + str(user_id) + '> RIP!'
                                       )  #Respond message
    else:

        RE_dc = re.compile(
            '(i|I) [a-zA-Z0-9_]* (disconnected|dc|GBJ|gbj|died)[a-zA-Z0-9_ !]*'
        )
        match_dc = RE_dc.search(filtered_message)
        if match_dc:
            await ctx.channel.send('<@' + str(user_id) + '> RIP!'
                                   )  #Respond message
        RE_ball = re.compile('(I|i) love ball(s)?')
        match_ball = RE_ball.search(filtered_message)
        if match_ball:
            await ctx.channel.send('<@' + str(user_id) + '> I love balls too'
                                   )  #Respond message

        RE_deadchat = re.compile(
            '.*(((d|D)e(a)?d chat)|((c|C)hat de(a)?d))( )?[a-zA-Z]*$')
        match_deadchat = RE_deadchat.search(filtered_message)
        if match_deadchat:
            await ctx.channel.send('RIP **CRP LAND 2022-' +
                                   str(date.today().year) + '**'
                                   )  #Respond message

        RE_sexy = re.compile('.*(sexy).*')
        match_sexy = RE_sexy.search(filtered_message)
        if match_sexy:
            await ctx.channel.send("I'm sexy and I know it")  #Respond message

        RE_meow = re.compile('(Meow|meow)')
        match_meow = RE_meow.search(filtered_message)
        if match_meow:
            await ctx.channel.send("Meow~")  #Respond message

        RE_hi = re.compile('^(hi|Hi|hello|Hello|hey|Hey)$')
        match_hi = RE_hi.search(filtered_message)
        if match_hi:
            await ctx.channel.send(filtered_message)  #Respond message


async def precheck(ctx):
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    if role in ctx.author.roles:
        return False
    return await checkAdmin(ctx) or await isBotChannel(ctx)
    #return await isBotChannel(ctx)


async def noPermission(ctx):
    await ctx.respond("Oh no! You can only run this command in <#" +
                      str(bot_channel_id) + "> (You also need <@&" +
                      level_1_role_id + "> role)")


@bot.command(guild_ids=[server_id], description="For command testing")
@commands.has_role("Crp")
async def test(ctx, tower):
    if (not await precheck(ctx)):
        await noPermission(ctx)
        return

    floor_list = await getTowerColorsTest(tower)
    floor_list2 = await getTowerColors(tower)

    print(floor_list)
    print(floor_list2)


@bot.command(guild_ids=[server_id],
             description="Admin can talk via this command")
#@commands.has_permissions(administrator=True)
@commands.has_role("Crp")
async def talk(ctx, text):

    #text=await filtering_message(text)
    if await checkAdmin(ctx):
        await ctx.send(text)


@bot.command(guild_ids=[server_id],
             description="Admin can reply via this command")
#@commands.has_permissions(administrator=True)
@commands.has_role("Crp")
async def reply(ctx, text, message_id):

    #text=await filtering_message(text)
    if await checkAdmin(ctx):
        channel_id = ctx.channel.id
        channel = bot.get_channel(int(channel_id))
        msg = await channel.fetch_message(int(message_id))
        await msg.reply(text)


@bot.command()
@commands.has_role("Crp")
async def slowmode(ctx, seconds: int):
    await ctx.channel.edit(slowmode_delay=seconds)
    await ctx.respond(
        f"Yay! I have changed the slowmode of this channel to **{seconds}** seconds"
    )


@bot.command()
#@commands.has_permissions(administrator=True)
@commands.has_role("Moderator")
async def forceshutdown(ctx):

    user_id = ctx.author.id

    await ctx.respond("NOOOOOO!!!!!! <@" + str(user_id) + ">  is killin...")
    await asyncio.sleep(2)
    await ctx.send("*died")
    global active_mode
    active_mode = 0


@bot.command()
#@commands.has_permissions(administrator=True)
@commands.has_role("Moderator")
async def forcestart(ctx):
    await ctx.respond("Oh")
    await asyncio.sleep(2)
    await ctx.send("Someone woke me up")
    global active_mode
    active_mode = 1


@bot.command()
#@commands.has_permissions(administrator=True)
@commands.has_role("Moderator")
async def forcerefresh(ctx):
    await ctx.defer()
    await refreshData()
    await ctx.respond("Yay!")
    await asyncio.sleep(2)
    await ctx.send("I learned new things about JToH")


@bot.command()
@commands.has_role("Crp")
async def feedtowerdetails(ctx):
    await ctx.defer()
    db_handler.feedTowerDetails()
    await ctx.respond("The difficulty points are updated!")


@bot.command()
@commands.has_role("Crp")
async def exporttrainingdata(ctx):
    await ctx.defer()
    data = db_handler.getAllTowerBeatenForTraining()

    # Header row
    header = ['user_id', 'acronym', 'date_beaten']
    # Open the file in write mode
    index = 0

    user_id_map = {}

    with open('output/training_data.csv', 'w', newline='') as csvfile:
        # Create a CSV writer object
        writer = csv.writer(csvfile)

        # Write the header row
        writer.writerow(header)

        # Write each tuple to the CSV file
        for row in data:
            row_refined = list(row)
            user_id = row_refined[0]

            if not user_id in user_id_map:
                user_id_map[user_id] = index
                index += 1

            row_refined[0] = user_id_map[user_id]
            writer.writerow(row_refined)

    await ctx.respond("Successfully export training data")


@bot.command()
#@commands.has_permissions(administrator=True)
@commands.has_role("Crp")
async def gettowerinfo(ctx, tower):
    tower = await filtering_input(ctx, tower)
    info = df_info[df_info['Acronym'] == tower].iloc[0]
    await ctx.send(info)


@bot.command(guild_ids=[server_id], description='Show help menu')
#@commands.has_permissions(administrator=True)
async def help(ctx):

    if (not await precheck(ctx)):
        await noPermission(ctx)
        return

    embed = discord.Embed(
        title="Welcome to Crp Junior Bot",
        description=
        "Hi! I know everything about JToH, please feel free to ask me anything",
        color=discord.Color.blue())

    embed.add_field(name="List of commands",
                    value="Check it in <#" + str(document_channel_id) + ">",
                    inline=False)

    embed.add_field(name="Terms and conditions",
                    value="Check it in <#" + str(document_channel_id) + ">",
                    inline=False)

    embed.add_field(
        name="Disclaimer",
        value=
        "Some data sources come from external website e.g. fandom, Roblox. I do not own some of the data generated by the bot",
        inline=False)

    embed.add_field(
        name="Credit to",
        value=
        "JToH wiki page\nhttps://jtoh.fandom.com/wiki/Juke%27s_Towers_of_Hell_Wiki\nRoblox API\nhttps://api.roblox.com/",
        inline=False)

    await ctx.respond(embed=embed)


async def getPlayerIdByUsername(username):

    userid = None

    cache = db_handler.getUserInfo(username)

    if len(cache) > 0:
        return cache[0][1]

    username_checker_url = "https://api.roblox.com/users/get-by-username?username=" + str(
        username)
    username_response = urlopen(username_checker_url)

    username_json = json.loads(username_response.read())

    if 'Id' in username_json:
        userid = username_json['Id']
        db_handler.updateUserId(username, userid)

    return userid


async def getPlayerBadgeByTower(username, tower):

    status = "ok"
    badge_json = []

    userid = await getPlayerIdByUsername(username)

    result = db_handler.getTowerBeaten(username, tower)

    if len(result) > 0:
        cache_list = {}
        cache_list['data'] = []

        badge_id = df_badge[(df_badge['Category'] == 'Beating Tower')
                            & (df_badge['Value 1'].str.lower() ==
                               tower.lower())].iloc[0]['Badge ID']

        date_beaten = result[0][2]

        cache_list['data'].append({
            'badgeId': badge_id,
            'awardedDate': date_beaten
        })

        #print("Using cache")
        #print(cache_list)

        return status, cache_list

    if not userid:
        status = "no user found"
        return status, badge_json

    info = df_badge[(df_badge['Category'] == 'Beating Tower')
                    & (df_badge['Value 1'].str.lower() == tower.lower())]

    if info.shape[0] > 0:
        info = info.iloc[0]
        badgeid = int(info['Badge ID'])
        tower_acronym = info['Value 1']

        badge_checker_url = "https://badges.roblox.com/v1/users/" + str(
            userid) + "/badges/awarded-dates?badgeIds=" + str(badgeid)
        badge_response = urlopen(badge_checker_url, timeout=5)
        badge_json = json.loads(badge_response.read())

        badgeid_old = info['Badge ID Old']

        if badgeid_old and str(badgeid_old) != 'nan':
            badge_checker_url = "https://badges.roblox.com/v1/users/" + str(
                userid) + "/badges/awarded-dates?badgeIds=" + str(
                    int(badgeid_old))
            badge_response = urlopen(badge_checker_url, timeout=5)
            badge_json_old = json.loads(badge_response.read())

            if len(badge_json_old) > 0 and len(badge_json_old['data']) > 0:
                badge_json = badge_json_old

        print(badge_json, tower_acronym)
        if len(badge_json['data']) > 0:
            db_handler.addTowerBeatenList(
                username,
                [(tower_acronym, badge_json['data'][0]['awardedDate'])])

    else:
        status = "no tower found"

    return status, badge_json


async def getPlayerBadgeByIdList(username, badge_list):

    status = "ok"
    badge_json = []

    userid = await getPlayerIdByUsername(username)

    if not userid:
        status = "no user found"
        return status, badge_json

    if len(badge_list) == 0:
        status = "no badge list found"
        return status, badge_json

    try:

        badge_parameter = ",".join(badge_list)
        badge_checker_url = "https://badges.roblox.com/v1/users/" + str(
            userid) + "/badges/awarded-dates?badgeIds=" + badge_parameter
        badge_response = urlopen(badge_checker_url, timeout=5)
        #print(badge_response.getcode())
        badge_json = json.loads(badge_response.read())

    except requests.exceptions.HTTPError as err:
        print(err)

    return status, badge_json


async def getAvatarImage(userid):

    avatar_url = "https://thumbnails.roblox.com/v1/users/avatar-headshot?userIds=" + str(
        userid) + "&size=60x60&format=Png&isCircular=false"
    avatar_response = urlopen(avatar_url, timeout=5)
    avatar_json = json.loads(avatar_response.read())

    #print(avatar_json)

    if "data" in avatar_json:
        return avatar_json['data'][0]['imageUrl']

    return "https://upload.wikimedia.org/wikipedia/en/5/5a/Black_question_mark.png"


@bot.command(guild_ids=[server_id],
             description="Request for the private channel to talk with crp")
@commands.has_role("Crp")
async def privatechat(ctx):
    if (not await precheck(ctx)):
        await noPermission(ctx)
        return

    user_id = ctx.author.id
    username = bot.get_user(int(user_id))
    thread_name = str(username) + " - private room"

    message = await ctx.send("Let me create the private channel for you")
    await message.create_thread(name=thread_name, auto_archive_duration=60)


@bot.command(guild_ids=[server_id],description="Check if player has beaten tower or not")
#@commands.has_role("Crp")
async def hasbeaten(ctx, username, tower):

    if (not await precheck(ctx)):
        await noPermission(ctx)
        return

    username = await filtering_input(ctx, username)
    tower = await filtering_input(ctx, tower)

    if await getPlayerIdByUsername(username) != None:

      info = df_info[df_info['Acronym'].str.lower() == tower.lower()]
      
      if len(info)==0:
        await ctx.respond(await noTowerFound(tower))
        return
      
      await ctx.defer()
      await updatetowercompletion(username)

      dif = info.iloc[0]['Difficulty']
      full_name = info.iloc[0]['Tower']

      obj= db_handler.getTowerBeaten(username, tower)

      embed = discord.Embed(title="Completion status of player",color=JToHDifficulties.getColorHex(dif))

      embed.add_field(name="Player", value=username, inline=False)

      embed.add_field(name="Tower", value="**[" + emoji.getEmoji(dif) + "]** " +full_name, inline=False)

      status="fail"
      if len(obj)>0: 
        status="pass"

      embed.add_field(name="Status",value=emoji.getEmoji(status),inline=False)

      if len(obj)>0:

        date_beaten = obj[0][2].split(".")[0]
        date_beaten_obj = datetime.strptime(date_beaten, '%Y-%m-%dT%H:%M:%S')
        unix_time = int(time.mktime(date_beaten_obj.timetuple()))
        unix_time_str = ("<t:" + str(unix_time) + ">")
        
        embed.add_field(name="Date beaten",value=unix_time_str,inline=False)

      username_id = await getPlayerIdByUsername(username)

      avatar_url = await getAvatarImage(username_id)
      
      embed.set_thumbnail(url=avatar_url)

      await ctx.respond(embed=embed)

    else:
        await ctx.respond(await noUsernameFound(username))

    #print(status,badge_json)


@hasbeaten.error
async def hasbeaten_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.respond(
            "You need to also give me Roblox username and acronym of tower (For example **"
            + prefix + "hasbeaten Crp_Killer ToCP**)")


"""
@bot.command(guild_ids=[server_id], description="Check the date that player beat tower")
async def datebeaten(ctx, username,tower):

  if (not await precheck(ctx)):
    await noPermission(ctx)
    return

  user_id = ctx.author.id
  
  username=await filtering_input(ctx,username)
  tower=await filtering_input(ctx,tower)

  status,badge_json=await getPlayerBadgeByTower(username,tower)
  
  if status=='ok':

    #print(badge_json,badge_json_old)
    
    if len(badge_json['data'])>0:

      info = df_info[df_info['Acronym'].str.lower() == tower.lower()]

      full_name=info.iloc[0]['Tower']
      
      date_obj = badge_json['data'][0]["awardedDate"]
      date_beaten=dateutil.parser.isoparse(date_obj)

      year=date_beaten.year
      month=date_beaten.strftime("%b")
      day=date_beaten.day

      await ctx.respond("<@" + str(user_id) +
                "> **"+username+"** has beaten **"+full_name+"** for the first time on **"+month+" "+str(day)+", "+str(year)+"**")
    else :
        await ctx.respond("<@" + str(user_id) +
                "> Looks like **"+username+"** has not beaten **"+tower+"**")

  elif status=='no tower found':
    await ctx.respond(await noTowerFound(tower))
    
  else:
    await ctx.respond(await noUsernameFound(username))

"""


async def getPlayerSkill(username):

    status = "ok"
    badge_json = []
    skill_list = []

    userid = await getPlayerIdByUsername(username)

    info = df_badge[(df_badge['Category'] == 'Beating First')]

    badge_list = info['Badge ID'].astype(str).tolist()
    difficulty_list = info['Value 1'].str.lower().tolist()

    difficulty_dict = {}

    for k in range(len(badge_list)):
        difficulty_dict[badge_list[k]] = difficulty_list[k]

    if not userid:
        status = "no user found"
        return status, badge_json

    if len(badge_list) == 0:
        status = "no badge list found"
        return status, badge_json

    badge_parameter = ",".join(badge_list)
    badge_checker_url = "https://badges.roblox.com/v1/users/" + str(
        userid) + "/badges/awarded-dates?badgeIds=" + badge_parameter
    badge_response = urlopen(badge_checker_url, timeout=5)
    badge_json = json.loads(badge_response.read())

    for info in badge_json['data']:

        diff_id = str(info['badgeId'])
        if diff_id in difficulty_dict:
            all_dif = difficulty_dict[diff_id].split(",")

            for dif in all_dif:
                skill_list.append(dif)

    return status, skill_list


@bot.command(guild_ids=[server_id],description="Check the hardest tower of player")
#@commands.has_permissions(administrator=True)
async def hardesttower(ctx, username):

    if (not await precheck(ctx)):
        await noPermission(ctx)
        return
    #username=await filtering_message(username)
    username = await filtering_input(ctx, username)
    user_id = ctx.author.id
    amount = 10

    if str(amount).isdigit():
        amount = int(amount)
        if amount > 10:
            amount = 10
    else:
        amount = 1

    if await getPlayerIdByUsername(username) != None:
      
        await ctx.defer()

        await updatetowercompletion(username)

        jtoh_table = db_handler.getHardestBeatenList(username,amount)
   
        if len(jtoh_table)>0:

          info = df_info[df_info['Acronym'] == jtoh_table[0][1]]

          dif = info.iloc[0]['Difficulty']

          total_count = str(min(amount, len(jtoh_table)))
          
          embed = discord.Embed(title="The top " + total_count + " hardest tower(s)",color=JToHDifficulties.getColorHex(dif))

          embed.add_field(name="Player", value=username, inline=False)

          hardest_str=""
          
          for row in jtoh_table:
              tower = row[1]
              date_beaten = row[2].split(".")[0]
              date_beaten_obj = datetime.strptime(date_beaten, '%Y-%m-%dT%H:%M:%S')
              unix_time = int(time.mktime(date_beaten_obj.timetuple()))
              unix_time_str = ("<t:" + str(unix_time) + ":R>")
      
              info = df_info[df_info['Acronym'] == tower]
              dif = info.iloc[0]['Difficulty']
      
              hardest_str += ("**[" + emoji.getEmoji(dif) + "]** " + tower + " - " + str(unix_time_str) + "\n")
  
          embed.add_field(name="The list of hardest towers", value=hardest_str, inline=False)
  
          username_id = await getPlayerIdByUsername(username)
  
          avatar_url =await getAvatarImage(username_id)
  
          embed.set_thumbnail(url=avatar_url)
  
          await ctx.respond(embed=embed)
              #await ctx.respond("<@" + str(user_id) +"> The top **"+str(min(amount,len(top_list)))+"** hardest tower(s) of **"+username+"** is **"+(", ".join(top_list))+"**")
        else:
          await ctx.respond("<@" + str(user_id) + "> I think **" + username +"** hasn't beaten any tower")

    else:
        await ctx.respond(await noUsernameFound(username))


@bot.command(guild_ids=[server_id],
             description="Check 10 most recent towers of player")
#@commands.has_role("Crp")
async def recentbeaten(ctx, username):

    if (not await precheck(ctx)):
        await noPermission(ctx)
        return
    #username=await filtering_message(username)
    #await ctx.send("test")

    username = await filtering_input(ctx, username)
    user_id = ctx.author.id

    if await getPlayerIdByUsername(username) == None:

        await ctx.respond(await noUsernameFound(username))
        return

    amount = 10

    if str(amount).isdigit():
        amount = int(amount)
        if amount > 10:
            amount = 10
    else:
        amount = 1

    await ctx.defer()

    await updatetowercompletion(username)

    jtoh_table = db_handler.getRecentBeatenList(username, amount)

    info = df_info[df_info['Acronym'] == jtoh_table[0][1]]

    dif = info.iloc[0]['Difficulty']

    total_count = str(min(amount, len(jtoh_table)))

    embed = discord.Embed(title=total_count + " most recent tower(s)",
                          color=JToHDifficulties.getColorHex(dif))

    embed.add_field(name="Player", value=username, inline=False)

    recent_list_str = ""

    for row in jtoh_table:
        tower = row[1]
        date_beaten = row[2].split(".")[0]
        date_beaten_obj = datetime.strptime(date_beaten, '%Y-%m-%dT%H:%M:%S')
        unix_time = int(time.mktime(date_beaten_obj.timetuple()))
        unix_time_str = ("<t:" + str(unix_time) + ":R>")

        info = df_info[df_info['Acronym'] == tower]
        dif = info.iloc[0]['Difficulty']

        recent_list_str += ("**[" + emoji.getEmoji(dif) + "]** " + tower +
                            " - " + str(unix_time_str) + "\n")

    embed.add_field(name="List of tower", value=recent_list_str, inline=False)

    username_id = await getPlayerIdByUsername(username)

    avatar_url = await getAvatarImage(username_id)
    #print(username,username_id,avatar_url)

    embed.set_thumbnail(url=avatar_url)

    await ctx.respond(embed=embed)

async def getPlayerJumpProgression(username):

  jtoh_table = db_handler.getTowerBeatenList(username)
  progression=[]
  current_hardest=0

  for row in jtoh_table:
    tower = row[1]
    info = df_info[df_info['Acronym'] == tower]
    dif_num = info.iloc[0]['Num Difficulty']
    date_beaten = row[2].split(".")[0]
    date_beaten_obj = datetime.strptime(date_beaten, '%Y-%m-%dT%H:%M:%S')
    if dif_num>=current_hardest:
      current_hardest=dif_num
      progression.append((tower,date_beaten_obj))

  return progression

@bot.command(guild_ids=[server_id],
             description="Show the significant progression of player")
#@commands.has_role("Crp")
async def jumpprogression(ctx, username):

    if (not await precheck(ctx)):
        await noPermission(ctx)
        return

    username = await filtering_input(ctx, username)
    user_id = ctx.author.id

    if await getPlayerIdByUsername(username) == None:

        await ctx.respond(await noUsernameFound(username))
        return

   
    await ctx.defer()

    await updatetowercompletion(username)

    progression=await getPlayerJumpProgression(username)

    #print(progression)

    progression_str = ""

    for row in progression:
        tower = row[0]
        date_beaten_obj = row[1]
        unix_time = int(time.mktime(date_beaten_obj.timetuple()))
        unix_time_str = ("<t:" + str(unix_time) + ":R>")

        info = df_info[df_info['Acronym'] == tower]
        dif = info.iloc[0]['Difficulty']

        progression_str += ("**[" + emoji.getEmoji(dif) + "]** " + tower +
                            " - " + str(unix_time_str) + "\n")

    embed = discord.Embed(title="Jump progression of "+(username),description=progression_str,
                          color=JToHDifficulties.getColorHex(dif))

    #embed.add_field(name="Player", value=username, inline=False)
      
    #embed.add_field(name="Jump progression", value=progression_str, inline=False)

    username_id = await getPlayerIdByUsername(username)

    avatar_url = await getAvatarImage(username_id)
    #print(username,username_id,avatar_url)

    embed.set_thumbnail(url=avatar_url)

    await ctx.respond(embed=embed)


@bot.command(guild_ids=[server_id],description="(Beta) Suggest the next tower to beat for player (Serie A/B)")
#@commands.has_role("Crp")
async def suggesttowers(ctx, username,serie='A'):

    
    
    if (not await precheck(ctx)):
        await noPermission(ctx)
        return

    username = await filtering_input(ctx, username)
    serie = await filtering_input(ctx, serie)

    serie=serie.upper()

    if not (serie=='A' or serie=='B'):
      serie='A'
  
    user_id = ctx.author.id

    if await getPlayerIdByUsername(username) == None:

      await ctx.respond(await noUsernameFound(username))
      return
 
    await ctx.defer()

    await updatetowercompletion(username)

    amount=5

    if serie=='B':
      amount=3
  
    jtoh_table = db_handler.getHardestBeatenList(username,amount)
   
    if len(jtoh_table)>0:

      progression=[]
      
      for row in jtoh_table:
        tower = row[1]
        progression.append(tower)

      hardest_tower=progression[0]
      
      progression.reverse()  
      
      suggested_list=NNModel.suggestedtower(progression,serie)

      suggest_str=""
      max_suggest=3
      count=0

      result=db_handler.getTowerBeatenList(username)

      beaten_list = {}
      for r in result:
        t = r[1].lower()
        beaten_list[t] = 0

      info = df_info[df_info['Acronym'] == hardest_tower]
      hardest_num_dif=info.iloc[0]['Num Difficulty']
      
      for tower in suggested_list:
        info = df_info[df_info['Acronym'] == tower]
        dif = info.iloc[0]['Difficulty']
        full_name = info.iloc[0]['Tower']
        num_dif=info.iloc[0]['Num Difficulty']

        location_code = info.iloc[0]['Area code']
        location = df_area[df_area['Acronym'] ==location_code].iloc[0]['Area name']

        if not tower.lower() in beaten_list and num_dif-hardest_num_dif<=1 and count<max_suggest:
          suggest_str += ("**[" + emoji.getEmoji(dif) + "]** " + full_name + " ("+location+")\n")
          count+=1

      if count==0:
        await ctx.respond("<@" + str(user_id) +"> I can't find the best towers to suggest to **" + username +"**")
        return

      info = df_info[df_info['Acronym'] == hardest_tower]
      dif=info.iloc[0]['Difficulty']
      
      embed = discord.Embed(title="Suggested towers for player",description="",color=JToHDifficulties.getColorHex(dif))

      embed.add_field(name="Player", value=username, inline=False)
  
      embed.add_field(name="Suggested towers", value=suggest_str, inline=False)

      embed.set_footer(text="Algorithm serie "+serie)
      
      username_id = await getPlayerIdByUsername(username)

      avatar_url = await getAvatarImage(username_id)

      embed.set_thumbnail(url=avatar_url)

      await ctx.respond(embed=embed)

    else:

      await ctx.respond("<@" + str(user_id) +"> I can't find the best towers to suggest to **" + username +"**")

@bot.command(guild_ids=[server_id],description="Show the achievement of player (mode can be only 0 or 1)")
#@commands.has_role("Crp")
async def achievement(ctx, username,mode=0):
  
    if (not await precheck(ctx)):
        await noPermission(ctx)
        return

    username = await filtering_input(ctx, username)
    user_id = ctx.author.id

    mode = await filtering_input(ctx,str(mode))
    if str(mode).isdigit():
        mode = int(mode)
    else:
        mode = 0

    if mode>1 or mode<0:
      mode=0

    if await getPlayerIdByUsername(username) == None:

      await ctx.respond(await noUsernameFound(username))
      return
 
    await ctx.defer()

    await updatetowercompletion(username)

    jtoh_table = db_handler.getTowerBeatenList(username)
   
    if len(jtoh_table)>0:

      date_list=[]
      diff_list={}
      progression={}

      difficulty_list=JToHDifficulties.getAllDifficulty()
      
      for row in jtoh_table:
        tower = row[1]
        date_beaten = row[2].split(".")[0]
        date_beaten_obj = datetime.strptime(date_beaten, '%Y-%m-%dT%H:%M:%S')
        date_index=str(date_beaten_obj.year)+"-"+str(date_beaten_obj.month).zfill(2)

        info = df_info[df_info['Acronym'] == tower]
        dif=info.iloc[0]['Difficulty']

        if not date_index in date_list:
          date_list.append(date_index)

        if not dif in progression:
          progression[dif]={}

        if not date_index in progression[dif]:
          progression[dif][date_index]=0

        progression[dif][date_index]+=1

      start_year,start_month=date_list[0].split("-")
      start_year=int(start_year)
      start_month=int(start_month)
      current_year=datetime.now().year
      current_month=datetime.now().month

      k_year=start_year
      k_month=start_month
      
      while( 12*(k_year)+k_month < 12*(current_year)+current_month  ):
        date_index=str(k_year)+"-"+str(k_month).zfill(2)

        if not date_index in date_list:
          date_list.append(date_index)

        k_month+=1
        if k_month==13:
          k_year+=1
          k_month=1

      date_list.sort()

      for date_index in date_list:
        for dif in difficulty_list:
          if not dif in diff_list:
            diff_list[dif]=[]

          if dif in progression and date_index in progression[dif]:
            diff_list[dif].append(progression[dif][date_index])
          else:
            diff_list[dif].append(0)

      fig, ax = plt.subplots()

      primary_color='#2F3136'
      secondary_color='#EEEEEE'
      
      fig.set(facecolor=primary_color)
      ax.set(facecolor=primary_color)

      ax.set_title("Achievements of "+username, color=secondary_color, fontsize=16)
      ax.set_xlabel("Date", color=secondary_color)
      ax.set_ylabel("Number of beaten towers", color=secondary_color)
      ax.spines['bottom'].set_color(secondary_color)
      ax.spines['top'].set_color(secondary_color) 
      ax.spines['right'].set_color(secondary_color)
      ax.spines['left'].set_color(secondary_color)
      for tick in ax.get_xticklabels():
        tick.set_color(secondary_color)
      for tick in ax.get_yticklabels():
        tick.set_color(secondary_color)
      ax.grid(color='#43454A')
      ax.grid(zorder=0)

      #plt.rcParams.update({'font.size': 20})
      #ax.tick_params(axis='both', labelsize=20)

      if mode==0:
        prev_dif=[0]*len(date_list)
        for dif in difficulty_list:
          if dif in diff_list:
            plt.bar(date_list,diff_list[dif],bottom=prev_dif,color=JToHDifficulties.getColor(dif), zorder=3)
            prev_dif=[x + y for x, y in zip(prev_dif, diff_list[dif])]
        plt.ylim(0, 1.1*max(prev_dif))
      elif mode==1:
        diff_stacked=[]
        color_stacked=[]
        for dif in difficulty_list:
          diff_stacked.append(np.cumsum(diff_list[dif]))
          color_stacked.append(JToHDifficulties.getColor(dif))
        plt.stackplot(date_list,diff_stacked,colors=color_stacked)
      
      plt.xticks(rotation=90)
      
    
      tempfilename = root_tmp_path +'temp_achievement_'+username+'.png'    
      
      plt.subplots_adjust(bottom=0.2)
      plt.gcf().set_size_inches(max(len(date_list)/4,5), max(len(date_list)/6,5))
      plt.savefig(tempfilename,dpi=150,bbox_inches='tight')
      
      embed = discord.Embed(title="Achievement for player",description="",color=discord.Color.blue())

      embed.add_field(name="Player", value=username, inline=False)

      username_id = await getPlayerIdByUsername(username)

      avatar_url = await getAvatarImage(username_id)

      embed.set_thumbnail(url=avatar_url)

      embed.set_footer(text="Click on the image to enlarge")

      file = discord.File(fp=tempfilename, filename="achievement_"+username+".png")
      
      embed.set_image(url="attachment://achievement_"+username+".png")
      
      os.remove(tempfilename)

      await ctx.respond(embed=embed,file=file)

    else:

      await ctx.respond("<@" + str(user_id) +"> Looks like **" + username +" hasn't beaten any tower**")



@bot.command(description='Check the list of beaten towers in area')
#@commands.has_permissions(administrator=True)
#@commands.has_role("Crp")
async def areacompletion(ctx, username, area_code):

    if (not await precheck(ctx)):
        await noPermission(ctx)
        return

    username = await filtering_input(ctx, username)
    user_id = ctx.author.id

    if await getPlayerIdByUsername(username) == None:

        await ctx.respond(await noUsernameFound(username))
        return

    await ctx.defer()

    await updatetowercompletion(username)
    jtoh_table = db_handler.getTowerBeatenList(username)

    area_code = await filtering_input(ctx, area_code)

    #print(area_code)

    if True:  #try:

        beaten_list = {}

        for data in jtoh_table:
            beaten_list[data[1]] = True

        tower_list = df_info[
            (df_info['Area code'].str.lower() == area_code.lower())
            & (df_info['Accessible'] == 'y') &
            (df_info['Tower type'] != 'TowerRush') &
            (df_info['Monthly'] == 'n')].sort_values(by='Num Difficulty',
                                                     ascending=True)
        if tower_list.shape[0] > 0:

            #await ctx.respond(tower_list)
            title = df_area[df_area['Acronym'].str.lower() ==
                            area_code.lower()].iloc[0]['Area name']

            list_str = ""

            for index, info in tower_list.iterrows():

                #guide_url = info['Video URL']

                dif = info['Difficulty']
                acronym = info['Acronym']
                emoji_dif = ":grey_question:"

                emoji_dif = emoji.getEmoji(dif)
                if str(emoji_dif) == 'nan':
                    emoji_dif = ":grey_question:"

                beaten_emoji = ":x:"

                if acronym in beaten_list:
                    beaten_emoji = ":white_check_mark:"

                list_str += (" **[" + emoji_dif + "]** " + info['Acronym'] +
                             "  - " + beaten_emoji + "\n")

            embed = discord.Embed(title="Area completion",
                                  description="",
                                  color=discord.Color.blue())

            embed.add_field(name="Player", value=username, inline=False)
            embed.add_field(name="Area", value=title, inline=False)
            embed.add_field(name="Completion", value=list_str, inline=False)

            username_id = await getPlayerIdByUsername(username)

            avatar_url = await getAvatarImage(username_id)
            #print(username,username_id,avatar_url)

            embed.set_thumbnail(url=avatar_url)

            await ctx.respond(embed=embed)
        else:
            error_list = [
                "What is **" + area_code +
                "**? The cemetery of ToDC:C and ToOEZ?",
                "What is **" + area_code +
                "**? The place that we can find ToAST:R that will never release?",
                "What is **" + area_code +
                "**? It is the location that bad tower like ToYV resides?",
                "What is **" + area_code +
                "**? The realm of hardfailed towers which curators think their design are not good?",
                "What is **" + area_code +
                "**? The place where we can play Mega Fun Obby?"
            ]
            error = random.choice(error_list)

            await ctx.respond(error)
    else:  #except Exception as e:
        print("error")
        #await ctx.respond(e)


@bot.command(guild_ids=[server_id],
             description="Check the areas that player can access")
@commands.has_role("Crp")
async def unlockedareadeprecated(ctx, username):

    if (not await precheck(ctx)):
        await noPermission(ctx)
        return
    #username=await filtering_message(username)
    #await ctx.send("test")

    username = await filtering_input(ctx, username)
    user_id = ctx.author.id

    if await getPlayerIdByUsername(username) == None:

        await ctx.respond(await noUsernameFound(username))
        return

    await ctx.defer()

    info = df_badge[(df_badge['Category'] == 'Unlock Area')].sort_values(
        by='Value 1', ascending=True)

    badge_list = info['Badge ID'].astype(str).tolist()

    area_unlock = {}
    area_mapping = {}

    area_unlock['R1'] = True
    area_unlock['Z1'] = True

    for index, row in info.iterrows():
        acronym = row['Value 1']
        badge_id = str(row['Badge ID'])

        area_mapping[badge_id] = acronym
        area_unlock[acronym] = False

    print(badge_list)

    status, badge_json = await getPlayerBadgeByIdList(username, badge_list)

    if 'data' in badge_json:
        for badge_data in badge_json['data']:
            badge_id = str(badge_data['badgeId'])
            acronym = area_mapping[badge_id]
            area_unlock[acronym] = True

    embed = discord.Embed(title="Unlocked Area", color=discord.Color.blue())

    embed.add_field(name="Player", value=username, inline=False)
    """
    Hardcoded due to bug in Zone 7 badge
    """
    zone7_badge_list = [
        "2127628452", "2127628469", "2127628476", "2127628496", "2127628515",
        "2127628573", "2127628592", "2127628598", "2127628604", "2127628615",
        "2127628626", "2127628633", "2127628644", "2127628655", "2127628708"
    ]
    zone7_status, zone7_badge_json = await getPlayerBadgeByIdList(
        username, zone7_badge_list)

    if 'data' in zone7_badge_json:
        if len(zone7_badge_json['data']) > 0:
            area_unlock['Z7'] = True

    area_list_str = ""

    for acronym in sorted(area_unlock):

        unlock_status = area_unlock[acronym]
        area_name = df_area[df_area['Acronym'] == acronym].iloc[0]['Area name']

        is_unlock = emoji.getEmoji("fail")
        if unlock_status:
            is_unlock = emoji.getEmoji("pass")

        area_list_str += (area_name + " - " + str(is_unlock) + "\n")

    embed.add_field(name="Unlocked area", value=area_list_str, inline=False)

    username_id = await getPlayerIdByUsername(username)

    avatar_url = await getAvatarImage(username_id)
    #print(username,username_id,avatar_url)

    embed.set_thumbnail(url=avatar_url)

    await ctx.respond(embed=embed)


@bot.command(guild_ids=[server_id],
             description="Check the areas that player can access")
#@commands.has_role("Crp")
async def unlockedarea(ctx, username):

    if (not await precheck(ctx)):
        await noPermission(ctx)
        return
    #username=await filtering_message(username)
    #await ctx.send("test")

    username = await filtering_input(ctx, username)
    user_id = ctx.author.id

    if await getPlayerIdByUsername(username) == None:

        await ctx.respond(await noUsernameFound(username))
        return

    await ctx.defer()

    await updatetowercompletion(username)
    jtoh_table = db_handler.getTowerBeatenList(username)

    area_unlock = {}
    area_mapping = {}

    area_unlock['R1'] = True
    area_unlock['Z1'] = True

    beat_list = []

    for info in jtoh_table:
        tower = info[1]
        beat_list.append(tower)

    df_beat = df_info[(df_info['Acronym'].isin(beat_list))
                      & (df_info['Location type'] != 'event')]
    access_list = df_beat["Area code"].dropna().values.tolist()

    access_list = list(dict.fromkeys(access_list))

    embed = discord.Embed(title="Unlocked Area", color=discord.Color.blue())

    embed.add_field(name="Player", value=username, inline=False)

    area_list_str = ""

    #print(access_list)
    area_list = df_area[(df_area['Location type'] != 'event')
                        & (df_area['Location subnumber'] == 1
                           )]["Acronym"].dropna().values.tolist()

    area_list.remove("ER")

    for acronym in sorted(access_list):
        area_unlock[acronym] = True

    for acronym in sorted(area_list):

        #for acronym in sorted(access_list):
        is_unlock = ":x:"  #emoji.getEmoji("fail")

        if acronym in area_unlock:
            is_unlock = ":white_check_mark:"  #emoji.getEmoji("pass")

        area_name = df_area[df_area['Acronym'] == acronym].iloc[0]['Area name']

        area_list_str += (area_name + " - " + str(is_unlock) + "\n")
        #print(area_list_str)

    embed.add_field(name="Unlocked area", value=area_list_str, inline=False)

    username_id = await getPlayerIdByUsername(username)

    avatar_url = await getAvatarImage(username_id)
    #print(username,username_id,avatar_url)

    embed.set_thumbnail(url=avatar_url)

    await ctx.respond(embed=embed)


@bot.command(
    guild_ids=[server_id],
    description=
    "Check the nth tower of player (May be inaccurate if player joined JToH before March 15, 2022)"
)
#@commands.has_role("Crp")
async def nthtower(ctx, username, nth):

    if (not await precheck(ctx)):
        await noPermission(ctx)
        return
    #username=await filtering_message(username)
    #await ctx.send("test")

    username = await filtering_input(ctx, username)
    user_id = ctx.author.id

    if await getPlayerIdByUsername(username) == None:

        await ctx.respond(await noUsernameFound(username))
        return

    nth = await filtering_input(ctx,nth)
  
    if str(nth).isdigit():
        nth = int(nth)
    else:
        nth = 1

    if nth>1000 or nth<1:
      nth=1

    await ctx.defer()

    await updatetowercompletion(username)

    jtoh_table = db_handler.getTowerBeatenByNth(username, nth)

    if (len(jtoh_table) <= 0):
        await ctx.respond("<@" + str(user_id) + "> Sorry! but **" + username +
                          "** beat less than " + str(nth) + " towers :sob:")
        return

    info = df_info[df_info['Acronym'] == jtoh_table[0][1]]

    dif = info.iloc[0]['Difficulty']

    embed = discord.Embed(
        title="The nth tower of player",
        description=
        "",
        color=JToHDifficulties.getColorHex(dif))

    embed.add_field(name="Player", value=username, inline=False)

    embed.add_field(name="No.", value=str(nth), inline=False)

    beat_str = ""

    tower = jtoh_table[0][1]
    date_beaten = jtoh_table[0][2].split(".")[0]
    date_beaten_obj = datetime.strptime(date_beaten, '%Y-%m-%dT%H:%M:%S')
    unix_time = int(time.mktime(date_beaten_obj.timetuple()))
    unix_time_str = ("<t:" + str(unix_time) + ">")

    info = df_info[df_info['Acronym'] == tower]
    dif = info.iloc[0]['Difficulty']

    beat_str += ("**[" + emoji.getEmoji(dif) + "]** " + tower)

    embed.add_field(name="Tower", value=beat_str, inline=False)

    embed.add_field(name="Date beaten", value=str(unix_time_str), inline=False)

    username_id = await getPlayerIdByUsername(username)

    avatar_url = await getAvatarImage(username_id)
    #print(username,username_id,avatar_url)

    embed.set_thumbnail(url=avatar_url)

    await ctx.respond(embed=embed)

@bot.command(guild_ids=[server_id],
             description="Reset the progress of player's tower completion"
             )
@commands.has_role("Crp")
async def resettowercompletion(ctx, username):
    if (not await precheck(ctx)):
        await noPermission(ctx)
        return
    #username=await filtering_message(username)
    username = await filtering_input(ctx, username)
    user_id = ctx.author.id

    await ctx.defer()
    
    db_handler.removeTowerBeatenList(username)
    await updatetowercompletionmode(username,mode=2)
    await updatetowercompletionmode(username,mode=1)
    await updatetowercompletionmode(username,mode=0)

    await ctx.respond("<@" + str(user_id) + "> The tower completion of **" + username + "** has been reset")

@bot.command(guild_ids=[server_id],
             description="Show the summary of tower completion for each player"
             )
#@commands.has_role("Crp")
async def towercompletion(ctx, username):
    if (not await precheck(ctx)):
        await noPermission(ctx)
        return
    #username=await filtering_message(username)
    username = await filtering_input(ctx, username)
    user_id = ctx.author.id

    if await getPlayerIdByUsername(username) == None:

        await ctx.respond(await noUsernameFound(username))
        return

    await ctx.defer()

    info = await updatetowercompletion(username)

    if info['total_completion'] > 0:

        badge_info = df_badge[(df_badge['Category'] == 'Beating Tower')]
        tower_info = df_info[(df_info['Accessible'] == 'y')]

        tower_info = tower_info.rename(columns={'Acronym': 'Acronym'})
        badge_info = badge_info.rename(columns={'Value 1': 'Acronym'})

        #badge_info = badge_info.set_index('Acronym')
        #tower_info = tower_info.set_index('Acronym')
        all_list = badge_info.merge(tower_info, on='Acronym', how='left')
        all_list = all_list[all_list['Location type'] != 'event']

        difficulty_count = all_list.groupby(['Difficulty'
                                             ])['Difficulty'].count()

        #print(difficulty_count)

        embed = discord.Embed(title="Tower completion",
                              color=discord.Color.blue())

        embed.add_field(name="Player", value=username, inline=False)

        completion_str = ""
        #completion_str+="Total: "+str(total_completion)+"\n"
        completion_str += "Towers: " + str(info['total_tower']) + "\n"
        completion_str += "Citadels: " + str(info['total_citadel']) + "\n"
        completion_str += "Steeples: " + str(info['total_steeple']) + "\n"
        completion_str += "Mini Tower: " + str(info['total_minitower']) + "\n"

        total_com_str = str(info['total_completion']) + " *(" + str(
            round(100 * info['total_completion'] / len(all_list), 1)) + "%)*"

        embed.add_field(name="Total completion",
                        value=total_com_str,
                        inline=False)

        embed.add_field(
            name="Total positive energies",
            value=str(
                round(
                    info['total_tower'] + 2 * info['total_citadel'] +
                    0.5 * info['total_steeple'], 1)),
            inline=False)

        embed.add_field(name="Tower type", value=completion_str, inline=False)

        difficulty_str = ""

        difficulty_list = [
            'easy', 'medium', 'hard', 'difficult', 'challenging', 'intense',
            'remorseless', 'insane', 'extreme', 'terrifying', 'catastrophic'
        ]

        total_difficulty = info['total_difficulty']

        for d in difficulty_list:
            if d in total_difficulty:
                difficulty_str += emoji.getEmoji(d) + " " + str(
                    total_difficulty[d]) + " *(" + str(
                        round(100 * total_difficulty[d] / difficulty_count[d],
                              1)) + "%)*\n"

        embed.add_field(name="Difficulty", value=difficulty_str, inline=False)
        username_id = await getPlayerIdByUsername(username)

        avatar_url = await getAvatarImage(username_id)
        #print(username,username_id,avatar_url)

        embed.set_thumbnail(url=avatar_url)

        await ctx.respond(embed=embed)
    else:
        await ctx.respond("<@" + str(user_id) + "> I think **" + username +
                          "** hasn't beaten any tower")


async def updatetowercompletion(username):
  current_list=db_handler.getTowerBeatenList(username)
  if len(current_list)==0:
    await updatetowercompletionmode(username,mode=2)
    await updatetowercompletionmode(username,mode=1)
  return await updatetowercompletionmode(username,mode=0)
  
#@commands.has_permissions(administrator=True)
async def updatetowercompletionmode(username,mode=0):

    #print(username,mode)
    """
    if (not await precheck(ctx)):
        await noPermission(ctx)
        return
    #username=await filtering_message(username)
    username = await filtering_input(ctx, username)
    user_id = ctx.author.id
    """

    badge_info = df_badge[(df_badge['Category'] == 'Beating Tower')]
    tower_info = df_info[(df_info['Accessible'] == 'y')]

    tower_info = tower_info.rename(columns={'Acronym': 'Acronym'})
    badge_info = badge_info.rename(columns={'Value 1': 'Acronym'})

    info = badge_info.merge(tower_info, on='Acronym', how='left')
    info = info[info['Location type'] != 'event']

    badge_list = []

    k = 0

    total_completion = 0
    total_tower = 0
    total_citadel = 0
    total_steeple = 0
    total_minitower = 0

    total_difficulty = {}

    update_database_beaten_list = []

    result = db_handler.getTowerBeatenList(username)

    existing_tower_list = {}
    for r in result:
        t = r[1].lower()
        existing_tower_list[t] = 0

    badge_column='Badge ID'

    if mode==1:
      badge_column='Badge ID (Old JToH)'
    elif mode==2:
      badge_column='Badge ID (KToH)'

    #print(badge_column)
    info = info[info[badge_column].notnull()]

    for index, row in info.iterrows():
        #print(row)
        
      
        badge_id = row[badge_column]

        if str(badge_id)=='nan':
          continue
      
        tower = row['Acronym']
        #print(tower,badge_id)
        if not tower.lower() in existing_tower_list:
            #print(tower)
            badge_list.append(str(int(badge_id)))
        else:

            tower_type = info[(info['Acronym'].str.lower() == tower.lower()
                               )].iloc[0]['Tower type']

            total_completion += 1

            if tower_type == 'Tower':
                total_tower += 1
            elif tower_type == 'Citadel':
                total_citadel += 1
            elif tower_type == 'Steeple':
                total_steeple += 1
            elif tower_type == 'MiniTower':
                total_minitower += 1

            difficulty = info[(info['Acronym'].str.lower() == tower.lower()
                               )].iloc[0]['Difficulty']

            if not difficulty in total_difficulty:
                total_difficulty[difficulty] = 0

            total_difficulty[difficulty] += 1

        if len(badge_list) >= 100 or k >= info.shape[0] - 1:

            #print(badge_list)
          
            time.sleep(1)

            badge_json = []

            #print("index="+str(k))

            status, badge_json = await getPlayerBadgeByIdList(username, badge_list)
            #print(badge_json)
            badge_list = []
            if 'data' in badge_json:
                for badge_data in badge_json['data']:
                    badge_id = int(badge_data['badgeId'])
                    #print(info[(info['Badge ID'] == badge_id)].iloc[0])
                    tower_type = info[(
                        info[badge_column] == badge_id)].iloc[0]['Tower type']

                    tower_acronym = info[(
                        info[badge_column] == badge_id)].iloc[0]['Acronym']

                    if info[(info[badge_column] == badge_id
                             )].iloc[0]['Location type'] == 'event':
                        continue

                    update_database_beaten_list.append(
                        (tower_acronym, badge_data['awardedDate']))

                    total_completion += 1

                    if tower_type == 'Tower':
                        total_tower += 1
                    elif tower_type == 'Citadel':
                        total_citadel += 1
                    elif tower_type == 'Steeple':
                        total_steeple += 1
                    elif tower_type == 'MiniTower':
                        total_minitower += 1

                    difficulty = info[(
                        info[badge_column] == badge_id)].iloc[0]['Difficulty']

                    if not difficulty in total_difficulty:
                        total_difficulty[difficulty] = 0

                    total_difficulty[difficulty] += 1
        k += 1

    if total_completion > 0 and len(update_database_beaten_list) > 0:
        db_handler.addTowerBeatenList(username, update_database_beaten_list)

    return {
        "total_completion": total_completion,
        "total_tower": total_tower,
        "total_steeple": total_steeple,
        "total_citadel": total_citadel,
        "total_minitower": total_minitower,
        "total_difficulty": total_difficulty
    }
    """
    if total_completion > 0:

        if len(update_database_beaten_list) > 0:
            db_handler.addTowerBeatenList(username,
                                          update_database_beaten_list)

        embed = discord.Embed(title="Tower completion for " + username,
                              color=discord.Color.blue())

        completion_str = ""
        #completion_str+="Total: "+str(total_completion)+"\n"
        completion_str += "Towers: " + str(total_tower) + "\n"
        completion_str += "Citadels: " + str(total_citadel) + "\n"
        completion_str += "Steeples: " + str(total_steeple) + "\n"
        completion_str += "Mini Tower: " + str(total_minitower) + "\n"

        embed.add_field(name="Total completion",
                        value=str(total_completion),
                        inline=False)

        embed.add_field(
            name="Total tower points",
            value=str(
                round(total_tower + 2 * total_citadel + 0.5 * total_steeple,
                      1)),
            inline=False)

        embed.add_field(name="Tower type", value=completion_str, inline=False)

        difficulty_str = ""

        difficulty_list = [
            'easy', 'medium', 'hard', 'difficult', 'challenging', 'intense',
            'remorseless', 'insane', 'extreme', 'terrifying', 'catastrophic'
        ]

        for d in difficulty_list:
            if d in total_difficulty:
                difficulty_str += emoji.getEmoji(d) + " " + str(
                    total_difficulty[d]) + "\n"

        embed.add_field(name="Difficulty", value=difficulty_str, inline=False)
        username_id = await getPlayerIdByUsername(username)

        avatar_url = await getAvatarImage(username_id)
        #print(username,username_id,avatar_url)

        embed.set_thumbnail(url=avatar_url)

        await ctx.respond(embed=embed)
    else:
        await ctx.respond("<@" + str(user_id) + "> I think **" + username +
                          "** hasn't beaten any tower")

    """


@bot.command(
    guild_ids=[server_id],
    description="Show the top 10 easiest unbeaten towers for each player")
#@commands.has_permissions(administrator=True)
async def unbeatentower(ctx, username):
    if (not await precheck(ctx)):
        await noPermission(ctx)
        return
    #username=await filtering_message(username)
    username = await filtering_input(ctx, username)
    user_id = ctx.author.id

    if await getPlayerIdByUsername(username) == None:

        await ctx.respond(await noUsernameFound(username))
        return

    amount = 10

    await ctx.defer()

    badge_info = df_badge[(df_badge['Category'] == 'Beating Tower')]
    tower_info = df_info[(df_info['Accessible'] == 'y')
                         & (df_info['Location type'] != 'event')]

    tower_info = tower_info.rename(columns={'Acronym': 'Acronym'})
    badge_info = badge_info.rename(columns={'Value 1': 'Acronym'})

    #badge_info = badge_info.set_index('Acronym')
    #tower_info = tower_info.set_index('Acronym')
    info = badge_info.merge(tower_info, on='Acronym', how='inner')
    info = info.sort_values(by=['Num Difficulty'], ascending=True)

    #print(info)

    badge_list = []

    #print("size=" + str(info.shape[0]))

    k = 0

    unbeaten_list = []
    badge_list = []

    result = db_handler.getTowerBeatenList(username)

    existing_tower_list = {}
    for r in result:
        t = r[1].lower()
        existing_tower_list[t] = 0

    badge_check = []
    badge_mapping = {}

    for index, row in info.iterrows():
        #print(row)
        badge_id = row['Badge ID']
        tower = row['Acronym']
        #print(tower,badge_id)
        if not tower.lower() in existing_tower_list:
            badge_list.append(str(badge_id))
            badge_mapping[str(badge_id)] = tower

        if len(badge_list) >= 100 or k >= info.shape[0] - 1:

            time.sleep(1)

            badge_json = []

            #print("index="+str(k))

            status, badge_json = await getPlayerBadgeByIdList(
                username, badge_list)
            #print(badge_json)
            if 'data' in badge_json:
                for badge_data in badge_json['data']:
                    badge_id = int(badge_data['badgeId'])
                    badge_check.append(str(badge_id))

                badge_missing = [
                    item for item in badge_list if item not in badge_check
                ]
                for id in badge_missing:
                    if len(unbeaten_list) < amount:
                        unbeaten_list.append(badge_mapping[id])
                    if len(unbeaten_list) >= amount:
                        break

            badge_list = []

        k += 1

    if len(unbeaten_list) > 0:

        info = df_info[df_info['Acronym'] == unbeaten_list[0]]

        dif = info.iloc[0]['Difficulty']

        total_count = str(min(amount, len(unbeaten_list)))

        embed = discord.Embed(title="The top " + total_count +
                              " easiest unbeaten tower(s)",
                              color=JToHDifficulties.getColorHex(dif))

        embed.add_field(name="Player", value=username, inline=False)

        unbeaten_list_str = ""
        k = 1
        for t in unbeaten_list:
            cur_info = df_info[df_info['Acronym'] == t]

            cur_dif = cur_info.iloc[0]['Difficulty']
            location_code = cur_info.iloc[0]['Area code']
            location = df_area[df_area['Acronym'] ==
                               location_code].iloc[0]['Area name']

            unbeaten_list_str += ("**[" + emoji.getEmoji(cur_dif) + "]** " +
                                  t + " *(" + location + ")*\n")
            k += 1

        embed.add_field(name="List of tower",
                        value=unbeaten_list_str,
                        inline=False)

        username_id = await getPlayerIdByUsername(username)

        avatar_url = await getAvatarImage(username_id)
        #print(username,username_id,avatar_url)

        embed.set_thumbnail(url=avatar_url)

        await ctx.respond(embed=embed)

    else:
        await ctx.respond("<@" + str(user_id) + "> I think **" + username +
                          "** has already beaten all towers in JToH")


#url='https://www.youtube.com/c/CrpKiller/playlists'


class MoreGuideView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

        guideButton = discord.ui.Button(
            label='More guides from Crp_Killer',
            style=discord.ButtonStyle.link,
            url='https://www.youtube.com/c/CrpKiller/')
        self.add_item(guideButton)

    async def button_callback(self, button, interaction):
        await interaction.response.defer()


#url=https://www.youtube.com/c/CrpKiller/playlists


@bot.command(guild_ids=[server_id], description="Get the video guide from CRP")
async def guide(ctx, tower):

    if (not await precheck(ctx)):
        await noPermission(ctx)
        return

    tower = await filtering_input(ctx, tower)
    user_id = ctx.author.id

    info = df_info[df_info['Acronym'].str.lower() == tower.lower()]

    if info.shape[0] > 0:
        try:
            full_name = info.iloc[0]['Tower']
            guide = info.iloc[0]['Video URL']
            await ctx.respond('<@' + str(user_id) +
                              '>, you can check the guide on **' + full_name +
                              '** via this link -> ' + guide,
                              view=MoreGuideView())
        except:
            await ctx.respond('<@' + str(user_id) +
                              '>, NOOOOOO!!!!!! I don\'t have a guide on **' +
                              full_name + "**")
    else:
        await ctx.respond(await noTowerFound(tower))


"""
@bot.command(guild_ids=[server_id], description="Check the difficulty of tower")
async def difficulty(ctx, tower):

  if (not await precheck(ctx)):
    await noPermission(ctx)
    return
  
  tower=await filtering_input(ctx,tower)
  user_id = ctx.author.id

  info = df_info[df_info['Acronym'].str.lower() == tower.lower()]

  if info.shape[0]>0:
    full_name=info['Tower'].values[0]
    try:
    
      cur_subdif = info['Sub difficulty'].values[0]
      cur_dif = info['Difficulty'].values[0]
      await ctx.respond('<@' + str(user_id) + '> Current difficulty of **' +
                                       full_name + '** is ' +
                                       cur_subdif + ' ' + emoji_code[cur_dif]
                                       )  #Respond message
    except:
      await ctx.respond(
                '<@' + str(user_id) +
                '> I don\'t know the difficulty of **' +
                full_name+'**')
    try:          
      dif = info['Personal difficulty'].values[0]
      sub_dif = info['Personal sub difficulty'].values[0]
      await ctx.send('I think **' +
                                       full_name + '** is ' +
                                       sub_dif + ' ' + emoji_code[dif]
                                       )  #Respond message
    except:
      await ctx.send(
                'I have no opinion about the difficulty on **' +
                full_name+'**')
    try:
      com_dif = info['Communal difficulty'].values[0]
      com_sub_dif = info['Communal sub difficulty'].values[0]
      await ctx.send(
                'Most people think **' + full_name + '** is ' +
                com_sub_dif + ' ' + emoji_code[com_dif])  #Respond message
    except:
      await ctx.send(
                'and I don\'t know what people think about **' +
                full_name+'**')
  else:
    await ctx.respond(await noTowerFound(tower))
"""


@bot.command(guild_ids=[server_id],
             description="Check the difficulty of tower")
#@commands.has_permissions(administrator=True)
async def difficulty(ctx, tower):

    if (not await precheck(ctx)):
        await noPermission(ctx)
        return

    tower = await filtering_input(ctx, tower)
    user_id = ctx.author.id

    info = df_info[df_info['Acronym'].str.lower() == tower.lower()]

    if info.shape[0] > 0:
        full_name = info['Tower'].values[0]
        diff_point = info['Num Difficulty'].values[0]
        if (str(diff_point) == "nan"):
            diff_point = ""
        else:
            diff_point = "(" + str(diff_point) + ")"

        cur_subdif = info['Sub difficulty'].values[0]
        cur_dif = info['Difficulty'].values[0]
        emoji_cur_dif = ""

        if (str(cur_subdif) == "nan"):
            cur_subdif = ""
        if (str(cur_dif) == "nan"):
            cur_dif = "Unknown"
        emoji_cur_dif = emoji.getEmoji(cur_dif)

        #print(emoji_cur_dif)

        dif = info['Personal difficulty'].values[0]
        sub_dif = info['Personal sub difficulty'].values[0]
        emoji_dif = ""

        if (str(sub_dif) == "nan"):
            sub_dif = ""
        if (str(dif) == "nan"):
            dif = "Unknown"
        emoji_dif = emoji.getEmoji(dif)

        com_dif = info['Communal difficulty'].values[0]
        com_sub_dif = info['Communal sub difficulty'].values[0]
        emoji_com_dif = ""

        if (str(com_sub_dif) == "nan"):
            com_sub_dif = ""
        if (str(com_dif) == "nan"):
            com_dif = "Unknown"
        emoji_com_dif = emoji.getEmoji(com_dif)

        embed = discord.Embed(title="Difficulty",
                              color=JToHDifficulties.getColorHex(cur_dif))

        embed.add_field(name="Tower", value=full_name, inline=False)
        embed.add_field(name="Current difficulty",
                        value=(cur_subdif + " " + emoji_cur_dif + " " +
                               diff_point),
                        inline=False)
        embed.add_field(name="Personal difficulty",
                        value=(sub_dif + " " + emoji_dif),
                        inline=False)
        embed.add_field(name="Communal difficulty",
                        value=(com_sub_dif + " " + emoji_com_dif),
                        inline=False)

        status, img_url = await printTowerImage(tower)
        embed.set_thumbnail(url=img_url)

        await ctx.respond(embed=embed)

    else:
        await ctx.respond(await noTowerFound(tower))

"""
@bot.command(
    guild_ids=[server_id],
    description="Check the estimated base points of tower (CE2022 event)")
#@commands.has_permissions(administrator=True)
async def basepoints(ctx, tower):

    if (not await precheck(ctx)):
        await noPermission(ctx)
        return

    tower = await filtering_input(ctx, tower)
    user_id = ctx.author.id

    info = df_info[df_info['Acronym'].str.lower() == tower.lower()]

    if info.shape[0] > 0:

        full_name = info['Tower'].values[0]
        tower_type = info['Tower type'].values[0]
        diff_point = info['Num Difficulty'].values[0]

        cur_dif = info['Difficulty'].values[0]
        cur_subdif = info['Sub difficulty'].values[0]

        emoji_cur_dif = emoji.getEmoji(cur_dif)

        try:
            df_basepoints = pd.read_csv(
                "https://docs.google.com/spreadsheets/d/1C4FVfF9pn1wpQs1Ch-bpO9bA50lx4kHktpPmBV-1fkM/gviz/tq?tqx=out:csv&sheet=Sheet1"
            )
            point_info = df_basepoints[
                df_basepoints['Difficulty:'].str.lower() == cur_dif.lower()]

            #print(point_info.iloc[0])

            search_key = ""

            if tower_type == "Tower":
                search_key = "Tower Rebeat"
            elif tower_type == "Steeple":
                search_key = "Steeple Rebeat"
            elif tower_type == "Citadel":
                search_key = "Citadel Rebeat"
            elif tower_type == "MiniTower":
                search_key = "Mini-Tower Rebeat"

            score_range = point_info.iloc[0][search_key]

            score_range = score_range.replace("Pokos", "").strip()

            min, max = score_range.split("-")
            min, max = int(min), int(max)

            decimal_part = (100 * float(diff_point)) % 100

            base_point = min + (decimal_part / 100) * (max - min)
            base_point = int(round(base_point, 0))

            embed = discord.Embed(
                title="Estimated base point for CE2022 event",
                color=JToHDifficulties.getColorHex(cur_dif))

            embed.add_field(name="Tower", value=full_name, inline=False)
            embed.add_field(name="Estimated base points",
                            value=str("{:,}".format(base_point)),
                            inline=False)
            embed.add_field(name="Estimated base points (First-time)",
                            value=str("{:,}".format(2 * base_point)),
                            inline=False)
            embed.add_field(
                name="Estimated base points (With ornament multipliers)",
                value=str("{:,}".format(round(1.5 * base_point))),
                inline=False)
            status, img_url = await printTowerImage(tower)
            embed.set_thumbnail(url=img_url)

            await ctx.respond(embed=embed)

        except Exception as e:
            print(e)
            await ctx.respond("<@" + str(user_id) +
                              "> Sorry! I can't find the base point of " +
                              full_name + " :sob:")

    else:
        await ctx.respond(await noTowerFound(tower))
"""
"""
@bot.command(
    guild_ids=[server_id],
    description="Check which towers has ornament booster today (CE2022 event)")
#@commands.has_permissions(administrator=True)
async def ornamentbooster(ctx):

    if (not await precheck(ctx)):
        await noPermission(ctx)
        return

    await ctx.defer()
    #await ctx.respond("Let me check...")

    #URL = "https://jtoh.fandom.com/wiki/Winter_Event_2022"
    URL = "https://pastebin.com/CrGkhMJ6"

    try:
        page = requests.get(URL, timeout=5)

        soup = BeautifulSoup(page.content, "html.parser")
      
        floor_table = soup.findAll('div', {"class": "de1"})[0]
        towers_info = floor_table.text

        tower_str = ""

        has_header = 0

        tower_list = {}

        #for tower in towers_info:
        for tower in towers_info.split(","):

            acronym = tower.strip()  #.text
            #print(acronym)
            cur_info = df_info[df_info['Acronym'] == acronym]

            if len(df_info[df_info['Acronym'] == acronym]) > 0:
                diff_point = cur_info['Num Difficulty'].values[0]

                tower_list[acronym] = diff_point

        sorted_tower_list = sorted(tower_list.items(), key=lambda x: x[1])

        for acronym, value in sorted_tower_list:

            cur_info = df_info[df_info['Acronym'] == acronym]

            cur_dif = cur_info.iloc[0]['Difficulty']
            location_code = cur_info.iloc[0]['Area code']
            location = df_area[df_area['Acronym'] ==
                               location_code].iloc[0]['Area name']

            tower_str += ("**[" + emoji.getEmoji(cur_dif) + "]** " + acronym +
                          " *(" + location + ")*\n")

            #embed.add_field(name=(acronym +" *("+location+")*\n"),value="",inline=False)

        embed = discord.Embed(
            title="Tower with ornament booster (CE2022 event)",
            description=tower_str,
            color=discord.Color.blue())
        #embed.add_field(name="List of tower",value=tower_str,inline=False)

        avatar_url = "https://static.wikia.nocookie.net/ktoh/images/8/89/Emblem_CE2021.png"
        #print(username,username_id,avatar_url)

        embed.set_thumbnail(url=avatar_url)

        await ctx.respond(embed=embed)

    except Exception as e:
        print(e)
        await ctx.respond(
            "I can't find the list of towers with ornament booster right now")
"""

@bot.command(guild_ids=[server_id],
             description="Check the communal score of the tower")
#@commands.has_permissions(administrator=True)
async def score(ctx, tower):

    if (not await precheck(ctx)):
        await noPermission(ctx)
        return

    tower = await filtering_input(ctx, tower)
    user_id = ctx.author.id

    info = df_info[df_info['Acronym'].str.lower() == tower.lower()]

    if info.shape[0] > 0:
        full_name = info['Tower'].values[0]
        gameplay_point = info['Communal gameplay score'].values[0]
        creativity_point = info['Communal creativity score'].values[0]
        design_point = info['Communal design score'].values[0]
        total_point = ":grey_question:"

        gameplay_str = "Unknown"
        creativity_str = "Unknown"
        design_str = "Unknown"
        total_str = "Unknown"

        if str(gameplay_point) != 'nan':
            gameplay_str = ""
            star_count = round(float(gameplay_point))
            for k in range(10):
                if k < star_count:
                    gameplay_str += emoji.getEmoji('gameplaystar')
                else:
                    gameplay_str += emoji.getEmoji('emptystar')

        if str(creativity_point) != 'nan':
            creativity_str = ""
            star_count = round(float(creativity_point))
            for k in range(10):
                if k < star_count:
                    creativity_str += emoji.getEmoji('creativitystar')
                else:
                    creativity_str += emoji.getEmoji('emptystar')

        if str(design_point) != 'nan':
            design_str = ""
            star_count = round(float(design_point))
            for k in range(10):
                if k < star_count:
                    design_str += emoji.getEmoji('designstar')
                else:
                    design_str += emoji.getEmoji('emptystar')

        if str(gameplay_point) != 'nan' and str(
                creativity_point) != 'nan' and str(design_point) != 'nan':
            total_str = ""
            total_point = round(
                float(gameplay_point) + float(creativity_point) +
                float(design_point), 2)
            star_count = round((total_point) / 3)
            for k in range(10):
                if k < star_count:
                    total_str += emoji.getEmoji('goldstar')
                else:
                    total_str += emoji.getEmoji('emptystar')

        if str(gameplay_point) == 'nan':
            gameplay_point = ':grey_question:'
        if str(creativity_point) == 'nan':
            creativity_point = ':grey_question:'
        if str(design_point) == 'nan':
            design_point = ':grey_question:'

        cur_dif = info['Difficulty'].values[0]

        embed = discord.Embed(title="Score",
                              color=JToHDifficulties.getColorHex(cur_dif))

        embed.add_field(name="Tower", value=full_name, inline=False)

        embed.add_field(name="Communal gameplay score (" +
                        str(gameplay_point) + "/10)",
                        value=(gameplay_str),
                        inline=False)
        embed.add_field(name="Communal creativity score (" +
                        str(creativity_point) + "/10)",
                        value=(creativity_str),
                        inline=False)
        embed.add_field(name="Communal design score (" + str(design_point) +
                        "/10)",
                        value=(design_str),
                        inline=False)
        embed.add_field(name="Communal total score (" + str(total_point) +
                        "/30)",
                        value=(total_str),
                        inline=False)

        status, img_url = await printTowerImage(tower)
        embed.set_thumbnail(url=img_url)

        await ctx.respond(embed=embed)

    else:
        await ctx.respond(await noTowerFound(tower))


@bot.command(guild_ids=[server_id],
             description="Lets EO share their opinion on a random tower")
async def eo(ctx):

    if (not await precheck(ctx)):
        await noPermission(ctx)
        return

    #tower=await filtering_input(ctx,tower)
    user_id = ctx.author.id

    #info = df_info[df_info['Acronym'].str.lower() == tower.lower()]
    difficulty_list = [
        'medium', 'hard', 'difficult', 'challenging', 'intense', 'remorseless',
        'insane', 'extreme', 'terrifying', 'catastrophic'
    ]
    tower_list = df_info[(df_info['Difficulty'].isin(difficulty_list)) & (
        df_info['Accessible'] == 'y')]['Acronym'].values.tolist()
    tower = random.choice(tower_list)

    #print(tower)

    try:
        cur_dif = df_info[df_info['Acronym'].str.lower() ==
                          tower.lower()]['Difficulty'].values[0]
        #eo_dif = difficultyDown(cur_dif.lower())
        #if random.choice([0, 1]) == 0:
        #    eo_dif = difficultyDown(eo_dif.lower())
        eo_dif = JToHDifficulties.decreaseDifficultyLabel(
            cur_dif, random.choice([1, 2]))
        await ctx.respond('<@' + str(user_id) + '> ' + tower + ' is ' + eo_dif
                          )  #Respond message
    except Exception as e:
        print(e)
        await ctx.respond("<@" + str(user_id) + "> Stop! I'm not EO :sob:")

    #else:
    #  await ctx.respond(await noTowerFound(tower))


"""
@bot.command(guild_ids=[server_id], description="Check how long does it take to beat tower")
async def beattime(ctx, tower):

  if (not await precheck(ctx)):
    await noPermission(ctx)
    return
  
  tower=await filtering_input(ctx,tower)
  user_id = ctx.author.id

  info = df_info[df_info['Acronym'].str.lower() == tower.lower()]

  if info.shape[0]>0:

    full_name=info['Tower'].values[0]
    
    try:
      normal_playtime = info['Average normal playtime (minute)'].values[0]
      speedrun_playtime = info['Average speedrun playtime (minute)'].values[0]
      await ctx.respond(
                '<@' + str(user_id) + '> Most people should beat **' +
                full_name + '** in **' +
                str(int(normal_playtime)) + '** minutes')  #Respond message
      await ctx.send(
                'unless you try to speedrun **' + full_name +
                '**, you should take **' + str(int(speedrun_playtime)) +
                '** minutes to beat it')  #Respond message
    except:
      await ctx.respond('<@' + str(user_id) +
                                       '> I have no information about **' +
                                       full_name+'**')
  else:
    await ctx.respond(await noTowerFound(tower))

"""


@bot.command(guild_ids=[server_id],
             description="Check how long does it take to beat tower")
#@commands.has_permissions(administrator=True)
async def beattime(ctx, tower):

    if (not await precheck(ctx)):
        await noPermission(ctx)
        return

    tower = await filtering_input(ctx, tower)
    user_id = ctx.author.id

    info = df_info[df_info['Acronym'].str.lower() == tower.lower()]

    if info.shape[0] > 0:

        full_name = info['Tower'].values[0]
        dif = info['Difficulty'].values[0]

        normal_playtime = info['Average normal playtime (minute)'].values[0]
        speedrun_playtime = info['Average speedrun playtime (minute)'].values[
            0]

        if (str(normal_playtime) == "nan" or (normal_playtime == 0)):
            normal_playtime = "Unknown"
        else:
            normal_playtime = int(normal_playtime)
        if (str(speedrun_playtime) == "nan" or (speedrun_playtime == 0)):
            speedrun_playtime = "Unknown"
        else:
            speedrun_playtime = int(speedrun_playtime)

        embed = discord.Embed(title="Time length",
                              color=JToHDifficulties.getColorHex(dif))

        embed.add_field(name="Tower", value=full_name, inline=False)

        embed.add_field(name="Average normal playtime:",
                        value=str(normal_playtime) + " minutes",
                        inline=False)

        embed.add_field(name="Average speedrunning playtime",
                        value=str(speedrun_playtime) + " minutes",
                        inline=False)

        status, img_url = await printTowerImage(tower)

        embed.set_thumbnail(url=img_url)

        await ctx.respond(embed=embed)

    else:
        await ctx.respond(await noTowerFound(tower))


@bot.command(guild_ids=[server_id], description="Check the location of tower")
async def location(ctx, tower):

    if (not await precheck(ctx)):
        await noPermission(ctx)
        return

    tower = await filtering_input(ctx, tower)
    user_id = ctx.author.id

    info = df_info[df_info['Acronym'].str.lower() == tower.lower()]

    if info.shape[0] > 0:

        try:
            full_name = info['Tower'].values[0]

            tower_location = info['Location'].values[0]
            tower_location_number = int(info['Location number'].values[0])
            tower_location_subnumber = int(
                info['Location subnumber'].values[0])
            tower_location_type = info['Location type'].values[0]

            #print(tower_location,tower_location_number,tower_location_subnumber,tower_location_type)

            if (info['Accessible'].values[0] != 'y'):
                await ctx.respond("<@" + str(user_id) +
                                  "> Looks like you can't access **" +
                                  full_name + "** right now")
                return

            subrealm_text = ''

            if (tower_location == 'ring' or tower_location == 'zone'):
                subrealm_text = ''

            if (tower_location_type == 'event'):
                subrealm_text = 'Event in '

            if (tower_location_type == 'subrealm'):
                subrealm_text = 'subrealm of '

            area_name = df_area[
                (df_area['Location'] == tower_location)
                & (df_area['Location number'] == tower_location_number) &
                (df_area['Location subnumber'] == tower_location_subnumber) &
                (df_area['Location type']
                 == tower_location_type)]['Area name'].values[0]

            area_full_name = df_area[
                (df_area['Location'] == tower_location)
                & (df_area['Location number'] == tower_location_number) &
                (df_area['Location subnumber'] == tower_location_subnumber) &
                (df_area['Location type']
                 == tower_location_type)]['Full name'].values[0]

            #print(area_full_name)

            dif = info['Difficulty'].values[0]

            embed = discord.Embed(title="The location",
                                  color=JToHDifficulties.getColorHex(dif))

            embed.add_field(name="Tower", value=full_name, inline=False)

            embed.add_field(name="Area name", value=area_name, inline=False)

            embed.add_field(name="Full name",
                            value=area_full_name,
                            inline=False)

            embed.add_field(
                name="Location",
                value=(subrealm_text + tower_location).capitalize() + ' ' +
                str(int(tower_location_number)),
                inline=False)

            emblem_url = df_area[
                (df_area['Location'] == tower_location)
                & (df_area['Location number'] == tower_location_number) &
                (df_area['Location subnumber'] == tower_location_subnumber) &
                (df_area['Location type']
                 == tower_location_type)]['Emblem URL']

            if emblem_url is not None and str(
                    emblem_url.values[0]) != 'nan' and len(emblem_url) > 0:
                emblem_url = emblem_url.values[0]
                embed.set_thumbnail(url=emblem_url)

            await ctx.respond(embed=embed)

        except Exception as e:
            print(e)
            await ctx.respond("I can't find the location of **" + full_name +
                              "**")

        #await ctx.respond('<@' + str(user_id) + '> **' + full_name +'** is in **'+area_full_name +" ("+ (subrealm_text + tower_location).capitalize()  + ' ' +str(int(tower_location_number))+")**")  #Respond message
    else:
        await ctx.respond(await noTowerFound(tower))


@bot.command(guild_ids=[server_id],
             description="Check the full name of the tower")
async def towerfullname(ctx, tower):

    if (not await precheck(ctx)):
        await noPermission(ctx)
        return

    tower = await filtering_input(ctx, tower)
    user_id = ctx.author.id

    info = df_info[df_info['Acronym'].str.lower() == tower.lower()]

    if info.shape[0] > 0:
        tower_full_name = df_info[df_info['Acronym'].str.lower() ==
                                  tower.lower()]['Tower'].values[0]
        acronym = info['Acronym'].values[0]
        dif = info['Difficulty'].values[0]

        embed = discord.Embed(title="The full name of tower",
                              color=JToHDifficulties.getColorHex(dif))

        embed.add_field(name="Acronym", value=acronym, inline=False)

        embed.add_field(name="Full name", value=tower_full_name, inline=False)

        status, img_url = await printTowerImage(tower)
        embed.set_thumbnail(url=img_url)

        await ctx.respond(embed=embed)
        #await ctx.respond('<@' + str(user_id) + '> **'+tower+"** is **"+ tower_full_name+"**")  #Respond message
    else:
        await ctx.respond(await noTowerFound(tower))


@bot.command(guild_ids=[server_id],
             description="Check the number of floors of the tower")
async def floors(ctx, tower):

    if (not await precheck(ctx)):
        await noPermission(ctx)
        return

    tower = await filtering_input(ctx, tower)
    user_id = ctx.author.id

    info = df_info[df_info['Acronym'].str.lower() == tower.lower()]

    if info.shape[0] > 0:
        total_floors = df_info[df_info['Acronym'].str.lower() ==
                               tower.lower()]['Floors'].values[0]
        acronym = info['Acronym'].values[0]
        dif = info['Difficulty'].values[0]

        embed = discord.Embed(title="The number of floors of tower",
                              color=JToHDifficulties.getColorHex(dif))

        embed.add_field(name="Acronym", value=acronym, inline=False)

        embed.add_field(name="Floors", value=int(total_floors), inline=False)

        status, img_url = await printTowerImage(tower)
        embed.set_thumbnail(url=img_url)

        await ctx.respond(embed=embed)
        #await ctx.respond('<@' + str(user_id) + '> **'+tower+"** is **"+ tower_full_name+"**")  #Respond message
    else:
        await ctx.respond(await noTowerFound(tower))


@bot.command(guild_ids=[server_id],
             description="Show the name of tower in Thai")
async def thainame(ctx, tower):

    if (not await precheck(ctx)):
        await noPermission(ctx)
        return

    tower = await filtering_input(ctx, tower)
    user_id = ctx.author.id

    info = df_info[df_info['Acronym'].str.lower() == tower.lower()]

    if info.shape[0] > 0:
        thai_name = df_info[df_info['Acronym'].str.lower() ==
                            tower.lower()]['Thai name'].values[0]
        acronym = info['Acronym'].values[0]
        dif = info['Difficulty'].values[0]

        embed = discord.Embed(title="The name of tower in Thai",
                              color=JToHDifficulties.getColorHex(dif))

        embed.add_field(name="Acronym", value=acronym, inline=False)

        embed.add_field(name="Thai name", value=thai_name, inline=False)

        status, img_url = await printTowerImage(tower)
        embed.set_thumbnail(url=img_url)

        await ctx.respond(embed=embed)
        #await ctx.respond('<@' + str(user_id) + '> **'+tower+"** is **"+ tower_full_name+"**")  #Respond message
    else:
        await ctx.respond(await noTowerFound(tower))


@bot.command(guild_ids=[server_id],
             description="Search for all towers which are built by creator")
async def towerbycreator(ctx, username):

    if (not await precheck(ctx)):
        await noPermission(ctx)
        return

    username = await filtering_input(ctx, username)
    user_id = ctx.author.id

    info = df_info[df_info['Creators'].str.contains(
        "(?:\s|^)" + username.lower() + "(?:\s|,|$)", case=False,
        na=False)].sort_values(by='Num Difficulty', ascending=True)

    if info.shape[0] > 0:

        tower_list = ""

        for index, value in info.iterrows():
            tower_list += ("**[" + emoji.getEmoji(value['Difficulty']) +
                           "]** " + value['Tower'] + "\n")

        embed = discord.Embed(title="Towers by creator",
                              color=discord.Color.blue())

        embed.add_field(name="Creator", value=username, inline=False)

        embed.add_field(name="The list of towers",
                        value=tower_list,
                        inline=False)

        username_id = await getPlayerIdByUsername(username)

        avatar_url = await getAvatarImage(username_id)
        #print(username,username_id,avatar_url)

        embed.set_thumbnail(url=avatar_url)

        await ctx.respond(embed=embed)

    else:
        await ctx.respond(await noUsernameFound(username))


@bot.command(description='Check the list of towers in area')
#@commands.has_permissions(administrator=True)
#@commands.has_role("Crp")
async def towersbyarea(ctx, area_code):

    if (not await precheck(ctx)):
        await noPermission(ctx)
        return

    area_code = await filtering_input(ctx, area_code)

    #print(area_code)

    if True:  #try:

        tower_list = df_info[
            (df_info['Area code'].str.lower() == area_code.lower())
            & (df_info['Accessible'] == 'y')].sort_values(by='Num Difficulty',
                                                          ascending=True)
        if tower_list.shape[0] > 0:

            #await ctx.respond(tower_list)
            title = df_area[df_area['Acronym'].str.lower() ==
                            area_code.lower()].iloc[0]['Area name']

            list_str = ""

            for index, info in tower_list.iterrows():

                #guide_url = info['Video URL']

                dif = info['Difficulty']
                emoji_dif = ":grey_question:"

                emoji_dif = emoji.getEmoji(dif)
                if str(emoji_dif) == 'nan':
                    emoji_dif = ":grey_question:"

                list_str += ("**[" + emoji_dif + "]** (" + info['Acronym'] +
                             ') ' + info['Tower'] + "\n")

            embed = discord.Embed(title=title,
                                  description=list_str,
                                  color=discord.Color.blue())

            emblem_url = df_area[(df_area['Acronym'].str.lower() ==
                                  area_code.lower())]['Emblem URL']

            if emblem_url is not None and str(emblem_url) != 'nan' and len(
                    emblem_url) > 0:
                emblem_url = emblem_url.values[0]
                embed.set_thumbnail(url=emblem_url)

            await ctx.respond(embed=embed)
        else:
            error_list = [
                "What is **" + area_code +
                "**? The cemetery of ToDC:C and ToOEZ?",
                "What is **" + area_code +
                "**? The place that we can find ToAST:R that will never release?",
                "What is **" + area_code +
                "**? It is the location that bad tower like ToYV resides?",
                "What is **" + area_code +
                "**? The realm of hardfailed towers which curators think their design are not good?",
                "What is **" + area_code +
                "**? The place where we can play Mega Fun Obby?"
            ]
            error = random.choice(error_list)

            await ctx.respond(error)
    else:  #except Exception as e:
        print("error")
        #await ctx.respond(e)


def isDifferentColor(color1, color2, threshold=50):
    # Split the hex colors into their red, green, and blue components
    r1, g1, b1 = [int(color1[i:i + 2], 16) for i in range(1, 7, 2)]
    r2, g2, b2 = [int(color2[i:i + 2], 16) for i in range(1, 7, 2)]

    # Calculate the Euclidean distance between the colors
    #dist = math.sqrt((r1 - r2)**2 + (g1 - g2)**2 + (b1 - b2)**2)
    #dist = math.sqrt((r1 - r2)**2)+math.sqrt((g1 - g2)**2)+math.sqrt((b1 - b2)**2)

    rm = 0.5 * (r1 + r2)
    dr = r1 - r2
    dg = g1 - g2
    db = b1 - b2
    dist = math.sqrt((2 + rm / 256) * (dr * dr) + 4 * dg * dg +
                     (2 + ((255 - rm) / 256)) * db * db)

    # Check if the distance is larger than the threshold
    return dist > threshold, dist


@bot.command(
    description=
    'Get the list of towers that has at least 1 floor with defined color (e.g. red/yellow/green)'
)
#@commands.has_permissions(administrator=True)
#@commands.has_role("Crp")
async def towersbycolor(ctx, color):

    if (not await precheck(ctx)):
        await noPermission(ctx)
        return

    user_id = ctx.author.id
    color = await filtering_input(ctx, color.lower())
    """
    if str(threshold).isdigit():
      threshold=int(threshold)
      if threshold>100:
        threshold=100
      elif threshold<1:
        threshold=1
    else:
      threshold=100
    """
    threshold = 100

    color_to_hex = {}
    color_to_hex['red'] = "#FF0000"
    color_to_hex['maroon'] = "#800000"
    color_to_hex['crimson'] = "#DC143C"
    color_to_hex['orange'] = "#FFA500"
    color_to_hex['yellow'] = "#FFFF00"
    color_to_hex['gold'] = "#FFD700"
    color_to_hex['olive'] = "#808000"
    color_to_hex['green'] = "#00FF00"
    color_to_hex['lime'] = "#32CD32"
    color_to_hex['blue'] = "#0000FF"
    color_to_hex['cyan'] = "#00FFFF"
    color_to_hex['navy'] = "#000080"
    color_to_hex['teal'] = "#008080"
    color_to_hex['purple'] = "#800080"
    color_to_hex['violet'] = "#EE82EE"
    color_to_hex['pink'] = "#FFC0CB"
    color_to_hex['magenta'] = '#FF00FF'
    color_to_hex['brown'] = "#964B00"
    color_to_hex['gray'] = "#808080"
    color_to_hex['silver'] = "#C0C0C0"
    color_to_hex['black'] = "#000000"
    color_to_hex['white'] = "#FFFFFF"

    if re.match("^([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$", color):
        color = ("#" + color)
        color_to_hex[color] = (color).upper()

    if color_to_hex[color][1:3] == color_to_hex[color][4:5] and color_to_hex[
            color][4:5] == color_to_hex[color][6:7] and color_to_hex[color][
                1:3] == color_to_hex[color][6:7]:
        threshold = 35

    tower_temp_list = []
    is_first_time = True

    if color in color_to_hex:

        await ctx.defer()
        #await ctx.respond("<@" + str(user_id) + "> Please wait patiently. I am currently checking...")

        for index, row in df_color_colors.iterrows():
            acronym = row.values.tolist()[0]
            #print(acronym)
            color_list = row.values.tolist()[1:]
            for c in color_list:
                if str(c) != 'nan':
                    isNotColor, dist = isDifferentColor(
                        color_to_hex[color], str(c), threshold)
                    #print(acronym,has_color,color,dist)
                if not isNotColor:
                    #print(acronym,c,color_to_hex[color],dist)
                    tower_temp_list.append(acronym)
                    break

        tower_list = {}

        for tower in tower_temp_list:
            acronym = tower.strip()  #.text
            cur_info = df_info[(df_info['Acronym'] == acronym)
                               & (df_info['Accessible'] == 'y')]

            if len(cur_info) > 0:
                diff_point = cur_info['Num Difficulty'].values[0]

                tower_list[acronym] = diff_point

        sorted_tower_list = sorted(tower_list.items(), key=lambda x: x[1])
        #print(tower_list,sorted_tower_list)
        color_int = int(color_to_hex[color][1:7], 16)
        tower_str = ""
        for acronym, dif in sorted_tower_list:

            #print(acronym)

            cur_info = df_info[(df_info['Acronym'] == acronym)
                               & (df_info['Accessible'] == 'y')]

            if len(cur_info) > 0:

                cur_dif = cur_info.iloc[0]['Difficulty']
                location_code = cur_info.iloc[0]['Area code']
                location = df_area[df_area['Acronym'] ==
                                   location_code].iloc[0]['Area name']

                #tower_str += ("**"+acronym +"**\n")
                #tower_str += ("**["+emoji.getEmoji(cur_dif)+"]** "+acronym +"*\n")
                #tower_str += (acronym +" *("+location+")*\n")
                if len(tower_str) < 3500:
                    tower_str += ("**[" + emoji.getEmoji(cur_dif) + "]** " +
                                  acronym + " *(" + location + ")*\n")
                else:
                    embed = discord.Embed(
                        title="The list of towers by color (" + color + ")",
                        description=tower_str,
                        color=color_int)

                    #embed.add_field(name="The list of towers", value=tower_str,inline=False)
                    embed.set_thumbnail(
                        url="https://singlecolorimage.com/get/" +
                        color_to_hex[color][1:7].lower() + "/50x50")
                    await ctx.respond(embed=embed)
                    tower_str = ""
                    is_first_time = False

        if len(tower_str) > 0:
            embed = discord.Embed(title="The list of towers by color (" +
                                  color + ")",
                                  description=tower_str,
                                  color=color_int)

            #embed.add_field(name="The list of towers", value=tower_str,inline=False)
            embed.set_thumbnail(url="https://singlecolorimage.com/get/" +
                                color_to_hex[color][1:7].lower() + "/50x50")

            if (is_first_time):
                await ctx.respond(embed=embed)
            else:
                await ctx.send(embed=embed)
    else:
        await ctx.respond("<@" + str(user_id) + "> What is **" + color +
                          "** color? I don't understand the meaning of it")


@bot.command(guild_ids=[server_id],
             description="Check the punishment level of the tower")
async def punishmentlevel(ctx, tower):

    if (not await precheck(ctx)):
        await noPermission(ctx)
        return

    tower = await filtering_input(ctx, tower)
    user_id = ctx.author.id

    info = df_info[df_info['Acronym'].str.lower() == tower.lower()]

    if info.shape[0] > 0:
        tower_full_name = info['Tower'].values[0]
        tower_punishment = info['Punishment'].values[0]

        if (str(tower_punishment) != 'nan'):

            code_color = 'yellow'

            if (tower_punishment == 'mild'):
                code_color = 'green'
            elif (tower_punishment == 'severe'):
                code_color = 'red'

            await ctx.respond("<@" + str(user_id) +
                              "> The punishment level of **" +
                              tower_full_name + "** is **" + tower_punishment +
                              " [:" + code_color + "_square:]**")
        else:
            await ctx.respond("<@" + str(user_id) +
                              "> I can't find the punishment  level of **" +
                              tower_full_name + "**")
    else:
        await ctx.respond(await noTowerFound(tower))


@bot.command(guild_ids=[server_id],
             description="Check the difficulty spike level of the tower")
async def spikelevel(ctx, tower):

    if (not await precheck(ctx)):
        await noPermission(ctx)
        return

    tower = await filtering_input(ctx, tower)
    user_id = ctx.author.id

    info = df_info[df_info['Acronym'].str.lower() == tower.lower()]

    if info.shape[0] > 0:
        tower_full_name = info['Tower'].values[0]
        tower_spike = info['Difficulty Spike'].values[0]

        if (str(tower_spike) != 'nan'):

            code_color = 'yellow'

            if (tower_spike == 'mild'):
                code_color = 'green'
            elif (tower_spike == 'severe'):
                code_color = 'red'

            await ctx.respond("<@" + str(user_id) +
                              "> The difficulty spike level of **" +
                              tower_full_name + "** is **" + tower_spike +
                              " [:" + code_color + "_square:]**")
        else:
            await ctx.respond(
                "<@" + str(user_id) +
                "> I can't find the difficulty spike level of **" +
                tower_full_name + "**")
    else:
        await ctx.respond(await noTowerFound(tower))


@bot.command(guild_ids=[server_id],
             description="Generate the fake win message")
#@commands.has_permissions(administrator=True)
async def fakewin(ctx, username, tower):

    if (not await precheck(ctx)):
        await noPermission(ctx)
        return

    username = await filtering_input(ctx, username)
    tower = await filtering_input(ctx, tower)

    info = df_info[df_info['Acronym'].str.lower() == tower.lower()]

    if info.shape[0] > 0:

        try:
            info = info.iloc[0]
            full_name = info['Tower']
            normal_playtime = 60
            speedrun_playtime = 10

            if not math.isnan(info['Average normal playtime (minute)']):
                normal_playtime = info['Average normal playtime (minute)']
            if not math.isnan(info['Average speedrun playtime (minute)']):
                speedrun_playtime = info['Average speedrun playtime (minute)']
            difficulty = info['Difficulty']

            beat_minute = str(
                random.randint(speedrun_playtime, normal_playtime))

            beat_second = str(random.randint(0, 59)).zfill(2)
            beat_subsecond = str(random.randint(0, 99)).zfill(2)

            beat_time = beat_minute + ":" + beat_second + ":" + beat_subsecond

            more_exclam = ""

            if JToHDifficulties.isSC(difficulty):
                more_exclam = "!"

            await ctx.respond("**" + username + "** has beaten **" +
                              full_name + " [" + emoji.getEmoji(difficulty) +
                              "]** in `" + beat_time + "`!" + more_exclam)
        except:
            await ctx.respond(
                "Sorry! We have not enough information about **" + tower +
                "** :sob:")
    else:
        await ctx.respond(await noTowerFound(tower))


@fakewin.error
async def fakewin_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.respond(
            "Please also tell me the username and the acronym of tower (For example **"
            + prefix + "fakewin Crp_Killer ToCP**)")


@bot.command(guild_ids=[server_id],
             description="Show the current monthly challenge list")
async def currentmonthlychallenge(ctx):

    if (not await precheck(ctx)):
        await noPermission(ctx)
        return

    await ctx.defer()
    #await ctx.respond("Let me check...")

    URL = "https://jtoh.fandom.com/wiki/Monthly_Challenges"

    try:
        page = requests.get(URL, timeout=5)

        soup = BeautifulSoup(page.content, "html.parser")

        difficulty_list = ["easy", "hard", "challenging", "remorseless"]
        challenge_list = [
            "Beginner Challenges", "Intermediate Challenges",
            "Advanced Challenges", "Psychologically Unsafe Challenges"
        ]

        k = 0

        embed = discord.Embed(title="Current monthly challenge",
                              color=discord.Color.blue())

        for challenge in challenge_list:
            header = soup.findAll(text=challenge)[0]
            parent_tag = header.parent.parent.parent.parent

            contents = parent_tag.findNext('ul').find_all('li')

            invalid_tags = ['b', 'i', 'u', 'a', 'p', 'ul', 'li']
            item = 1

            diff = difficulty_list[k]

            #await ctx.send(emoji_code[diff]+" **"+challenge+"** "+emoji_code[diff])
            #time.sleep(0.5)
            content_string = ""

            for content in contents:

                content_string += (str(item) + ". " + content.text + "\n")
                item += 1

            embed.add_field(name=emoji.getEmoji(diff) + " **" + challenge +
                            "** ",
                            value=content_string,
                            inline=False)
            #await ctx.send(content_string)
            #time.sleep(1)
            k += 1

        avatar_url = "https://static.wikia.nocookie.net/ktoh/images/b/b1/Challengeticket.png/revision/latest/scale-to-width-down/180?cb=20210509102258"
        #print(username,username_id,avatar_url)

        embed.set_thumbnail(url=avatar_url)

        await ctx.respond(embed=embed)

    except Exception as e:
        print(e)
        await ctx.respond(
            "I can't find the information of monthly challenges right now")


@bot.command(guild_ids=[server_id],
             description="Check the trivia of the tower")
@commands.has_permissions(administrator=True)
async def trivia(ctx, tower):

    if (not await precheck(ctx)):
        await noPermission(ctx)
        return

    user_id = ctx.author.id

    tower = await filtering_input(ctx, tower)
    #tower=await correctTowerCaseSensitive(tower)
    #await ctx.respond("Let me check it...")
    await ctx.defer()

    info = df_info[df_info['Acronym'].str.lower() == tower.lower()]

    if info.shape[0] > 0:
        full_name = info.iloc[0]['Tower']
        tower_url = full_name.title().replace(" ",
                                              "_").replace("Of", "of").replace(
                                                  "And", "and")

        URL = "https://jtoh.fandom.com/wiki/" + tower_url

        URL = URL.replace("?", "%3F")

        page = requests.get(URL, timeout=5)

        if (page.status_code != 200):
            await ctx.respond(
                "Looks like I can't search for the trivia of **" + tower +
                "** right now")
        else:

            dif = info.iloc[0]['Difficulty']

            soup = BeautifulSoup(page.content, "html.parser")
            trivia_header = soup.find(id="Trivia")
            parent_tag = trivia_header.parent
            contents = parent_tag.findNext('ul', attrs={
                'class': None
            }).find_all('li', recursive=False)

            invalid_tags = ['b', 'i', 'u', 'a', 'p', 'ul', 'li']
            item = 1

            embed = discord.Embed(title="Trivia of " + full_name,
                                  color=JToHDifficulties.getColorHex(dif))

            try:
                for content in contents:

                    #for tag in invalid_tags:
                    #    for match in content.findAll(tag):
                    #        match.replaceWithChildren()
                    subcontents = content.find_all('li')

                    for s in content.select('li'):
                        s.extract()

                    main_content = content.text
                    #await ctx.send("`"+str(item)+". "+content.text+"`")
                    #time.sleep(0.75)

                    sub_content = "‎ \n"

                    subitem = 1

                    if (subcontents):
                        for subcontent in subcontents:
                            sub_content += (str(subitem) + ". " +
                                            subcontent.text + "\n")
                            #await ctx.send("`"+str(item)+"."+str(subitem)+". "+subcontent.text+"`")
                            #time.sleep(0.75)
                            subitem += 1

                    main_content = main_content.replace(",",
                                                        "").replace("\"", "'")
                    sub_content = sub_content.replace(",",
                                                      "").replace("\"", "'")
                    #print(main_content,sub_content)

                    embed.add_field(name="No." + str(item),
                                    value=main_content + " " + sub_content,
                                    inline=False)
                    item += 1

            except Exception as e:
                print(e)

            status, img_url = await printTowerImage(tower)
            embed.set_thumbnail(url=img_url)

            await ctx.respond(embed=embed)

            #await ctx.respond("<@"+str(user_id)+"> That's all for **"+full_name+"**")
    else:
        await ctx.respond(await noTowerFound(tower))


@trivia.error
async def trivia_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.respond(
            "Please also tell me the acronym of the tower you wanna see its trivia (For example **"
            + prefix + "trivia ToDC**)")


@bot.command(guild_ids=[server_id], description="Show the image of the tower")
async def towerimage(ctx, tower):

    if (not await precheck(ctx)):
        await noPermission(ctx)
        return

    tower = await filtering_input(ctx, tower)
    #tower=await correctTowerCaseSensitive(tower)

    #await ctx.respond("Let me find an image...")
    await ctx.defer()

    status, img_url = await printTowerImage(tower)

    user_id = ctx.author.id

    if img_url is not None:

        info = df_info[df_info['Acronym'].str.lower() == tower.lower()]
        dif = info.iloc[0]['Difficulty']
        full_name = info.iloc[0]['Tower']

        embed = discord.Embed(title="The image of " + full_name,
                              color=JToHDifficulties.getColorHex(dif))
        print(img_url)
        embed.set_image(url=img_url)
        await ctx.respond(embed=embed)
        #await ctx.send(img_url)
        """
        tempfilename = root_tmp_path + "tempimageimage" + tower + ".png"
        img = Image.open(requests.get(img_url, stream=True).raw)
        img = img.save(tempfilename)
        await ctx.respond("<@" + str(user_id) + "> This is the image of **" +
                          tower + "**",
                          file=discord.File(fp=tempfilename,
                                            filename="towerimage.png"))
        os.remove(tempfilename)
      """

    elif status == 1:

        await ctx.respond("<@" + str(user_id) +
                          "> I can\'t find the image of **" + tower +
                          "** right now")

    else:
        await ctx.respond(await noTowerFound(tower))


@towerimage.error
async def towerimage_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.respond(
            "Please also tell me the acronym of the tower you wanna see its image (For example **"
            + prefix + "towerimage ToDC**)")


@bot.command(guild_ids=[server_id], description="Show the colors of the tower")
#@commands.has_permissions(administrator=True)
async def towercolors(ctx, tower):

    if (not await precheck(ctx)):
        await noPermission(ctx)
        return

    user_id = ctx.author.id
    """
    global is_drawing
    if is_drawing == 1:
        await ctx.respond("<@" + str(user_id) +
                          "> Sorry I'm busy drawing tower")
        return
    """
    tower = await filtering_input(ctx, tower)
    #tower=await correctTowerCaseSensitive(tower)

    await ctx.defer()
    #await ctx.respond("Please wait for me while I'm drawing the tower")
    status = await printTowerColors(ctx, tower, 'e')

    if status == -1:

        full_name = df_info[df_info["Acronym"].str.lower() ==
                            tower.lower()].iloc[0]['Tower']
        await ctx.respond("<@" + str(user_id) +
                          "> This is the visualization of **" +
                          str(full_name) + "**")
    elif status == 1:
        await ctx.respond("<@" + str(user_id) +
                          "> Looks like I can't search for the image of **" +
                          tower + "** right now")
    elif status == 0:

        await ctx.respond("<@" + str(user_id) +
                          "> Sorry but I can't find the colors of **" +
                          str(tower) + "** :sob:")

    else:
        await ctx.respond(await noTowerFound(tower))


@towercolors.error
async def towercolors_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.respond(
            "Please also tell me the acronym of the tower you wanna see its colors (For example **"
            + prefix + "towercolors ToDC**)")


@bot.command(guild_ids=[server_id],
             description="Get the name of all creators of the tower")
#@commands.has_permissions(administrator=True)
async def creator(ctx, tower):
    if (not await precheck(ctx)):
        await noPermission(ctx)
        return

    user_id = ctx.author.id

    tower = await filtering_input(ctx, tower)

    info = df_info[df_info['Acronym'].str.lower() == tower.lower()]

    if info.shape[0] > 0:
        full_name = info.iloc[0]['Tower']
        #tower_url = full_name.title().replace(" ", "_").replace("Of", "of").replace("And", "and").replace("\'S", "\'s")

        dif = info.iloc[0]['Difficulty']
        """
        URL = "https://jtoh.fandom.com/wiki/" + tower_url
        URL = URL.replace("?", "%3F")

        page = requests.get(URL, timeout=5)

        if (page.status_code != 200):
            await ctx.respond("Oh no! I can't find the creators of " +
                              tower_url)
        else:
            soup = BeautifulSoup(page.content, "html.parser")
            creator_table = soup.findAll('div', {"data-source": "creator(s)"})
            creator_table = creator_table[0].findNext(
                'div', {'class', 'pi-data-value'}).text
            name_list = creator_table.replace(", ", "\n").replace(
                "and ", "\n").replace("& ", "\n").replace("\n\n", "\n")

            embed = discord.Embed(title="Creators of " + full_name,
                                  color=JToHDifficulties.getColorHex(dif))
            embed.add_field(name="List of the creators",
                            value=name_list,
                            inline=False)

            status, img_url = await printTowerImage(tower)

            embed.set_thumbnail(url=img_url)
            await ctx.respond(embed=embed)
        """
        creator = str(info.iloc[0]['Creators'])
        name_list = creator.replace(", ", "\n")

        embed = discord.Embed(title=full_name,
                              color=JToHDifficulties.getColorHex(dif))

        embed.add_field(name="Creator(s)", value=name_list, inline=False)

        status, img_url = await printTowerImage(tower)

        embed.set_thumbnail(url=img_url)
        await ctx.respond(embed=embed)
    else:
        await ctx.respond(await noTowerFound(tower))


@bot.command(guild_ids=[server_id],
             description="Get the song playlist of the tower")
#@commands.has_permissions(administrator=True)
async def towerplaylist(ctx, tower):

    if (not await precheck(ctx)):
        await noPermission(ctx)
        return

    user_id = ctx.author.id

    tower = await filtering_input(ctx, tower)
    #tower=await correctTowerCaseSensitive(tower)

    info = df_info[df_info['Acronym'].str.lower() == tower.lower()]

    if info.shape[0] > 0:

        await ctx.respond("I'm finding the playlist...")
        music_list = await getTowerPlaylist(ctx, tower)

        print(music_list)

        if len(music_list) > 0:

            full_name = df_info[df_info["Acronym"].str.lower() ==
                                tower.lower()].iloc[0]['Tower']

            dif = info['Difficulty'].values[0]

            embed = discord.Embed(title="The playlist of " + full_name,
                                  color=JToHDifficulties.getColorHex(dif))

            k = 1

            for music in music_list:
                embed.add_field(name="Music " + str(k),
                                value=music[1],
                                inline=False)
                k += 1
                #await ctx.send(music)
                #time.sleep(0.75)

            status, img_url = await printTowerImage(tower)
            embed.set_thumbnail(url=img_url)

            await ctx.respond(embed=embed)
            #await ctx.respond("<@"+str(user_id)+"> This is the playlist of **"+str(full_name)+"**")
        else:

            await ctx.respond("<@" + str(user_id) +
                              "> Sorry but I can't find the playlist of **" +
                              str(tower) + "** :sob:")

    else:
        await ctx.respond(await noTowerFound(tower))


@towercolors.error
async def towerplaylist_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.respond(
            "Please also tell me the acronym of the tower you wanna see its towerplaylist (For example **"
            + prefix + "towerplaylist ToBBB**)")


@bot.command(
    guild_ids=[server_id],
    description="Give an idea of the gradient of the tower (Between 5-25 floors)"
)
#@commands.has_permissions(administrator=True)
async def gradient(ctx, floor=10):

    floor = await filtering_input(ctx,floor)
  
    if str(floor).isdigit():
        floor = int(floor)
        if floor > 25:
            floor = 25
        elif floor < 5:
            floor = 5
    else:
        floor = 10

    user_id = ctx.author.id
    await ctx.defer()

    #hex_code=['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F']

    color_start = [
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255)
    ]
    color_end = [
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255)
    ]

    floors = []

    embed = discord.Embed(title="Tower gradient idea",
                          color=discord.Color.blue())

    for k in range(floor):
        color_r = int((color_start[0]) * (k / (floor - 1)) + (color_end[0]) *
                      ((floor - 1 - k) / (floor - 1)))
        color_g = int((color_start[1]) * (k / (floor - 1)) + (color_end[1]) *
                      ((floor - 1 - k) / (floor - 1)))
        color_b = int((color_start[2]) * (k / (floor - 1)) + (color_end[2]) *
                      ((floor - 1 - k) / (floor - 1)))

        hex_r = hex(color_r)
        hex_g = hex(color_g)
        hex_b = hex(color_b)

        hex_code = hex_r[2:].zfill(2) + hex_g[2:].zfill(2) + hex_b[2:].zfill(2)

        color_code = "(" + str(color_r) + "," + str(color_g) + "," + str(
            color_b) + ")"

        #print(hex_code)
        embed.add_field(name="Floor " + str(k + 1),
                        value=color_code,
                        inline=True)
        floors.append(hex_code)

    #print(floors)

    tower_img_template = generatetowerfromcolors(reversed(floors))
    tempfilename = root_tmp_path + "tempgradient.png"
    tower_img_template = tower_img_template.save(tempfilename)

    file = discord.File(fp=tempfilename, filename="towergradient.png")

    #print(tempfilename)
    embed.set_image(url="attachment://towergradient.png")

    await ctx.respond("<@" + str(user_id) +
                      "> This is my tower gradient idea in RGB mode 😍",
                      file=file,
                      embed=embed)

    os.remove(tempfilename)


@bot.command(guild_ids=[server_id],
             description="Make a new tower from the two existing towers")
#@commands.has_permissions(administrator=True)
async def breed(ctx, male, female):

    if (not await precheck(ctx)):
        await noPermission(ctx)
        return

    #tower=await correctTowerCaseSensitive(tower)
    male = await filtering_input(ctx, male)
    female = await filtering_input(ctx, female)

    floor_list_male = []
    floor_list_female = []
    info_male = None
    info_female = None

    user_id = ctx.author.id
    """
    global is_drawing
    if is_drawing == 1:
        await ctx.respond("<@" + str(user_id) +
                          "> Sorry I'm busy drawing tower")
        return

    is_drawing = 1
    """
    await ctx.respond("Please don't disturb them while they are breeding")

    try:
        info_male = df_info[df_info['Acronym'].str.lower() == male.lower()]
        floor_list_male = await getTowerColors(male)
    except:
        await ctx.respond(await noTowerFound(male))
        is_drawing = 0
        return

    try:
        info_female = df_info[df_info['Acronym'].str.lower() == female.lower()]
        floor_list_female = await getTowerColors(female)
    except:
        await ctx.respond(await noTowerFound(female))
        is_drawing = 0
        return

    if (len(floor_list_male) != len(floor_list_female)):
        await ctx.respond("<@" + str(user_id) +
                          "> NOOO! They have different size. They can't breed!"
                          )
    else:

        floor_list_kid = []

        for k in range(len(floor_list_male)):
            color_male = floor_list_male[k]
            color_female = floor_list_female[k]

            #R part
            color_r_kid = hex(
                round((int(color_male[0:2], 16) + int(color_female[0:2], 16)) /
                      2))[2:]
            color_g_kid = hex(
                round((int(color_male[2:4], 16) + int(color_female[2:4], 16)) /
                      2))[2:]
            color_b_kid = hex(
                round((int(color_male[4:6], 16) + int(color_female[4:6], 16)) /
                      2))[2:]

            #print(color_r_kid,color_g_kid,color_b_kid)

            floor_list_kid.append(
                str(color_r_kid.zfill(2)) + str(color_g_kid.zfill(2)) +
                str(color_b_kid.zfill(2)))
        """
    for floor in reversed(floor_list_kid):
      color_url="https://singlecolorimage.com/get/"+floor+"/25x25"

      await ctx.send(color_url)
      time.sleep(0.75)
    """
        #print(floor_list_kid)
        tower_img_template = generatetowerfromcolors(reversed(floor_list_kid))
        tempfilename = root_tmp_path + "tempbreed" + male + "_" + female + ".png"
        tower_img_template = tower_img_template.save(tempfilename)

        await ctx.send(
            file=discord.File(fp=tempfilename, filename="towerbreed.png"))

        os.remove(tempfilename)

        is_drawing = 0

        full_name_male = info_male.iloc[0]['Tower']
        full_name_female = info_female.iloc[0]['Tower']

        kid_name = ""

        male_token = full_name_male.split(" ")

        if len(male) > 3 or len(male) == 2:
            male_token.pop()

        kid_name += (" ".join(male_token) + " ")

        #print(male)

        if len(male) == 3:
            kid_name += "and "

        female_token = full_name_female.split(" ")
        kid_name += (female_token[-1])

        #print(female_token)

        await ctx.send("<@" + str(user_id) +
                       "> Yay! They successfully bred **" + kid_name + "**")

    is_drawing = 0
    return


@breed.error
async def breed_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.respond(
            "Please also tell me the acronym of the tower you want them to breed (For example **"
            + prefix + "breed ToAAA ToFE**)")


@bot.command()
@commands.has_role("Crp")
async def imagetest(ctx, tower):
    status, img_url = await printTowerImage(tower)
    img = Image.open(requests.get(img_url, stream=True).raw)
    tempfilename = root_tmp_path + "tempimage" + tower + ".png"
    #img = img.filter(ImageFilter.GaussianBlur(5))
    width, height = img.size
    small_img = img.resize((25, 25), Image.Resampling.BILINEAR)
    img = small_img.resize((width, height), Image.Resampling.NEAREST)
    img = img.save(tempfilename)
    await ctx.respond(file=discord.File(tempfilename))
    os.remove(tempfilename)

    #await ctx.send(img_url)


class DifficultyModeButtons(discord.ui.View):

    difficulty_mode = "e"

    async def on_timeout(self):
        for child in self.children:
            child.disabled = True
        await self.message.edit(
            content="You can no longer select the difficulty", view=self)

    @discord.ui.button(label="Easy", row=0, style=discord.ButtonStyle.success)
    async def first_button_callback(self, button, interaction):
        self.difficulty_mode = "e"
        await interaction.response.defer()
        #await interaction.response.send_message("You clicked easy")

    @discord.ui.button(label="Hard", row=0, style=discord.ButtonStyle.danger)
    async def second_button_callback(self, button, interaction):
        self.difficulty_mode = "h"
        await interaction.response.defer()
        #await interaction.response.send_message("You clicked hard")


@bot.command(guild_ids=[server_id],
             description="Play the tower guessing game by its image")
#@commands.has_permissions(administrator=True)
async def guesstowerimage(ctx):

    if (not await precheck(ctx)):
        await noPermission(ctx)
        return

    user_id = ctx.author.id

    timeout_period = 10

    view = DifficultyModeButtons(timeout=timeout_period)

    await ctx.respond("Choose the difficulty please", view=view)

    def check(m):
        return True

    try:
        interaction = await bot.wait_for("interaction",
                                         check=check,
                                         timeout=timeout_period)

    except Exception as e:
        print(e)
        await ctx.send(
            "<@" + str(user_id) +
            "> You ran out of time! You can no longer select the difficulty")
        return

    difficulty = view.difficulty_mode

    #await ctx.defer()
    await ctx.send("Let me pick an image...")

    tower_list = df_info[(df_info['Accessible'] == 'y') & (
        df_info['Tower type'] != 'TowerRush')]["Acronym"].values.tolist()
    tower = random.choice(tower_list)

    status, img_url = await printTowerImage(tower)

    user_id = ctx.author.id

    if img_url is not None:
        if difficulty == 'h':
            img = Image.open(requests.get(img_url, stream=True).raw)
            tempfilename = root_tmp_path + "tempimage" + tower + ".png"
            #img = img.filter(ImageFilter.GaussianBlur(5))
            width, height = img.size
            small_img = img.resize((25, 25), Image.Resampling.BILINEAR)
            img = small_img.resize((width, height), Image.Resampling.NEAREST)
            img = img.save(tempfilename)
            await ctx.send(
                "<@" + str(user_id) +
                "> OK pls tell me the acronym of the tower in image",
                file=discord.File(fp=tempfilename, filename="towerimage.png"))
            os.remove(tempfilename)
        else:
            #time.sleep(1)
            """
      embed = discord.Embed()
      embed.set_image(url=img_url)
      await ctx.respond("<@"+str(user_id)+"> OK pls tell me the acronym of the tower in image",embed=embed)
      """
            tempfilename = root_tmp_path + "tempimageimage" + tower + ".png"
            img = Image.open(requests.get(img_url, stream=True).raw)
            img = img.save(tempfilename)
            await ctx.send(
                "<@" + str(user_id) +
                "> OK pls tell me the acronym of the tower in image",
                file=discord.File(fp=tempfilename, filename="towerimage.png"))
            os.remove(tempfilename)

        def checkAnswer(m):
            return m.author == ctx.author

        try:

            full_name = df_info[df_info["Acronym"] == tower].iloc[0]['Tower']
            guess = await bot.wait_for('message',
                                       check=checkAnswer,
                                       timeout=15)

            answer = await filtering_message(guess.content)

            if ((answer).lower() == tower.lower()
                    or (answer).lower() == (full_name).lower()):
                await ctx.send("<@" + str(user_id) +
                               "> Wow! You are so smart. It is **" +
                               full_name + "**")
                if difficulty == 'e':
                    db_handler.addGameScore(user_id, 1)
                elif difficulty == 'h':
                    db_handler.addGameScore(user_id, 2)
            else:
                await ctx.send("<@" + str(user_id) +
                               "> Oh! you are wrong. It is **" + full_name +
                               "**")

        except Exception as e:
            print(e)
            await ctx.send("<@" + str(user_id) +
                           "> You ran out of time. It is **" + full_name +
                           "**")
    else:
        await ctx.send("<@" + str(user_id) +
                       "> Sorry! I can't think of any tower right now :sob:")


@bot.command(guild_ids=[server_id],
             description="Play the tower guessing game by its colors")
#@commands.has_permissions(administrator=True)
async def guesstowercolors(ctx):

    if (not await precheck(ctx)):
        await noPermission(ctx)
        return

    user_id = ctx.author.id

    timeout_period = 10

    view = DifficultyModeButtons(timeout=timeout_period)

    await ctx.respond("Choose the difficulty please", view=view)

    def check(m):
        return True

    try:
        interaction = await bot.wait_for("interaction",
                                         check=check,
                                         timeout=timeout_period)

    except Exception as e:
        print(e)
        await ctx.send(
            "<@" + str(user_id) +
            "> You ran out of time! You can no longer select the difficulty")
        return

    difficulty = view.difficulty_mode

    #difficulty = await filtering_message(difficulty)

    #user_id = ctx.author.id
    """
    global is_drawing
    if is_drawing == 1:
        await ctx.respond("<@" + str(user_id) +
                          "> Sorry I'm busy drawing tower")
        return
    """
    #await ctx.defer()
    await ctx.send("Let me pick the tower...")

    tower_list = df_info[(df_info['Accessible'] == 'y') & (
        df_info['Tower type'] != 'TowerRush')]["Acronym"].values.tolist()
    tower = random.choice(tower_list)

    status = await printTowerColors(ctx, tower, difficulty)

    full_name = df_info[df_info["Acronym"] == tower].iloc[0]['Tower']

    if status == -1:
        await ctx.respond(
            "<@" + str(user_id) +
            "> Can you guess the acronym of the tower by its colors?")

        def checkAnswer(m):
            return m.author == ctx.author

        try:

            guess = await bot.wait_for('message',
                                       check=checkAnswer,
                                       timeout=15)

            answer = await filtering_message(guess.content)

            if ((answer).lower() == tower.lower()
                    or (answer).lower() == (full_name).lower()):
                await ctx.send("<@" + str(user_id) +
                               "> Wow! You are so smart. It is **" +
                               full_name + "**")
                if difficulty == 'e':
                    db_handler.addGameScore(user_id, 3)
                elif difficulty == 'h':
                    db_handler.addGameScore(user_id, 5)
            else:
                await ctx.send("<@" + str(user_id) +
                               "> Oh! you are wrong. It is **" + full_name +
                               "**")

        except Exception as e:
            print(e)
            await ctx.send("<@" + str(user_id) +
                           "> You ran out of time. It is **" + full_name +
                           "**")
    else:
        await ctx.send("<@" + str(user_id) +
                       "> Sorry! I can't think of any tower right now :sob:")


@bot.command(guild_ids=[server_id],
             description="Play the tower guessing game by its missing letters")
#@commands.has_permissions(administrator=True)
async def guesstowerword(ctx):

    if (not await precheck(ctx)):
        await noPermission(ctx)
        return

    user_id = ctx.author.id

    timeout_period = 10

    view = DifficultyModeButtons(timeout=timeout_period)

    await ctx.respond("Choose the difficulty please", view=view)

    def check(m):
        return True

    try:
        interaction = await bot.wait_for("interaction",
                                         check=check,
                                         timeout=timeout_period)

    except Exception as e:
        print(e)
        await ctx.send(
            "<@" + str(user_id) +
            "> You ran out of time! You can no longer select the difficulty")
        return

    difficulty = view.difficulty_mode

    await ctx.respond("Let me pick the tower...")

    tower_list = df_info[(df_info['Accessible'] == 'y') & (
        df_info['Tower type'] != 'TowerRush')]["Acronym"].values.tolist()
    tower = random.choice(tower_list)

    full_name = df_info[df_info["Acronym"] == tower].iloc[0]['Tower']

    lives = 3
    answer_waiting_period = 20

    if difficulty == 'h':
        lives = 1
        answer_waiting_period = 15

    letters_list = []
    status = None
    msg = None

    while lives > 0:

        is_reveal = True

        hidden_word = ""

        for k in range(0, len(full_name)):

            letter = full_name[k]
            is_found_letter = False

            if letter.lower() in letters_list or letter.upper(
            ) in letters_list:
                is_found_letter = True

            if not is_found_letter and letter != ' ':
                hidden_word += "#"
                is_reveal = False
            else:
                hidden_word += letter

        #print(full_name,hidden_word)
        if is_reveal == True:
            status = 'Win'
            break

        color_status = discord.Color.green()

        if (lives == 2):
            color_status = discord.Color.yellow()
        elif (lives == 1):
            color_status = discord.Color.red()

        embed = discord.Embed(title="Guess the tower word game",
                              color=color_status)

        lives_status = ""
        for k in range(0, 3):
            if k < lives:
                lives_status += ":heart:"
            else:
                lives_status += ":black_heart:"

        embed.add_field(name="Lives", value=lives_status, inline=False)

        embed.add_field(name="Your guessing", value=hidden_word, inline=True)

        if True:
            msg = await ctx.send("<@" + str(user_id) + ">", embed=embed)
            await ctx.send(
                "Please suggest the letter you think it is included in the word (Or tell me its full name if you know the answer)"
            )
        else:
            await msg.edit("<@" + str(user_id) + ">", embed=embed)

        def checkAnswer(m):
            return m.author == ctx.author

        try:
            """
            await ctx.send(
                "Please suggest the letter you think it is included in the word (Or tell me its full name if you know the answer)"
            )
           """
            guess = await bot.wait_for('message',
                                       check=checkAnswer,
                                       timeout=answer_waiting_period)

            def filtering_answer(input):

                #if input.index("@")>=0:
                #await hacking_handler(ctx)
                #await ctx.send("c!warns <@" + str(user_id) + ">")

                if not re.match("^[-a-zA-Z0-9_\':?, ]*$", input):
                    input = ""
                return input[0:50]

            answer = filtering_answer(guess.content)

            if answer.lower() == full_name.lower():
                #print("yes")
                status = 'Win'
                break
            elif answer.lower() in full_name.lower() and answer.lower(
            ) not in letters_list:
                letters_list.append(answer.lower())
            else:
                lives -= 1
                if lives == 0:
                    status = 'Lose'
                    break

            #await guess.delete()

        except Exception as e:
            print(e)
            await ctx.send("<@" + str(user_id) +
                           "> You ran out of time! The answer is **" +
                           full_name + "**. Please try again next time")
            return

    if (status == 'Win'):
        await ctx.send("<@" + str(user_id) +
                       "> Wow! You are intelligent. The answer is **" +
                       full_name + "**")
        if difficulty == 'e':
            db_handler.addGameScore(user_id, 5)
        elif difficulty == 'h':
            db_handler.addGameScore(user_id, 10)
    else:
        await ctx.send("<@" + str(user_id) + "> You died! The answer is **" +
                       full_name + "**. Please try again next time")


@bot.command(guild_ids=[server_id],
             description="Play the tower guessing game by its difficulty")
#@commands.has_permissions(administrator=True)
async def guesstowerbydifficulty(ctx):

    if (not await precheck(ctx)):
        await noPermission(ctx)
        return

    user_id = ctx.author.id

    timeout_period = 10

    view = DifficultyModeButtons(timeout=timeout_period)

    await ctx.respond("Choose the difficulty please", view=view)

    def check(m):
        return True

    try:
        interaction = await bot.wait_for("interaction",
                                         check=check,
                                         timeout=timeout_period)

    except Exception as e:
        print(e)
        await ctx.send(
            "<@" + str(user_id) +
            "> You ran out of time! You can no longer select the difficulty")
        return

    difficulty = view.difficulty_mode

    await ctx.respond("Let me pick the tower...")

    tower_list = df_info[
        (df_info['Accessible'] == 'y') & (df_info['Tower type'] != 'TowerRush')
        & (df_info['Location type'] != 'event') &
        (df_info['Num Difficulty'].notnull())]["Acronym"].values.tolist()
    tower = random.choice(tower_list)

    full_name = df_info[df_info["Acronym"] == tower].iloc[0]['Tower']
    diff_point = df_info[df_info["Acronym"] == tower].iloc[0]['Num Difficulty']

    lives = 10
    answer_waiting_period = 25

    if difficulty == 'h':
        answer_waiting_period = 20

    guess_list = [tower]
    guess_description = {}
    status = None
    msg = None

    while lives > 0:

        color_status = discord.Color.red()

        if (lives >= 7):
            color_status = discord.Color.green()
        elif (lives >= 4):
            color_status = discord.Color.yellow()

        guessing_str = ":question: :question: :question:"

        if len(guess_list) > 0:
            guessing_str = ""
            for t in guess_list:
                if t == tower:
                    guessing_str += (":question: :question: :question:\n")
                else:
                    guessing_str += ("**" + t + "** " + guess_description[t] +
                                     "\n")

        embed = discord.Embed(title="Guess the tower's difficulty game",
                              color=color_status)

        lives_status = ""
        for k in range(0, 10):
            if k < lives:
                lives_status += ":heart:"
            else:
                lives_status += ":black_heart:"

        embed.add_field(name="Lives", value=lives_status, inline=False)

        embed.add_field(name="Your guessing", value=guessing_str, inline=True)

        if True:
            msg = await ctx.send("<@" + str(user_id) + ">", embed=embed)
            await ctx.send(
                "Please suggest the acronym of the tower you think it is correct"
            )
        else:
            await msg.edit("<@" + str(user_id) + ">", embed=embed)

        def checkAnswer(m):
            return m.author == ctx.author

        try:
            """
            await ctx.send(
                "Please suggest the letter you think it is included in the word (Or tell me its full name if you know the answer)"
            )
           """
            guess = await bot.wait_for('message',
                                       check=checkAnswer,
                                       timeout=answer_waiting_period)

            def filtering_answer(input):

                #if input.index("@")>=0:
                #await hacking_handler(ctx)
                #await ctx.send("c!warns <@" + str(user_id) + ">")

                if not re.match("^[-a-zA-Z0-9_':?, ]*$", input):
                    input = ""
                return input[0:50]

            answer = filtering_answer(guess.content)

            if answer.lower() == tower.lower():
                #print("yes")
                status = 'Win'
                break
            else:
                lives -= 1

                if lives == 0:
                    status = 'Lose'
                    break

                if len(df_info[df_info["Acronym"].str.lower() ==
                               answer.lower()]) > 0:

                    your_point = df_info[df_info["Acronym"].str.lower(
                    ) == answer.lower()].iloc[0]['Num Difficulty']

                    your_acronym = df_info[df_info["Acronym"].str.lower() ==
                                           answer.lower()].iloc[0]['Acronym']

                    your_dif = df_info[df_info["Acronym"].str.lower() ==
                                       answer.lower()].iloc[0]['Difficulty']

                    your_subdif = df_info[df_info["Acronym"].str.lower(
                    ) == answer.lower()].iloc[0]['Sub difficulty']

                    difficulty_label = your_subdif.capitalize(
                    ) + " " + emoji.getEmoji(your_dif)
                    difficulty_hint = " "

                    is_append = True

                    if not re.match("^-?[0-9]*\.?[0-9]+$", str(your_point)):
                        await ctx.send(
                            "<@" + str(user_id) +
                            "> Oh! Looks like I can't determine the difficulty of **"
                            + your_acronym + "**")
                        is_append = False
                    elif your_point < diff_point:
                        keyword = ""
                        if diff_point - your_point >= 1:
                            keyword = "extremely "
                            difficulty_hint = " :arrow_up_small: :arrow_up_small: :arrow_up_small:"
                        elif diff_point - your_point >= 0.5:
                            keyword = "kinda "
                            difficulty_hint = " :arrow_up_small: :arrow_up_small:"
                        else:
                            keyword = "slightly "
                            difficulty_hint = " :arrow_up_small:"

                        if difficulty == 'h':
                            keyword = "just "
                            difficulty_hint = "harder"

                        await ctx.send("<@" + str(user_id) +
                                       "> Oh no! My tower is " + keyword +
                                       "harder than **" + your_acronym + "**")
                    elif your_point > diff_point:
                        keyword = ""
                        if your_point - diff_point >= 1:
                            keyword = "extremely "
                            difficulty_hint = " :arrow_down_small: :arrow_down_small: :arrow_down_small:"
                        elif your_point - diff_point >= 0.5:
                            keyword = "kinda "
                            difficulty_hint = " :arrow_down_small: :arrow_down_small:"
                        else:
                            keyword = "slightly "
                            difficulty_hint = " :arrow_down_small:"

                        if difficulty == 'h':
                            keyword = "just "
                            difficulty_hint = "easier"

                        await ctx.send("<@" + str(user_id) +
                                       "> Oh no! My tower is " + keyword +
                                       "easier than **" + your_acronym + "**")
                    else:
                        difficulty_hint = "same difficulty"
                        await ctx.send(
                            "<@" + str(user_id) +
                            "> Almost there! My tower is as hard as **" +
                            your_acronym + "**")

                    if is_append:
                        guess_list.append(your_acronym)
                    guess_description[
                        your_acronym] = "( " + difficulty_label + " - " + difficulty_hint + ")"

                    tower_point = {}

                    for t in guess_list:
                        d = df_info[df_info["Acronym"].str.lower() ==
                                    t.lower()].iloc[0]['Num Difficulty']
                        tower_point[t] = d

                    sorted_tower_point = dict(
                        sorted(tower_point.items(),
                               key=operator.itemgetter(1),
                               reverse=True))

                    guess_list = list(sorted_tower_point.keys())

                else:
                    await ctx.send("<@" + str(user_id) +
                                   "> I don't know what are you talking about")

                time.sleep(1)

            #await guess.delete()

        except Exception as e:
            print(e)
            await ctx.send("<@" + str(user_id) +
                           "> You ran out of time! The answer is **" +
                           full_name + "**. Please try again next time")
            return

    if (status == 'Win'):
        await ctx.send("<@" + str(user_id) +
                       "> Wow! You are intelligent. The answer is **" +
                       full_name + "**")
        if difficulty == 'e':
            db_handler.addGameScore(user_id, 15)
        elif difficulty == 'h':
            db_handler.addGameScore(user_id, 25)
    else:
        await ctx.send("<@" + str(user_id) + "> You died! The answer is **" +
                       full_name + "**. Please try again next time")


@bot.command(guild_ids=[server_id],
             description="Play the 'Not that letter' game")
#@commands.has_permissions(administrator=True)
async def notthatletter(ctx):

    if (not await precheck(ctx)):
        await noPermission(ctx)
        return

    user_id = ctx.author.id

    timeout_period = 10

    embed = discord.Embed(title="Welcome to 'Not that letter' game",
                          description="",
                          color=discord.Color.green())

    embed.add_field(
        name="How to play?",
        value=
        "**1.** You have to say the acronym whose letters is not in my blacklist\n**2.** If it is tower/citadel/steeple, you can ignore the first two letters of the acronym (To/Co/So)\n**3.** Let's say that the letter in my blacklist is **T**, you can't say the acronym of the tower with the letter **T**; For example, **ToT, ToGT, or ToTA**, but you can say the acronym like **ToA, ToBC** as we ignore the first letter **T**\n**4.** If you say the acronym whose letter is in my blacklist, or you say the acronym that you already said, the game ends",
        inline=False)

    await ctx.respond(embed=embed)

    view = DifficultyModeButtons(timeout=timeout_period)

    await ctx.send("Choose the difficulty please", view=view)

    def check(m):
        return True

    try:
        interaction = await bot.wait_for("interaction",
                                         check=check,
                                         timeout=timeout_period)

    except Exception as e:
        print(e)
        await ctx.send(
            "<@" + str(user_id) +
            "> You ran out of time! You can no longer select the difficulty")
        return

    difficulty = view.difficulty_mode
    """
    await ctx.respond("Let me pick the tower...")

    tower_list = df_info[(df_info['Accessible'] == 'y') & (
        df_info['Tower type'] != 'TowerRush')]["Acronym"].values.tolist()
    tower = random.choice(tower_list)

    full_name = df_info[df_info["Acronym"] == tower].iloc[0]['Tower']
    """

    round = 0
    answer_waiting_period = 15
    diff_mode = '**[' + emoji.getEmoji('easy') + ']** Easy'

    if difficulty == 'h':
        answer_waiting_period = 10
        diff_mode = '**[' + emoji.getEmoji('difficult') + ']** Hard'

    letters_list = 'abcdefghijklmnopqrstuvwxyz'

    guess_list = {}
    danger_letter = {}
    is_dead = False

    while round < 100:

        if (round % 3 == 0) or (difficulty == 'h'):
            random_letter = random.choice(letters_list)
            danger_letter[random_letter] = 1
            letters_list = letters_list.replace(random_letter, '')

        round += 1

        danger_letter_list = list(danger_letter.keys())
        danger_letter_upper = [v.upper() for v in danger_letter_list]
        letter_str = ", ".join(danger_letter_upper)

        await ctx.send(
            "<@" + str(user_id) + "> **Round " + str(round) +
            "**: Please tell me the acronym of the tower without the letter **"
            + letter_str +
            "**. Don't say the tower that you already said or the game ends")

        def checkAnswer(m):
            return m.author == ctx.author

        try:

            guess = await bot.wait_for('message',
                                       check=checkAnswer,
                                       timeout=answer_waiting_period)

            def filtering_answer(input):

                #if input.index("@")>=0:
                #await hacking_handler(ctx)
                #await ctx.send("c!warns <@" + str(user_id) + ">")

                if not re.match("^[-a-zA-Z0-9_':?, ]*$", input):
                    input = ""
                return input[0:50]

            answer = filtering_answer(guess.content).lower()

            info = df_info[(df_info["Acronym"].str.lower() == answer)]

            if len(info) > 0:
                acronym = info.iloc[0]["Acronym"]
                tower_type = info.iloc[0]['Tower type']
            else:
                is_dead = True

            if tower_type == 'Tower' and answer[0:2] == 'to':
                answer = answer[2:]
            elif tower_type == 'Citadel' and answer[0:2] == 'co':
                answer = answer[2:]
            elif tower_type == 'Steeple' and answer[0:2] == 'so':
                answer = answer[2:]
            elif tower_type == 'MiniTower' and answer[-2:] == 'at':
                answer = answer[:-2]

            #print(answer)
            is_contain = False

            for letter in answer:
                if letter in danger_letter:
                    is_contain = True

            if is_contain or acronym in guess_list:
                is_dead = True
            else:
                guess_list[acronym] = 1

            if is_dead:
                round -= 1
                await ctx.send("<@" + str(user_id) +
                               "> You died! Your streak is **" + str(round) +
                               "**. Please try again next time")
                time.sleep(2)
                break

        except Exception as e:
            round -= 1
            await ctx.send("<@" + str(user_id) +
                           "> You ran out of time! Your streak is **" +
                           str(round) + "**. Please try again next time")
            time.sleep(2)
            break

    embed = discord.Embed(title="The result of 'Not that letter' game",
                          description="",
                          color=discord.Color.blue())

    username = bot.get_user(int(user_id))

    embed.add_field(name="Player", value=username, inline=False)

    embed.add_field(name="Difficulty mode", value=diff_mode, inline=False)
    embed.add_field(name="Your streak", value=str(round), inline=False)

    pfp = ctx.author.avatar.url

    embed.set_thumbnail(url=pfp)

    await ctx.send(embed=embed)


@bot.command(guild_ids=[server_id], description="Play the 'Simon says' game")
#@commands.has_permissions(administrator=True)
async def simonsays(ctx):

    if (not await precheck(ctx)):
        await noPermission(ctx)
        return

    user_id = ctx.author.id

    timeout_period = 10

    embed = discord.Embed(title="Welcome to 'Simon says' game",
                          description="",
                          color=discord.Color.green())

    embed.add_field(
        name="How to play?",
        value=
        "**1.** If I start the sentence with *Simon says*, you need to follow my instruction\n**2.** Conversely, if I don't start the sentence with *Simon says*, answer something else which is different from the instruction\n**3.** If you do not react to my instruction before time runs out, or you fail on my instruction, your game ends",
        inline=False)

    await ctx.respond(embed=embed)

    view = DifficultyModeButtons(timeout=timeout_period)

    await ctx.send("Choose the difficulty please", view=view)

    def check(m):
        return True

    try:
        interaction = await bot.wait_for("interaction",
                                         check=check,
                                         timeout=timeout_period)

    except Exception as e:
        print(e)
        await ctx.send(
            "<@" + str(user_id) +
            "> You ran out of time! You can no longer select the difficulty")
        return

    difficulty = view.difficulty_mode

    round = 0
    answer_waiting_period = 10
    diff_mode = '**[' + emoji.getEmoji('easy') + ']** Easy'

    if difficulty == 'h':
        answer_waiting_period = 5
        diff_mode = '**[' + emoji.getEmoji('difficult') + ']** Hard'

    is_simon = True
    is_dead = False

    while round < 100:

        if (round % 3 == 0) and (round != 0) and (answer_waiting_period > 5):
            answer_waiting_period -= 1

        round += 1

        def checkAnswer(m):
            return m.author == ctx.author

        def filtering_answer(input):

            if not re.match("^[-a-zA-Z0-9_':?, ]*$", input):
                input = ""
            return input[0:50]

        try:

            simon_word = ""
            simon_predict = random.randint(0, 100)

            if simon_predict < 30:
                is_simon = False
                simon_word = ""
            else:
                is_simon = True
                simon_word = "Simon says, "

            random_list = [0]
            random_key = random.choice(random_list)

            time_limit = "You have " + str(answer_waiting_period) + " seconds"

            if random_key == 0:

                tower_list = df_info[(df_info['Sub difficulty'].notnull()) &
                                     (df_info['Difficulty'] != 'gingerbread')]
                tower = tower_list.sample()

                dif = tower.iloc[0]['Difficulty']

                await ctx.send("<@" + str(user_id) + "> **Round " +
                               str(round) + "**: " + simon_word +
                               "Tell me an acronym of the **" + dif +
                               "** building. " + time_limit)

                guess = await bot.wait_for('message',
                                           check=checkAnswer,
                                           timeout=answer_waiting_period)

                answer = filtering_answer(guess.content).lower()

                info = df_info[(df_info["Acronym"].str.lower() == answer)]

                if len(info) == 0:
                    is_simon = True
                    is_dead = True
                else:
                    dif_answer = info.iloc[0]['Difficulty']

                    if not (dif_answer == dif):
                        is_dead = True

            elif random_key == 1:

                area_list = df_area[(df_area['Location type'] != 'event')
                                    & (df_area['Accessible'] == 'y')]

                area = area_list.sample()
                area_name = area.iloc[0]['Area name']
                area_code = area.iloc[0]['Acronym']

                await ctx.send("<@" + str(user_id) + "> **Round " +
                               str(round) + "**: " + simon_word +
                               "Tell me an acronym of the building in **" +
                               area_name + "**. " + time_limit)

                guess = await bot.wait_for('message',
                                           check=checkAnswer,
                                           timeout=answer_waiting_period)

                answer = filtering_answer(guess.content).lower()

                info = df_info[(df_info["Acronym"].str.lower() == answer)]

                if len(info) == 0:
                    is_simon = True
                    is_dead = True
                else:
                    area_answer = info.iloc[0]['Area code']

                    if not (area_answer == area_code):
                        is_dead = True

            elif random_key == 2:

                tower_list = df_info[(df_info['Tower type'] != 'TowerRush'
                                      )]['Tower type'].unique().tolist()
                #tower=tower_list.sample()
                tower_type = random.choice(tower_list)

                #tower_type=tower.iloc[0]['Tower type']

                await ctx.send("<@" + str(user_id) + "> **Round " +
                               str(round) + "**: " + simon_word +
                               "Tell me an acronym of any **" + tower_type +
                               "**. " + time_limit)

                guess = await bot.wait_for('message',
                                           check=checkAnswer,
                                           timeout=answer_waiting_period)

                answer = filtering_answer(guess.content).lower()

                info = df_info[(df_info["Acronym"].str.lower() == answer)]

                if len(info) == 0:
                    is_simon = True
                    is_dead = True
                else:
                    type_answer = info.iloc[0]['Tower type']

                    if not (type_answer == tower_type):
                        is_dead = True

            elif random_key == 3:

                length_list = [3, 4, 5, 6]
                length = random.choice(length_list)

                await ctx.send("<@" + str(user_id) + "> **Round " +
                               str(round) + "**: " + simon_word +
                               "Tell me an acronym with **" + str(length) +
                               "** letters. " + time_limit)

                guess = await bot.wait_for('message',
                                           check=checkAnswer,
                                           timeout=answer_waiting_period)

                answer = filtering_answer(guess.content).lower()

                info = df_info[(df_info["Acronym"].str.lower() == answer)]

                if len(info) <= 0:
                    is_simon = True
                    is_dead = True

                if len(answer) != length:
                    is_dead = True

            if not is_simon:
                is_dead = not is_dead

            if is_dead:
                round -= 1
                await ctx.send("<@" + str(user_id) +
                               "> You died! Your streak is **" + str(round) +
                               "**. Please try again next time")
                time.sleep(2)
                break

        except Exception as e:
            print(e)
            round -= 1
            await ctx.send("<@" + str(user_id) +
                           "> You ran out of time! Your streak is **" +
                           str(round) + "**. Please try again next time")
            time.sleep(2)
            break

    embed = discord.Embed(title="The result of 'Simon says' game",
                          description="",
                          color=discord.Color.blue())

    username = bot.get_user(int(user_id))

    embed.add_field(name="Player", value=username, inline=False)

    embed.add_field(name="Difficulty mode", value=diff_mode, inline=False)
    embed.add_field(name="Your streak", value=str(round), inline=False)

    pfp = ctx.author.avatar.url

    embed.set_thumbnail(url=pfp)

    await ctx.send(embed=embed)


@bot.command(guild_ids=[server_id],
             description="Get the quote from the badge of the tower")
async def quote(ctx, tower):

    if (not await precheck(ctx)):
        await noPermission(ctx)
        return

    user_id = ctx.author.id
    tower = await filtering_input(ctx, tower)

    info = df_badge[(df_badge['Category'] == 'Beating Tower')
                    & (df_badge['Value 1'].str.lower() == tower.lower())]

    if info.shape[0] > 0:

        quote = info.iloc[0]['Description']
        full_name = df_info[df_info["Acronym"].str.lower() ==
                            tower.lower()].iloc[0]['Tower']
        await ctx.respond("<@" + str(user_id) + "> ''*" + quote +
                          "''* said by **" + full_name + "**")

    else:
        await ctx.respond(await noTowerFound(tower))


@bot.command(guild_ids=[server_id],
             description="Get the badge image from its tower")
#@commands.has_permissions(administrator=True)
async def badge(ctx, tower):

    if (not await precheck(ctx)):
        await noPermission(ctx)
        return

    user_id = ctx.author.id
    tower = await filtering_input(ctx, tower)

    info = df_badge[(df_badge['Category'] == 'Beating Tower')
                    & (df_badge['Value 1'].str.lower() == tower.lower())]

    if info.shape[0] > 0:

        badge_id = info.iloc[0]['Badge ID']
        description = info.iloc[0]['Description']
        full_name = df_info[df_info["Acronym"].str.lower() ==
                            tower.lower()].iloc[0]['Tower']

        badge_img_url = "https://thumbnails.roblox.com/v1/badges/icons?badgeIds=" + str(
            badge_id) + "&size=150x150&format=Png&isCircular=true"
        badge_response = urlopen(badge_img_url, timeout=5)
        badge_json = json.loads(badge_response.read())
        #await ctx.respond("<@" + str(user_id) + "> This is the badage of **" +tower + "**",file=discord.File(fp=tempfilename,filename="badge_"+tower+".png"))

        #print(badge_json)
        if ("data" in badge_json):

            real_url = badge_json['data'][0]['imageUrl']

            embed = discord.Embed(title="Badge")
            embed.add_field(name="Tower", value=full_name, inline=False)
            embed.add_field(name="Description",
                            value=description,
                            inline=False)
            embed.set_image(url=real_url)
            await ctx.respond(embed=embed)
        #os.remove(tempfilename)

    else:
        await ctx.respond(await noTowerFound(tower))


class BuildingTypeDropdown(discord.ui.View):

    building_type = 'tower'

    async def on_timeout(self):
        for child in self.children:
            child.disabled = True
        await self.message.edit(
            content="You can no longer select the building type", view=self)

    @discord.ui.select(placeholder="Building type",
                       min_values=1,
                       max_values=1,
                       options=[
                           discord.SelectOption(label="Tower"),
                           discord.SelectOption(label="Citadel"),
                           discord.SelectOption(label="Steeple")
                       ])
    async def select_callback(
        self, select, interaction
    ):  # the function called when the user is done selecting options
        self.building_type = (select.values[0]).lower()
        await interaction.response.defer()


@bot.command(guild_ids=[server_id], description="Draw GAT style tower")
async def drawgat(ctx):

    if (not await precheck(ctx)):
        await noPermission(ctx)
        return

    user_id = ctx.author.id

    timeout_period = 10

    view = BuildingTypeDropdown(timeout=timeout_period)

    await ctx.respond("Choose the building type please", view=view)

    def check(m):
        return True
        #user_id = m.author.id
        #return str(user_id) == str(bot_id) and m.channel.id == ctx.channel.id

    try:
        interaction = await bot.wait_for("interaction",
                                         check=check,
                                         timeout=timeout_period)

        type = view.building_type

        if (type == 'tower' or type == 'citadel' or type == 'steeple'):

            #await ctx.defer()
            """
            global is_drawing
            if is_drawing == 1:
                await ctx.send("<@" + str(user_id) +
                               "> Sorry I'm busy drawing tower")
                return

            is_drawing = 1
            """
            await ctx.send("Let me draw a GAT " + type)

            hex_code = ['0', 'F']

            max_floor = 10
            if (type == 'citadel'):
                max_floor = random.randint(12, 25)
            elif (type == 'steeple'):
                max_floor = random.randint(5, 6)

            floor_list = []

            for k in range(max_floor):

                hex_string = ""

                for k2 in range(6):
                    hex_string += random.choice(hex_code)

                #color_url="https://singlecolorimage.com/get/"+hex_string+"/25x25"
                floor_list.append(hex_string)
                #await ctx.send(color_url)
                #time.sleep(0.75)
            tower_img_template = generatetowerfromcolors(reversed(floor_list))
            tempfilename = root_tmp_path + "tempgat.png"
            tower_img_template = tower_img_template.save(tempfilename)

            is_drawing = 0
            await ctx.send(
                file=discord.File(fp=tempfilename, filename="towercolors.png"))
            await ctx.send("<@" + str(user_id) + "> This is my GAT " + type +
                           " :smile:")
            os.remove(tempfilename)
        else:
            await ctx.send(
                "<@" + str(user_id) +
                "> I don't understand what you mean. You can input only the word **Tower/Citadel/Steeple** :)"
            )
    except Exception as e:
        print(e)
        await ctx.send(
            "<@" + str(user_id) +
            "> You ran out of time! You can no longer select the buliding type"
        )


@drawgat.error
async def drawgat_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.respond(
            "You need to also tell me the type of building like tower/citadel/steeple (For example **"
            + prefix + "drawgat steeple**)")


#portal_font_url="https://github.com/googlefonts/roboto/blob/main/src/hinted/Roboto-Black.ttf?raw=true"

portal_font_url = "font/ComicNeue-Angular-Bold.ttf"

#r = requests.get(portal_font_url, allow_redirects=True)

#portal_font_large = ImageFont.truetype(io.BytesIO(r.content), size=30)

portal_font_large = ImageFont.truetype(portal_font_url, size=30)
portal_font_normal = ImageFont.truetype(portal_font_url, size=24)
portal_font_small = ImageFont.truetype(portal_font_url, size=18)
portal_font_very_small = ImageFont.truetype(portal_font_url, size=15)


async def getportalimage(tower,
                         enable_label=True,
                         custom_name=None,
                         custom_color=(256, 256, 256),
                         custom_building_type=None,
                         custom_difficulty=None):

    if not tower and ((custom_name == None) or (custom_color == None) or
                      (custom_building_type == None) or
                      (custom_difficulty == None)):
        return ("Error", None)

    difficulty_color = {}
    difficulty_color['effortless'] = "#00CE01"
    difficulty_color['easy'] = "#76F447"
    difficulty_color['medium'] = "#FFFE02"
    difficulty_color['hard'] = "#FE7C00"
    difficulty_color['difficult'] = "#FF0C04"
    difficulty_color['challenging'] = "#C10000"
    difficulty_color['intense'] = "#192832"
    difficulty_color['remorseless'] = "#C901C9"
    difficulty_color['insane'] = "#0000FF"
    difficulty_color['extreme'] = "#0389FF"
    difficulty_color['terrifying'] = "#01FFFF"
    difficulty_color['catastrophic'] = "#FFFFFF"
    difficulty_color['horrific'] = "#9691FF"
    difficulty_color['unreal'] = "#4B00C8"
    difficulty_color['nil'] = "#797981"

    info = None
    if tower:
        info = df_info[df_info['Acronym'].str.lower() == tower.lower()]

    if (tower and info.shape[0] > 0) or tower is None:

        tower_full_name = custom_name
        difficulty = custom_difficulty
        tower_type = custom_building_type

        if custom_color is None:
            custom_color = (256, 256, 256)

        portal_color = custom_color

        if tower:
            tower_full_name = info.iloc[0]['Tower']
            difficulty = info.iloc[0]['Difficulty']
            tower_type = (info.iloc[0]['Tower type']).lower()
            floors = await getTowerColors(tower)

            try:
                portal_color = ImageColor.getcolor("#" + str(floors[0]), "RGB")
            except Exception as e:
                portal_color = ImageColor.getcolor("#FFFFFF", "RGB")

        portal_scaled_color = 0.95
        portal_darker_color = (math.floor(portal_scaled_color *
                                          portal_color[0]),
                               math.floor(portal_scaled_color *
                                          portal_color[1]),
                               math.floor(portal_scaled_color *
                                          portal_color[2]))
        emblem_scaled_color = 0.6
        emblem_color = (math.floor(emblem_scaled_color * portal_color[0]),
                        math.floor(emblem_scaled_color * portal_color[1]),
                        math.floor(emblem_scaled_color * portal_color[2]))
        difficulty_color = ImageColor.getcolor(difficulty_color[difficulty],
                                               "RGB")

        #Size of image
        img_width = 10
        img_height = 11
        #Size of Portal
        portal_width = 10
        portal_height = 8
        #Top-left position of Portal
        portal_x0 = 0
        portal_y0 = 3
        #Size of difficulty
        difficulty_width = 6
        difficulty_height = 6.25
        #Top-left position of difficulty
        difficulty_x0 = 2
        difficulty_y0 = 3.75
        #Size of sign
        sign_width = 10
        sign_height = 3.5
        #Top-left position of sign
        sign_x0 = 0
        sign_y0 = 0
        #Emblem offset
        emblem_offset = 0.05
        #Size of embled
        emblem_width = 2
        emblem_height = 2
        #Top-left position of emblem
        emblem_x0 = 0
        emblem_x1 = 8
        emblem_y0 = 4.75
        #Label
        label_height = 3.25
        label_color = (255, 255, 255)
        #Type of tower
        building_type = 'tower'

        if tower is None:
            building_type = custom_building_type

        #Font size
        font = portal_font_large
        if len(tower_full_name) >= 14:
            font = portal_font_normal
        if len(tower_full_name) >= 30:
            font = portal_font_small
        if len(tower_full_name) >= 42:
            font = portal_font_very_small
        max_width_label = 20

        #if tower_type!='Tower' and tower_type!='MiniTower':
        #  await ctx.respond("<@"+str(user_id)+"> Sorry! I don't know how to draw the portal in "+tower_type+" style :sob:")
        #  return

        if tower_type == 'citadel':
            #Size of image
            img_width = 28
            img_height = 22
            #Size of Portal
            portal_width = 28
            portal_height = 19
            #Top-left position of Portal
            portal_x0 = 0
            portal_y0 = 3
            #Size of difficulty
            difficulty_width = 18
            difficulty_height = 16
            #Top-left position of difficulty
            difficulty_x0 = 5
            difficulty_y0 = 3
            #Size of sign
            sign_width = 11
            sign_height = 3.5
            #Top-left position of sign
            sign_x0 = 8.5
            sign_y0 = 0
            #Emblem offset
            emblem_offset = 0.05
            #Size of embled
            emblem_width = 3
            emblem_height = 3
            #Top-left position of emblem
            emblem_x0 = 1
            emblem_x1 = 24
            emblem_y0 = 12.75
            #Label
            label_height = 1.6
            label_color = (54, 186, 184)
            #Type of tower
            building_type = 'citadel'
            #Font size
            font = portal_font_large
            if len(tower_full_name) >= 14:
                font = portal_font_normal
            if len(tower_full_name) >= 30:
                font = portal_font_small
            if len(tower_full_name) >= 42:
                font = portal_font_very_small
            max_width_label = 20

        elif tower_type == 'steeple':
            #Size of image
            img_width = 6
            img_height = 9
            #Size of Portal
            portal_width = 5
            portal_height = 6
            #Top-left position of Portal
            portal_x0 = 0.5
            portal_y0 = 3
            #Size of difficulty
            difficulty_width = 3
            difficulty_height = 4.5
            #Top-left position of difficulty
            difficulty_x0 = 1.5
            difficulty_y0 = 3.75
            #Size of sign
            sign_width = 6
            sign_height = 3.25
            #Top-left position of sign
            sign_x0 = 0
            sign_y0 = 0
            #Emblem offset
            emblem_offset = 0.05
            #Size of embled
            emblem_width = 1
            emblem_height = 1
            #Top-left position of emblem
            emblem_x0 = 0.25
            emblem_x1 = 4.75
            emblem_y0 = 5
            #Label
            label_height = 3.75
            label_color = (255, 255, 255)
            #Type of tower
            building_type = 'steeple'
            #Font size
            font = portal_font_normal
            if len(tower_full_name) >= 14:
                font = portal_font_small
            if len(tower_full_name) >= 26:
                font = portal_font_very_small
            max_width_label = 16

        try:
            scale = 25
            canvas_width, canvas_height = scale * img_width, scale * img_height

            img = Image.new('RGBA', (canvas_width, canvas_height),
                            (125, 125, 125, 0))
            draw = ImageDraw.Draw(img)

            # Draw the difficulty
            #draw.polygon([(scale*2.75,scale*10), (scale*2.75,scale*5), (scale*4,scale*4.25),(scale*6,scale*4.25), (scale*7.25,scale*5),(scale*7.25,scale*10)], fill = difficulty_color)
            difficulty_template_filename = "image/portal_template/portal_difficulty_template.png"
            difficulty_img = Image.open(difficulty_template_filename, 'r')
            small_difficulty_img = difficulty_img.resize(
                (int(scale * difficulty_width), int(
                    scale * difficulty_height)), Image.Resampling.BILINEAR)

            temp_difficulty_filename = "difficulty_portal_template.png"

            _, _, _, difficulty_alpha = small_difficulty_img.split()

            small_difficulty_img = small_difficulty_img.convert('L')

            small_difficulty_img = ImageOps.colorize(small_difficulty_img,
                                                     black=(0, 0, 0),
                                                     white=difficulty_color)

            small_difficulty_img.putalpha(difficulty_alpha)

            difficulty_mask = Image.new('RGBA', (canvas_width, canvas_height),
                                        (125, 125, 125, 0))
            difficulty_mask.paste(
                small_difficulty_img,
                (int(scale * difficulty_x0), int(scale * difficulty_y0)))
            img = Image.alpha_composite(img, difficulty_mask)

            #Draw the portal
            portal_template_filename = "image/portal_template/" + building_type + "_portal_template.png"
            portal_img = Image.open(portal_template_filename, 'r')

            small_portal_img = portal_img.resize(
                (int(scale * portal_width), int(scale * portal_height)),
                Image.Resampling.BILINEAR)

            tempportalfilename = building_type + "_portal_template.png"

            _, _, _, portal_alpha = small_portal_img.split()

            small_portal_img = small_portal_img.convert('L')

            small_portal_img = ImageOps.colorize(small_portal_img,
                                                 black=(0, 0, 0),
                                                 white=portal_color)

            small_portal_img.putalpha(portal_alpha)

            portal_mask = Image.new('RGBA', (canvas_width, canvas_height),
                                    (125, 125, 125, 0))
            portal_mask.paste(small_portal_img,
                              (int(scale * portal_x0), int(scale * portal_y0)))

            img = Image.alpha_composite(img, portal_mask)
            #img.paste(small_portal_img,(scale*0,scale*3))

            # Draw sign
            """
        draw.rectangle(
         (scale*0, scale*0, scale*10, scale*3),
         fill=(35, 35, 35),
          outline=None)
      """
            sign_template_filename = "image/portal_template/" + building_type + "_sign_template.png"
            sign_img = Image.open(sign_template_filename, 'r')
            small_sign_img = sign_img.resize(
                (int(scale * sign_width), int(scale * sign_height)),
                Image.Resampling.BILINEAR)
            img.paste(small_sign_img,
                      (int(scale * sign_x0), int(scale * sign_y0)),
                      mask=small_sign_img)

            # Draw the name of the tower
            # Load font from URI
            #truetype_url = 'https://github.com/googlefonts/roboto/blob/main/src/hinted/Roboto-Black.ttf?raw=true'
            #truetype_url = 'https://github.com/googlefonts/roboto/blob/main/src/hinted/Itim.ttf?raw=true'

            #r = requests.get(truetype_url, allow_redirects=True)

            # reference -> https://www.alpharithms.com/fit-custom-font-wrapped-text-image-python-pillow-552321/
            if enable_label:
                avg_char_width = sum(
                    math.floor(font.getlength(char))
                    for char in ascii_letters) / len(ascii_letters)
                max_char_count = int((canvas_width * 1.25) / avg_char_width)
                tower_label = textwrap.fill(text=tower_full_name,
                                            width=max_width_label)
                w_text, h_text = draw.textsize(tower_label, font=font)
                draw = ImageDraw.Draw(img)
                draw.text(((canvas_width - w_text) / 2,
                           ((canvas_height * label_height / 11) - h_text) / 2),
                          tower_label,
                          font=font,
                          align="center",
                          fill=label_color)

            #Draw emblem
            if tower:
                tower_location = df_info[df_info['Acronym'].str.lower() ==
                                         tower.lower()]['Location'].values[0]
                tower_location_number = int(
                    df_info[df_info['Acronym'].str.lower() ==
                            tower.lower()]['Location number'].values[0])
                tower_location_subnumber = int(
                    df_info[df_info['Acronym'].str.lower() ==
                            tower.lower()]['Location subnumber'].values[0])
                tower_location_type = df_info[df_info['Acronym'].str.lower(
                ) == tower.lower()]['Location type'].values[0]

                emblem_url = df_area[
                    (df_area['Location'] == tower_location)
                    & (df_area['Location number'] == tower_location_number) &
                    (df_area['Location subnumber'] == tower_location_subnumber)
                    & (df_area['Location type']
                       == tower_location_type)]['Emblem URL']

                if emblem_url is not None and str(emblem_url) != 'nan' and len(
                        emblem_url) > 0:
                    emblem_url = emblem_url.values[0]
                    emblemimg = Image.open(
                        requests.get(emblem_url, stream=True).raw)

                    #small_emblemimg=emblemimg.resize(math.floor((scale-2*emblem_offset)*2),math.floor((scale-2*emblem_offset)*2),Image.Resampling.NEAREST)
                    small_emblemimg = emblemimg.resize(
                        (int(scale * (emblem_width - 2 * emblem_offset)),
                         int(scale * (emblem_height - 2 * emblem_offset))),
                        Image.Resampling.BILINEAR)

                    _, _, _, emblem_alpha = small_emblemimg.convert(
                        "RGBA").split()
                    small_emblemimg = ImageOps.grayscale(small_emblemimg)

                    small_emblemimg = ImageOps.colorize(small_emblemimg,
                                                        black=portal_color,
                                                        white=emblem_color)
                    #print(emblem_alpha)
                    small_emblemimg.putalpha(emblem_alpha)
                    #img = Image.blend(img, small_emblemimg, alpha=0.5)

                    emblem_offset_2 = 0.5

                    emblem_mask = Image.new('RGBA',
                                            (canvas_width, canvas_height),
                                            (125, 125, 125, 0))
                    emblem_mask.paste(
                        small_emblemimg,
                        (int(scale *
                             (emblem_x0 + emblem_offset + emblem_offset_2)),
                         int(scale * (emblem_y0 + emblem_offset))))
                    emblem_mask.paste(
                        small_emblemimg,
                        (int(scale *
                             (emblem_x1 + emblem_offset - emblem_offset_2)),
                         int(scale * (emblem_y0 + emblem_offset))))

                    img = Image.alpha_composite(img, emblem_mask)

                    #img.paste(small_emblemimg, (math.floor(scale*(0+emblem_offset+emblem_offset_2)), math.floor(scale*(5+emblem_offset))))
                    #img.paste(small_emblemimg, (math.floor(scale*(8+emblem_offset-emblem_offset_2)), math.floor(scale*(5+emblem_offset))))

            if tower:
                tempfilename = root_tmp_path + "tempportal" + tower + ".png"
            else:
                tempfilename = root_tmp_path + "tempportalcustom_" + (
                    custom_name).replace(" ", "_") + ".png"

            img = img.save(tempfilename, quality=100)

            return "OK", tempfilename

        except Exception as e:
            print(e)
            return "Drawing error", None
        #else:
        #  await ctx.respond("<@"+str(user_id)+"> Sorry! I don't know how to draw the portal in "+tower_type+" style :sob:")
    else:
        return "No tower", None


@bot.command(guild_ids=[server_id], description="Draw the portal of the tower")
#@commands.has_permissions(administrator=True)
async def drawportal(ctx, tower):

    if (not await precheck(ctx)):
        await noPermission(ctx)
        return

    #tower=await correctTowerCaseSensitive(tower)
    tower = await filtering_input(ctx, tower)
    user_id = ctx.author.id

    await ctx.defer()
    #await ctx.followup.send("Please wait for me while I'm drawing the portal")
    status, img_url = await getportalimage(tower)
    if status == 'OK':

        tower_full_name = df_info[df_info['Acronym'].str.lower() ==
                                  tower.lower()].iloc[0]['Tower']

        await ctx.respond("<@" + str(user_id) + "> This is the portal of **" +
                          tower_full_name + "**",
                          file=discord.File(img_url,
                                            filename="towerportal.png"))
        os.remove(img_url)

    elif status == 'Drawing error':

        tower_full_name = df_info[df_info['Acronym'].str.lower() ==
                                  tower.lower()].iloc[0]['Tower']

        await ctx.respond(
            "<@" + str(user_id) +
            "> Sorry! It's too difficult to draw the portal of **" +
            tower_full_name + "** :sob:")
    elif status == 'No tower':
        await ctx.respond(await noTowerFound(tower))
    else:
        await ctx.respond("<@" + str(user_id) +
                          "> Oh no! I lost my drawing skill")


@bot.command(guild_ids=[server_id],
             description="Draw the custom portal of the tower")
#@commands.has_permissions(administrator=True)
async def drawcustomportal(ctx,
                           full_name,
                           color_r=256,
                           color_g=256,
                           color_b=256,
                           type='tower',
                           difficulty='hard'):

    if (not await precheck(ctx)):
        await noPermission(ctx)
        return

    #tower=await correctTowerCaseSensitive(tower)
    full_name = await filtering_input_with_space(ctx, full_name)
    #color_hex=await filtering_input(ctx,color_hex)

    if str(color_r).isdigit():
        color_r = int(color_r)
        if color_r > 256:
            color_r = 256
        elif color_r < 0:
            color_r = 0
    else:
        color_r = 256

    if str(color_g).isdigit():
        color_g = int(color_g)
        if color_g > 256:
            color_g = 256
        elif color_g < 0:
            color_g = 0
    else:
        color_g = 256

    if str(color_b).isdigit():
        color_b = int(color_b)
        if color_b > 256:
            color_b = 256
        elif color_b < 0:
            color_b = 0
    else:
        color_b = 256

    type = await filtering_input(ctx, type.lower())
    difficulty = await filtering_input(ctx, difficulty.lower())

    user_id = ctx.author.id

    await ctx.defer()
    #await ctx.followup.send("Please wait for me while I'm drawing the custom portal")
    status, img_url = await getportalimage(None,
                                           enable_label=True,
                                           custom_name=full_name,
                                           custom_color=(color_r, color_g,
                                                         color_b),
                                           custom_building_type=type,
                                           custom_difficulty=difficulty)
    if status == 'OK':

        await ctx.respond("<@" + str(user_id) + "> This is your custom portal",
                          file=discord.File(img_url,
                                            filename="towercustomportal.png"))
        os.remove(img_url)

    elif status == 'Drawing error':

        await ctx.respond(
            "<@" + str(user_id) +
            "> Sorry! It's too difficult to draw the custom portal :sob:")
    elif status == 'No tower':
        await ctx.respond(await noTowerFound(tower))
    else:
        await ctx.respond("<@" + str(user_id) +
                          "> Oh no! I lost my drawing skill")


@bot.command(guild_ids=[server_id],
             description="Give an idea for the name of tower")
#@commands.has_permissions(administrator=True)
async def towernameidea(ctx, acronym=""):

    if (not await precheck(ctx)):
        await noPermission(ctx)
        return

    #print(acronym)

    user_id = ctx.author.id
    r = RandomWord()
    random_list = [0, 1]
    random_key = random.choice(random_list)

    word = ""

    if len(acronym) <= 0:

        if random_key == 0:
            adj = r.random_words(include_parts_of_speech=["adjective"])
            noun = r.random_words(include_parts_of_speech=["noun"])
            word = "Tower of " + adj[0].capitalize(
            ) + " " + noun[0].capitalize()
        elif random_key == 1:
            adj1 = r.random_words(include_parts_of_speech=["adjective"])
            adj2 = r.random_words(include_parts_of_speech=["adjective"])
            noun = r.random_words(include_parts_of_speech=["noun"])
            word = "Tower of " + adj1[0].capitalize(
            ) + " " + adj2[0].capitalize() + " " + noun[0].capitalize()

        acronym = word.split(" ")
        letters = []
        for w in acronym:
            letters.append(w[0])
        acronym = "".join(letters)
    elif len(acronym) > 6:
        await ctx.respond(
            "<@" + str(user_id) +
            "> Oh no! Your acronym is too long. It should not be greater than 6 letters"
        )
        return
    else:
        if not (acronym[0:2] == "To" or acronym[0:2] == "Co"
                or acronym[0:2] == "So"):
            await ctx.respond("<@" + str(user_id) +
                              "> You input the wrong format of the acronym")
            return
        else:
            if (acronym[0:2] == "To"):
                word = "Tower of "
            elif (acronym[0:2] == "Co"):
                word = "Citadel of "
            elif (acronym[0:2] == "So"):
                word = "Steeple of "

            for pivot in range(2, len(acronym), 1):
                letter = acronym[pivot].lower()
                if pivot == len(acronym) - 1:
                    word += (r.random_words(
                        include_parts_of_speech=["noun"],
                        starts_with=letter)[0].capitalize())
                else:
                    word += (r.random_words(
                        include_parts_of_speech=["adjective"],
                        starts_with=letter)[0].capitalize())
                word += " "
        word = word.strip()

    embed = discord.Embed(title="Tower's name idea",
                          description=word + " (" + acronym + ")",
                          color=discord.Color.blue())

    await ctx.respond(embed=embed)


class ScoreDropdown(discord.ui.View):

    score = 0

    async def on_timeout(self):
        for child in self.children:
            child.disabled = True
        await self.message.edit(content="You can no longer select the score",
                                view=self)

    @discord.ui.select(
        placeholder="Score",
        min_values=1,
        max_values=1,
        options=[
            #discord.SelectOption(label="All"),
            discord.SelectOption(label="0", emoji=emoji.getEmoji("0_g")),
            discord.SelectOption(label="1", emoji=emoji.getEmoji("1_g")),
            discord.SelectOption(label="2", emoji=emoji.getEmoji("2_g")),
            discord.SelectOption(label="3", emoji=emoji.getEmoji("3_g")),
            discord.SelectOption(label="4", emoji=emoji.getEmoji("4_g")),
            discord.SelectOption(label="5", emoji=emoji.getEmoji("5_g")),
            discord.SelectOption(label="6", emoji=emoji.getEmoji("6_g")),
            discord.SelectOption(label="7", emoji=emoji.getEmoji("7_g")),
            discord.SelectOption(label="8", emoji=emoji.getEmoji("8_g")),
            discord.SelectOption(label="9", emoji=emoji.getEmoji("9_g")),
            discord.SelectOption(label="10", emoji=emoji.getEmoji("10_g"))
        ])
    async def select_callback(
        self, select, interaction
    ):  # the function called when the user is done selecting options
        self.score = int(select.values[0])
        await interaction.response.defer()
        #await interaction.response.send_message("You selected **" +select.values[0] + "**")


class SubDifficultyDropdown(discord.ui.View):

    subdifficulty = "bottom"
    subdifficulty_list = [
        discord.SelectOption(label="All"),
        discord.SelectOption(label="Bottom"),
        discord.SelectOption(label="Bottom-low"),
        discord.SelectOption(label="Low"),
        discord.SelectOption(label="Low-mid"),
        discord.SelectOption(label="Mid"),
        discord.SelectOption(label="Mid-high"),
        discord.SelectOption(label="High"),
        discord.SelectOption(label="High-peak"),
        discord.SelectOption(label="Peak"),
    ]

    def __init__(self, timeout=None, has_all=True):

        if not has_all:
            self.subdifficulty_list.pop(0)

        super().__init__(timeout=timeout)

    async def on_timeout(self):
        for child in self.children:
            child.disabled = True
        await self.message.edit(
            content="You can no longer select the subdifficulty", view=self)

    @discord.ui.select(placeholder="Subdifficulty",
                       min_values=1,
                       max_values=1,
                       options=subdifficulty_list)
    async def select_callback(
        self, select, interaction
    ):  # the function called when the user is done selecting options
        self.subdifficulty = (select.values[0]).lower()
        await interaction.response.defer()
        #await interaction.response.send_message("You selected **" +select.values[0] + "**")


class DifficultyDropdown(discord.ui.View):

    difficulty = "challenging"
    difficulty_list = [
        discord.SelectOption(label="All", value='All'),
        discord.SelectOption(label="Easy",
                             value="Easy",
                             emoji=emoji.getEmoji("Easy")),
        discord.SelectOption(label="Medium",
                             value="Medium",
                             emoji=emoji.getEmoji("Medium")),
        discord.SelectOption(label="Hard",
                             value="Hard",
                             emoji=emoji.getEmoji("Hard")),
        discord.SelectOption(label="Difficult",
                             value="Difficult",
                             emoji=emoji.getEmoji("Difficult")),
        discord.SelectOption(label="Challenging",
                             value="Challenging",
                             emoji=emoji.getEmoji("Challenging")),
        discord.SelectOption(label="Intense",
                             value="Intense",
                             emoji=emoji.getEmoji("Intense")),
        discord.SelectOption(label="Remorseless",
                             value="Remorseless",
                             emoji=emoji.getEmoji("Remorseless")),
        discord.SelectOption(label="Insane",
                             value="Insane",
                             emoji=emoji.getEmoji("Insane")),
        discord.SelectOption(label="Extreme",
                             value="Extreme",
                             emoji=emoji.getEmoji("Extreme")),
        discord.SelectOption(label="Terrifying",
                             value="Terrifying",
                             emoji=emoji.getEmoji("Terrifying")),
        discord.SelectOption(label="Catastrophic",
                             value="Catastrophic",
                             emoji=emoji.getEmoji("Catastrophic")),
        discord.SelectOption(label="Horrific",
                             value="Horrific",
                             emoji=emoji.getEmoji("Horrific")),
        discord.SelectOption(label="Unreal",
                             value="Unreal",
                             emoji=emoji.getEmoji("Unreal"))
    ]

    def __init__(self, timeout=None, has_all=True):

        if not has_all:
            self.difficulty_list.pop(0)

        super().__init__(timeout=timeout)

    async def on_timeout(self):
        for child in self.children:
            child.disabled = True
        await self.message.edit(
            content="You can no longer select the difficulty", view=self)

    @discord.ui.select(placeholder="Difficulty",
                       min_values=1,
                       max_values=1,
                       options=difficulty_list)
    async def select_callback(
        self, select, interaction
    ):  # the function called when the user is done selecting options
        self.difficulty = (select.values[0]).lower()
        await interaction.response.defer()
        #await interaction.response.send_message("You selected **" +select.values[0] + "**")


@bot.command(guild_ids=[server_id],
             description="Give random tower by difficulty")
#@commands.has_permissions(administrator=True)
async def roulette(ctx):

    if (not await precheck(ctx)):
        await noPermission(ctx)
        return

    user_id = ctx.author.id

    timeout_period = 10
    view = DifficultyDropdown(timeout=timeout_period)

    await ctx.respond("Choose the difficulty please", view=view)

    def check(m):
        return True
        #user_id = m.author.id
        #return str(user_id) == str(bot_id)

    try:
        interaction = await bot.wait_for("interaction",
                                         check=check,
                                         timeout=timeout_period)
        #print(interaction)
        #difficulty = interaction.content
        #difficulty = JToHDifficulties.correctDifficulty(interaction.content.replace("You selected ","").replace("**", ""))
        difficulty = JToHDifficulties.correctDifficulty(view.difficulty)
        #print("Difficulty is "+difficulty)
        #await interaction.delete()

        #tower_list = df_info[df_info['Difficulty']==difficulty & (df_info['Location type']=='main' | df_info['Location type']=='subrealm') ]
        try:
            if difficulty != 'all':
                tower_list = df_info[(df_info['Difficulty'] == difficulty) & (
                    df_info['Accessible'] == 'y')]["Tower"].values.tolist()
            else:
                tower_list = df_info[(
                    df_info['Accessible'] == 'y')]["Tower"].values.tolist()

            tower_name = random.choice(tower_list)

            panel_color = discord.Color.blue()
            panel_color = JToHDifficulties.getColorHex(difficulty)

            embed = discord.Embed(title="Roulette", color=panel_color)

            preemoji = ""

            if difficulty != 'all':
                preemoji = "**[" + emoji.getEmoji(difficulty) + "]** "

            embed.add_field(name="Difficulty",
                            value=preemoji + difficulty,
                            inline=False)

            embed.add_field(name="Tower", value=tower_name, inline=False)

            acronym = df_info[(
                df_info['Tower'] == tower_name)].iloc[0]['Acronym']
            status, img_url = await printTowerImage(acronym)
            embed.set_thumbnail(url=img_url)

            await ctx.send(embed=embed)

            #await ctx.send("<@" + str(user_id) + "> I picked **" + tower_name +"**")
        except Exception as e:
            print(e)
            await ctx.send("<@" + str(user_id) +
                           "> Please type difficulty correctly")
    except Exception as e:
        #print(e)
        await ctx.send(
            "<@" + str(user_id) +
            "> You ran out of time! You can no longer select the difficulty")


"""
@bot.command(guild_ids=[server_id], description="Give random tower by difficulty (Type the first 3 letters of difficulty e.g. med/rem)")
@commands.has_permissions(administrator=True)
async def rouletteoriginal(ctx, difficulty='all'):

    if (not await precheck(ctx)):
      await noPermission(ctx)
      return
  
    user_id = ctx.author.id
    difficulty=await filtering_message(difficulty)


    difficulty=JToHDifficulties.correctDifficulty(difficulty)
  
    #tower_list = df_info[df_info['Difficulty']==difficulty & (df_info['Location type']=='main' | df_info['Location type']=='subrealm') ]
    try:
      if difficulty!='all':
        tower_list = df_info[(df_info['Difficulty']==difficulty) & (df_info['Accessible']=='y')]["Tower"].values.tolist()
      else:
        tower_list = df_info[ (df_info['Accessible']=='y')]["Tower"].values.tolist()
      tower_name=random.choice(tower_list)
      await ctx.respond("<@"+str(user_id)+"> I picked **"+tower_name+"**")
    except:
      await ctx.respond("<@"+str(user_id)+"> Please type difficulty correctly")

@roulette.error
async def roulette_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.respond("You need to also tell me the difficulty (For example **"+prefix+"roulette intense**)")
"""


@bot.command(guild_ids=[server_id],
             description="Search for towers by difficulty")
#@commands.has_permissions(administrator=True)
async def towerbydifficulty(ctx):
    if (not await precheck(ctx)):
        await noPermission(ctx)
        return

    user_id = ctx.author.id

    timeout_period = 10
    view_diff = DifficultyDropdown(timeout=timeout_period)

    await ctx.respond("Choose the difficulty please", view=view_diff)

    def check(m):
        return True

    interaction = await bot.wait_for("interaction",
                                     check=check,
                                     timeout=timeout_period)
    difficulty = JToHDifficulties.correctDifficulty(view_diff.difficulty)

    view_subdiff = SubDifficultyDropdown(timeout=timeout_period, has_all=True)

    await ctx.send("Choose the subdifficulty please", view=view_subdiff)

    interaction2 = await bot.wait_for("interaction",
                                      check=check,
                                      timeout=timeout_period)
    subdifficulty = JToHDifficulties.correctSubdifficulty(
        view_subdiff.subdifficulty)

    tower_list = None

    if subdifficulty == 'all':
        tower_list = df_info[(df_info['Difficulty'] == difficulty)
                             & (df_info['Accessible'] == 'y')].sort_values(
                                 by='Num Difficulty', ascending=True)
    else:
        tower_list = df_info[(df_info['Difficulty'] == difficulty)
                             & (df_info['Sub difficulty'] == subdifficulty) &
                             (df_info['Accessible'] == 'y')].sort_values(
                                 by='Num Difficulty', ascending=True)

    if tower_list.shape[0] > 0:

        panel_color = JToHDifficulties.getColorHex(difficulty)
        tower_str = ""

        for index, tower in tower_list.iterrows():
            acronym = tower['Acronym']
            num_dif = tower['Num Difficulty']
            tower_str += ("**" + acronym + "** (" + str(num_dif) + ")\n")

        embed = discord.Embed(title="The list of " + subdifficulty + " " +
                              difficulty + " towers",
                              description=tower_str,
                              color=panel_color)

        await ctx.send(embed=embed)

    else:
        await ctx.send("Sorry! I can't find any " + subdifficulty + " " +
                       difficulty + " towers :sob:")


class CommentModal(discord.ui.Modal):

    comment = ""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(
            discord.ui.InputText(label="Comment",
                                 style=discord.InputTextStyle.long,
                                 max_length=300,
                                 required=False))

    async def callback(self, interaction: discord.Interaction):

        self.comment = self.children[0].value
        await interaction.response.defer()


@bot.command(guild_ids=[server_id],
             description="Add score to user with defined difficulty")
@commands.has_role("Guessing Manager")
async def addscoreguessinggame(ctx, user, difficulty, question_no):
    """
  if (not await precheck(ctx)):
    await noPermission(ctx)
    return
  """

    user_id = ctx.author.id
    await ctx.defer()

    if not re.match("<@[0-9]*>$", user):
        await ctx.respond(
            "<@" + str(user_id) +
            "> Please mention user to add score...like <@904270269227626496>")
        return

    user = str(await filtering_input(ctx, user))

    if str(user) != owner_id and str(user_id) == str(user):
        await ctx.respond(
            "<@" + str(user_id) +
            "> Oh no! You are trying to add score to yourself. How shameless!")
        return

    difficulty = str(await filtering_input(ctx, difficulty)).lower()

    score = 0

    if difficulty == 'easy':
        score = 1
    elif difficulty == 'difficult':
        score = 3
    elif difficulty == 'intense':
        score = 5
    elif difficulty == 'insane':
        score = 7
    elif difficulty == 'horrific':
        score = 10
    elif difficulty.lstrip('-').isdigit():
        score = int(difficulty)

    if score == 0:
        await ctx.respond(
            "<@" + str(user_id) +
            "> Please input the correct difficulty **(easy/difficult/intense/insane/horrific)**. Or you may assign the actual score to me"
        )
        return

    if not str(question_no).isdigit():
        await ctx.respond("<@" + str(user_id) +
                          "> Please input only **number** to question no.")
        return

    score_info = db_handler.getGuessingScore(user)

    current_score = 0

    if len(score_info) > 0:
        current_score = score_info[0][1]

    username = bot.get_user(int(user))

    #print(user,score)
    db_handler.addGuessingScore(user, score)
    await ctx.respond("<@" + str(user_id) + "> The score of **" +
                      str(username) + "** has been updated from **" +
                      str(current_score) + "** to **" +
                      str(int(current_score) + int(score)) +
                      "** for the question **#" + str(question_no) + "**")


@bot.command(guild_ids=[server_id], description="Vote any tower manually")
@commands.has_role("Crp")
async def votetower(ctx, tower):
    if (not await precheck(ctx)):
        await noPermission(ctx)
        return

    tower = await filtering_input(ctx, tower)
    user_id = ctx.author.id

    info = df_info[df_info['Acronym'].str.lower() == tower.lower()]

    if info.shape[0] > 0:

        def check(m):
            return True

        timeout_period = 10
        view_diff = DifficultyDropdown(timeout=timeout_period)

        await ctx.respond("Vote your personal difficulty please",
                          view=view_diff)

        def check(m):
            return True

        interaction = await bot.wait_for("interaction",
                                         check=check,
                                         timeout=timeout_period)
        difficulty = JToHDifficulties.correctDifficulty(view_diff.difficulty)

        view_subdiff = SubDifficultyDropdown(timeout=timeout_period)

        await ctx.send("Vote your personal subdifficulty please",
                       view=view_subdiff)

        interaction = await bot.wait_for("interaction",
                                         check=check,
                                         timeout=timeout_period)
        subdifficulty = JToHDifficulties.correctSubdifficulty(
            view_subdiff.subdifficulty)

        view_gameplay = ScoreDropdown(timeout=timeout_period)

        await ctx.send("Vote your gameplay score " +
                       emoji.getEmoji("gameplaystar") + " please",
                       view=view_gameplay)

        interaction = await bot.wait_for("interaction",
                                         check=check,
                                         timeout=timeout_period)
        gameplay = view_gameplay.score

        view_creativity = ScoreDropdown(timeout=timeout_period)

        await ctx.send("Vote your creativity " +
                       emoji.getEmoji("creativitystar") + " score please",
                       view=view_gameplay)

        interaction = await bot.wait_for("interaction",
                                         check=check,
                                         timeout=timeout_period)
        creativity = view_creativity.score

        view_design = ScoreDropdown(timeout=timeout_period)

        await ctx.send("Vote your design " + emoji.getEmoji("designstar") +
                       " score please",
                       view=view_design)

        interaction = await bot.wait_for("interaction",
                                         check=check,
                                         timeout=timeout_period)
        design = view_design.score

        comment_modal = CommentModal(title="Your comment")
        await ctx.send_modal(comment_modal)

        interaction3 = await bot.wait_for("interaction", check=check)
        comment = comment_modal.comment

        #print(difficulty,subdifficulty,gameplay,creativity,design,comment)

    else:
        await ctx.respond(await noTowerFound(tower))


@bot.command(guild_ids=[server_id],
             description="Give an idea of monthly challenge")
async def monthlychallengeidea(ctx):

    if (not await precheck(ctx)):
        await noPermission(ctx)
        return

    user_id = ctx.author.id

    random_list = [0, 1, 2]
    random_key = random.choice(random_list)

    try:

        idea = ""

        difficulty_list = [
            "easy", "medium", "hard", "difficult", "challenging", "intense",
            "remorseless", "insane", "extreme", "terrifying", "catastrophic"
        ]

        difficulty_nonsc_list = [
            "easy", "medium", "hard", "difficult", "challenging", "intense",
            "remorseless"
        ]

        if random_key == 0:

            info = df_info[(df_info['Accessible'] == 'y')
                           & (df_info['Difficulty'].isin(difficulty_list)) &
                           (df_info['Monthly'] == 'n')]
            tower_name = random.choice(info['Acronym'].values.tolist())

            tower_info = df_info[df_info['Acronym'] == tower_name].iloc[0]

            speedrun_time = tower_info['Average speedrun playtime (minute)']
            idea = "Beat " + tower_name + " in under " + str(
                math.ceil(speedrun_time / 0.6)) + " minutes"
        if random_key == 1:

            info = df_info[(df_info['Accessible'] == 'y')
                           & (df_info['Difficulty'].isin(difficulty_list)) &
                           (df_info['Monthly'] == 'n')]
            tower_name = random.choice(info['Acronym'].values.tolist())

            tower_info = df_info[df_info['Acronym'] == tower_name].iloc[0]

            floors = int(tower_info['Floors'])
            floor_list = list(range(3, floors + 1))
            random_floor = random.choice(floor_list)
            idea = "Reach floor " + str(random_floor) + " of " + tower_name
        if random_key == 2:

            info = df_info[(df_info['Accessible'] == 'y') &
                           (df_info['Difficulty'].isin(difficulty_nonsc_list))
                           & (df_info['Monthly'] == 'n')]
            tower_name = random.choice(info['Acronym'].values.tolist())

            tower_info = df_info[df_info['Acronym'] == tower_name].iloc[0]

            idea = "Reach " + tower_name + " in Tower Rush"
        embed = discord.Embed(title="Monthly challenge idea",
                              description=idea,
                              color=discord.Color.blue())

        await ctx.respond(embed=embed)
    except Exception as e:
        print(e)
        await ctx.respond(
            "<@" + str(user_id) +
            "> Sorry! I can't think of any idea about monthly challenge :sob:")


@bot.command(description='Ring 1/ring/main/1/1')
#@commands.has_permissions(administrator=True)
@commands.has_role("Crp")
async def generateguidelist(ctx, area_code, message_id=None):
    #async def generateguidelist(ctx,title='Arcane Area', tower_location='zone',tower_location_type='subrealm',tower_location_number='2',tower_location_subnumber='1',message_id=None):
    try:
        """
        tower_list = df_info[
            (df_info['Location'] == tower_location)
            & (df_info['Location type'] == tower_location_type) &
            ((df_info['Location number']) == int(tower_location_number)) &
            ((df_info['Location subnumber']) == int(tower_location_subnumber))
            & (df_info['Accessible'] == 'y')].sort_values(by='Num Difficulty',
                                                          ascending=True)
        """
        tower_list = df_info[(df_info['Area code'] == area_code)
                             & (df_info['Accessible'] == 'y') &
                             (df_info['Monthly'] == 'n')].sort_values(
                                 by='Num Difficulty', ascending=True)
        if tower_list.shape[0] > 0:

            #print(tower_list)

            #await ctx.respond(tower_list)
            title = df_area[df_area['Acronym'] ==
                            area_code].iloc[0]['Area name']

            embed = discord.Embed(title="The guide list",
                                  color=discord.Color.blue())

            for index, info in tower_list.iterrows():

                guide_url = info['Video URL']

                dif = info['Difficulty']
                emoji_dif = ":grey_question:"
                if str(guide_url) == 'nan':
                    guide_url = ":no_entry:"

                emoji_dif = emoji.getEmoji(dif)
                if str(emoji_dif) == 'nan':
                    emoji_dif = ":grey_question:"

                embed.add_field(name=("**[" + emoji_dif + "]** (" +
                                      info['Acronym'] + ') ' + info['Tower']),
                                value=guide_url,
                                inline=False)

            emblem_url = df_area[(
                df_area['Acronym'] == area_code)]['Emblem URL']

            if emblem_url is not None and str(emblem_url) != 'nan' and len(
                    emblem_url) > 0:
                emblem_url = emblem_url.values[0]
                embed.set_thumbnail(url=emblem_url)

            if message_id is None:
                await ctx.send("**" + title + "**", embed=embed)
            else:
                channel = bot.get_channel(int(guide_channel_id))
                #channel = bot.get_channel(976080610034593843)
                msg = await channel.fetch_message(int(message_id))
                await msg.edit("**" + title + "**", embed=embed)
                #print(msg)

        else:
            await ctx.respond("No tower in the list")
    except Exception as e:
        print(e)
        await ctx.respond(e)


@bot.command()
#@commands.has_permissions(administrator=True)
@commands.has_role("Crp")
async def generatetowerdetail(ctx, tower):

    tower = await filtering_input(ctx, tower)

    try:

        tower_progress = df_progress[df_progress['Acronym'] == tower].iloc[
            0].dropna().values.flatten().tolist()
        tower_feature = df_feature[df_feature['Acronym'] ==
                                   tower].iloc[0].values.flatten().tolist()
        tower_perdif = df_perdif[df_perdif['Acronym'] ==
                                 tower].iloc[0].values.flatten().tolist()

        tower_full_name = df_info[df_info['Acronym'] == tower]['Tower'].iloc[0]

        detail = "\*\*(" + tower + ") " + tower_full_name + "\*\*"
        detail += "\n\n"

        for k in range(1, len(tower_progress)):
            print(k)
            detail += ("\*\*" + tower_progress[k] + "\*\*: ")

            per_sub, per_dif = tower_perdif[k].split(" ")

            #detail+=(per_sub+" "+emoji_code[per_dif.lower()]+" ")
            detail += (per_sub + " :" + per_dif.capitalize() + ": ")

            if str(tower_feature[k]).strip() != 'nan':
                #feature_code
                detail += "\*("

                for feature in tower_feature[k].split("/"):
                    if not feature in feature_code:
                        feature_code[feature] = df_feature_code[
                            df_feature_code['Acronym'] ==
                            feature]['Full name'].iloc[0]
                    detail += feature_code[feature]
                    detail += ', '

                detail = detail[:-2]
                detail += ")\*"

            detail += "\n"

        await ctx.respond(detail)

    except Exception as e:
        #print(e)
        #await ctx.send('I can\'t find information about **'+tower+"**")
        tower_full_name = df_info[df_info['Acronym'] == tower]['Tower'].iloc[0]

        detail = ""
        detail += "\*\*(" + tower + ") " + tower_full_name + "\*\*"
        detail += "\n\n"
        detail += "\:question\: Currently no information \:question\:"
        tower_full_name = df_info[df_info['Acronym'] == tower]['Tower'].iloc[0]
        await ctx.respond(detail)


@bot.command()
#@commands.has_permissions(administrator=True)
@commands.has_role("Crp")
async def generatetowerpoll(ctx, tower):

    tower = await filtering_input(ctx, tower)

    info = df_info[df_info['Acronym'] == tower].iloc[0]
    subdifficulty = JToHDifficulties.correctSubdifficulty(
        info['Sub difficulty'])
    difficulty = JToHDifficulties.correctDifficulty(info['Difficulty'])

    dif_value = JToHDifficulties.difficulty_to_num[
        difficulty] + JToHDifficulties.subdifficulty_to_num[subdifficulty]

    #await ctx.respond("Current DC: "+subdifficulty.capitalize() +" "+emoji_code[difficulty])
    await ctx.respond("Please vote your personal difficulty")

    poll_text = ""
    current_difficulty, current_subdifficulty = JToHDifficulties.decreaseDifficulty(
        difficulty, subdifficulty, 10)

    for k in range(1, 21):
        poll_text += emoji.getEmoji(
            str(k) + "_g") + " " + current_subdifficulty.capitalize(
            ) + " " + emoji.getEmoji(current_difficulty) + "\n"
        current_difficulty, current_subdifficulty = JToHDifficulties.increaseDifficultyByOne(
            current_difficulty, current_subdifficulty)

    poll_message = await ctx.send(poll_text)
    for k in range(1, 21):
        await poll_message.add_reaction(emoji=emoji.getEmoji(str(k) + "_g"))

    floors = int(info['Floors'])

    hardest_message = await ctx.send(":person_climbing: The hardest floor?")
    for k in range(1, floors + 1):
        if k == 11 or k == 21:
            hardest_message = await ctx.send("(Continued)")
        await hardest_message.add_reaction(emoji=emoji.getEmoji(str(k) + "_g"))

    longest_message = await ctx.send(":clock10: The longest floor?")
    for k in range(1, floors + 1):
        if k == 11 or k == 21:
            hardest_message = await ctx.send("(Continued)")
        await longest_message.add_reaction(emoji=emoji.getEmoji(str(k) + "_g"))

    gameplay_message = await ctx.send(
        emoji.getEmoji('gameplaystar') + " Gameplay score?")
    for k in range(0, 11):
        await gameplay_message.add_reaction(
            emoji=emoji.getEmoji(str(k) + "_g"))

    creativity_message = await ctx.send(
        emoji.getEmoji('creativitystar') + " Creativity score?")
    for k in range(0, 11):
        await creativity_message.add_reaction(
            emoji=emoji.getEmoji(str(k) + "_g"))

    design_message = await ctx.send(
        emoji.getEmoji('designstar') + " Design score?")
    for k in range(0, 11):
        await design_message.add_reaction(emoji=emoji.getEmoji(str(k) + "_g"))


@bot.command()
#@commands.has_permissions(administrator=True)
@commands.has_role("Crp")
async def unixtimestamp(ctx):
    await ctx.respond(int(time.time()))


#@bot.command(guild_ids=[server_id], description="Check for update")
#@commands.has_permissions(administrator=True)
#@commands.has_role("Crp")
#@tasks.loop(minutes=15)

tower_log_list = {}


@bot.command()
#@commands.has_permissions(administrator=True)
@commands.has_role("Crp")
async def generatefeaturedetail(ctx):

    for index, row in df_feature_code.iterrows():
        embed = discord.Embed(title=row['Full name'],
                              color=discord.Color.blue())
        embed.add_field(name="Acronym", value=row['Acronym'], inline=False)
        embed.add_field(name="Description",
                        value=row['Description'],
                        inline=False)
        file = discord.File("image/feature_code/" + row['Acronym'] + ".png",
                            filename=row['Acronym'] + ".png")
        #print("image/feature_code/"+row['Acronym']+".png")
        embed.set_image(url="attachment://" + row['Acronym'] + ".png")
        await ctx.send(file=file, embed=embed)




@bot.command()
#@commands.has_permissions(administrator=True)
@commands.has_role("Crp")
async def recheckjtohleaderboard(ctx):
    jtoh_table = db_handler.getTotalTowerCompletion()
    threshold = 1
    now = datetime.now()
    for players in jtoh_table:
        tower_point = players[0]
        username = players[1]
        latest_update = players[3]
        latest_date_obj = datetime.strptime(latest_update, '%m/%d/%Y %H:%M:%S')
        day_diff = (now - latest_date_obj).days
        if tower_point >= threshold and day_diff > 1:
            latest_date_obj = datetime.strptime(latest_update,
                                                '%m/%d/%Y %H:%M:%S')
            await ctx.send("Updating the tower completion of **" + username +
                           "**")
            
            #await updatetowercompletion(username)
            #db_handler.removeTowerBeatenList(username)
            #await updatetowercompletionmode(username,mode=2)
            #await updatetowercompletionmode(username,mode=1)
            await updatetowercompletionmode(username,mode=0)
            #time.sleep(1)


async def activeStatus(bot):
    today = datetime.now()
    year = today.year
    month = today.month
    day = today.day

    date_format = today.strftime("%d/%m/%Y %H:%M")
    channel = bot.get_channel(int(bot_status_channel_id))
    await channel.edit(name=date_format)

    print(date_format)


@tasks.loop(hours=1)
async def updateYoutubeStat():

    print("Checking yt stats")

    request = youtube_api.channels().list(part='statistics',
                                          id=youtube_channel_id)
    response = request.execute()

    views = int(response['items'][0]['statistics']['viewCount'])
    subs = int(response['items'][0]['statistics']['subscriberCount'])
    print(views, subs)

    channel = bot.get_channel(int(youtube_view_channel_id))
    await channel.edit(name=("Total views: " + "{:,}".format(views)))
    channel = bot.get_channel(int(youtube_sub_channel_id))
    await channel.edit(name=("Total subs: " + "{:,}".format(subs)))


@tasks.loop(minutes=10)
#@tasks.loop(seconds=10)
async def updateleaderboard():
    score_table = db_handler.getGameScore()

    rank = 1
    rank_text = ""

    role_threshold = 1000

    channel = bot.get_channel(int(leaderboard_channel_id))

    for info in score_table:
        id = info[0]
        #if str(id)==str(owner_id):
        #  continue
        score = info[1]
        username = bot.get_user(int(id))
        #print(username)
        #if channel.guild.get_member(id):
        #username = "<@"+str(id)+"> "

        #username = "<@"+str(id)+"> "
        if username is None:
            continue

        rank_text += (str(rank) + ". **" + str(username) + "** - " +
                      "{:,}".format(score) + " points \n")

        if score >= role_threshold:
            member = channel.guild.get_member(id)
            role = get(channel.guild.roles, name="Crp Game Guessing Master")
            if member and role:
                await member.add_roles(role)

        rank += 1

        if rank > 100:
            break

    embed = discord.Embed(title="Top 100 players Leaderboard",
                          description=rank_text,
                          color=discord.Color.blue())

    #leaderboard_channel_id
    msg = await channel.fetch_message(int(1019460041939636256))

    now = datetime.now()
    date_time = now.strftime("%a %b %d, %Y at %H:%M:%SUTC")
    date_time = " <t:" + str(int(time.time())) + ":F>"

    await msg.edit(content="Last updated: " + date_time, embed=embed)

    print("updating the leaderboard")
    #1019460041939636256
    #await channel.edit(embed=embed)


@tasks.loop(minutes=60)
#@tasks.loop(seconds=10)
async def updateguessingleaderboard():
    score_table = db_handler.getGuessingScore()

    rank = 1
    rank_text = ""

    role_threshold = 100

    channel = bot.get_channel(int(guessing_leaderboard_channel_id))

    for info in score_table:
        id = info[0]
        #if str(id)==str(owner_id):
        #  continue
        score = info[1]
        username = bot.get_user(int(id))
        #print(username)
        #if channel.guild.get_member(id):
        #username = "<@"+str(id)+"> "

        #username = "<@"+str(id)+"> "
        if username is None:
            continue

        rank_text += (str(rank) + ". **" + str(username) + "** - " +
                      "{:,}".format(score) + " points \n")

        if score >= role_threshold:
            member = channel.guild.get_member(id)
            role = get(channel.guild.roles, name="Tower Guessing Master")
            if member and role:
                await member.add_roles(role)

        rank += 1

        if rank > 100:
            break

    embed = discord.Embed(title="Tower Guessing Leaderboard",
                          description=rank_text,
                          color=discord.Color.blue())

    #leaderboard_channel_id
    msg = await channel.fetch_message(int(1053185397502509076))

    now = datetime.now()
    date_time = now.strftime("%a %b %d, %Y at %H:%M:%SUTC")
    date_time = " <t:" + str(int(time.time())) + ":F>"

    await msg.edit(content="Last updated: " + date_time, embed=embed)

    print("updating the guessing leaderboard")
    #1019460041939636256
    #await channel.edit(embed=embed)


@tasks.loop(minutes=60)
#@tasks.loop(seconds=10)
async def updatejtohleaderboard():
    jtoh_table = db_handler.getTotalTowerCompletion()

    channel = bot.get_channel(int(jtoh_leaderboard_channel_id))
    rank_text = ""

    rank = 1
    rank_limit = 500

    text_id = [
        1033283336661110826, 1033283350561038356, 1033283366314844180,
        1033283408576643112, 1033283450683273216,1065844321489788978,
      1065844356042457138,1065844386279202897,1065844406487367714,
      1065844430520713266
    ]

    limit_per_message = 50

    for info in jtoh_table:

        score = info[0]
        username = info[1]
        difficulty = df_info[df_info['Acronym'] ==
                             info[2]].iloc[0]['Difficulty']
        hardest_tower = info[2]
        #last_update = info[3]
        #date_time_obj = datetime.strptime(last_update, '%d/%m/%y %H:%M:%S')

        #print(username)
        rank_text += (str(rank) + ". " + str(username.lower()) + " - **" +
                      "{:,}".format(score) + " (" +
                      emoji.getEmoji(difficulty) + " " + hardest_tower +
                      ")**\n")
        #print(time.mktime(date_time_obj.timetuple()))

        #print(score)

        rank += 1
        #if rank>=190:
        #print(rank)

        if (rank - 1) % limit_per_message == 0 or rank >= len(jtoh_table):
            #print(rank)
            embed = discord.Embed(
                title="JToH Leaderboard (with their hardest tower)",
                description=rank_text,
                color=discord.Color.blue())

            #leaderboard_channel_id
            msg_index = (rank - 2) / limit_per_message
            #print(msg_index)

            msg = await channel.fetch_message(text_id[math.floor(msg_index)])

            now = datetime.now()
            date_time = now.strftime("%a %b %d, %Y at %H:%M:%SUTC")
            date_time = " <t:" + str(int(time.time())) + ":F>"

            #await msg.send(content="Last updated: " + date_time, embed=embed)
            await msg.edit(content="", embed=embed)

            rank_text = ""

        if rank > rank_limit or rank >= len(jtoh_table):
            break

    print("updating the jtoh leaderboard")
    #1019460041939636256
    #await channel.edit(embed=embed)


@tasks.loop(seconds=360)
async def updateserverclock():

    print("updating the time")

    today = datetime.now() + timedelta(hours=7)
    year = today.year
    month = today.month
    day = today.day

    date_format = today.strftime("%d/%m/%Y %I:%M %p")
    channel = bot.get_channel(int(bot_status_channel_id))
    await channel.edit(name=date_format)

    print(date_format)


@tasks.loop(minutes=5)
async def checkforupdate():

    print("Checking for difficulty update")

    #await activeStatus(bot)

    df_official = pd.read_csv(official_difficulty_url)
    df_old_dif = df_info[['Acronym', 'Num Difficulty']]
    df_new_dif = df_official[[
        'Tower', 'Num Difficulty', 'Difficulty', 'Level'
    ]]
    df_old_dif = df_old_dif.rename(columns={
        'Acronym': 'Tower',
        'Num Difficulty': 'Num Difficulty Old'
    })
    df_new_dif = df_new_dif.rename(columns={
        'Tower': 'Tower',
        'Num Difficulty': 'Num Difficulty New'
    })
    df_old_dif = df_old_dif.set_index('Tower')
    df_new_dif = df_new_dif.set_index('Tower')
    df_dif_compare = df_new_dif.merge(df_old_dif, on='Tower', how='left')

    df_mismatch = df_dif_compare[(df_dif_compare['Num Difficulty Old'] !=
                                  df_dif_compare['Num Difficulty New'])]

    if len(df_mismatch) > 25:
        print("Bug founded in the difficulty update channel")
        return

    #print(df_mismatch)

    channel = bot.get_channel(int(update_log_channel_id))
    #channel = bot.get_channel(976080610034593843)

    for tower, row in df_mismatch.iterrows():
        if tower == '???':
            continue
        if (str(row['Num Difficulty Old']) == 'nan'
                and str(row['Num Difficulty New']) == 'nan'):
            continue
        try:
            time.sleep(1)

            if (not tower in tower_log_list):
                if (str(row['Num Difficulty Old']) != 'nan'):
                    await channel.send(
                        "<@&" + jtoh_real_time_role_id +
                        "> The difficulty of **" + tower +
                        "** has been changed to " + row['Level'].lower() +
                        " " + emoji.getEmoji(row['Difficulty'].lower()) +
                        " (" + str(row['Num Difficulty Old']) + "->" +
                        str(row['Num Difficulty New']) + ")")
                else:
                    await channel.send(
                        "<@&" + jtoh_real_time_role_id + "> **" + tower +
                        "** is expected to be added to the game as " +
                        row['Level'].lower() + " " +
                        emoji.getEmoji(row['Difficulty'].lower()) + " (" +
                        str(row['Num Difficulty New']) + ")")

            if not tower in tower_log_list:
                tower_log_list[tower] = 1

        except Exception as e:
            print(e)

    #976080433676689408


#keep_alive()
          
token = os.environ['TOKEN']
print("Starting...")
#client.run(token)
#bot.run(token)
try:
    bot.run(token)
except:
    os.system("kill 1")
#bot.run(os.environ['TOKEN'])  #Run bot
