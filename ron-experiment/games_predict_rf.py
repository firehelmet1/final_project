#Import Dependencies
import numpy as np
import pandas as pd
from datetime import datetime, date
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

## Read in Games, Teams, Matchups datasets
games = pd.read_csv('games.csv')
teams = pd.read_csv('teams.csv')
matchups = pd.read_csv('matchups_early.csv')
matchups.reset_index(drop=True).head(2)

# Drop redundant columns
games.drop(['TEAM_ID_home','TEAM_ID_away', 'GAME_STATUS_TEXT', 'GAME_DATE_EST'], axis=1, inplace=True)
games.drop_duplicates()

# Loop through recent games (matchups_early)
spread_predict = []
record_predict = []
score_predict = []
winner_predict = []
hscore = []
vscore = []
rf_predictor = []
predictor = []

for x in range(len(matchups)):
      
    home = matchups.iloc[x]['Home']
    visitor = matchups.iloc[x]['Visitor']
    game = games

    for i in range(len(teams)):
        if teams.iloc[i]['ABBREVIATION'] == home:
            home_id = teams.iloc[i]['TEAM_ID']

        if teams.iloc[i]['ABBREVIATION'] == visitor:
            visitor_id = teams.iloc[i]['TEAM_ID']

#Filter games to matched home, visitor teams
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

#Calculate Historical Win%
    wins = 0
    for j in range(len(y)):
        wins = wins + round(y.iloc[j])
    record = wins / len(y)    

#Random Forest Classification
    rf = RandomForestClassifier(n_estimators=200)
    rf = rf.fit(X_train, y_train)
    
# Fitting our model with all of our features in X
    score = rf.score(X, y)
    predictor.append(rf.predict(X).mean()- 0.5*np.var(rf.predict(X))/record)

# Calculate Spread
    home_score = game['PTS_home'].mean()
    visitor_score = game['PTS_away'].mean()
    spread = home_score - visitor_score

# Append Scoring Lists
    spread_predict.append(spread)
    record_predict.append(record)
    score_predict.append(score)
    hscore.append(home_score)
    vscore.append(visitor_score)

# Populate Dataframe, write to CSV Output
matchups['Home_Score'] = hscore
matchups['Visitor_Score'] = vscore
matchups['R-Coefficient'] = score_predict
matchups['Historical Home Win Record'] = record_predict

win_predictor = []
win_logic = []

for i in range (len(matchups)):
    if predictor[i] > 0.5:
        win_predictor.append(matchups.iloc[i]['Home'])
    else:
        win_predictor.append(matchups.iloc[i]['Visitor'])
            
#Calculate Logic - 1 if correct, 0 if incorrect
    if win_predictor[i] == matchups.iloc[i]['Winner']:
        win_logic.append(1)
    else:
        win_logic.append(0)

matchups['Prediction'] = win_predictor
matchups['Logic'] = win_logic
matchups.to_csv('matchup_output_early.csv')

#matchups prediction accuracy
print((sum(win_logic) / len(win_logic)), sum(score_predict)/len(score_predict))