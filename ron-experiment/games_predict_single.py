#Import Dependencies
import numpy as np
import pandas as pd
from datetime import datetime, date
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

## Read in Games, Teams, Matchups datasets
game = pd.read_csv('games.csv')
teams = pd.read_csv('teams.csv')

# Drop redundant columns
game.drop(['TEAM_ID_home','TEAM_ID_away', 'GAME_STATUS_TEXT', 'GAME_DATE_EST'], axis=1, inplace=True)
game.drop_duplicates()

#Input Home, Visitor Teams  
home = input("Enter Home Team Abbreviation: ") 
visitor = input("Enter Visitor Team Abbreviation: ")

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
y = game["HOME_TEAM_WINS"]
X = game.drop("HOME_TEAM_WINS", axis=1)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1, stratify=y)

#Calculate Historical Win%
wins = 0
for j in range(len(y)):
    wins = wins + round(y.iloc[j])
record = wins / len(y)    

#Random Forest Classification
rf = RandomForestClassifier(n_estimators=128)
rf = rf.fit(X_train, y_train)
    
# Fitting our model with all of our features in X
score = rf.score(X, y)
predictor=(rf.predict(X).mean()- 0.5*np.var(rf.predict(X))/record)

# Calculate Spread
home_score = game['PTS_home'].mean()
visitor_score = game['PTS_away'].mean()
spread = home_score - visitor_score

# Predict
if predictor >= 0.5:
    if spread >= 3:
        win_predictor = home
    else:
        win_predictor = visitor
else:
    win_predictor = visitor
            
#game prediction accuracy
print(win_predictor, score, spread)
feature_weights = (sorted(zip(rf.feature_importances_, X.columns), reverse = True))
