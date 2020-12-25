import time
import requests
from bs4 import BeautifulSoup
import sqlite3

months = {
'Dec':'december',
'Nov':'november',
'Oct':'october',
'Sep':'september',
'Aug':'august',
'Jul':'july',
'Jun':'june',
'May':'may',
'Apr':'april',
'Mar':'march',
'Feb':'february',
'Jan':'january'}

daysInWeek = {
'Mon': 'monday',
'Tue': 'tuesday',
'Wed': 'wednesday',
'Thu': 'thursday',
'Fri': 'friday',
'Sat': 'saturday',
'Sun': 'sunday'}

database = 'database/database.db'

# time.asctime().split(" ") - 1El [dayInWeek], 2El - [month], 3El - [day(Number)], 4El - [timeNow], 5El - [year] 
class workWithTime():
    def getDay(self):
        return time.asctime().split(" ")[2]

    def getYear(self):
        return time.asctime().split(" ")[4]

    def getDayInWeek(self):
        return daysInWeek[time.asctime().split(" ")[0]]

    def getMonth(self):
        return months[time.asctime().split(" ")[1]]

    def getTime(self):
        return time.asctime().split(" ")[3]

class news():
    def __init__(self):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()
        self.datatime = workWithTime()  
        self.url = 'https://www.hltv.org/'

    def get_news(self):
        New = False
        names = []
        contents = []
        urls = []
        ID = []
        ID_href = []
        text = ''

        site = requests.get(self.url)
        soup = BeautifulSoup(site.text.encode("utf-8"), 'html.parser')
        news = soup.find_all('div', {"class": "standard-box standard-list"})[0]
        news_id = news.find_all('a', {'class': 'newsline article'})

        for i in news_id:
            ID.append(i.get('href').split("/")[2])

        for i in news_id:
            ID_href.append(f"https://hltv.org{i.get('href')}")

        ID = list(map(int,ID))

        id_posted = []

        with self.connection:
            id_today = list(self.cursor.execute("SELECT news_id FROM `news`"))

        for a in id_today:
            id_posted.append(a[0])

        for i in range(len(ID_href)):
            if ID[i] in id_posted:
                pass
            else:
                New = True
                with self.connection:
                    self.cursor.execute(f"INSERT INTO `news` (`news_id`) VALUES({ID[i]})")
                site = requests.get(ID_href[i])
                soup_2 = BeautifulSoup(site.text.encode("utf-8"), 'html.parser')
                new_news = soup_2.find('article', {"class": "newsitem standard-box"})

                for a in new_news.find('h1', {'class': 'headline'}):
                    names.append(a)

                text = text + new_news.find('p', {'class': 'headertext'}).text
                for a in new_news.find_all('p', {'class': 'news-block'})[0:3]:
                    text = text + a.text + "\n"

                urls.append(f"{ID_href[i]}")
                
                contents.append(f"{text}")

        info = {
			"name": names,
			"content": contents,
			"url": urls }
        return [New, soup.find_all('h2', {'class': 'newsheader'})[0].text, info]

class matches():
    def __init__(self):
        self.datatime = workWithTime()  
        self.url = 'https://www.hltv.org/matches'

    def get_matches(self):
        New = True
        names_teams = []
        names_tournaments = []
        time_matches = []
        view_matches = []
        url_matches = []
        url_analitic = []

        site = requests.get(self.url)
        soup = BeautifulSoup(site.text.encode("utf-8"), 'html.parser')
        matches = soup.find_all('div', {"class": "upcomingMatchesSection"})[0]
        match = matches.find_all('div', {'class': 'upcomingMatch'}) # type = list()

        for i in match:
            time = i.find_all('div', {'class': 'matchTime'})[0].text
            time_matches.append(time)

        for i in match:
            view = i.find_all('div', {'class': 'matchMeta'})[0].text
            view_matches.append(view)

        for i in match:
            teams = f"{i.find_all('div', {'class': 'matchTeamName'})[0].text}|{i.find_all('div', {'class': 'matchTeamName'})[1].text}"
            names_teams.append(teams)

        for i in match:
            tournament = i.find_all('div', {'class': 'matchEventName'})[0].text
            names_tournaments.append(tournament)

        for i in match:
            url = i.find('a', {'class':'match a-reset'})
            url = url.get('href')
            url_matches.append(f"https://hltv.org{str(url)}")

        for i in match:
            url = i.find('a', {'class':'matchAnalytics'})
            url = url.get('href')
            url_analitic.append(f"https://hltv.org{str(url)}")

        info = { 
			"teams": names_teams,
			"tournament": names_tournaments,
            "time": time_matches,
            "view": view_matches,
			"url_match": url_matches,
            "url_analitic": url_analitic}

        return [New, matches.find_all('span', {'class': 'matchDayHeadline'})[0].text, info]

