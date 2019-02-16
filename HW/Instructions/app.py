import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
from flask import Flask, jsonify



def get_session_and_tables():
    engine = create_engine("sqlite:///Resources/hawaii.sqlite")
    Base = automap_base()
    Base.prepare(engine, reflect=True)
    Measurement = Base.classes.measurement
    Station = Base.classes.station
    session = Session(engine)
    return (session, Measurement, Station)
app = Flask(__name__)


# last_day_string = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
# end_date = str(last_day_string)[2:-3]
# start_date = str(eval(end_date[0:4])-1)+ end_date[4:]
# last_12_month_prcp = session.query(Measurement.date, Measurement.prcp).\
#     filter(Measurement.date > start_date).\
#     order_by(Measurement.date).all()



@app.route("/")
def home():
    return "Hello, Welcome to weather forecast"


@app.route("/api/v1.0/precipitation")
def precipitation():
   # connection to the db, session, tables
    session, Measurement, Station = get_session_and_tables()
    """Return Dates and Temp from the last year."""
    precip_analysis = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= "2016-08-23").\
    filter(Measurement.date <= "2017-08-23").all()
    # creates JSONified list
    precipitation_list = [precip_analysis]
    return jsonify(precipitation_list)



@app.route("/api/v1.0/stations")
def stations():
    session, Measurement, Station = get_session_and_tables()
    station_list = session.query(Station.station).\
    order_by(Station.station).all()
    return jsonify(station_list)


@app.route("/api/v1.0/tobs")
def tobs():
    session, Measurement, Station = get_session_and_tables()
    tobs_results = session.query(Measurement.tobs).\
    order_by(Measurement.date).all()
    return jsonify(tobs_results)


@app.route('/api/v1.0/<start>')
def combined_start_stat(start):
    session, Measurement, Station = get_session_and_tables()

    last_day_string = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    end_date = str(last_day_string)[2:-3]
    start_date = str(eval(end_date[0:4])-1)+ end_date[4:]

    last_12_month_prcp = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date > start_date).\
    order_by(Measurement.date).all()


    q =  session.query(Station.id,Station.station,func.avg(Measurement.tobs),
    func.min(Measurement.tobs),
    func.max(Measurement.tobs)).\
    filter (Measurement.station == Station.station).\
    filter (Measurement.date >= start_date).all()

    return jsonify(q)



@app.route('/api/v1.0/<start>/<end>')
def combined_start_end_stat(start,end):
    session, Measurement, Station = get_session_and_tables()
   
    last_day_string = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    end_date = str(last_day_string)[2:-3]
    start_date = str(eval(end_date[0:4])-1)+ end_date[4:]

    last_12_month_prcp = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date > start_date).\
    order_by(Measurement.date).all()
  
    q =  session.query(Station.id,Station.station,func.avg(Measurement.tobs),
    func.min(Measurement.tobs),
    func.max(Measurement.tobs)).\
    filter (Measurement.station == Station.station).\
    filter (Measurement.date <= end_date).\
    filter (Measurement.date >= start_date).all()

    return jsonify(q)

if __name__ == "__main__":
    app.run(debug=True)