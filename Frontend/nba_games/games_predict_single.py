#Import Dependencies
import numpy as np
import pandas as pd
from datetime import datetime, date
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from flask import jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

# Create an engine
engine = create_engine("sqlite:///./db/nba_data2.sqlite")

## Use Pandas to read in games and teams data
# pd.read_sql_table(table_name, con=connection)
# See documentation for more: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_sql_table.html#pandas.read_sql_table
game = pd.read_sql_table("Games", con=engine)
teams = pd.read_sql_table("Teams", con=engine)

# Build a function that will run the prediction model
def prediction_model(home, away):

    #Input Home, Visitor Teams  
    home = home
    visitor = away

    for i in range(len(teams)):
        if teams.iloc[i]['ABBREVIATION'] == home:
            home_id = teams.iloc[i]['TEAM_ID']

        if teams.iloc[i]['ABBREVIATION'] == visitor:
            visitor_id = teams.iloc[i]['TEAM_ID']

    #Filter games to matched home, visitor teams
    games = game[game['HOME_TEAM_ID'] == home_id]
    games = games[games['VISITOR_TEAM_ID'] == visitor_id]
    
    #Drop dates, team_ids, game_ids, season - will not be useful
    games.drop(['GAME_ID','HOME_TEAM_ID', 
                'VISITOR_TEAM_ID'], axis=1)
    # games.dropna(inplace=True)
    
    #Split Dataset for training, test
    y = games["HOME_TEAM_WINS"]
    X = games.drop("HOME_TEAM_WINS", axis=1)
    # X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1, stratify=y)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, train_size=0.8, random_state=1)

    #Calculate Historical Win%
    wins = 0
    for j in range(len(y)):
        wins = wins + round(y.iloc[j])
    record = wins / len(y)    

    #Random Forest Classification
    rf = RandomForestClassifier(n_estimators=128)
    rf = rf.fit(X_train, y_train)
    
    # Fitting our model with all of our features in X
    score = rf.score(X_test, y_test)
    predictor=(rf.predict(X).mean()- 0.5*np.var(rf.predict(X))/record)

    # Calculate Spread
    home_score = games['PTS_home'].mean()
    visitor_score = games['PTS_away'].mean()
    spread = home_score - visitor_score

    # Predict
    if predictor > 0.5:
        if spread >= 3:
            win_predictor = home
        else:
            win_predictor = visitor
    else:
        win_predictor = visitor
            
    #game prediction accuracy
    print(win_predictor, score, spread)
    feature_weights = (sorted(zip(rf.feature_importances_, X.columns), reverse = True))
    
    # Put the prediction, score, spread, and feature weights into a dictionary
    predict_dict = {}
    predict_dict["prediction"] = win_predictor
    predict_dict["score"] = score
    predict_dict["spread"] = spread
    predict_dict["weights"] = feature_weights

    # Return a jsonified version of the dictionary
    return jsonify(predict_dict)