class results():
    datatime = workWithTime()
    def __init__(self):
        self.datatime = workWithTime()
        self.url = 'https://www.hltv.org/results'

    def get_result(self):
        New = True
        names_teams = []
        names_tournaments = []
        scores_matches = []
        view_matches = []
        url_matches = []
        
        site = requests.get(self.url)
        soup = BeautifulSoup(site.text.encode("utf-8"), 'html.parser')
        results = soup.find_all('div', {"class": "results-sublist"})[0]
        div_result = results.find_all('div', {'class': 'result'}) # type = list()

        for i in div_result:
            team_won = i.find_all('div', {'class': 'team-won'})[0].text
            for a in i.find_all('div', {'class': 'team'}):
                if not a.text == team_won:
                    team_lose = a.text
            names_teams.append(f"{team_won}|{team_lose}")

        for i in div_result:
            tournament = i.find_all('span', {'class': 'event-name'})[0].text
            names_tournaments.append(f"{tournament}")
        
        for i in div_result:
            score_won = i.find_all('span', {'class': 'score-won'})[0].text
            score_lose = i.find_all('span', {'class': 'score-lost'})[0].text
            scores_matches.append(f"{score_won} - {score_lose}")

        for i in div_result:
            view_match = i.find_all('div', {'class': 'map-text'})[0].text
            view_matches.append(f"{view_match}")

        for i in results.find_all('a', {"class": "a-reset"}):
            i = i.get('href')
            url_matches.append(f"https://hltv.org"+str(i))
        
        info = {
			"teams": names_teams,
			"tournaments": names_tournaments,
            "scores": scores_matches,
            "view": view_matches,
			"url": url_matches
            }
        return [New, results.find_all('span', {"class": "standard-headline"})[0].text, info]

class updates():
    def __init__(self):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()
        self.datatime = workWithTime()  
        self.url = 'https://blog.counter-strike.net/index.php/category/updates/'

    def get_updates(self):
        New = False
        name = []
        date = []
        content = []
        url = []
        ID = []
        ID_href = []
        
        site = requests.get(self.url)
        soup = BeautifulSoup(site.text.encode("utf-8"), 'html.parser')
        update = soup.find_all('div', {"class": "inner_post"})[0]

        ID.append(update.find('a').get('href').split("/")[6])

        ID_href.append(f"{update.find('a').get('href')}")

        ID = list(map(int,ID))

        id_posted = []

        with self.connection:
            id_posted = list(self.cursor.execute("SELECT id_update FROM `update`"))

        for i in range(len(ID_href)):
            if ID[i] in id_posted:
                pass
            else:
                New = True
                with self.connection:
                    self.cursor.execute(f"INSERT INTO `update` (`id_update`) VALUES({ID[i]})")

                name.append(update.find('a').text)
                site = requests.get(ID_href[0])
                soup = BeautifulSoup(site.text.encode("utf-8"), 'html.parser')
                update = soup.find('div', {"class": "inner_post"})
                date.append(update.find('p', {'class': 'post_date'}).text.split(" ")[0])
                url = ID_href[0]
                all_content = update.find_all('p')[1:]
                for i in range(len(all_content)):
                    content.append(all_content[i].text)

        info = {
			"name": name,
            'date': date,
            'content': content,
            'url': url       
               }
        return [New, info]
