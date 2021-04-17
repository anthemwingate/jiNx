
# Project                                                   : jiNx 
# Purpose                                                   : Capstone Project Stevens Institute of Tecchnology SSW 695A Spring 2021
# Author                                                    : Anthem Rukiya J. Wingate
# Revision History                                          : Version 1.0

# Import Data Handling Libraries
from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, BooleanField
from wtforms import validators, ValidationError


class VideoForm(FlaskForm):
    video_source = TextAreaField("Please enter the url to your video", [validators.data_required("Please enter a url.")])
    submit = SubmitField("Submit")
    cancel = SubmitField(label="Cancel", id="cancel")
