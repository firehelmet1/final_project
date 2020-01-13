import os

import pandas as pd
import numpy as np

from datetime import datetime, date
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

# Importing our prediction function
from .games_predict_single import prediction_model

app = Flask(__name__)


#################################################
# Database Setup
#################################################

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db/nba_data2.sqlite"
db = SQLAlchemy(app)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(db.engine, reflect=True)

# Save references to each table
Samples_Metadata = Base.classes.Teams
Samples = Base.classes.Games


@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")


@app.route("/names")
def names():
    """Return a list of sample names."""

    # Use Pandas to perform the sql query
    stmt = db.session.query(Samples_Metadata).statement
    df = pd.read_sql_query(stmt, db.session.bind)

    # Return a list of the column names (sample names)
    # return jsonify(list(df.columns)[5:])
    return jsonify(list(df["NICKNAME"]))



@app.route("/metadata/<NICKNAME>")
def sample_metadata(NICKNAME):
    """Return the MetaData for a given NICKNAME."""
    sel = [
        Samples_Metadata.TEAM_ID,
        Samples_Metadata.CITY,
        Samples_Metadata.ABBREVIATION,
        Samples_Metadata.NICKNAME
    ]

    results = db.session.query(*sel).filter(Samples_Metadata.NICKNAME == NICKNAME).all()

    # Create a dictionary entry for each row of metadata information
    sample_metadata = {}
    for result in results:
        sample_metadata["TEAM_ID"] = result[0]
        sample_metadata["CITY"] = result[1]
        sample_metadata["ABBREVIATION"] = result[2]
        sample_metadata["NICKNAME"] = result[3]

    print(sample_metadata)
    return jsonify(sample_metadata)


# @app.route("/games/<a>/<b>")
# def samples(a, b):

#     """Return the game data."""
#     sample_data = [
#         Samples.GAME_ID,
#         Samples.HOME_TEAM_ID,
#         Samples.VISITOR_TEAM_ID,
#         Samples.PTS_home,
#         Samples.FG_PCT_home,
#         Samples.FT_PCT_home,
#         Samples.FG3_PCT_home,
#         Samples.AST_home,
#         Samples.REB_home,
#         Samples.PTS_away,
#         Samples.FG_PCT_away,
#         Samples.FT_PCT_away,
#         Samples.FG3_PCT_away,
#         Samples.AST_away,
#         Samples.REB_away,
#         Samples.HOME_TEAM_WINS
#     ]
#     # Return the team data
#     sel = [
#         Samples_Metadata.TEAM_ID,
#         Samples_Metadata.ABBREVIATION,
#         Samples_Metadata.NICKNAME,
#         Samples_Metadata.CITY
#     ]

#     # Query the database for the games data
#     results = db.session.query(*sample_data).all()
#     results2 = db.session.query(*sel).all()

#     # Format the data into a Pandas Dataframe
#     game_data = pd.DataFrame()
#     for game_id, home_team_id, visitor_team, pts_home, fg_pct_home, ft_pct_home, fg3_pct_home, ast_home, reb_home,  pts_away, fg_pct_away, ft_pct_away, fg3_pct_away, ast_away, reb_away, home_wins in results:
#         game_data["GAME_ID"] = game_id
#         game_data["HOME_TEAM_ID"] = home_team_id
#         game_data["VISITOR_TEAM_ID"] = visitor_team
#         game_data["PTS_home"] = pts_home
#         game_data["FG_PCT_home"] = fg_pct_home
#         game_data["FT_PCT_home"] = ft_pct_home
#         game_data["FG3_PCT_home"] = fg3_pct_home
#         game_data["AST_home"] = ast_home
#         game_data["REB_home"] = reb_home
#         game_data["PTS_away"] = pts_away
#         game_data["FG_PCT_away"] = fg_pct_away
#         game_data["FT_PCT_away"] = ft_pct_away
#         game_data["FG3_PCT_away"] = fg3_pct_away
#         game_data["AST_away"] = ast_away
#         game_data["REB_away"] = reb_away
#         game_data["HOME_TEAM_WINS"] = home_wins

#     team_data = pd.DataFrame()
#     for team_id, abbreviation, nickname, city in results2:
#         team_data["TEAM_ID"] = team_id
#         team_data["ABBREVIATION"] = abbreviation
#         team_data["NICKNAME"] = nickname
#         team_data["CITY"] = city

#     #Input Home, Visitor Teams  
#     home = a 
#     visitor = b

#     for i in range(len(team_data)):
#         if team_data.iloc[i]['NICKNAME'] == home:
#             home_id = team_data.iloc[i]['TEAM_ID']

#         if team_data.iloc[i]['NICKNAME'] == visitor:
#             visitor_id = team_data.iloc[i]['TEAM_ID']

#     #Filter games to matched home, visitor teams
#     games = game_data[game_data['HOME_TEAM_ID'] == home_id]
#     games = games[games['VISITOR_TEAM_ID'] == visitor_id]
    
#     #Drop dates, team_ids, game_ids, season - will not be useful
#     game_data.drop(['GAME_ID','HOME_TEAM_ID', 
#                 'VISITOR_TEAM_ID'], axis=1)
#     game_data.dropna(inplace=True)
    
#     #Split Dataset for training, test
#     y = game_data["HOME_TEAM_WINS"]
#     X = game_data.drop("HOME_TEAM_WINS", axis=1)
#     X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1, stratify=y)

#     #Calculate Historical Win%
#     wins = 0
#     for j in range(len(y)):
#         wins = wins + round(y.iloc[j])
#     record = wins / len(y)    

#     #Random Forest Classification
#     rf = RandomForestClassifier(n_estimators=128)
#     rf = rf.fit(X_train, y_train)
    
#     # Fitting our model with all of our features in X
#     score = rf.score(X_test, y_test)
#     predictor=(rf.predict(X).mean()- 0.5*np.var(rf.predict(X))/record)

#     # Calculate Spread
#     home_score = game_data['PTS_home'].mean()
#     visitor_score = game_data['PTS_away'].mean()
#     spread = home_score - visitor_score

#     # Predict
#     if predictor >= 0.5:
#         if spread >= 3:
#             win_predictor = home
#         else:
#             win_predictor = visitor
#     else:
#         win_predictor = visitor
            
#     #game prediction accuracy
#     print(win_predictor, score, spread)
#     feature_weights = (sorted(zip(rf.feature_importances_, X.columns), reverse = True))

#     # Put the prediction, score, spread, and feature weights into a dictionary
#     predict_dict = {}
#     predict_dict["prediction"] = win_predictor
#     predict_dict["score"] = score
#     predict_dict["spread"] = spread
#     predict_dict["weights"] = feature_weights

#     # Return a jsonified version of the dictionary
#     return jsonify(predict_dict)
    

    

@app.route("/predictor/<home>/<away>")
def prediction(home, away):
    
    output = prediction_model(home, away)
    print(output)
    return output


if __name__ == "__main__":
    app.run()
