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


from __future__ import unicode_literals

# Import Data Handling Libraries
from pathlib import Path
import csv
import sys
import os
import datetime
import time
import http.cookiejar


# Import DiTTo_YoutubePredictor Utilities
import youtubePredictor_logger as ypLogger
import youtubePredictor_constants as youtubePredictorConstants
import youtubePredictor_dbBldr_const as dbbConst

# Import APIs
import youtube_dl
from youtube_dl.extractor.youtube import YoutubeIE
from ibm_watson import ToneAnalyzerV3, SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


# @TODO add yplogger_info and yplogger_error statements

class YoutubePredictorError(Exception):
    def __init__(self, message):
        self.message = message


class DataBuilder:
    def __init__(self):
        # Speech To Text Service Initialization
        self.speech_to_text_authenticator = IAMAuthenticator(dbbConst.SPEECH_TO_TEXT_API_KEY)
        self.speech_to_text = SpeechToTextV1(authenticator=self.speech_to_text_authenticator)
        self.speech_to_text.set_service_url(dbbConst.SPEECH_TO_TEXT_API_URL)

        # Tone Analyzer Service Initialization
        self.tone_analyzer_authenticator = IAMAuthenticator(apikey=dbbConst.TONE_ANALYZER_API_KEY)
        self.tone_analyzer = ToneAnalyzerV3(version=youtubePredictorConstants.TONE_ANALYZER_VERSION,
                                            authenticator=self.tone_analyzer_authenticator)
        self.tone_analyzer.set_service_url(dbbConst.TONE_ANALYZER_API_URL)

        # Variables
        self.record_count = 0
        self.db_builder_log = ypLogger.YoutubePredictorLogger()
        self.url_list_file = 'url_list.txt'
        self.youtube_downloads_folder = Path("audio_files/").rglob('*.mp3')
        self.audio_files = [x for x in self.youtube_downloads_folder]
        self.average_tones_data = {}
        self.column_names = youtubePredictorConstants.CSV_FILE_COLUMN_NAMES
        self.urls = []
        self.views = []
        self.duration = 0
        self.ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': 'audio_files/ytdl_' + str(datetime.datetime.now()).replace(" ", "_"),
        }

    def get_urls(self):  # Process Step 1
        try:
            with open(self.url_list_file, "r") as f:
                urls_from_file = f.readlines()
                f.close()
            for line in urls_from_file:
                self.urls.append(line.strip('\n'))
        except YoutubePredictorError('Unable to open file') as e:
            raise

    def get_video(self):  # Process Step 2
        for url in self.urls:
            with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
                extraction_info = ydl.extract_info(url, download=True, ie_key=youtubePredictorConstants.YOUTUBE_EXTRACTOR_KEY)
                self.views.append(extraction_info.get("view_count"))
                #time.sleep(extraction_info.get("duration") * 0.5)

    def get_speech_to_text(self):  # Process Step 3
        print(self.audio_files)
        for filename in self.audio_files:
            transcript = ""
            with open(filename, 'rb') as f:
                response = self.speech_to_text.recognize(audio=f, content_type="audio/mp3",
                                                         model="en-US_NarrowbandModel").get_result()
                for chunk in response['results']:
                    transcript += chunk['alternatives'][0]['transcript']
            f.close()
            os.remove(filename)
            self.get_tone_analysis(transcript)

    def get_tone_analysis(self, transcript):  # Process Step 4
        try:
            self.get_record(
                response=self.tone_analyzer.tone(transcript)
            )
        except ConnectionError('Unable to connect to IBM Watson Tone Analyzer service.') as e:
            raise

    def get_record(self, response):  # Called from Process Step 4
        sentence_ids = []
        anger_scores = []
        disgust_scores = []
        fear_scores = []
        joy_scores = []
        sadness_scores = []
        tentative_scores = []
        analytical_scores = []
        confident_scores = []
        for sentence in response.result["sentences_tone"]:
            if not sentence["tones"]:
                continue
            else:
                sentence_id = sentence["sentence_id"]
                is_new_sentence = not (sentence_id in sentence_ids)
                if is_new_sentence:
                    sentence_ids.append(sentence_id)
                    for tone in sentence["tones"]:
                        tone_name = tone["tone_name"]
                        if tone_name == self.column_names[0]:
                            anger_scores.append(tone["score"])
                        if tone_name == self.column_names[1]:
                            disgust_scores.append(tone["score"])
                        if tone_name == self.column_names[2]:
                            fear_scores.append(tone["score"])
                        if tone_name == self.column_names[3]:
                            joy_scores.append(tone["score"])
                        if tone_name == self.column_names[4]:
                            sadness_scores.append(tone["score"])
                        if tone_name == self.column_names[5]:
                            tentative_scores.append(tone["score"])
                        if tone_name == self.column_names[6]:
                            analytical_scores.append(tone["score"])
                        if tone_name == self.column_names[7]:
                            confident_scores.append(tone["score"])

        record = [
            self.record_count + 1,
            self.get_average_tone(anger_scores),
            self.get_average_tone(disgust_scores),
            self.get_average_tone(fear_scores),
            self.get_average_tone(joy_scores),
            self.get_average_tone(sadness_scores),
            self.get_average_tone(tentative_scores),
            self.get_average_tone(analytical_scores),
            self.get_average_tone(confident_scores),
            self.views[self.record_count],
            self.urls[self.record_count]
        ]
        self.average_tones_data[str(self.record_count)] = record
        self.record_count += 1

    def get_average_tone(self, scores):  # Called from process step 4
        if len(scores) > 0:
            return sum(scores) / len(scores)
        else:
            return 0

    def create_csv_file(self):  # Process Step 5
        try:
            training_file = open("test_init.csv", "w+")
            csv_writer = csv.writer(training_file)

            csv_writer.writerow(["ID",
                                 "ANGER",
                                 "DISGUST",
                                 "FEAR",
                                 "JOY",
                                 "SADNESS",
                                 "TENTATIVE",
                                 "ANALYTICAL",
                                 "CONFIDENT",
                                 "VIEWS",
                                 "URL",
                                 ])

            for record in self.average_tones_data:
                csv_writer.writerow(self.average_tones_data[record])

            training_file.close()

        except YoutubePredictorError('Unable to connect to IBM Watson Tone Analyzer Service') as e:
            raise


if __name__ == '__main__':
    data_bldr = DataBuilder()
    data_bldr.get_urls()
    data_bldr.get_video()
    data_bldr.get_speech_to_text()
    data_bldr.get_tone_analysis()
    data_bldr.create_csv_file()
    sys.exit()