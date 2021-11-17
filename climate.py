import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session, session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# create engine to hawaii.sqlite
engine = create_engine("sqlite:///hawaii.sqlite")

# set up the Database#
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

print(Base.classes.keys())

# Flask#

app =  Flask(__name__)

#Flask Route#

@app.route("/")
def Home():
    return (
        "Available Routes:<br/>"
        "/api/v1.0/precipitation<br>"
        "/api/v1.0/stations<br>"
        "/api/v1.0/tobs"
    )

 #Convert the query results to a dictionary using `date` as the key and `prcp` as the value#

 @app.route("/api/v1.0/precipitation")
def prcp():

      session = Session(engine)   
      #Calculate the date one year from the last date in data set
      prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)    

      results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date>=prev_year).all()
      Session.close()

      precip = {date: prcp for date, prcp in results}
      return jsonify(precip)

#JSON list of stations from the dataset#
@app.route("/api/v1.0/stations")
def stations():
    
       #list of stations."""#
    session = Session(engine)
    results = session.query(Station.station).all()

    session.close()

    stations = list(np.ravel(results))
    return jsonify(stations=stations)


#Query the dates and temperature observations of the most active station for the last year of data.

app.route("/api/v1.0/tobs")
def temp():

    # the date 1 year ago from last date in database#

    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)   

    last_year = session.query(Measurement.tobs).\
       filter(Measurement.station == 'USC00519281').\
       filter(Measurement.date>=prev_year).all()

    session.close() 
    # coverting result to a list#
    temps = list(np.ravel(last_year))
    
    return jsonify(temps=temps)


if __name__ == '__main__':
    app.run()
