
# Project                                                   : jiNx 
# Purpose                                                   : Capstone Project Stevens Institute of Tecchnology SSW 695A Spring 2021
# Author                                                    : Anthem Rukiya J. Wingate
# Revision History                                          : Version 1.0

# Notes:
#
#   dummy method for testing environment
#
#

import unittest
import os
import coverage


class NotReallyATestCase(unittest.TestCase):
    maxDiff = None

    def setUp(self):
        """ Class setup  """
        self.dir_abs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        self.directory_path = f"{self.dir_abs_path}/tests/"
        return super().setUp()

    def test_nothing(self):
        print(self.directory_path)
        self.assertEqual(True, True)

    def teardown(self):
        """ Class tear down  """

        self.dir_abs_path.dispose()
        self.directory_path.dispose()
        self.data_mgr.dispose()


if __name__ == '__main__':
    cov = coverage.Coverage()
    cov.start()
    unittest.TestCase.maxDiff = None
    framework = unittest.TestLoader().loadTestsFromTestCase(NotReallyATestCase)
    test_result = unittest.TextTestRunner(verbosity=2).run(framework).wasSuccessful()
    print("\nTesting Concluded with result:", test_result)
    cov.stop()
    cov.save()
    print('Coverage Summary: ')
    cov.report()
    basedir = os.path.abspath(os.path.dirname(__file__))
    covdir = os.path.join(basedir, 'coverage')
    cov.html_report(directory=covdir)
    cov.xml_report()
    cov.erase()
