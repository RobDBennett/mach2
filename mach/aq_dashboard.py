from flask import Flask, render_template
from os import getenv
import requests
from flask_sqlalchemy import SQLAlchemy
import openaq
from .models import db, Record
from .openaq import *


def create_app():
    """Create and configure an instance of the Flask application. 
    I am hoping that heroku can fix the database_url like it did yesterday
    with Heroku"""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    @app.route('/')
    def root():
        """Base page. Should pull 20 values in real-time from the API,
        evaluate which are 'dangerous', and return a list of less than 20."""
        opens= []
        for i in range(20):
            api = openaq.OpenAQ()
            status, body = api.measurements(
                city='Los Angeles', parameter='pm25')
            datetime = body['results'][i]['date']['utc']
            value = body['results'][i]['value']
            if value >= 10:
                opens.append([datetime,value])
            else:
                pass
        return render_template("base.html", opens=opens, value=value)

    @app.route('/refresh')
    def refresh():
        """Destroys the existing database, and loads in 100 values for
        Los Angeles to populate a new database."""
        db.drop_all()
        db.create_all()
        for i in range(100):
            api = openaq.OpenAQ()
            status, body = api.measurements(
                city='Los Angeles', parameter='pm25')
            time = body['results'][i]['date']['utc']
            value = body['results'][i]['value']
            record = Record(datetime=time, value=value)
            db.session.add(record)
        db.session.commit()
        return 'Data refreshed!'

    @app.route('/query')
    def query():
        """The homepage pulls data from the API in real time.
        The query page references the database and pulls essentially
        the same information but for a much more robust number."""
        q1 = Record.query.filter(Record.value >= 10).all()
        return render_template("query.html", q1=q1)
    return app
