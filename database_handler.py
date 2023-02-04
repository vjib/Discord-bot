import sqlite3

import os
import pandas as pd
import numpy as np

from datetime import date, datetime, timedelta

#"TABLE game_score -- score for crp guessing game

# user_id int NOT NULL
# score int
# last_update date
# PRIMARY KEY (user_id)"

#Table guessing_score -- score for tower guessing game

# user_id int NOT NULL
# score int
# last_update date
# PRIMARY KEY (user_id)"

#"TABLE user_info

# username varchar(50) NOT NULL
# user_id int NOT NULL
# last_update date
# PRIMARY KEY (username)"

#Table beaten_list

# user_id int NOT NULL
#tower varchar(10)
#date_beaten date
#last_update date
#PRIMARY KEY (user_id))

#Table tower_vote

#user_id int NOT NULL
#tower varchar(10) NOT NULL
#personal_diff varchar(30)
#personal_subdiff varchar(30)
#gameplay int
#creativity int
#design int
#comment varchar(300)
#last_update date
#PRIMARY KEY (user_id,tower))



def addGameScore(userid, score):

    now = datetime.now()
    date_time = now.strftime("%m/%d/%Y %H:%M:%S")

    con = sqlite3.connect("CrpLand.db")

    try:

        with con:
            cur = con.cursor()

            sql_check_user = "SELECT * FROM game_score WHERE user_id=" + str(
                userid)
            cur.execute(sql_check_user)
            result = cur.fetchall()

            #print(result)

            if len(result) == 0:
                sql_add_user = "INSERT INTO game_score VALUES (" + str(
                    userid) + "," + str(score) + ",'" + date_time + "');"

                #print(sql_add_user)

                cur.execute(sql_add_user)
            else:
                #print(result[0])
                current_score = int(result[0][1])
                sql_update_user = "UPDATE game_score SET score=" + str(
                    current_score + int(score)
                ) + ",last_update='" + date_time + "' WHERE user_id=" + str(
                    userid)

                #print(sql_update_user)

                cur.execute(sql_update_user)

        if con:
            con.close()

        return True
    except Exception as e:
        #print(e)
        return False

    return True


def getGameScore(userid=None, limit=None):
    con = sqlite3.connect("CrpLand.db")

    try:

        with con:
            cur = con.cursor()

            sql_get_scores = "SELECT * FROM game_score"

            if userid is not None:
                sql_get_scores += " WHERE user_id=" + str(userid)

            sql_get_scores += " ORDER BY score DESC"

            if limit is not None:
                sql_get_scores += " LIMIT " + str(limit)

            cur.execute(sql_get_scores)
            return cur.fetchall()

        if con:
            con.close()

        return []
    except Exception as e:
        #print(e)
        return []

    return []

def addGuessingScore(userid, score):

    now = datetime.now()
    date_time = now.strftime("%m/%d/%Y %H:%M:%S")

    con = sqlite3.connect("CrpLand.db")

    try:

        with con:
            cur = con.cursor()

            sql_check_user = "SELECT * FROM guessing_score WHERE user_id=" + str(
                userid)
            cur.execute(sql_check_user)
            result = cur.fetchall()

            #print(result)

            if len(result) == 0:
                sql_add_user = "INSERT INTO guessing_score VALUES (" + str(
                    userid) + "," + str(score) + ",'" + date_time + "');"

                #print(sql_add_user)

                cur.execute(sql_add_user)
            else:
                #print(result[0])
                current_score = int(result[0][1])
                sql_update_user = "UPDATE guessing_score SET score=" + str(
                    current_score + int(score)
                ) + ",last_update='" + date_time + "' WHERE user_id=" + str(
                    userid)

                #print(sql_update_user)

                cur.execute(sql_update_user)

        if con:
            con.close()

        return True
    except Exception as e:
        #print(e)
        return False

    return True

def getGuessingScore(userid=None, limit=None):
    con = sqlite3.connect("CrpLand.db")

    try:

        with con:
            cur = con.cursor()

            sql_get_scores = "SELECT * FROM guessing_score"

            if userid is not None:
                sql_get_scores += " WHERE user_id=" + str(userid)

            sql_get_scores += " ORDER BY score DESC"

            if limit is not None:
                sql_get_scores += " LIMIT " + str(limit)

            cur.execute(sql_get_scores)
            return cur.fetchall()

        if con:
            con.close()

        return []
    except Exception as e:
        #print(e)
        return []

    return []

