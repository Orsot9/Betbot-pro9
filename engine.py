import math
import numpy as np
import json

BANKROLL_FILE = "bankroll.json"
MAX_GOALS = 6
KELLY_FRACTION = 0.4

def poisson(lmbda,k):
    return (math.exp(-lmbda) * lmbda**k)/math.factorial(k)

def kelly(p,cote):
    return KELLY_FRACTION*((p*cote-1)/(cote-1))

def monte_carlo(xg_home,xg_away,simulations=5000):
    res=[0,0,0]
    for _ in range(simulations):
        gh=np.random.poisson(xg_home)
        ga=np.random.poisson(xg_away)
        if gh>ga: res[0]+=1
        elif gh==ga: res[1]+=1
        else: res[2]+=1
    return np.array(res)/simulations

def analyse_match(match):
    matrix=np.zeros((MAX_GOALS,MAX_GOALS))
    prob1=probX=prob2=0
    for i in range(MAX_GOALS):
        for j in range(MAX_GOALS):
            matrix[i][j]=poisson(match["xg_home"],i)*poisson(match["xg_away"],j)
            if i>j: prob1+=matrix[i][j]
            elif i==j: probX+=matrix[i][j]
            else: prob2+=matrix[i][j]
    mc=monte_carlo(match["xg_home"],match["xg_away"])
    prob1=(prob1+mc[0])/2
    probX=(probX+mc[1])/2
    prob2=(prob2+mc[2])/2
    values=[]
    for p,cote,label in [(prob1,match["cote1"],"1"),
                         (probX,match["coteX"],"X"),
                         (prob2,match["cote2"],"2")]:
        if p*cote>1.05:
            mise=read_bankroll()*kelly(p,cote)
            values.append({"label":label,"prob":round(p*100,2),"mise":round(mise,2)})
    return values

def read_bankroll():
    with open(BANKROLL_FILE,"r") as f:
        return json.load(f)["bankroll"]

def update_bankroll(mise,gain):
    with open(BANKROLL_FILE,"r") as f:
        data=json.load(f)
    data["bankroll"]=data["bankroll"]-mise+gain
    data["history"].append(data["bankroll"])
    with open(BANKROLL_FILE,"w") as f:
        json.dump(data,f)
