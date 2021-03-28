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
from dotenv import load_dotenv
import csv
from bs4 import BeautifulSoup
import requests
import pafy
import fluteline
from urllib.request import urlopen
from urllib3 import request
import pyaudio
from flask import Flask, render_template, request, flash, redirect, url_for, send_from_directory, jsonify
import vlc

from flask_sockets import Sockets
import json
import base64
import math
from werkzeug.utils import secure_filename
from prettytable import PrettyTable
import functools

# Import DiTTo_YoutubePredictor Utilities
import youtubePredictor_logger as youtubePredictorConstants
import youtubePredictor_constants as ypLogger

# Import APIs
from ibm_watson import SpeechToTextV1, ToneAnalyzerV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

#@ TODO add fully operational websockets implementation

class YoutubePredictorError(Exception):
    def __init__(self, message):
        self.message = message


class UrlAudioGen(fluteline.Producer):

    def __init__(self, url):

        super(UrlAudioGen, self).__init__()
        self.url = pafy.new(url)
        self.stream_ = urlopen(self.url.audiostreams[youtubePredictorConstants.AUDIO_STREAM_QUALITY])

    def produce(self):
        samples = self.stream_.read(1024)
        if samples:
            p = vlc.MediaPlayer(samples)
            p.play()
        else:
            self.stop()

    def exit(self):
        self.stream_.close()


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
        self.py_aud = pyaudio.PyAudio()
        self.CHUNK = 1024  # @TODO move to constants class
        self.S_RATE = 44100  # @TODO move to constants class

    def analyze_transcript(self, audio_stream):
        self.db_builder_log.log_method_started(method_name=self.analyze_transcript.__name__, msg='Analyzing transcript')
        try:
            response = self.speech_to_text.recognize_using_websocket(audio=audio_stream,
                                                                     content_type='audio/webm',
                                                                     timestamps=False,
                                                                     word_confidence=False,
                                                                     continuous=True).get_result()

            for chunk in response['results']:
                self.transcript += chunk['alternatives'][0]['transcript']
        except YoutubePredictorError('IBM Watson Speech to Text Service connection failure') as e:
            self.db_builder_log.log_error(ex=e, method_name=self.analyze_transcript.__name__)
            self.db_builder_log.log_info(method_name=self.analyze_transcript.__name__, msg=jsonify(response))
        else:
            self.db_builder_log.log_method_completed(method_name=self.analyze_transcript.__name__,
                                                     msg='Transcript analysis completed')

    def calculate_tones(self):
        self.db_builder_log.log_method_started(method_name=self.calculate_tones.__name__, msg='Calculating tones')
        scores = []

        try:
            response = self.tone_analyzer.tone(self.transcript)

            for tone in response["document_tone"]["tone_categories"][0]["tones"]:
                scores.append(tone["score"])
            self.db_builder_log.log_method_completed(method_name=self.calculate_tones.__name__,
                                                     msg='Tone calculation completed')
            return scores
        except YoutubePredictorError('IBM Watson Tone Analyzer Service connection failure') as e:
            self.db_builder_log.log_error(ex=e, method_name=self.calculate_tones.__name__)
            self.db_builder_log.log_info(method_name=self.calculate_tones.__name__, msg=jsonify(response))
            return None

    def create_csv_file(self, url=None, view_count=None):
        self.db_builder_log.log_method_started(method_name=self.create_csv_file.__name__, msg="Creating CSV File")
        try:
            training_file = open("init.csv", "w+")
            csv_writer = csv.writer(training_file)
            if self.record_count == 0:
                csv_writer.writerow(["ID",
                                     "URL",
                                     "ANGER",
                                     "DISGUST",
                                     "FEAR",
                                     "JOY",
                                     "SADNESS",
                                     "VIEWS"
                                     ])

            record = self.calculate_tones()
            record.insert(0, url)
            record.append(view_count)
            csv_writer.writerow(record)
            training_file.close()
            self.record_count += 1
            self.db_builder_log.log_method_completed(method_name=self.create_csv_file.__name__,
                                                     msg="CSV file creation completed")
        except YoutubePredictorError('Unable to create file') as e:
            self.db_builder_log.log_error(ex=e, method_name=self.create_csv_file.__name__)
            raise

    def get_urls(self):
        self.db_builder_log.log_method_started(method_name=self.get_urls.__name__, msg="Getting urls from file")
        try:
            youtube_urls_file = open("url_list.txt", "r")
            url_list = youtube_urls_file.readlines()
            youtube_urls_file.close()
            for line in url_list:
                url = line.rstrip('\n')
                r = requests.get(url)
                s = BeautifulSoup(r.text, "html.parser")
                views = s.find("div", class_="watch-view-count").text
                self.web_streamer(url=url, view_count=views)
        except YoutubePredictorError('Unable to open file') as e:
            self.db_builder_log.log_error(ex=e, method_name=self.get_urls.__name__)
            raise

    def web_streamer(self, url, view_count):
        self.db_builder_log.log_method_started(method_name=self.web_streamer.__name__, msg="Streaming audio")
        url_request = request.RequestMethods.urlopen(method=request.RequestMethods.request_encode_url(method="GET"),
                                                     url=pafy.new(url))
        stream = self.py_aud.open(format=self.py_aud.get_format_from_width(2),
                                  channels=1,
                                  rate=self.S_RATE,
                                  output=True)
        data = url_request.read(self.CHUNK)
        while data:
            self.analyze_transcript(audio_stream=stream.produce())
        stream.exit()
        self.create_csv_file(url=url, view_count=view_count)


if __name__ == '__main__':
    load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))
    data_bldr = DataBuilder(
        os.environ.get('SPEECH_TO_TEXT_API_KEY'),
        os.environ.get('TONE_ANALYZER_API_KEY'),
    )
    data_bldr.get_urls()