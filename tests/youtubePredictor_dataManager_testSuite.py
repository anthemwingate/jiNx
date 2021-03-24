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
import os
import sqlite3
import psycopg2
from mockito import when, unstub

# Import DiTTo_YoutubePredictor Utilities
import youtubePredictor.youtubePredictor_constants as ypConst
import youtubePredictor.youtubePredictor_dataManager as dataMgr
import youtubePredictor_testSuiteConstants as testConst


def connect_db():
    return sqlite3.connect(testConst.APP_TEST_DB)


class TestSuite(unittest.TestCase):
    """ Test Class for DiTTo_YoutubePredictor """

    maxDiff = None

    def setUp(self):
        """ Class setup  """

        self.dir_abs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        self.directory_path = f"{self.dir_abs_path}/ypTester/"

        # Mock Initializers
        self.data_mgr = dataMgr.DataManager(speech_to_text_api_key=testConst.STT_API_KEY_TESTER,
                                            speech_to_text_endpoint_url=testConst.STT_ENDPOINT_URL_TESTER,
                                            tone_analyzer_api_key=testConst.TA_API_KEY_TESTER,
                                            tone_analyzer_endpoint_url=testConst.TA_ENDPOINT_URL_TESTER,
                                            natural_language_understanding_api_key=testConst.NLU_API_KEY_TESTER,
                                            natural_language_understanding_endpoint_url=testConst.NLU_ENDPOINT_URL_TESTER,
                                            alchemy_api_key=testConst.ALCHEMY_API_KEY_TESTER,
                                            postgresql_username=testConst.PGSL_USERNAME_TESTER,
                                            postgresql_password=testConst.PGSL_PASSWORD_TESTER,
                                            postgresql_host=testConst.PGSL_HOST_TESTER,
                                            postgresql_dbname=testConst.PGSL_DBNAME_TESTER,
                                            postgresql_port=testConst.PGSL_PORT_TESTER,
                                            )
        self.db = connect_db()
        with self.db as connection:
            self.c = connection.cursor()
        when(psycopg2).connect(any(str)).thenReturn(self.db)

        """
        In DataManager:  stub???
        self.column_headers = []
        self.transcript = ""
        """
        return super().setUp()

    #
    # Begin Phase 2 Core Implementation Testing
    #

    def test_dataManager_initialization(self):
        """ Test youtubePredictor_dataManager class initialization """

        # Stub
        when(any(connect_db().cursor())).execute(ypConst.CREATE_TABLE).thenReturn(
            self.c.execute(testConst.CREATE_TEST_TABLE))
        when(any(connect_db().cursor())).execute(ypConst.FIND_TABLE).thenReturn(
            self.c.execute(testConst.GET_TEST_TABLE))

        # Execute
        self.data_mgr.init()
        actual_result = self.data_mgr.get_all_records_from_database()
        expected_result = self.c.execute(testConst.GET_TEST_TABLE).fetchall()

        # Test outcome
        self.assertEqual(actual_result, expected_result, 'Tables do not match')

        # Clean Up Mocks
        unstub()
        return None

    def test_dataManager_add_record(self):
        """ Test youtubePredictor_dataManager add record functionality """
        """ This test class tests the calculate_tones class by extension"""

        # Stub
        when(any(connect_db().cursor())).execute(ypConst.ADD_RECORD).thenReturn(
            self.c.execute(testConst.ADD_TEST_RECORD))
        when(self.data_mgr.calculate_tones()).thenReturn(testConst.VIDEO_STATS_LIST)

        # Execute
        actual_result = self.data_mgr.add_video_stats(url=testConst.USER_INPUT, views=testConst.VIEW_COUNT)
        expected_result = []
        expected_result[0] = testConst.USER_INPUT
        expected_result.append(testConst.VIDEO_STATS_LIST)
        expected_result.append(testConst.VIEW_COUNT)

        # Test outcome
        self.assertEqual(actual_result, expected_result, 'Records do not match')

        # Clean Up Mocks
        unstub()
        return None

    # @TODO create the following test cases
    # @TODO reset_cursor
    # @TODO Test get_column_headers
    # @TODO Test get_record_from_database
    # @TODO Test update_record_in_database
    # @TODO Test delete_record_from_database
    # @TODO Test analyze_transcript
    # @TODO Test create_transcript_file
    # @TODO Test import_data_from_file
    # @TODO Test remove_all_data_from_database

    #
    # Tear down class
    #

    def teardown(self):
        """ Class tear down  """

        self.dir_abs_path.dispose()
        self.directory_path.dispose()
        self.data_mgr.dispose()
        # @TODO add any additional self variables


if __name__ == '__main__':
    unittest.TestSuite.maxDiff = None
    unittest.main(verbosity=2)
