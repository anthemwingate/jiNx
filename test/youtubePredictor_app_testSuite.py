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
import sqlite3
from mockito import when, unstub

# Import DiTTo_YoutubePredictor Utilities
from DiTTo_YoutubePredictor import youtubePredictor_app as app
from test import youtubePredictor_testSuiteConstants as tsConst


def connect_db():
    return sqlite3.connect(tsConst.APP_TEST_DB)


class BaseTestCase(TestCase):
    """A base test case."""
    maxDiff = None

    def __init__(self):
        self.db = connect_db()
        with self.db as connection:
            self.c = connection.cursor()
            # create the table
            self.c.execute(tsConst.CREATE_TEST_TABLE)
            # insert dummy data into the table
            self.c.execute(tsConst.ADD_TEST_RECORD)

    # Prep for testing
    def create_app(self):
        app.config.from_object('config.TestConfig')
        return app

    def __repr__(self):
        return '<url {}>'.format(self.url)

    def get_id(self):
        return self.id

    def get_views(self):
        return self.views

    def get_stats(self):
        cur = self.db.execute(tsConst.GET_TEST_TABLE)
        stats = [dict(url=row[1], anger=row[2], disgust=row[3], fear=row[4], joy=row[5], sadness=row[6], views=row[7]) for row in cur.fetachll()]
        return {
                'url:': stats[0].get('url'),
                'anger:': stats[0].get('anger'),
                'disgust:': stats[0].get('disgust'),
                'fear:': stats[0].get('fear'),
                'joy:': stats[0].get('joy'),
                'sadness:': stats[0].get('sadness'),
                'views:': stats[0].get('views'),
                }

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
                                        stats=tsConst.VIDEO_STATS_RECORD,
                                        follow_redirects=True
                                        )
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Video successfully analyzed.',
                          response.data)

    # Post testing clean up
    def tearDown(self):
        self.db.session.remove()
        self.db.drop_all()


if __name__ == '__main__':
    unittest.TestSuite.maxDiff = None
    unittest.main(verbosity=2)
