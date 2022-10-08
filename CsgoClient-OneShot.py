import datetime
import time
from steam.client import SteamClient
from csgo.client import CSGOClient
from csgo.enums import ECsgoGCMsg
from Config import USERS, DYNAMO_DB
from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, UTCDateTimeAttribute

client = SteamClient()
cs = CSGOClient(client)

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

@cs.on('ready')
def getAllRanks():

    for user in USERS:
        username = user[0]
        steamid = user[1]

        cs.request_player_profile(steamid)
        PlayerProfile = cs.wait_event('player_profile')
        print(username + " - " + parseRank(str(PlayerProfile)))

        time.sleep(5)

        databaseEntry = RankModel(str(datetime.datetime.now().date()), username=username, rank=parseRank(str(PlayerProfile)))
        databaseEntry.save()

    exit()

client.cli_login()
client.run_forever()
