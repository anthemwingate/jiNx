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

# Utilities
YOUTUBE_FILENAME = './youtube_dl_audio_file.mp3'
DATABASE_NAME = 'TranscriptStats'
AUDIO_STREAM_QUALITY = 1
WEBSOCKETS_PORT = 5000
YOUTUBE_PREDICTOR_APP_PORT = 8080
YOUTUBE_PREDICTOR_APP_HOST = '0.0.0.0'
URL_TEMPLATE = 'wss://{}/speech-to-text/api/v1/recognize'
UPLOAD_FOLDER_PATH = 'save/'
PACKAGE_VERSION = 0.0
LOGGING_FORMAT = '%(asctime)-15s %(message)s'

# Credentials
NATURAL_LANGUAGE_UNDERSTANDING_VERSION = ''
SPEECH_TO_TEXT_VERSION = ''
TONE_ANALYZER_VERSION = ''

# DataBase Queries
FIND_TABLE = "SELECT * FROM TranscriptStats"
GET_COLUMN_HEADERS = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = " + DATABASE_NAME
CREATE_TABLE = 'CREATE TABLE TranscriptStats (ID SERIAL, URL TEXT NOT NULL UNIQUE, ANGER BOOLEAN NOT NULL, DISGUST BOOLEAN NOT NULL, FEAR BOOLEAN NOT NULL, JOY BOOLEAN NOT NULL, SADNESS BOOLEAN NOT NULL, VIEWS INTEGER NOT NULL);'  # @TODO check if this semi-colon should be removed
GET_TABLE = "SELECT * FROM TranscriptStats ORDER by Id"
FILL_TABLE = "INSERT INTO TranscriptStats (URL, ANGER, DISGUST, FEAR, JOY, SADNESS, VIEWS) VALUES (%s, %s, %s, %s, %s, %s, %s)"
GET_SINGLE_RECORD = "SELECT * FROM TranscriptStats WHERE Id=%s"
UPDATE_RECORD = "UPDATE TranscriptStats SET URL=%s, ANGER=%s, DISGUST=%s, FEAR=%s, JOY=%s, SADNESS=%s, VIEWS=%s WHERE Id=%s"
REMOVE_SINGLE_RECORD = "DELETE from TranscriptStats where ID=%s"
ADD_RECORD = "INSERT INTO TranscriptStats (URL, ANGER, DISGUST, FEAR, JOY, SADNESS, VIEWS) VALUES (%s, %s, %s, %s, %s, %s, %s)"
CLEAR_TABLE = 'DELETE FROM TranscriptStats'
