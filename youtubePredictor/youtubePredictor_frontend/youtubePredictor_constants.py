
# Project                                                   : jiNx 
# Purpose                                                   : Capstone Project Stevens Institute of Tecchnology SSW 695A Spring 2021
# Author                                                    : Anthem Rukiya J. Wingate
# Revision History                                          : Version 1.0

# Utilities
DATABASE_NAME = 'TranscriptStats'
AUDIO_STREAM_QUALITY = 1
WEBSOCKETS_PORT = 5000
YOUTUBE_PREDICTOR_APP_PORT = 8080
YOUTUBE_PREDICTOR_APP_HOST = '0.0.0.0'
URL_TEMPLATE = 'wss://{}/speech-to-text/api/v1/recognize'
UPLOAD_FOLDER_PATH = '../save/'
PACKAGE_VERSION = 0.0
LOGGING_FORMAT = '%(asctime)-15s %(message)s'
LOG_FILE_PATH = "../logs/youtubePredictor.log"
YOUTUBE_EXTRACTOR_KEY = 'Youtube'
YOUTUBE_URL_PREFIX = 'https://www.youtube.com/watch?v='
YOUTUBE_DOWNLOAD_OPTIONS = {
    'ignoreerrors': True,
    'skip_download': True,
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'writesubtitles': True,
    'writeautomaticsub': True,
    'subtitleslangs': ['en'],
    'outtmpl': 'audio_files/%(id)s.%(ext)s',
    'quiet': True,
}
YOUTUBE_DOWNLOAD_ALTERNATIVE_OPTIONS = {
    'ignoreerrors': True,
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'outtmpl': 'audio_files/%(id)s.%(ext)s',
}
ML_MODEL = "C:\\Users\\awingate\\IdeaProjects\\jiNx\\youtubePredictor\\youtubePredictor_frontend\\youtubePredictor_gpt2_finetuned_355M.sav"
MVR_MODEL = "C:\\Users\\awingate\\IdeaProjects\\jiNx\\youtubePredictor\\youtubePredictor_frontend\\youtubePredictor_MVR.sav"

# Credentials
TONE_ANALYZER_VERSION = "2017-09-21"
NATURAL_LANGUAGE_UNDERSTANDING_VERSION = '2020-08-01'

TONE_ANALYZER_API_KEY="NPYWY8TX5JQxBbs3HtJYdt8BQS_fm7PuqVtu74ga68Jb"
TONE_ANALYZER_API_URL="https://api.us-south.tone-analyzer.watson.cloud.ibm.com/instances/95c8ca9b-79db-4d00-8751-762c2e1afa55"
SPEECH_TO_TEXT_API_KEY="-sMeyBgh6r2QJ6ktabwYFHwa55x9TqbWo90kc3BuzDlN"
SPEECH_TO_TEXT_API_URL="https://api.us-south.speech-to-text.watson.cloud.ibm.com/instances/ba93f800-bb3b-4a65-a22f-0d6bae8b09b3"
WATSON_ML_API_KEY = "bbF3EjlYBATdUIhgi12zykN58c0QC9iwsu60lKFwWjE3"
WATSON_ML_URL = "https://us-south.ml.cloud.ibm.com"
NATURAL_LANGUAGE_UNDERSTANDING_API_KEY =""
NATURAL_LANGUAGE_UNDERSTANDING_API_KEY =""

# DataBase Queries
CSV_FROM_DATABASE_FILE_COLUMN_NAMES = ["ID",
                                       "ANGER",
                                       "DISGUST",
                                       "FEAR",
                                       "JOY",
                                       "SADNESS",
                                       "TENTATIVE",
                                       "ANALYTICAL",
                                       "CONFIDENT",
                                       "VIEWS",
                                       "AGE",
                                       "URL",
                                       "PREDICTION"
                                       ]
FIND_TABLE = "SELECT * FROM TranscriptStats"
GET_COLUMN_HEADERS = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = " + DATABASE_NAME
CREATE_TABLE = 'CREATE TABLE TranscriptStats (ID SERIAL, ANGER BOOLEAN NOT NULL, DISGUST BOOLEAN NOT NULL, FEAR BOOLEAN NOT NULL, JOY BOOLEAN NOT NULL, SADNESS BOOLEAN NOT NULL, VIEWS INTEGER NOT NULL, URL TEXT NOT NULL UNIQUE, PREDICTION INTEGER NOT NULL, );'
GET_TABLE = "SELECT * FROM TranscriptStats ORDER by Id"
FILL_TABLE = "INSERT INTO TranscriptStats (ANGER, DISGUST, FEAR, JOY, SADNESS, VIEWS, URL, PREDICTION) VALUES (%s, %s, %s, %s, %s, %s, %s)"
GET_SINGLE_RECORD = "SELECT * FROM TranscriptStats WHERE Id=%s"
UPDATE_RECORD = "UPDATE TranscriptStats SET ANGER=%s, DISGUST=%s, FEAR=%s, JOY=%s, SADNESS=%s, VIEWS=%s, URL=%s, PREDICTION=%s WHERE Id=%s"
REMOVE_SINGLE_RECORD = "DELETE from TranscriptStats where ID=%s"
ADD_RECORD = "INSERT INTO TranscriptStats (ANGER, DISGUST, FEAR, JOY, SADNESS, VIEWS, URL, PREDICTION) VALUES (%s, %s, %s, %s, %s, %s, %s)"
CLEAR_TABLE = 'DELETE FROM TranscriptStats'
