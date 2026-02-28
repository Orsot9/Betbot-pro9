import math
import numpy as np

BANKROLL = 1000
KELLY_FRACTION = 0.4
MAX_GOALS = 6

def poisson(lmbda, k):
    return (math.exp(-lmbda) * lmbda**k) / math.factorial(k)

def kelly(p, cote):
    return KELLY_FRACTION * ((p*cote-1)/(cote-1))

def monte_carlo(xg_home, xg_away, simulations=5000):
    results=[0,0,0]
    for _ in range(simulations):
        gh=np.random.poisson(xg_home)
        ga=np.random.poisson(xg_away)
        if gh>ga: results[0]+=1
        elif gh==ga: results[1]+=1
        else: results[2]+=1
    return np.array(results)/simulations

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
            mise=BANKROLL*kelly(p,cote)
            values.append({"label":label,"prob":round(p*100,2),"mise":round(mise,2)})
    return values
