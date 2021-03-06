import json
import pymongo
import os
from dotenv import load_dotenv

def setup(userid: str, ign: str, rank: str, userdata):

    # if the user is not in the database
    if userdata.find_one({"userid":userid}) == None:

        newUser = {
                    "userid": userid,
                    "ign": ign,
                    "rank": rank,
                    "win": 0,
                    "loss": 0,
                    "winrate": 0,
                    "lp": 0
                
                }
        
        userdata.insert_one(newUser)
        
    else:
        
        filter = {"userid":userid}

        newValues = { "$set": {"ign":ign,
                               "rank":rank} }

        userdata.update_one(filter, newValues)

def incrementWin(winners: list, userdata):
    
    for winnerid in winners:

        winner = str(winnerid)

        filter = {"userid":winner}

        newWin = userdata.find_one({"userid":winner})["win"] + 1 
        newWinRate = newWin/(newWin + userdata.find_one({"userid":winner})["loss"])
        newLp = userdata.find_one({"userid":winner})["lp"] + 15

        newValues = { "$set": {"win": newWin,
                                "winrate": newWinRate ,
                                "lp": newLp } }

        userdata.update_one(filter, newValues)

def incrementLoss(losers: list, userdata):
    
    for loserid in losers:

        loser = str(loserid)

        filter = {"userid":loser}

        newLoss = userdata.find_one({"userid":loser})["loss"] + 1 
        newWinRate = userdata.find_one({"userid":loser})["win"]/(userdata.find_one({"userid":loser})["win"] + newLoss)

        newLp = userdata.find_one({"userid":loser})["lp"] - 10

        if newLp < 0:
            newLp = 0

        newValues = { "$set": {"loss": newLoss,
                                "winrate": newWinRate ,
                                "lp": newLp } }

        userdata.update_one(filter, newValues)