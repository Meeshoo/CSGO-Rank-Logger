import sqlite3
import datetime
import time
# from timeloop import Timeloop
import schedule
from datetime import timedelta
from steam.client import SteamClient
from csgo.client import CSGOClient
from csgo.enums import ECsgoGCMsg
from Config import USERS, DYNAMO_DB
from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute

client = SteamClient()
cs = CSGOClient(client)

# schedule = Timeloop()

class RankModel(Model):
    class Meta:
        table_name = DYNAMO_DB["table"]
        region = DYNAMO_DB["region"]
    username = UnicodeAttribute(hash_key=True)
    rank = UnicodeAttribute()
    date = UnicodeAttribute()

def parseRank(rankData):

    rankList = [
    "Silver 1", 
    "Silver 2", 
    "Silver 3", 
    "Silver 4", 
    "Silver Elite", 
    "Silver Elite Master", 
    "Gold Nova 1", 
    "Gold Nova 2", 
    "Gold Nova 3", 
    "Gold Nova Master", 
    "Master Guardian 1", 
    "Master Guardian 2", 
    "Master Guardian Elite", 
    "Distinguished Master Guardian", 
    "Legendary Eagle", 
    "Legendary Eagle Master", 
    "Supereme Master First Class", 
    "Global Elite"
    ]

    rankDataByLine = rankData.split("\n")
    rankID = int(rankDataByLine[3].split(":")[1].replace(" ", ""))

    if rankID == 0:
        return "Unranked"
    else:
        return rankList[rankID - 1]

@client.on('logged_on')
def start_csgo():
    cs.launch()

# @schedule.job(interval=timedelta(seconds=60))
# @cs.on('ready')
def getAllRanks():

    print("Time is: " + str(datetime.datetime.now().date()))

    # if client.relogin_available: 
    #     client.relogin()
    # else:
    #     client.login()

    for user in USERS:
        username = user[0]
        steamid = user[1]

        cs.request_player_profile(steamid)
        PlayerProfile = cs.wait_event('player_profile')
        print(username + " - " + parseRank(str(PlayerProfile)))

        # databaseEntry = RankModel(username, rank=parseRank(str(PlayerProfile)), date=str(datetime.datetime.now().date()))
        # databaseEntry.save()

    # client.logout()

# schedule.every().day.at("09:00").do(getAllRanks)
# schedule.every(2).minutes.do(getAllRanks)

client.cli_login()

while not cs.ready:
    print(str(cs.ready))
    time.sleep(1)

getAllRanks()

# while True:
#     if datetime.datetime.now():
#         getAllRanks()
#         time.sleep
#     else:
#         time.sleep(30)
