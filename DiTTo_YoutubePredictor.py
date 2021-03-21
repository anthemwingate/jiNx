# Project           : DiTTo Yoututbe Predictor
# Author            : Team DiTTo Stevens Institute of Tecchnology SSW 695A Spring 2021
# Debugger         : Farnaz Sabetpour
# Purpose           : Flask APP to run Youtube Predictor Implementation
# Revision History  : Version 1.0
# Notes:
#
#
#

# Import Data Handling Libraries
from dotenv import load_dotenv
from werkzeug.utils import secure_filename, Request, Response
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


def initiateWebsockets(videoURL):

    youtube_video_request = requests.get(videoURL)
    html_parser = BeautifulSoup(youtube_video_request.text, "html.parser")
    view_count = html_parser.find("div", class_="watch-view-count").text
    # @TODO use decorators for add_video_stats and analyze_transcript
    tones = youtubePredictorDatamanager.add_video_stats(transcript=youtubePredictorDatamanager.analyze_transcript(youtubePredictor_constants.YOUTUBE_FILENAME), url=videoURL, views=view_count)
    return tones


@app.route("/", methods=['GET', 'POST'])
def index():
    form = VideoForm()
    if request.method == 'POST':
        if not form.validate():
            return render_template('youtubePredictor_user.html', form=form)

        videoSource = form.videoSource.data  # @TODOD change feelings to reflectinput of tones from video transcript
        tones = initiateWebsockets(videoSource)
        flash("Video successfully analyzed.")
        # @TODO implement prettytable to output tones
    if request.method == 'GET':
        return render_template('youtubePredictor_user.html', form=form)


@app.route('/youtubePredictor_administrator', methods=['GET', 'POST'])
def admin():
    return render_template('youtubePredictor_administrator.html')


@app.route('/youtubePredictor_videoSubmission', methods=['GET', 'POST'])
def video_submission():
    return render_template('youtubePredictor_videoSubmission.html')

@app.route('/youtubePredictor_importExportDatabase', methods=['GET', 'POST'])
def video_submission():
    return render_template('youtubePredictor_importExportDatabase.html')


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
