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
    date = UnicodeAttribute(hash_key=True)
    username = UnicodeAttribute()
    rank = UnicodeAttribute()

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
def getAllRanks():

    print("Time is: " + str(datetime.datetime.now()))

    # if client.relogin_available: 
    #     client.relogin()
    # else:
    #     client.login()

    for user in USERS:
        username = user[0]
        steamid = user[1]

        PlayerProfile = cs.request_player_profile(steamid)
        time.sleep(5)
        PlayerProfile = cs.wait_event('player_profile')
        print(username + " - " + parseRank(str(PlayerProfile)))

        # databaseEntry = RankModel(str(datetime.datetime.now().date()), username=username, rank=parseRank(str(PlayerProfile)))
        # databaseEntry.save()

    time.sleep(60)
    # client.logout()


client.cli_login()
# client.run_forever()

time.sleep(10)
print(str(cs.ready))

while True:
    if datetime.datetime.now().hour == 11 and datetime.datetime.now().minute == 38:
        print("Time matched run")
        getAllRanks()
    else:
        print("No match, sleeping")
        time.sleep(30)
