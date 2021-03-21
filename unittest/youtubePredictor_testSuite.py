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
import unittest
import os
from mockito import when, mock, unstub
import requests


# Import DiTTo_YoutubePredictor Utilities
import youtubePredictor_dataManager as mgr
import youtubePredictor_constants as const


class TestSuite(unittest.TestCase):
    """ Test Class for DiTTo_YoutubePredictor """

    maxDiff = None

    def setUp(self) -> None:
        """ Class setup  """

        self.dir_abs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        self.directory_path = f"{self.dir_abs_path}/data/testURLs.txt"

        # Mock Initializers
        self.speech_to_text_api_key_tester = test
        self.speech_to_text_endpoint_url_tester = test
        self.tone_analyzer_api_key_tester = test
        self.tone_analyzer_endpoint_url_tester = test
        self.natural_language_understanding_api_key_tester = test
        self.natural_language_understanding_endpoint_url_tester = test
        self.alchemy_api_key_tester = test
        self.postgresql_username_tester = test
        self.postgresql_password_tester = test
        self.postgresql_host_tester = test
        self.postgresql_dbname_tester = test
        self.postgresql_port_tester = test
        self.test_database = "this is a database"
        self.data_mgr = mgr(self.speech_to_text_api_key_tester,
                       self.speech_to_text_endpoint_url_tester,
                       self.tone_analyzer_api_key_tester,
                       self.tone_analyzer_endpoint_url_tester,
                       self.natural_language_understanding_api_key_tester,
                       self.natural_language_understanding_endpoint_url_tester,
                       self.alchemy_api_key_tester,
                       self.postgresql_username_tester,
                       self.postgresql_password_tester,
                       self.postgresql_host_tester,
                       self.postgresql_dbname_tester,
                       self.postgresql_port_tester,
                       )

        # @TODO add any additional self variables
        return super().setUp()

    #
    # Begin Phase 2 Core Implementation Testing
    #

    def test_dataManager_initialization(self):
        """ Test youtubePredictor_dataManager class """

        # Stub
        self.data_mgr.init()
        when(self.cursor).execute(const.CREATE_TABLE).thenReturn(self.test_database)

        # Test outcome
        self.assertEqual((self.cursor.execute(const.FIND_TABLE)), self.test_database)

        # Clean Up Mocks
        unstub()
        return None



    #
    # Tear down class
    #

    def tearDown(self):
        """ Class tear down  """

        self.dir_abs_path.dispose
        self.directory_path.dispose
        # @TODO add any additional self variables


if __name__ == '__main__':
    unittest.TestCase.maxDiff = None
    unittest.main(verbosity=2)
