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
from requests_html import HTMLSession
from bs4 import BeautifulSoup as bs

# Import DiTTo_YoutubePredictor Utilities
import youtubePredictor_logger as ypLogger
import youtubePredictor_constants as youtubePredictorConstants
import youtubePredictor_dbBldr_const as dbbConst

# Import APIs
from ibm_watson import ToneAnalyzerV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


# @TODO get views and add to record prior to creating init.csv

class YoutubePredictorError(Exception):
    def __init__(self, message):
        self.message = message


def get_average_tone(scores):
    if len(scores) > 0:
        return sum(scores) / len(scores)
    else:
        return 0


def get_video_info(url):
    session = HTMLSession()
    # download HTML code
    response = session.get(url)
    # execute Javascript
    response.html.render(sleep=1)
    # create beautiful soup object to parse HTML
    soup = bs(response.html.html, "html.parser")
    return int(''.join([c for c in soup.find("span", attrs={"class": "view-count"}).text if c.isdigit()]))


class DataBuilder:
    def __init__(self):

        # Tone Analyzer Service Initialization
        self.tone_analyzer_authenticator = IAMAuthenticator(apikey=dbbConst.TONE_ANALYZER_API_KEY)
        self.tone_analyzer = ToneAnalyzerV3(version=youtubePredictorConstants.TONE_ANALYZER_VERSION,
                                            authenticator=self.tone_analyzer_authenticator)
        self.tone_analyzer.set_service_url(dbbConst.TONE_ANALYZER_API_URL)
        self.record_count = 0
        self.db_builder_log = ypLogger.YoutubePredictorLogger()
        self.transcript_folder = Path("transcripts/").rglob('*.txt')
        self.transcript_files = [x for x in self.transcript_folder]
        self.average_tones_data = {}
        self.column_names = ["Anger", "Disgust", "Fear", "Joy", "Sadness", "Tentative", "Analytical", "Confident"]
        self.urls = []
        self.views = []

    def get_urls(self):
        try:
            with open("url_list.txt", "r") as f:
                self.urls.append(f.readline().strip('\n'))
            f.close()
            for url in self.urls:
                print(url)
                self.views.append(get_video_info(url=url))
                self.urls.append(url)
        except YoutubePredictorError('Unable to open file') as e:
            raise

    def temp_get_views(self):
        try:
            with open("test_views_list.txt", "r") as f:
                lines = f.readlines()
                for line in lines:
                    self.views.append(line.strip('\n'))
            f.close()
        except YoutubePredictorError('Unable to open file') as e:
            raise
        for i in range(11):
            self.urls.append("")

    def get_record(self, response):
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
            get_average_tone(anger_scores),
            get_average_tone(disgust_scores),
            get_average_tone(fear_scores),
            get_average_tone(joy_scores),
            get_average_tone(sadness_scores),
            get_average_tone(tentative_scores),
            get_average_tone(analytical_scores),
            get_average_tone(confident_scores),
            self.views[self.record_count],
            self.urls[self.record_count]
        ]
        self.average_tones_data[str(self.record_count)] = record
        self.record_count += 1

    def create_csv_file(self):
        try:
            training_file = open("test_init.csv", "w+")
            csv_writer = csv.writer(training_file)

            csv_writer.writerow(["ID",
                                 "ANGER",
                                 "DISGUST"
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

    def calculate_tones(self, transcript):
        return self.tone_analyzer.tone(transcript)

    def get_transcript(self):
        try:
            for filename in self.transcript_files:
                transcript_stream = open(filename, 'r')
                self.get_record(
                    response=self.calculate_tones(transcript=str(transcript_stream.readlines())
                                                  .encode('utf-8')))
                transcript_stream.close()
        except YoutubePredictorError('Unable to Open file') as e:
            raise


if __name__ == '__main__':
    data_bldr = DataBuilder()
    #data_bldr.get_urls() # @TODO un-comment when url_list.txt can be utilized with websockets implementation
    data_bldr.temp_get_views() # @TODO remove when url_list.txt can be utilized with websockets implementation
    data_bldr.get_transcript()
    data_bldr.create_csv_file()
    sys.exit()
