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
from mockito import when, unstub

# Import DiTTo_YoutubePredictor Utilities
from DiTTo_YoutubePredictor import youtubePredictor_dataManager as data_mgr, youtubePredictor_constants as const
from tests import youtubePredictor_testSuiteConstants as test_const


class TestSuite(unittest.TestSuite):
    """ Test Class for DiTTo_YoutubePredictor """

    maxDiff = None

    def setUp(self) -> None:
        """ Class setup  """

        self.dir_abs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        self.directory_path = f"{self.dir_abs_path}/tests/data/testURLs.txt"

        # Mock Initializers
        self.data_mgr = data_mgr.DataManager(test_const.STT_API_KEY_TESTER,
                                             test_const.STT_ENDPOINT_URL_TESTER,
                                             test_const.TA_API_KEY_TESTER,
                                             test_const.TA_ENDPOINT_URL_TESTER,
                                             test_const.NLU_API_KEY_TESTER,
                                             test_const.NLU_ENDPOINT_URL_TESTER,
                                             test_const.ALCHEMY_API_KEY_TESTER,
                                             test_const.PGSL_USERNAME_TESTER,
                                             test_const.PGSL_PASSWORD_TESTER,
                                             test_const.PGSL_HOST_TESTER,
                                             test_const.PGSL_DBNAME_TESTER,
                                             test_const.PGSL_PORT_TESTER,
                                             )

        # @TODO add any additional self variables
        return super().setUp()

    #
    # Begin Phase 2 Core Implementation Testing
    #

    def test_dataManager_initialization(self):
        """ Test youtubePredictor_dataManager class initialization """

        # Stub
        self.data_mgr.init()
        when(self.cursor).execute(const.CREATE_TABLE).thenReturn(test_const.TEST_DB)

        # Test outcome
        self.assertEqual(self.cursor.execute(const.FIND_TABLE), test_const.TEST_DB, 'Database not found')

        # Clean Up Mocks
        unstub()
        return None

    #
    # Tear down class
    #

    def tearDown(self):
        """ Class tear down  """

        self.dir_abs_path.dispose()
        self.directory_path.dispose()
        self.data_mgr.dispose()
        # @TODO add any additional self variables


if __name__ == '__main__':
    unittest.TestSuite.maxDiff = None
    unittest.main(verbosity=2)
