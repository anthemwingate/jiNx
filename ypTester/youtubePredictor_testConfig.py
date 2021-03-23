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
import os

# Import DiTTo_YoutubePredictor Utilities
import ypTester.youtubePredictor_testSuiteConstants as tsConst

# default config
class BaseConfig(object):
    DEBUG = False
    #SECRET_KEY = '\xbf\xb0\x11\xb1\xcd\xf9\xba\x8bp\x0c...' @TODO determine if sqlite3 requires an API Key
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']


class TestConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = tsConst.SQL_DATABASE_URI


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False