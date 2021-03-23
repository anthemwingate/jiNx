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
import sqlite3

# Import DiTTo_YoutubePredictor Utilities
import ypTester.youtubePredictor_constants as ypConst
import ypTester.youtubePredictor_testSuiteConstants as tsConst

# create a new database if the database doesn't already exist
with sqlite3.connect(tsConst.APP_TEST_DB) as connection:

    # get a cursor object used to execute SQL commands
    c = connection.cursor()

    # create the table
    c.execute(ypConst.CREATE_TABLE)

    # insert dummy data into the table
    c.execute(tsConst.ADD_TEST_RECORD)
