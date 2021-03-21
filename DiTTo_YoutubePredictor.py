# Project                                                  : DiTTo Yoututbe Predictor
# Author                                                   : Team DiTTo Stevens Institute of Tecchnology SSW 695A Spring 2021
# Architect/Core Implementation                            : Anthem Rukiya J. Wingate
# Architect/Production Design                              : Hanqing Liu
# Version Control Management and Quality Assurance Tester  : Farnaz Sabetpour
# Purpose                                                  : Flask APP to run Youtube Predictor Implementation
# Revision History                                         : Version 1.0

# Notes:
#
#
#

# Import Data Handling Libraries
import math
from dotenv import load_dotenv
from werkzeug.utils import secure_filename, Request, Response
from prettytable import PrettyTable
import os
from __future__ import unicode_literals
import logging
from flask import Flask, jsonify, render_template, request, flash, redirect, url_for, make_response, send_from_directory
from flask_cors import CORS
from bs4 import BeautifulSoup
import requests

# Import DiTTo_YoutubePredictor Utilities
from youtubePredictor_forms import VideoForm
from youtubePredictor_dataManager import DataManager
import youtubePredictor_constants

app = Flask(__name__)
app.secret_key = 'development key'
port = int(os.getenv('PORT', 8080))
logging.basicConfig(level=logging.DEBUG)
CORS(app)

UPLOAD_FOLDER = 'save/'
ALLOWED_EXTENSIONS = set(['csv'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def initiate_websockets(videoURL):
    youtube_video_request = requests.get(videoURL)
    html_parser = BeautifulSoup(youtube_video_request.text, "html.parser")
    view_count = int(html_parser.find("div", class_="watch-view-count").text)
    # @TODO use decorators for add_video_stats and analyze_transcript
    record = youtubePredictorDatamanager.add_video_stats(
        transcript=youtubePredictorDatamanager.analyze_transcript(youtubePredictor_constants.YOUTUBE_FILENAME),
        url=videoURL, views=view_count)
    return record


@app.route("/", methods=['GET', 'POST'])
def index():
    form = VideoForm()
    if request.method == 'POST':
        if not form.validate():
            return render_template('youtubePredictor_user.html', form=form)

        video_source = form.videoSource.data
        record = initiate_websockets(video_source)
        flash("Video successfully analyzed.")
        record_table = PrettyTable()
        record_table.field_names = youtubePredictorDatamanager.get_column_headers()
        record_table.add_row(record)
        print(record_table)
        return render_template('youtubePredictor_submissionSuccess.html', video_source=video_source, record=record)

    if request.method == 'GET':
        return render_template('youtubePredictor_user.html', form=form)


@app.route('/youtubePredictor_administrator', methods=['GET', 'POST'])
def admin():
    return render_template('youtubePredictor_administrator.html')


@app.route('/youtubePredictor_data', methods=['GET', 'POST'])
@app.route('/youtubePredictor_data/', methods=['GET', 'POST'], defaults={'page': 1})
@app.route('/youtubePredictor_data/<int:page>', methods=['GET', 'POST'])
def data5(page):
    data = youtubePredictorDatamanager.get_all_records_from_database()
    length = len(data)
    if request.method == 'POST':
        if "submit" in request.form:
            return update(page)
    if length == 0:
        flash("Please initialize database in order to view records.")
        return redirect(url_for('youtubePredictor_administrator'))
    prv = page - 1
    nxt = page + 1
    if page == 1:
        prv = int(math.ceil(length / 25.0))
    if math.ceil(length / 25.0) == page:
        nxt = 1
    data = data[(page - 1) * 25:page * 25]
    return render_template('youtubePredictor_data.html', data=data, len=len(data), nxt=nxt, prv=prv, page=page)


@app.route('/youtubePredictor_data/youtubePredictor_updateDatabase', methods=['GET', 'POST'])
def update():
    if "save" in request.form:
        if request.form['save'] == "Delete Record":
            youtubePredictorDatamanager.delete_record_from_database(request.form["id"])
        else:
            i = int(request.form["id"])
            item = youtubePredictorDatamanager.get_record_from_database(i)
            val = request.form['new_record']
            if val != str(item[1]):
                youtubePredictorDatamanager.update_record_in_database(val, i)
        return redirect(url_for('data5'))
    x = request.form['submit']
    item = youtubePredictorDatamanager.get_record_from_database(int(x))
    return render_template('youtubePredictor_updateDatabase.html', item=item, len=len(item))


@app.route('/youtubePredictor_save', methods=['GET', 'POST'])
def import_export():
    if request.method == 'POST':
        if request.form["submit"] == "Export":
            youtubePredictorDatamanager.get_all_records_from_database()
            return render_template("youtubePredictor_data.html")
        if 'file' not in request.files:
            return render_template('youtubePredictor_batch.html')
        file = request.files['file']
        if file.filename == '':
            flash('Please select a file.')
        if file and not allowed_file(file.filename):
            flash('Only .csv files can be imported.')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash(youtubePredictorDatamanager.import_data_from_file("save/" + filename))
            os.remove("save/" + filename)
            return redirect(url_for('youtubePredictor_administrator'))

    return render_template('youtubePredictor_batch.html')


@app.route('/youtubePredictor_exportDatabase', methods=['GET', 'POST'])
def export_data():
    youtubePredictorDatamanager.get_all_records_from_database()
    uploads = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
    return send_from_directory(directory=uploads, filename="trainingData.csv")


@app.route('/youtubePredictor_emptyDatabase', methods=['GET', 'POST'])
def empty_database():
    if request.method == 'POST':
        if request.form["submit"] == "Yes":
            youtubePredictorDatamanager.remove_all_data_from_database()
            flash("All data has been removed from the database.")
            return redirect(url_for('youtubePredictor_administrator'))
        else:
            return redirect(url_for('youtubePredictor_administrator'))
    return render_template('youtubePredictor_emptyDatabase.html')


if __name__ == '__main__':
    load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))
    youtubePredictorDatamanager = DataManager(
        os.environ.get('SPEECH_TO_TEXT_API_KEY'),
        os.environ.get('SPEECH_TO_TEXT_ENDPOINT_URL'),
        os.environ.get('TONE_ANALYZER_API_KEY'),
        os.environ.get('TONE_ANALYZER_ENDPOINT_URL'),
        os.environ.get('NATURAL_LANGUAGE_UNDERSTANDING_API_KEY'),
        os.environ.get('NATURAL_LANGUAGE_UNDERSTANDING_ENDPOINT_URL'),
        os.environ.get('ALCHEMY_API_KEY'),
        os.environ.get('POSTGRESQL_USERNAME'),
        os.environ.get('POSTGRESQL_PASSWORD'),
        os.environ.get('POSTGRESQL_HOST'),
        os.environ.get('POSTGRESQL_DBNAME'),
        os.environ.get('POSTGRESQL_PORT'), )

    youtubePredictorDatamanager.init()
    app.run(host='0.0.0.0', port=port, debug=True)
