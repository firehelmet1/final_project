#Import dependencies
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, date
import os
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

## Read in Games and Game Details datasets
games = pd.read_csv('nba-games/games.csv')
game_details = pd.read_csv('nba-games/games_details.csv')
teams = pd.read_csv('nba-games/teams.csv')
teams.reset_index(drop=True)

## Merge game dataframes, drop rows with NAN values in OREB, PLUS_MINUS columns
games_df = pd.merge(games, game_details, on='GAME_ID', how='inner') 
games_df = games_df.dropna(how='any', subset=['OREB', 'PLUS_MINUS'])
games_df.drop(['GAME_DATE_EST','TEAM_ABBREVIATION','TEAM_CITY', 'PLAYER_NAME','START_POSITION', 'MIN'], axis=1, inplace=True)

# games dataframe - drop columns, change game_date_est to datetime format
games.drop(['TEAM_ID_home','TEAM_ID_away', 'GAME_STATUS_TEXT'], axis=1, inplace=True)
games['GAME_DATE_EST'] = (pd.to_datetime(games['GAME_DATE_EST']))

# Match Team Abbreviation to Team ID
home = input("Enter Home Team Abbreviation: ") 
visitor = input("Enter Visitor Team Abbreviation: ")

for i in range(len(teams)):
    if teams.iloc[i]['ABBREVIATION'] == home:
        home_id = teams.iloc[i]['TEAM_ID']
    if teams.iloc[i]['ABBREVIATION'] == visitor:
        visitor_id = teams.iloc[i]['TEAM_ID']

## Drop Rows to only teams specified as home, visitor
#games = games[games['GAME_DATE_EST'] <=game_date]
games = games[games['HOME_TEAM_ID'] == home_id]
games = games[games['VISITOR_TEAM_ID'] == visitor_id]

#Drop additional columns in games dataframe
games.drop(['GAME_DATE_EST','GAME_ID','HOME_TEAM_ID', 
            'VISITOR_TEAM_ID', 'SEASON'], axis=1, inplace=True)
games.dropna(inplace=True)

#Assign X and y dataframes
X = games.drop("HOME_TEAM_WINS", axis=1)
y = games["HOME_TEAM_WINS"]

#Use SciKitLearn to Split into Train / Test datasets
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1, stratify=y)

#SciKitLearn - Linear Regression
model = LinearRegression()

# Fitting our model with all of our features in X
model.fit(X, y)

score = model.score(X, y)
print(f"R2 Score: {score}")
predict = pd.DataFrame({"Prediction": model.predict(X_test), "Actual": y_test}).reset_index(drop=True)
contribution = pd.DataFrame({"Parameter": list(X.columns), "Weight": model.coef_ }).reset_index(drop=True)

#Output train / test prediction accuracy, contribution factors, sorted descending
predict
print(contribution.sort_values(by='Weight', ascending=False))