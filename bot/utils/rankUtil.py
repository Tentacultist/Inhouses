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
        return 60

    if rank == "Grandmaster":
        return 50

    if rank == "Master":
        return 40

    strSplit = rank.split()

    rankWord = strSplit[0]
    rankNumber = int(strSplit[1])

    if rankWord == "Iron":
        rankValue += 10
    elif rankWord == "Bronze":
        rankValue += 15
    elif rankWord == "Silver":
        rankValue += 20
    elif rankWord == "Gold":
        rankValue += 25
    elif rankWord == "Platinum":
        rankValue += 30
    elif rankWord == "Diamond":
        rankValue += 35

    rankValue = rankValue + (5 - rankNumber)

    return rankValue