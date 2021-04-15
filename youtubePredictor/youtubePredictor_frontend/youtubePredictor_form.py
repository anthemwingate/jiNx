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
from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, BooleanField
from wtforms import validators, ValidationError


class VideoForm(FlaskForm):
    video_source = TextAreaField("Please enter the url to your video", [validators.data_required("Please enter a url.")])
    submit = SubmitField("Submit")
    cancel = SubmitField(label="Cancel", id="cancel")