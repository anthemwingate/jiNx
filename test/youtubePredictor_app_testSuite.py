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
import unittest
import os
from mockito import when, unstub

# Import DiTTo_YoutubePredictor Utilities
from DiTTo_YoutubePredictor import youtubePredictor_app as app
from test.youtubePredictor_testingModel import VideoStats
from test import youtubePredictor_testSuiteConstants as tsConst


# @TODO import database object as db


class BaseTestCase(TestCase):
    """A base test case."""
    maxDiff = None

    # Prep for testing
    def create_app(self):
        app.config.from_object('config.TestConfig')
        return app

    def setUp(self):
        db.create_all()
        db.session.add(VideoStats(tsConst.VIDEO_STATS_RECORD))
        db.session.commit()

        # Test setup
    def test_index(self):
        response = self.client.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    # Test User Input
    def test_user_can_post(self):
        with self.client:
            self.client.post('/',
                             data=dict(video_source=tsConst.USER_INPUT),
                             follow_redirects=True
                             )
            response = self.client.post('/youtubePredictor_submissionSuccess.html',
                                        data=dict(title="test", description="test"),
                                        follow_redirects=True
                                        )
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Video successfully analyzed.',
                          response.data)
    # Post testing clean up
    def tearDown(self):
        db.session.remove()
        db.drop_all()


if __name__ == '__main__':
    unittest.TestSuite.maxDiff = None
    unittest.main(verbosity=2)
