import json
import pymongo
import os
from dotenv import load_dotenv

def setup(userid: str, ign: str, rank: str):

    load_dotenv()

    username = os.getenv('MONGO_USER')
    password = os.getenv('MONGO_PASS')

    client = pymongo.MongoClient(f"mongodb+srv://{username}:{password}@inhouseusers.ur0plx1.mongodb.net/?retryWrites=true&w=majority")

    db = client.inhouse
    userdata = db.userdata

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

def incrementWin(winners: list):
    
    with open("users.json", "r") as infile:
        data = json.load(infile)

    for id in winners:
        data[str(id)]["win"] = data[str(id)]["win"] + 1
        data[str(id)]["lp"] = 15 + data[str(id)]["lp"]
    
    with open("users.json", "w") as outfile:
        outfile.write(json.dumps(data, indent=4))
    
    recalculateWL(winners)

def incrementLoss(losers: list):
    
    with open("users.json", "r") as infile:
        data = json.load(infile)

    for id in losers:
        data[str(id)]["loss"] = data[str(id)]["loss"] + 1
        data[str(id)]["lp"] = -10 + data[str(id)]["lp"]

        if(data[str(id)]["lp"] < 0):
            data[str(id)]["lp"] = 0
    
    with open("users.json", "w") as outfile:
        outfile.write(json.dumps(data, indent=4))

    recalculateWL(losers)

def recalculateWL(players: list):

    with open("users.json", "r") as infile:
        data = json.load(infile)

    for id in players:
        data[str(id)]["winrate"] = data[str(id)]["win"]/(data[str(id)]["win"]+data[str(id)]["loss"])
    
    with open("users.json", "w") as outfile:
        outfile.write(json.dumps(data, indent=4))

def getRank(id: int):

    with open("users.json", "r") as infile:
        data = json.load(infile)

    return data[str(id)]["rank"]

def getPlayerData(id: int):

    with open("users.json", "r") as infile:
        data = json.load(infile)

    return data[str(id)]["ign"],data[str(id)]["rank"],data[str(id)]["win"],data[str(id)]["loss"],data[str(id)]["winrate"],data[str(id)]["lp"]