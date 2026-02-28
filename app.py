from flask import Flask, render_template, jsonify
from engine import analyse_match
import requests

app = Flask(__name__)

TOKEN = "TON_TOKEN"
CHAT_ID = "TON_CHAT_ID"
API_KEY = "TON_API_KEY"

LEAGUES = [
    "soccer_epl",
    "soccer_spain_la_liga",
    "soccer_france_ligue_one",
    "soccer_italy_serie_a"
]

def send_telegram(msg):
    url=f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url,data={"chat_id":CHAT_ID,"text":msg})

def get_live_matches():
    matches=[]
    for league in LEAGUES:
        url=f"https://api.the-odds-api.com/v4/sports/{league}/odds/?apiKey={API_KEY}&regions=eu&markets=h2h"
        res=requests.get(url).json()
        for m in res:
            try:
                matches.append({
                    "home": m["home_team"],
                    "away": m["away_team"],
                    "xg_home": 1.7,
                    "xg_away": 1.3,
                    "cote1": m["bookmakers"][0]["markets"][0]["outcomes"][0]["price"],
                    "coteX": m["bookmakers"][0]["markets"][0]["outcomes"][1]["price"],
                    "cote2": m["bookmakers"][0]["markets"][0]["outcomes"][2]["price"]
                })
            except:
                continue
    return matches

@app.route("/")
def home():
    return render_template("dashboard.html")

@app.route("/data")
def data():
    matches = get_live_matches()
    results=[]
    for m in matches:
        values=analyse_match(m)
        if values:
            for v in values:
                msg=f"🔥 VALUE {m['home']} vs {m['away']} | {v['label']} | Mise {v['mise']}€"
                send_telegram(msg)
            results.append({"match":f"{m['home']} vs {m['away']}","values":values})
    return jsonify(results)

if __name__=="__main__":
    app.run()
