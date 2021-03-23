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
from mockito import when, unstub

# Import DiTTo_YoutubePredictor Utilities
import ypTester.youtubePredictor_constants as ypConst
import ypTester.youtubePredictor_dataManager as dataMgr
import youtubePredictor_testSuiteConstants as testConst


class TestSuite(unittest.TestCase):
    """ Test Class for DiTTo_YoutubePredictor """

    maxDiff = None

    def setup(self) -> None:
        """ Class setup  """

        self.dir_abs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        self.directory_path = f"{self.dir_abs_path}/ypTester/"

        # Mock Initializers
        self.data_mgr = dataMgr.DataManager(testConst.STT_API_KEY_TESTER,
                                            testConst.STT_ENDPOINT_URL_TESTER,
                                            testConst.TA_API_KEY_TESTER,
                                            testConst.TA_ENDPOINT_URL_TESTER,
                                            testConst.NLU_API_KEY_TESTER,
                                            testConst.NLU_ENDPOINT_URL_TESTER,
                                            testConst.ALCHEMY_API_KEY_TESTER,
                                            testConst.PGSL_USERNAME_TESTER,
                                            testConst.PGSL_PASSWORD_TESTER,
                                            testConst.PGSL_HOST_TESTER,
                                            testConst.PGSL_DBNAME_TESTER,
                                            testConst.PGSL_PORT_TESTER,
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
        when(self.cursor).execute(ypConst.CREATE_TABLE).thenReturn(testConst.DATA_MANAGER_TEST_DB)

        # Test outcome
        self.assertEqual(self.cursor.execute(ypConst.FIND_TABLE), testConst.DATA_MANAGER_TEST_DB, 'Database not found')

        # Clean Up Mocks
        unstub()
        return None

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
