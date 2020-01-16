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

# import logging
# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
# logging.debug('This is a log message.')

# Importing our prediction function
# import nba_games.games_predict_single
from nba_games.games_predict_single import prediction_model


app = Flask(__name__)

#################################################
# Database Setup
#################################################

# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///./db/nba_data2.sqlite"
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', '') or "sqlite:///nba_data2.sqlite"

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

@app.route("/predictor/<home>/<away>")
def prediction(home, away):
    
    output = prediction_model(home, away)
    print(output)
    return output


if __name__ == "__main__":
    app.run()
