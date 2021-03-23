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
import unittest

from test.youtubePredictor_app_testSuite import BaseTestCase
from test import youtubePredictor_testSuiteConstants as tsConst


class FlaskTestCase(BaseTestCase):

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



if __name__ == '__main__':
    unittest.main()