def updateUserId(username, userid):

    username = username.lower()

    now = datetime.now()
    date_time = now.strftime("%m/%d/%Y %H:%M:%S")

    con = sqlite3.connect("CrpLand.db")

    try:

        with con:
            cur = con.cursor()

            sql_check_user = "SELECT * FROM user_info WHERE LOWER(username)='" + username + "'"
            cur.execute(sql_check_user)
            result = cur.fetchall()

            #print(result)

            if len(result) == 0:
                sql_add_user = "INSERT INTO user_info VALUES ('" + str(
                    username) + "'," + str(userid) + ",'" + date_time + "');"

                #print(sql_add_user)

                cur.execute(sql_add_user)
            else:
                sql_update_user = "UPDATE user_info SET user_id=" + str(
                    userid
                ) + ",last_update='" + date_time + "' WHERE LOWER(username)='" + str(
                    username) + "'"

                #print(sql_update_user)

                cur.execute(sql_update_user)

        if con:
            con.close()

        return True
    except Exception as e:
        #print(e)
        return False

    return True


def getUserInfo(username):

    username = username.lower()

    con = sqlite3.connect("CrpLand.db")

    try:

        with con:
            cur = con.cursor()

            sql_get_scores = "SELECT * FROM user_info WHERE LOWER(username)='" + username + "'"

            cur.execute(sql_get_scores)
            return cur.fetchall()

        if con:
            con.close()

        return []
    except Exception as e:
        #print(e)
        return []

    return []


def addTowerBeatenList(username, tower_list):

    now = datetime.now()
    date_time = now.strftime("%m/%d/%Y %H:%M:%S")

    con = sqlite3.connect("CrpLand.db")

    username = username.lower()

    try:

        with con:
            cur = con.cursor()

            sql_check_user = "SELECT * FROM user_info WHERE LOWER(username)='" + username + "'"

            #print(sql_check_user)

            cur.execute(sql_check_user)
            result = cur.fetchall()

            #print(result)

            if len(result) > 0:

                userid = result[0][1]

                sql_check_beaten = "SELECT * FROM beaten_list WHERE user_id=" + str(
                    userid) + ""

                #print(sql_check_beaten)
                cur.execute(sql_check_beaten)
                result = cur.fetchall()
                #print(result)
                existing_tower_list = {}
                for r in result:
                    t = r[1].lower()
                    existing_tower_list[t] = 0

                sql_add_beaten = "INSERT INTO beaten_list (user_id,tower,date_beaten,last_update) VALUES"
                for tower in tower_list:
                    acronym = tower[0]
                    date_beaten = tower[1]

                    if not acronym.lower() in existing_tower_list:

                        sql_add_beaten += "(" + str(
                            userid
                        ) + ",'" + acronym + "','" + date_beaten + "','" + date_time + "'),"

                sql_add_beaten = sql_add_beaten[:-1] + ";"

                #print(sql_add_beaten)

                cur.execute(sql_add_beaten)

        if con:
            con.close()

        return True
    except Exception as e:
        print(e)
        return False

    return True

def removeTowerBeatenList(username):

    con = sqlite3.connect("CrpLand.db")

    username = username.lower()

    try:

        with con:
            cur = con.cursor()

            sql_check_user = "SELECT * FROM user_info WHERE LOWER(username)='" + username + "'"

            #print(sql_check_user)

            cur.execute(sql_check_user)
            result = cur.fetchall()

            #print(result)

            if len(result) > 0:

                userid = result[0][1]

                sql_remove_beaten = "DELETE FROM beaten_list WHERE user_id=" + str( userid) + ""

                cur.execute(sql_remove_beaten)

        if con:
            con.close()

        return True
    except Exception as e:
        print(e)
        return False

    return True

def getTowerBeaten(username, tower):

    username = username.lower()
    tower = tower.lower()

    con = sqlite3.connect("CrpLand.db")

    try:

        with con:
            cur = con.cursor()

            sql_get_beaten_list = "SELECT * FROM beaten_list b INNER JOIN user_info u ON b.user_id=u.user_id WHERE LOWER(u.username)='" + username + "' AND LOWER(b.tower)='" + tower + "'"

            #print(sql_get_beaten_list)

            cur.execute(sql_get_beaten_list)
            return cur.fetchall()

        if con:
            con.close()

        return []
    except Exception as e:
        #print(e)
        return []

    return []


def getTowerBeatenList(username):

    username = username.lower()

    con = sqlite3.connect("CrpLand.db")

    try:

        with con:
            cur = con.cursor()

            sql_get_beaten_list = "SELECT * FROM beaten_list b INNER JOIN user_info u ON b.user_id=u.user_id WHERE LOWER(u.username)='" + username + "' ORDER BY b.date_beaten ASC"

            #print(sql_get_beaten_list)

            cur.execute(sql_get_beaten_list)
            return cur.fetchall()

        if con:
            con.close()

        return []
    except Exception as e:
        #print(e)
        return []

    return []

def getTowerBeatenByNth(username,nth):

    username = username.lower()

    con = sqlite3.connect("CrpLand.db")

    try:

        with con:
            cur = con.cursor()

            sql_get_beaten_list = "SELECT * FROM beaten_list b INNER JOIN user_info u ON b.user_id=u.user_id LEFT JOIN tower_details p ON b.tower=p.acronym WHERE LOWER(u.username)='" + username + "' AND p.tower_type<>'MiniTower' AND p.location_type<>'event' ORDER BY b.date_beaten ASC LIMIT 1 OFFSET "+str(int(nth)-1)

            #print(sql_get_beaten_list)

            cur.execute(sql_get_beaten_list)
            return cur.fetchall()

        if con:
            con.close()

        return []
    except Exception as e:
        #print(e)
        return []

    return []

