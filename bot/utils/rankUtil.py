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