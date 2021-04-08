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
#

# Import Data Handling Libraries
from flask import Flask, render_template, request, flash, redirect, session, url_for, g, jsonify, make_response

# Import DiTTo_YoutubePredictor Utilities
from youtubePredictor.youtubePredictor_frontend.youtubePredictor_databaseBuilder_app import DataBuilder
from youtubePredictor.youtubePredictor_frontend.youtubePredictor_form import VideoForm

# App config.
DEBUG = True
app = Flask(__name__)
app.secret_key = 'development key'
app.config.from_object(__name__)
# test_url = https://www.youtube.com/watch?v=ojhTu9aAa_Y&t=8s

@app.route("/", methods=['GET', 'POST'])
def submission():
    form = VideoForm()
    if request.method == 'POST':
        if not form.validate():
            flash('A youtube url is required to run analysis.')

    return render_template('youtubePredictor_videoSubmission.html', form=form)


@app.route("/handle_url_sub", methods=['GET', 'POST'])
def handle_url_sub():
    video_source = request.form['video_source']
    data_bldr.urls.append(video_source)
    data_bldr.get_video_info()
    data_bldr.api_manager()
    flash('Analyzing')


@app.route("/analysis", methods=['GET', 'POST'])
def analysis():
    return render_template('youtubePredictor_videoAnalysis.html', results=data_bldr.display_results())


if __name__ == "__main__":
    data_bldr = DataBuilder()
    app.run()
