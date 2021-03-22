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
import coverage

# Import DiTTo_YoutubePredictor Utilities
from tests import youtubePredictor_testSuite as testSuite

if __name__ == '__main__':
    cov = coverage.Coverage()
    cov.start()
    framework = unittest.TestLoader().loadTestsFromModule(testSuite)

    test_result = unittest.TextTestRunner(verbosity=2).run(framework).wasSuccessful()
    cov.stop()
    cov.save()

    print("\nTesting Concluded with result:", test_result)
    cov.html_report()