import bs4
import urllib
import requests
import os
from dotenv import load_dotenv

load_dotenv()

def get_Rank(username: str) -> str:

    rank_number = {
        "I": "1",
        "II": "2",
        "III": "3",
        "IV": "4"
    }

    API_KEY = os.environ.get("API_KEY")
    SUMMONER_API = f"https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{username}?api_key={API_KEY}"

    response = requests.get(f"{SUMMONER_API}")
    if response.status_code == 200:
        summoner_json = response.json()
        SUMMONER_ID = summoner_json["id"]
        RANKED_API = f"https://na1.api.riotgames.com/lol/league/v4/entries/by-summoner/{SUMMONER_ID}?api_key={API_KEY}"

        ranked_response = requests.get(f"{RANKED_API}")
        if ranked_response.status_code == 200:
            ranked_json = ranked_response.json()

            TIER = "Unranked"
            RANK = ""

            for entry in ranked_json:
                if entry["queueType"] == "RANKED_SOLO_5x5":
                    TIER = entry["tier"].lower().capitalize()
                    RANK = rank_number[entry["rank"]]
                    break;

            return f"{TIER} {RANK}"
        else:
            return ""
    else:
        return ""

def rankValue(rank: str) -> int:

    rankValue = 0

    if rank == "Challenger":
        rankValue = 45
        return rankValue

    if rank == "Grandmaster":
        rankValue = 42
        return rankValue

    if rank == "Master":
        rankValue = 40
        return rankValue

    if rank == "Unranked":
        rankValue = 1
        return rankValue
        
    strSplit = rank.split()

    rankWord = strSplit[0]
    rankNumber = int(strSplit[1])

    if rankWord == "Iron":
        rankValue = 5

    elif rankWord == "Bronze":
        rankValue = 10

    elif rankWord == "Silver":
        if rankNumber == 1 or rankNumber == 2:
            rankValue = 16
        if rankNumber == 3 or rankNumber == 4:
            rankValue = 15

    elif rankWord == "Gold":
        if rankNumber == 1:
            rankValue =  20
        if rankNumber == 2:
            rankValue = 19
        if rankNumber == 3:
            rankValue = 18
        if rankNumber == 4:
            rankValue = 17

    elif rankWord == "Platinum":
        if rankNumber == 1:
            rankValue = 27
        if rankNumber == 2:
            rankValue = 26
        if rankNumber == 3:
            rankValue = 23
        if rankNumber == 4:
            rankValue = 21

    elif rankWord == "Diamond":
        if rankNumber == 1:
            rankValue = 36
        if rankNumber == 2:
            rankValue = 34
        if rankNumber == 3:
            rankValue = 31
        if rankNumber == 4:
            rankValue = 29
            
    return rankValue