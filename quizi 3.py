import requests
import json
import sqlite3

url = "https://api-football-beta.p.rapidapi.com/players/topscorers"
querystring = {"season": "2019", "league": '78'}
headers = {
    'x-rapidapi-key': "216fb76abbmsh1d9181870c82430p1b28b5jsn0eb9ad8b39a6",
    'x-rapidapi-host': "api-football-beta.p.rapidapi.com"
}
# კითხვა 1
# response = requests.get(url, headers=headers, params=querystring)
response = requests.request("GET", url, headers=headers, params=querystring)
# print(response)
# print(response.status_code)
# print(response.headers)

# კითხვა 2
with open('data.json', 'w') as file:
    json.dump(response.json(), file, indent=4)

# კითხვა 3
res = json.loads(response.text)
top_scorer = res["response"][0]["player"]["lastname"]
goals = res["response"][0]["statistics"][0]["goals"]["total"]
print("ბუნდესლიგის 2019-20 წლების სეზონში " + str(top_scorer) + " -იმ გაიტანა " + str(goals) + " გოლი")

# კითხვა 4, ცხრილში ინახება გერმანიის ლიგაში მოთამაშე ფეხბურთელების შესახებ მონაცემები
conn = sqlite3.connect('player_statistics.sqlite')
c = conn.cursor()
c.execute('''CREATE TABLE if not exists statistic
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
            players VARCHAR (20),
            nationality VARCHAR (32),
            appearances INT,
            shots INT,
            goals INT);''')

all_rows = []
i = 0
for each in res["response"]:
    players = res["response"][i]["player"]["lastname"]
    nationality = res["response"][i]["player"]["nationality"]
    appearances = res["response"][i]["statistics"][0]["games"]["appearences"]
    shots = res["response"][i]["statistics"][0]["shots"]["total"]
    goals = res["response"][i]["statistics"][0]["goals"]["total"]
    i += 1
    row = (players, nationality, appearances, shots, goals)
    all_rows.append(row)
c.executemany('INSERT INTO statistic (players, nationality, appearances, shots, goals) VALUES (?, ?, ?, ?, ?)', all_rows)
conn.commit()
conn.close()