# Python script to download advanced stats from internet and store them in a list of teams.

from bs4 import BeautifulSoup
import urllib


def data(url):
    r = urllib.urlopen(url).read()
    return BeautifulSoup(r, "html.parser")


teams = []
names = open("names.csv")
lines = names.readlines()
for line in lines:
    team_names = line.split(",")
    team_names[5] = team_names[5].rstrip()
    teams.append({"name": team_names[0], "kenpom_name": team_names[1], "espn_name": team_names[2],
                  "sagarin_name": team_names[3], "bracket_matrix_name": team_names[4], "poll_name": team_names[5]})
names.close()
soup = data('http://kenpom.com/')
table = soup.tbody.find_all("tr")
for row in table:
    kenpom_name = ""
    pyth = 0.0
    if len(row.select('td')) > 2:
        kenpom_name = row.select('td')[1].select('a')[0].string
        kenpom_name = kenpom_name.replace(';', '')
    if kenpom_name != "":
        if len(row.select("td")) > 4:
            pyth = float(row.select("td")[4].string)
        for team in teams:
            if team["kenpom_name"] == kenpom_name:
                team['pyth'] = pyth
soup = data('http://espn.go.com/mens-college-basketball/bpi')
table = soup.table.find_all("tr")
for row in table:
    espn_name = ""
    if len(row.select('a')) == 1:
        espn_name = row.select('a')[0].string
        espn_name = espn_name.replace(';', '')
    if espn_name != "":
        pva = float(row.select('td')[4].string)
        for team in teams:
            if team["espn_name"] == espn_name:
                team['pva'] = pva
soup = data('http://espn.go.com/mens-college-basketball/rankings/_/year/2016/week/1/seasontype/2')
tables = soup.findAll("table")
ap = tables[0].findAll("tr")
coaches = tables[1].findAll("tr")
for row in ap:
    if len(row.findAll('a')) > 0:
        poll_name = row.findAll('a')[0].string
        if len(row.findAll('td')) > 3:
            preseason_ap = int(row.findAll('td')[3].string.replace(',', ''))
            for team in teams:
                if team["poll_name"] == poll_name:
                    team['preseason_ap'] = preseason_ap
ap = soup.findAll("div", {"class": "foot-content"})[0]
ap = ap.findAll("li")[0].get_text().replace('Others receiving votes: ', '').split(',')
for item in ap:
    item = item.lstrip()
    preseason_ap = int(item[item.rfind(' '):len(item)])
    poll_name = item[0:item.rfind(' ')].replace(';', '')
    for team in teams:
        if team["poll_name"] == poll_name:
            team['preseason_ap'] = preseason_ap
for row in coaches:
    if len(row.findAll('a')) > 0:
        poll_name = row.findAll('a')[0].string
        if len(row.findAll('td')) > 3:
            preseason_coaches = int(row.findAll('td')[3].string.replace(',', ''))
            for team in teams:
                if team["poll_name"] == poll_name:
                    team['preseason_coaches'] = preseason_coaches
coaches = soup.findAll("div", {"class": "foot-content"})[1]
coaches = coaches.findAll("li")[0].get_text().replace('Others receiving votes: ', '').split(',')
for item in coaches:
    item = item.lstrip()
    preseason_coaches = int(item[item.rfind(' '):len(item)])
    poll_name = item[0:item.rfind(' ')].replace(';', '')
    for team in teams:
        if team["poll_name"] == poll_name:
            team['preseason_coaches'] = preseason_coaches
soup = data('http://sagarin.com/sports/cbsend.htm').select("pre")[1].font
table = soup.findAll("font")
for i in range(10, len(table)):
    sag_name = table[i].string
    if sag_name is not None and sag_name.endswith("="):
        sag_name = sag_name.replace("=", '').rstrip()
        sag_name = sag_name.replace(";", '')
        sag_name = sag_name[6:len(sag_name)]
        sag_predictor = float(table[i + 3].string[3:8])
        for team in teams:
            if team["sagarin_name"] == sag_name:
                team['sag_predictor'] = sag_predictor
soup = data('http://www.bracketmatrix.com/')
table = soup.table.find_all("tr")
for row in table:
    seed = row.findAll("td", {"height" : "17", "style" : "height:12.75pt"})
    if len(seed) > 0:
        bracket_matrix_name = seed[0].findAllNext(style=True)[0].string
    if len(seed) > 0 and seed[0].string is not None:
        seed = int(seed[0].string)
    if type(seed) == int:
        for team in teams:
            if team['bracket_matrix_name'] == bracket_matrix_name or team['name'] == bracket_matrix_name:
                team['seed'] = seed
out_file = open("team_data.csv", "wb")
out_file.write("Name,Kenpom,PVA,Sagarin,AP,Coaches,Seed\n")
for team in teams:
    out_file.write(team.get('name','') + "," + str(team.get('pyth','')) + "," + str(team.get('pva','')) + "," + str(team.get('sag_predictor','')) + "," + str(team.get('preseason_ap','')) + "," + str(team.get('preseason_coaches','')) + "," + str(team.get('seed','')) + "\n")
out_file.close()
