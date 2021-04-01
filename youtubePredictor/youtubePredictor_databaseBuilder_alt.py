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
#  @TODO list of youtube urls in txt files which meet training specification, "url_list.txt"
#  @TODO iterate over a list of youtube video urls and send each url to websockets implementation
#  @TODO send the stream to STT Service
#  @TODO send the STT results to TA Service
#  @TODO open new CSV file and store
#  @TODO output stats to init.csv file


from __future__ import unicode_literals

# Import Data Handling Libraries
import os
import csv
from flask import Flask, render_template, request, flash, redirect, url_for, send_from_directory, jsonify


# Import DiTTo_YoutubePredictor Utilities
from

# Import APIs
from ibm_watson import SpeechToTextV1, ToneAnalyzerV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


# @ TODO add fully operational websockets implementation

class YoutubePredictorError(Exception):
    def __init__(self, message):
        self.message = message


class DataBuilder:
    def __init__(self,
                 speech_to_text_api_key,
                 tone_analyzer_api_key,
                 ):
        # Speech To Text Service Initialization
        self.speech_to_text_authenticator = IAMAuthenticator(apikey=speech_to_text_api_key)
        self.speech_to_text = SpeechToTextV1(authenticator=self.speech_to_text_authenticator)

        # Tone Analyzer Service Initialization
        self.tone_analyzer_authenticator = IAMAuthenticator(apikey=tone_analyzer_api_key)
        self.tone_analyzer = ToneAnalyzerV3(version=youtubePredictorConstants.TONE_ANALYZER_VERSION,
                                            authenticator=self.tone_analyzer_authenticator)
        self.record_count = 0
        self.db_builder_log = ypLogger.YoutubePredictorLogger()
        self.transcript = ""


    def calculate_tones(self):
        self.db_builder_log.log_method_started(method_name=self.calculate_tones.__name__, msg='Calculating tones')
        scores = []

        try:
            response = self.tone_analyzer.tone(self.transcript)

            for tone in response["document_tone"]["tone_categories"][0]["tones"]:
                scores.append(tone["score"])
            self.db_builder_log.log_method_completed(method_name=self.calculate_tones.__name__,
                                                     msg='Tone calculation completed')
            self.transcript = ""
            return scores
        except YoutubePredictorError('IBM Watson Tone Analyzer Service connection failure') as e:
            self.db_builder_log.log_error(ex=e, method_name=self.calculate_tones.__name__)
            self.db_builder_log.log_info(method_name=self.calculate_tones.__name__, msg=jsonify(response))
            return None

    def create_csv_file(self, record):
        self.db_builder_log.log_method_started(method_name=self.create_csv_file.__name__, msg="Creating CSV File")
        try:
            training_file = open("init.csv", "w+")
            csv_writer = csv.writer(training_file)
            if self.record_count == 0:
                self.record_count += 1
                csv_writer.writerow(["ID",
                                     "ANGER",
                                     "DISGUST",
                                     "FEAR",
                                     "JOY",
                                     "SADNESS",
                                     "VIEWS",
                                     "URL",
                                     ])
            record.insert(self.record_count)
            csv_writer.writerow(record)
            training_file.close()
            self.record_count += 1
            self.db_builder_log.log_method_completed(method_name=self.create_csv_file.__name__,
                                                     msg="CSV file creation completed")
        except YoutubePredictorError('Unable to create file') as e:
            self.db_builder_log.log_error(ex=e, method_name=self.create_csv_file.__name__)
            raise

    def get_transcript(self):
        self.db_builder_log.log_method_started(method_name=self.get_transcript().__name__,
                                               msg="Getting transcript from file")
        try:
            for filename in os.listdir("youtubePredictor/transcripts"):
                with open(filename, "r") as f:
                    self.transcript = f.readlines()
                self.create_csv_file(record=self.calculate_tones())
                f.close()

        except YoutubePredictorError('Unable to open file') as e:
            self.db_builder_log.log_error(ex=e, method_name=self.get_urls.__name__)
            raise


if __name__ == '__main__':

    data_bldr = DataBuilder(
        os.environ.get('SPEECH_TO_TEXT_API_KEY'),
        os.environ.get('TONE_ANALYZER_API_KEY'),
    )
    data_bldr.get_transcript()
