# Project           : DiTTo Yoututbe Predictor
# Author            : Team DiTTo Stevens Institute of Tecchnology SSW 695A Spring 2021
# Debugger         : Farnaz Sabetpour
# Purpose           : Flask APP to run Youtube Predictor Implementation
# Revision History  : Version 1.0
# Notes:
#
#
#

# Import Data Handling Libraries
import time
import os
from os.path import join, dirname
import csv
import psycopg2
from __future__ import unicode_literals
import logging
from flask import Flask, jsonify, render_template, request, flash, redirect, url_for, make_response, send_from_directory

# Import DiTTo_YoutubePredictor Utilities
import youtubePredictor_constants as youtubePredictorConstants

# Import APIs
from ibm_watson import SpeechToTextV1, ToneAnalyzerV3, NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import watson_developer_cloud
import watson_developer_cloud.natural_language_understanding.features.v1 as features

logging.basicConfig(level=logging.DEBUG)


class DataManager():

    def __init__(self, speech_to_text_api_key, speech_to_text_endpoint_url, tone_analyzer_api_key,
                 tone_analyzer_endpoint_url,
                 natural_language_understanding_api_key, natural_language_understanding_endpoint_url, alchemy_api_key,
                 postgresql_username, postgresql_password, postgresql_host, postgresql_dbname, postgresql_port):

        # Speech To Text Service Initialization
        self.speech_to_text_authenticator = IAMAuthenticator(apikey=tone_analyzer_api_key)
        self.speech_to_text = SpeechToTextV1(authenticator=self.speech_to_text_authenticator)

        # Natural Language Understanding Initialization
        self.natural_language_understanding_authenticator = IAMAuthenticator(
            apikey=natural_language_understanding_api_key)
        self.natural_language_understanding = NaturalLanguageUnderstandingV1(
            version=youtubePredictorConstants.NATURAL_LANGUAGE_UNDERSTANDING_VERSION,
            authenticator=self.natural_language_understanding.authenticator)

        # Tone Analyzer Service Initialization
        self.tone_analyzer_authenticator = IAMAuthenticator(apikey=tone_analyzer_api_key)
        self.tone_analyzer = ToneAnalyzerV3(version=youtubePredictorConstants.TONE_ANALYZER_VERSION,
                                            authenticator=self.tone_analyzer_authenticator)

        self.conn_string = "host='{}' dbname='{}' user='{}' password={} port={}".format(postgresql_host,
                                                                                        postgresql_dbname,
                                                                                        postgresql_username,
                                                                                        postgresql_password,
                                                                                        postgresql_port)

        self.conn = psycopg2.connect(self.conn_string)
        self.cursor = self.conn.cursor()

    def init(self):
        try:
            self.cursor.execute(youtubePredictorConstants.FIND_TABLE)
        except:
            self.reset_cursor()
            self.cursor.execute(youtubePredictorConstants.CREATE_TABLE)
            self.fill_db("init.csv")
            self.conn.commit()

    def reset_cursor(self):
        self.conn = psycopg2.connect(self.conn_string)
        self.cursor = self.conn.cursor()

    def get_all_records_from_database(self):
        self.cursor.execute(youtubePredictorConstants.GET_TABLE)
        return self.cursor.fetchall()

    def get_record_from_database(self, i):
        try:
            update_st = youtubePredictorConstants.GET_SINGLE_RECORD
            self.cursor.execute(update_st, (i,))
            return self.cursor.fetchone()
        except:
            self.reset_cursor()

    def update_record_in_database(self, val, i):
        try:
            newtones = self.calculate_tones(val) + (i,)
            update_st = youtubePredictorConstants.UPDATE_RECORD
            self.cursor.execute(update_st, newtones)
            self.conn.commit()
        except:
            self.reset_cursor()

    def delete_record_from_database(self, i):
        update_st = youtubePredictorConstants.REMOVE_SINGLE_RECORD
        self.cursor.execute(update_st, (i,))
        self.conn.commit()

    def measure_process_duration(self, func):
        def time_wrap():
            process_timer = time.time()
            process_function = func(*arg)
            flash("Function took" + str(time.time()-process_timer) + " seconds to complete.")
            return process_function
        return time_wrap()

    @measure_process_duration()
    def analyze_transcript(self, youtubeFilename):
        transcript = ""

        with open(join(dirname(__file__), youtubeFilename), 'rb') as audio_file:
            response = self.speech_to_text.recognize(audio_file,
                                                     content_type='audio/mp3',
                                                     timestamps=False,
                                                     word_confidence=False,
                                                     continuous=True).get_result()
            for chunk in response['results']:
                transcript += chunk['alternatives'][0]['transcript']

        os.remove(youtubeFilename) # @TODO consider sending transcript to GPT-3 API or similar neural network before removing file

        return jsonify(transcript)

    def calculate_tones(self, transcript):
        data_store = (transcript.encode('utf-8'),)
        scores = []

        try:
            response = self.tone_analyzer.tone(text=transcript)

            for tone in response["document_tone"]["tone_categories"][0]["tones"]:
                scores.append(tone["score"])
            return scores
        except:
            return None

    def add_video_stats(self, transcript, url, views):
        try:
            update_st = youtubePredictorConstants.ADD_RECORD
            tones = []
            tones[0] = url
            tones.append(self.calculate_tones(transcript))
            tones.append(views)
            self.cursor.execute(update_st, tones)
            self.conn.commit()
            return tones
        except:
            self.reset_cursor()
            return None

    def import_data_from_file(self, filename):
        isAdded = False
        isSkippedRecord = False
        csvfile = open(filename, "rb")
        reader = csv.reader(csvfile)
        for row in reader:
            try:
                update_st = youtubePredictorConstants.FILL_TABLE
                self.cursor.execute(update_st, row)
                self.conn.commit()
                isAdded = True
            except:
                isSkippedRecord = True
                self.reset_cursor()
        csvfile.close()
        flash = 'CSV File successfully imported.'
        if isAdded and isSkippedRecord:
            flash = 'Partial Import Successful. Some records were skipped.'
        if isSkippedRecord and not isAdded:
            flash = 'Import was unsuccessful.'
        return flash

    def remove_all_data_from_database(self):
        try:
            self.cursor.execute(youtubePredictorConstants.CLEAR_TABLE)
            self.conn.commit()
        except:
            self.reset_cursor()
