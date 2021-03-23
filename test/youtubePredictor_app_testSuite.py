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

from __future__ import absolute_import

# Import Data Handling Libraries
from flask.ext.testing import TestCase

# Import DiTTo_YoutubePredictor Utilities
from DiTTo_YoutubePredictor import youtubePredictor_app as app
from test.youtubePredictor_testingModel import VideoStats
from test import youtubePredictor_testSuiteConstants as tsConst
# @TODO import database object as db


class BaseTestCase(TestCase):
    """A base test case."""

    def create_app(self):
        app.config.from_object('config.TestConfig')
        return app

    def setUp(self):
        db.create_all()
        db.session.add(VideoStats(tsConst.VIDEO_STATS_RECORD))
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
