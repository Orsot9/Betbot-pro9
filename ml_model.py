import pandas as pd
from xgboost import XGBRegressor
from sklearn.preprocessing import StandardScaler
import joblib

def train_xg_model():
    df = pd.read_csv("data/championnat.csv")
    X = df[["FTHG","FTAG"]]
    y_home = df["xG_Home"]
    y_away = df["xG_Away"]
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    model_home = XGBRegressor()
    model_away = XGBRegressor()
    model_home.fit(X_scaled,y_home)
    model_away.fit(X_scaled,y_away)
    joblib.dump((model_home,model_away,scaler),"xg_model.pkl")

def predict_xg(fthg,ftag):
    import joblib
    model_home,model_away,scaler = joblib.load("xg_model.pkl")
    X_scaled = scaler.transform([[fthg,ftag]])
    return model_home.predict(X_scaled)[0], model_away.predict(X_scaled)[0]
