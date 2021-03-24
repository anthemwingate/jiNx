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

# DataManager Testing
STT_API_KEY_TESTER = "speech_to_text_api_key_tester"
STT_ENDPOINT_URL_TESTER = "speech_to_text_endpoint_url_tester"
TA_API_KEY_TESTER = "tone_analyzer_api_key_tester"
TA_ENDPOINT_URL_TESTER = "tone_analyzer_endpoint_url_tester"
NLU_API_KEY_TESTER = "natural_language_understanding_api_key_tester"
NLU_ENDPOINT_URL_TESTER = "natural_language_understanding_endpoint_url_tester"
ALCHEMY_API_KEY_TESTER = "alchemy_api_key_tester"
PGSL_USERNAME_TESTER = "postgresql_username_tester"
PGSL_PASSWORD_TESTER = "postgresql_password_tester"
PGSL_HOST_TESTER = "postgresql_host_tester"
PGSL_DBNAME_TESTER = "postgresql_dbname_tester"
PGSL_PORT_TESTER = 8080
DATA_MANAGER_TEST_DB = "this is a database"

# App Testing
USER_INPUT = 'this is a URL'
VIEW_COUNT = 42
VIDEO_STATS_DICT = dict(url=USER_INPUT, anger=True, disgust=True, fear=False, joy=False, sadness=True, views=42)
VIDEO_STATS_LIST = [True, True, False, False, True]
APP_TEST_DB = 'youtubePredictor_testDatabase.db'
APP_TEST_TABLE = 'ypTestStats'
CREATE_TEST_TABLE = f'CREATE TABLE {APP_TEST_TABLE} (ID SERIAL, URL TEXT NOT NULL UNIQUE, ANGER BOOLEAN NOT NULL, DISGUST BOOLEAN NOT NULL, FEAR BOOLEAN NOT NULL, JOY BOOLEAN NOT NULL, SADNESS BOOLEAN NOT NULL, VIEWS INTEGER NOT NULL);'
GET_TEST_TABLE = f"SELECT * FROM {APP_TEST_TABLE} ORDER by Id"
ADD_TEST_RECORD = f"INSERT INTO {APP_TEST_TABLE} VALUES (USER_INPUT, True, True, False, False, True, 42)"
SQL_DATABASE_URI = 'sqlite:///:memory:'
