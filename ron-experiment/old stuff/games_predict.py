#Import Dependencies
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, date
import os
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import ElasticNet
from sklearn.linear_model import Lasso
from sklearn.linear_model import Ridge

## Read in Games, Teams, Matchups datasets
games = pd.read_csv('games.csv')
teams = pd.read_csv('teams.csv')
matchups = pd.read_csv('matchups_early.csv')
matchups.reset_index(drop=True)

# Drop redundant columns
games.drop(['TEAM_ID_home','TEAM_ID_away', 'GAME_STATUS_TEXT', 'GAME_DATE_EST'], axis=1, inplace=True)

# Loop through recent games (matchups_early)
spread_predict = []
record_predict = []
score_predict = []
winner_predict = []

for x in range(len(matchups)):
      
    home = matchups.iloc[x]['Home']
    visitor = matchups.iloc[x]['Visitor']
    game = games

    for i in range(len(teams)):
        if teams.iloc[i]['ABBREVIATION'] == home:
            home_id = teams.iloc[i]['TEAM_ID']

        if teams.iloc[i]['ABBREVIATION'] == visitor:
            visitor_id = teams.iloc[i]['TEAM_ID']

#Narrow games to matched home, visitor teams
    game = game[game['HOME_TEAM_ID'] == home_id]
    game = game[game['VISITOR_TEAM_ID'] == visitor_id]
 
    
#Drop dates, team_ids, game_ids, season - will not be useful
    game.drop(['GAME_ID','HOME_TEAM_ID', 
            'VISITOR_TEAM_ID', 'SEASON'], axis=1)
    game.dropna(inplace=True)
    
#Split Dataset for training, test
    X = game.drop("HOME_TEAM_WINS", axis=1)
    y = game["HOME_TEAM_WINS"]
 
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1, stratify=y)

#Linear Regression 
    model = ElasticNet()

# Fitting our model with all of our features in X
    model.fit(X, y)

    score = model.score(X, y)
    predict = pd.DataFrame({"Prediction": model.predict(X_test), "Actual": y_test}).reset_index(drop=True)
    contribution = pd.DataFrame({"Parameter": list(X.columns), "Weight": model.coef_ }).reset_index(drop=True)

    
# Calculate Predicted Win%
    wins = 0
    for j in range(len(predict)):
        wins = wins + round(predict.iloc[j]['Prediction'])
    record = wins / len(predict)

# Calculate Spread
    home_score = game['PTS_home'].mean()
    visitor_score = game['PTS_away'].mean()
    spread = home_score - visitor_score

# Write to DataFrame
    spread_predict.append(spread)
    record_predict.append(record)
    score_predict.append(score)

## Populate matchups dataframe, write to CSV
matchups['Spread Predict'] = spread_predict
matchups['R-Coefficient'] = score_predict
matchups['Historical Home Win Record'] = record_predict

holder = []
logic = []

for i in range (len(matchups)):
    if matchups.iloc[i]['Historical Home Win Record'] > 0.5:
        holder.append(matchups.iloc[i]['Visitor'])
    else:
        holder.append(matchups.iloc[i]['Home'])
    #Calculate Logic - 1 if correct, 0 if incorrect
    if holder[i] == matchups.iloc[i]['Winner']:
        logic.append(1)
    else:
        logic.append(0)

matchups['Prediction'] = holder
matchups['Logic'] = logic
matchups.to_csv('matchup_output_early.csv')

# output matchups prediction accuracy
print(sum(logic) / len(logic))