def getHardestBeatenList(username,amount):

    username = username.lower()

    con = sqlite3.connect("CrpLand.db")

    try:

        with con:
            cur = con.cursor()

            sql_get_beaten_list = "SELECT u.user_id as user_id,b.tower as tower,b.date_beaten as date_beaten FROM beaten_list b INNER JOIN user_info u ON b.user_id=u.user_id LEFT JOIN tower_details p ON b.tower=p.acronym WHERE LOWER(u.username)='" + username + "' ORDER BY p.num_difficulty DESC LIMIT "+str(amount)

            #print(sql_get_beaten_list)

            cur.execute(sql_get_beaten_list)
            return cur.fetchall()

        if con:
            con.close()

        return []
    except Exception as e:
        #print(e)
        return []

    return []

def getRecentBeatenList(username,amount):

    username = username.lower()

    con = sqlite3.connect("CrpLand.db")

    try:

        with con:
            cur = con.cursor()

            sql_get_beaten_list = "SELECT u.user_id as user_id,b.tower as tower,b.date_beaten as date_beaten FROM beaten_list b INNER JOIN user_info u ON b.user_id=u.user_id WHERE LOWER(u.username)='" + username + "' ORDER BY date_beaten DESC LIMIT "+str(amount)

            #print(sql_get_beaten_list)

            cur.execute(sql_get_beaten_list)
            return cur.fetchall()

        if con:
            con.close()

        return []
    except Exception as e:
        #print(e)
        return []

    return []

def getTotalTowerCompletion():

    con = sqlite3.connect("CrpLand.db")

    try:

        with con:
            cur = con.cursor()

            sql_get_total = "SELECT COUNT(*) AS tower_completion,u.username AS username,b2.tower as hardest_tower,MAX(u.last_update) as latest_update FROM beaten_list b INNER JOIN user_info u ON b.user_id=u.user_id LEFT JOIN tower_details p ON b.tower=p.acronym LEFT JOIN beaten_list b2 ON b.user_id=b2.user_id AND b.tower=b2.tower WHERE p.tower_type<>'MiniTower' and p.location_type<>'event' GROUP BY u.username ORDER BY COUNT(*) DESC,MAX(p.num_difficulty) DESC,b.date_beaten DESC"
            #sql_get_total="SELECT COUNT(*) AS tower_completion,u.username AS username,MAX(u.last_update) as latest_update FROM beaten_list b INNER JOIN user_info u ON b.user_id=u.user_id GROUP BY u.username ORDER BY COUNT(*) DESC"

            #print(sql_get_beaten_list)

            cur.execute(sql_get_total)
            return cur.fetchall()

        if con:
            con.close()

        return []
    except Exception as e:
        print(e)
        return []

    return []

def getAllTowerBeatenForTraining():

    con = sqlite3.connect("CrpLand.db")

    try:

        with con:
            cur = con.cursor()

            sql_get_beaten_list = "SELECT b.user_id,b.tower,b.date_beaten FROM beaten_list b INNER JOIN (SELECT user_id AS temp_user_id,MIN(date_beaten) AS first_beaten FROM beaten_list b GROUP BY user_id) m ON b.user_id=m.temp_user_id ORDER BY b.user_id ASC,b.date_beaten ASC"

            #print(sql_get_beaten_list)

            cur.execute(sql_get_beaten_list)
            return cur.fetchall()

        if con:
            con.close()

        return []
    except Exception as e:
        #print(e)
        return []

    return []

def feedTowerDetails():
    con = sqlite3.connect("CrpLand.db")

    try:

        tower_info_url = os.environ['TOWER_INFO_URL']
        df_info = pd.read_csv(tower_info_url)

        badge_info_url = os.environ['BADGE_INFO_URL']
        df_badge = pd.read_csv(badge_info_url)

        info = df_info[["Acronym", "Num Difficulty", "Tower type","Location type"]]

        """
        badge_info = df_badge[(df_badge['Category'] == 'Beating Tower')]
        badge_info = badge_info[["Value 1","Badge ID"]]
        badge_info = badge_info.rename(columns={'Value 1': 'Acronym'})
      
        info = df_points.merge(badge_info, on='Acronym', how='left')
        """
        

        info = info.rename(
            columns={
                'Acronym': 'acronym',
                'Num Difficulty': 'num_difficulty',
                'Tower type': 'tower_type',
                'Location type':'location_type'
            })

        with con:

            info.to_sql("tower_details",
                             con,
                             if_exists='replace')
            print(con)
            print("Successfully updated")

    except Exception as e:
        print(e)
