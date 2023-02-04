import sqlite3
from datetime import date, datetime, timedelta

import database_handler as db_handler

con = sqlite3.connect("CrpLand.db")
cur = con.cursor()

#create table score for user
#SQL_STATEMENT = "CREATE TABLE guessing_score (user_id int NOT NULL,score int,last_update date,PRIMARY KEY (user_id));"
#cur.execute(SQL_STATEMENT)

# user_id int NOT NULL
# score int
# last_update date
# PRIMARY KEY (user_id)"

#Create index for table
#SQL_STATEMENT = "CREATE INDEX index_userid_beaten ON beaten_list (user_id);"
#cur.execute(SQL_STATEMENT)


#Insert value into table score
#now=datetime.now()
#date_time=now.strftime("%m/%d/%Y %H:%M:%S")
#SQL_STATEMENT = "INSERT INTO game_score VALUES (1234,1,'"+date_time+"');"
#cur.execute(SQL_STATEMENT)

#Test table score
SQL_STATEMENT="SELECT * FROM beaten_list b INNER JOIN user_info u ON b.user_id=u.user_id WHERE LOWER(u.username)='crp_killer' ORDER BY b.date_beaten ASC"


#SQL_STATEMENT="SELECT user_id,MIN(date_beaten) FROM beaten_list b GROUP BY user_id"
cur.execute(SQL_STATEMENT)
result = cur.fetchall()
print(result)
#field_names = [i[0] for i in cur.description]
#print(field_names)

#Test table score
#SQL_STATEMENT="DELETE FROM guessing_score WHERE user_id=727812978996412497"
#SQL_STATEMENT="DROP TABLE guess_score"
#cur.execute(SQL_STATEMENT)

con.commit()
con.close()


#Check function
#db_handler.addTowerBeatenList("Crp_Killer",[{'badgeId': 2125418287, 'awardedDate': '2022-03-14T17:03:11.4798701Z'}, {'badgeId': 2125418485, 'awardedDate': '2022-10-14T09:45:14.2779187Z'}, {'badgeId': 2125416780, 'awardedDate': '2022-03-14T17:04:11.6697413Z'}])
#result=db_handler.getTotalTowerCompletion()
#esult=db_handler.getTowerBeatenList("Crp_Killer")
#print(result)
#db_handler.feedTowerDifficultyPoint()


"""
{'data': [{'badgeId': 2125418287, 'awardedDate': '2022-03-14T17:03:11.4798701Z'}, {'badgeId': 2125418485, 'awardedDate': '2022-10-14T09:45:14.2779187Z'}, {'badgeId': 2125416780, 'awardedDate': '2022-03-14T17:04:11.6697413Z'}]}
"""