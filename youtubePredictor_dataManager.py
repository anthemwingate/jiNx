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

# Import Data Handling Libraries
import time
import os
from _ast import arg
from os.path import join, dirname
import csv
import psycopg2
from prettytable import from_db_cursor
from __future__ import unicode_literals
import logging
from flask import Flask, jsonify, render_template, request, flash, redirect, url_for, make_response, send_from_directory
import websocket

# Import DiTTo_YoutubePredictor Utilities
import youtubePredictor_constants as youtubePredictorConstants

# Import APIs
from ibm_watson import SpeechToTextV1, ToneAnalyzerV3, NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import watson_developer_cloud
import watson_developer_cloud.natural_language_understanding.features.v1 as features
import pafy

logging.basicConfig(filename="logs\\youtubePredictor.log", level=logging.DEBUG)
logger = logging.getLogger()


class YoutubePredictorError(Exception):
    def __init__(self, message):
        self.message = message


def measure_process_duration(func):
    def time_wrap():
        process_timer = time.time()
        process_function = func(*arg)
        logger.info("Function took" + str(time.time() - process_timer) + " seconds to complete.")
        return process_function

    return time_wrap()


class DataManager:

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
        self.column_headers = []
        self.transcript = ""

    @measure_process_duration
    def init(self):
        logger.info('YoutubePredictor DataManager initializing')
        try:
            self.cursor.execute(youtubePredictorConstants.FIND_TABLE)
        except YoutubePredictorError('Table not found.') as e:
            self.reset_cursor()
            self.cursor.execute(youtubePredictorConstants.CREATE_TABLE)
            self.import_data_from_file("init.csv")
            self.conn.commit()
            logger.error(e)
            raise
        else:
            logger.info('Table found.')
        finally:
            self.column_headers = self.get_column_headers()
            logger.info('YoutubePredictor DataManager initialization complete')

    @measure_process_duration
    def reset_cursor(self):
        logger.info('method: reset_cursor \nResetting database cursor.')
        self.conn = psycopg2.connect(self.conn_string)
        self.cursor = self.conn.cursor()

    @measure_process_duration
    def get_all_records_from_database(self):
        logger.info('method: get_all_records_from_database \nGetting records')
        self.cursor.execute(youtubePredictorConstants.GET_TABLE)
        return self.cursor.fetchall()

    @measure_process_duration
    def get_column_headers(self):
        logger.info('method: get_column_headers \nGetting column headers')
        self.cursor.execute(youtubePredictorConstants.GET_COLUMN_HEADERS)
        return from_db_cursor(self.cursor.fetchall)

    @measure_process_duration
    def get_record_from_database(self, i):
        logger.info('method: get_record_from_database \nGetting record with id: ' + i)
        try:
            update_st = youtubePredictorConstants.GET_SINGLE_RECORD
            self.cursor.execute(update_st, (i,))
            logger.info('Record found.')
            return self.cursor.fetchone()
        except YoutubePredictorError('Record not found.') as e:
            self.reset_cursor()
            logger.error(e)

    @measure_process_duration
    def update_record_in_database(self, val, i):
        logger.info('method: update_record_in_database \nUpdating record with id: ' + i)
        try:
            newtones = self.calculate_tones(val) + (i,) # @TODO needs rework, newtones isn't a complete record
            update_st = youtubePredictorConstants.UPDATE_RECORD
            self.cursor.execute(update_st, newtones)
            self.conn.commit()
        except YoutubePredictorError('Record not found') as e:
            self.reset_cursor()
            logger.error(e)
            raise
        else:
            logger.info('Record found')

    @measure_process_duration
    def delete_record_from_database(self, i):
        logger.info('method: delete_record_from_database \nDeleting record with id: ' + i)
        try:
            update_st = youtubePredictorConstants.REMOVE_SINGLE_RECORD
            self.cursor.execute(update_st, (i,))
            self.conn.commit()
        except YoutubePredictorError('Record not found') as e:
            self.reset_cursor()
            logger.error(e)
            raise
        else:
            logger.info('Record deleted')

    @measure_process_duration()
    def analyze_transcript(self, audio_stream):
        logger.info('method: analyze_transcript \nAnalyzing transcript')
        try:
            response = self.speech_to_text.recognize_using_websocket(audio=audio_stream,
                                                                     content_type='audio/webm',
                                                                     timestamps=False,
                                                                     word_confidence=False,
                                                                     continuous=True).get_result()

            for chunk in response['results']:
                self.transcript += chunk['alternatives'][0]['transcript']
        except YoutubePredictorError('IBM Watson Speech to Text Service connection failure') as e:
            logger.error(e)
            logger.info(jsonify(response))
        else:
            logger.info('Transcript analysis completed')

    @measure_process_duration
    def calculate_tones(self, transcript):
        logger.info('method: calculate_tones \nCalculating tones')
        data_store = (transcript.encode('utf-8'),)
        scores = []

        try:
            response = self.tone_analyzer.tone(text=transcript)

            for tone in response["document_tone"]["tone_categories"][0]["tones"]:
                scores.append(tone["score"])
            logger.info('Tone calculation completed')
            return scores
        except YoutubePredictorError('IBM Watson Tone Analyzer Service connection failure') as e:
            logger.error(e)
            logger.info(jsonify(response))
            return None

    @measure_process_duration
    def add_video_stats(self, transcript, url, views):
        logger.info('method: add_video_stats \nAdding stats to database')
        try:
            update_st = youtubePredictorConstants.ADD_RECORD
            record = []
            record[0] = url
            record.append(self.calculate_tones(transcript))
            record.append(views)
            self.cursor.execute(update_st, record)
            self.conn.commit()
            logger.info('Record added to database')
            return record
        except YoutubePredictorError('IBM Watson PostGreSQL Service connection failure') as e:
            self.reset_cursor()
            logger.error(e)
            return None

    @measure_process_duration
    def import_data_from_file(self, filename):
        logger.info('method: import_data_from_file \nImporting data from file ' + filename)
        isAdded = False
        isSkippedRecord = False

        try:
            csvfile = open(filename, "rb")
            reader = csv.reader(csvfile)
            for row in reader:
                update_st = youtubePredictorConstants.FILL_TABLE
                try:
                    self.cursor.execute(update_st, row)
                    self.conn.commit()
                    isAdded = True
                except YoutubePredictorError('Record Skipped') as x:
                    isSkippedRecord = True
                    self.reset_cursor()
                    logger.error(x)
                    raise
        except YoutubePredictorError('File import failure. File not found.') as e:
            self.reset_cursor()
            logger.error(e)
            raise
        else:
            csvfile.close()
            logger.info('CSV File successfully imported.')
            flash('CSV File successfully imported.')

        if isAdded and isSkippedRecord:
            logger.info('Partial Import Successful. Some records were skipped.')
            flash('Partial Import Successful. Some records were skipped.')
        if isSkippedRecord and not isAdded:
            logger.info('Import was unsuccessful.')
            flash('Import was unsuccessful.')
        return flash

    @measure_process_duration
    def remove_all_data_from_database(self):
        logger.info('method: remove_all_data_from_database \nRemoving contents from database')
        try:
            self.cursor.execute(youtubePredictorConstants.CLEAR_TABLE)
            self.conn.commit()
        except YoutubePredictorError('Database unavailable') as e:
            self.reset_cursor()
            logger.error(e)
            raise
        else:
            logger.info('Contents removal completed')
