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
from flask import Flask, render_template, request, flash, redirect, url_for, send_from_directory

# Import DiTTo_YoutubePredictor Utilities
from youtubePredictor.youtubePredictor_frontend.youtubePredictor_databaseBuilder_app import DataBuilder
from youtubePredictor.youtubePredictor_frontend.youtubePredictor_form import VideoForm

# App config.
DEBUG = True
app = Flask(__name__)
app.secret_key = 'development key'
app.config.from_object(__name__)


@app.route("/", methods=['GET', 'POST'])
def index():
    form = VideoForm()
    if request.method == 'POST':
        if not form.validate():
            flash('A youtube url is required to run analysis. ')

        video_source = form.videoSource.data
        data_bldr.get_urls(url=video_source)
        data_bldr.get_video_info()
        data_bldr.api_manager()
        flash(data_bldr.display_results())

    return render_template('youtubePredictor_videoSubmission.html', form=form)


if __name__ == "__main__":
    data_bldr = DataBuilder()
    app.run()
