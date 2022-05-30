import cloudscraper
import bs4
import urllib

def get_Rank(username: str) -> str:
   
    try:

        scraper = cloudscraper.create_scraper()

        safeLink = "https://u.gg/lol/profile/na1/" + urllib.parse.quote(username) + "/overview"

        s = scraper.get(safeLink).text

        response_html = bs4.BeautifulSoup(s, features="html.parser")

        d = response_html.find_all("div", {"class":"rank-text"})

        return d[0].findAll("strong")[0].text

    except:
        return ""
    

def rankValue(rank: str) -> int:

    rankValue = 0

    if rank == "Challenger":
        rankValue = 45

    if rank == "Grandmaster":
        rankValue = 42

    if rank == "Master":
        rankValue = 40

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

