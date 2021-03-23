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


# Import DiTTo_YoutubePredictor Utilities
from test.youtubePredictor_testingModel import VideoStats
from test import youtubePredictor_testSuiteConstants as tsConst
# @TODO import test database object as db

# create the database and the db table
db.create_all()

# insert data
db.session.add(VideoStats(tsConst.VIDEO_STATS_RECORD))
# db.session.add(BlogPost("postgres", "we setup a local postgres instance"))

# commit the changes
db.session.commit()