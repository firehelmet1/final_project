import os

import pandas as pd
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

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


@app.route("/games")
def samples():
    """Return the game data."""
    sample_data = [
        Samples.GAME_ID,
        Samples.HOME_TEAM_ID,
        Samples.VISITOR_TEAM_ID,
        Samples.PTS_home,
        Samples.FG_PCT_home,
        Samples.FT_PCT_home,
        Samples.FG3_PCT_home,
        Samples.AST_home,
        Samples.REB_home,
        Samples.PTS_away,
        Samples.FG_PCT_away,
        Samples.FT_PCT_away,
        Samples.FG3_PCT_away,
        Samples.AST_away,
        Samples.REB_away,
        Samples.HOME_TEAM_WINS
    ]

    # Query the database for the games data
    results = db.session.query(*sample_data).all()

    # Format the data to send as json
    game_data = []
    home_team = {}
    for game_id, home_team_id, visitor_team, pts_home, fg_pct_home, ft_pct_home, fg3_pct_home, ast_home, reb_home,  pts_away, fg_pct_away, ft_pct_away, fg3_pct_away, ast_away, reb_away, home_wins in results:
        home_team["GAME_ID"] = game_id
        home_team["HOME_TEAM_ID"] = home_team_id
        home_team["VISITOR_TEAM_ID"] = visitor_team
        home_team["PTS_home"] = pts_home
        home_team["FG_PCT_home"] = fg_pct_home
        home_team["FT_PCT_home"] = ft_pct_home
        home_team["FG3_PCT_home"] = fg3_pct_home
        home_team["AST_home"] = ast_home
        home_team["REB_home"] = reb_home
        home_team["PTS_away"] = pts_away
        home_team["FG_PCT_away"] = fg_pct_away
        home_team["FT_PCT_away"] = ft_pct_away
        home_team["FG3_PCT_away"] = fg3_pct_away
        home_team["AST_away"] = ast_away
        home_team["REB_away"] = reb_away
        home_team["HOME_TEAM_WINS"] = home_wins
        game_data.append(home_team)
    print(f'......>>>>>>>>>>>>>>>>.......This is the home team: {home_team}')
    return jsonify(game_data)


if __name__ == "__main__":
    app.run()
