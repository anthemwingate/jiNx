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
from os.path import join, dirname
import csv
import psycopg2
from mockito import kwargs
from prettytable import from_db_cursor
from __future__ import unicode_literals
from flask import Flask, jsonify, render_template, request, flash, redirect, url_for, make_response, send_from_directory
import functools
# Import DiTTo_YoutubePredictor Utilities
import youtubePredictor_constants as youtubePredictorConstants
import youtubePreditor_logger as ypLog

# Import APIs
from ibm_watson import SpeechToTextV1, ToneAnalyzerV3, NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


class YoutubePredictorError(Exception):
    def __init__(self, message):
        self.message = message


def measure_process_duration(func):
    @functools.wraps(func)
    def time_wrap():
        process_timer = time.time()
        process_function = func(**kwargs)
        return process_function
        flash("Function took" + str(time.time() - process_timer) + " seconds to complete.")

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
        self.data_mgr_log = ypLog.YoutubePredictorLogger()

    @measure_process_duration
    def init(self):
        self.data_mgr_log.log_method_started(method_name=self.init.__name__, msg='Initializing data manager')
        try:
            self.cursor.execute(youtubePredictorConstants.FIND_TABLE)
        except YoutubePredictorError('Table not found.') as e:
            self.reset_cursor()
            self.cursor.execute(youtubePredictorConstants.CREATE_TABLE)
            self.import_data_from_file("init.csv")
            self.conn.commit()
            self.data_mgr_log.log_error(ex=e, method_name=self.init.__name__)
            raise
        else:
            self.data_mgr_log.info(method_name=self.init.__name__,
                                   msg='Table found.')
        finally:
            self.column_headers = self.get_column_headers()
            self.data_mgr_log.info(method_name=self.init.__name__, 
                                   msg='YoutubePredictor DataManager initialization complete')

    @measure_process_duration
    def reset_cursor(self):
        self.data_mgr_log.log_method_started(method_name=self.reset_cursor.__name__, msg='Resetting database cursor')
        self.conn = psycopg2.connect(self.conn_string)
        self.cursor = self.conn.cursor()

    @measure_process_duration
    def get_all_records_from_database(self):
        self.data_mgr_log.log_method_started(method_name=self.get_all_records_from_database.__name__, msg='Getting records')
        self.cursor.execute(youtubePredictorConstants.GET_TABLE)
        return self.cursor.fetchall()

    @measure_process_duration
    def get_column_headers(self):
        self.data_mgr_log.log_method_started(method_name=self.get_column_headers.__name__, msg='Getting column headers')
        self.cursor.execute(youtubePredictorConstants.GET_COLUMN_HEADERS)
        return from_db_cursor(self.cursor.fetchall)

    @measure_process_duration
    def get_record_from_database(self, i):
        self.data_mgr_log.log_method_started(method_name=self.get_record_from_database.__name__, msg=f'Getting record with id: {i}')
        try:
            update_st = youtubePredictorConstants.GET_SINGLE_RECORD
            self.cursor.execute(update_st, (i,))
            self.data_mgr_log.log_method_started(method_name=self.get_record_from_database.__name__, msg='Record found.')
            return self.cursor.fetchone()
        except YoutubePredictorError('Record not found.') as e:
            self.reset_cursor()
            self.data_mgr_log.log_error(e)

    @measure_process_duration
    def update_record_in_database(self, val, i):
        self.data_mgr_log.log_method_started(method_name=self.update_record_in_database.__name__, msg=f'Updating record with id: {i}')
        try:
            newtones = self.calculate_tones(val) + (i,)  # @TODO needs rework, newtones isn't a complete record
            update_st = youtubePredictorConstants.UPDATE_RECORD
            self.cursor.execute(update_st, newtones)
            self.conn.commit()
        except YoutubePredictorError('Record not found') as e:
            self.reset_cursor()
            self.data_mgr_log.log_error(ex=e, method_name=self.update_record_in_database.__name__)
            raise
        else:
            self.data_mgr_log.log_info(method_name=self.update_record_in_database.__name__, msg='Record found')

    @measure_process_duration
    def delete_record_from_database(self, i):
        self.data_mgr_log.log_method_started(method_name=self.delete_record_from_database.__name__, msg=f'Deleting record with id: {i}')
        try:
            update_st = youtubePredictorConstants.REMOVE_SINGLE_RECORD
            self.cursor.execute(update_st, (i,))
            self.conn.commit()
        except YoutubePredictorError('Record not found') as e:
            self.reset_cursor()
            self.data_mgr_log.log_error(ex=e, method_name=self.delete_record_from_database.__name__)
            raise
        else:
            self.data_mgr_log.log_info(method_name=self.delete_record_from_database.__name__, msg='Record deleted')

    @measure_process_duration()
    def analyze_transcript(self, audio_stream):
        self.data_mgr_log.log_method_started(method_name=self.analyze_transcript.__name__, msg='Analyzing transcript')
        try:
            response = self.speech_to_text.recognize_using_websocket(audio=audio_stream,
                                                                     content_type='audio/webm',
                                                                     timestamps=False,
                                                                     word_confidence=False,
                                                                     continuous=True).get_result()

            for chunk in response['results']:
                self.transcript += chunk['alternatives'][0]['transcript']
        except YoutubePredictorError('IBM Watson Speech to Text Service connection failure') as e:
            self.data_mgr_log.log_error(ex=e, method_name=self.analyze_transcript.__name__)
            self.data_mgr_log.log_info(method_name=self.analyze_transcript.__name__, msg=jsonify(response))
        else:
            self.data_mgr_log.log_info(method_name=self.analyze_transcript.__name__, msg='Transcript analysis completed')

    @measure_process_duration
    def calculate_tones(self):
        self.data_mgr_log.log_method_started(method_name=self.calculate_tones.__name__, msg='Calculating tones')
        scores = []

        try:
            response = self.tone_analyzer.tone(self.transcript)

            for tone in response["document_tone"]["tone_categories"][0]["tones"]:
                scores.append(tone["score"])
            self.data_mgr_log.log_info(method_name=self.calculate_tones.__name__, msg='Tone calculation completed')
            return scores
        except YoutubePredictorError('IBM Watson Tone Analyzer Service connection failure') as e:
            self.data_mgr_log.log_error(ex=e, method_name=self.calculate_tones.__name__)
            self.data_mgr_log.log_info(method_name=self.calculate_tones.__name__, msg=jsonify(response))
            return None

    @measure_process_duration
    def add_video_stats(self, url, views):
        self.data_mgr_log.log_method_started(method_name=self.add_video_stats.__name__, msg='Adding stats to database')
        try:
            update_st = youtubePredictorConstants.ADD_RECORD
            record = []
            record[0] = url
            record.append(self.calculate_tones())
            record.append(views)
            self.cursor.execute(update_st, record)
            self.conn.commit()
            self.data_mgr_log.log_info(method_name=self.add_video_stats.__name__, msg='Record added to database')
            return record
        except YoutubePredictorError('IBM Watson PostGreSQL Service connection failure') as e:
            self.reset_cursor()
            self.data_mgr_log.log_error(ex=e, method_name=self.add_video_stats.__name__)
            return None

    @measure_process_duration
    def create_transcript_file(self, title):
        self.data_mgr_log.log_method_started(method_name=self.create_transcript_file.__name__, msg='Creating file')

        try:
            transcript_file = open(f"transcripts\{title}.txt", "w+")
            transcript_file.write(self.transcript.encode('utf-8'), )
            transcript_file.close()
            self.data_mgr_log.log_info(method_name=self.create_transcript_file.__name__, msg='File creation completed')
        except YoutubePredictorError('Unable to create file') as e:
            self.data_mgr_log.log_error(ex=e, method_name=self.add_video_stats.__name__)
            raise

    @measure_process_duration
    def import_data_from_file(self, filename):
        self.data_mgr_log.log_method_started(method_name=self.import_data_from_file.__name__, msg=f'Importing data from file {filename}')
        is_added = False
        is_skipped_record = False

        try:
            csvfile = open(filename, "rb")
            reader = csv.reader(csvfile)
            for row in reader:
                update_st = youtubePredictorConstants.FILL_TABLE
                try:
                    self.cursor.execute(update_st, row)
                    self.conn.commit()
                    is_added = True
                except YoutubePredictorError('Record Skipped') as x:
                    is_skipped_record = True
                    self.reset_cursor()
                    self.data_mgr_log.log_error(ex=x, method_name=self.import_data_from_file.__name__)
                    raise
        except YoutubePredictorError('File import failure. File not found.') as e:
            self.reset_cursor()
            self.data_mgr_log.log_error(ex=e, method_name=self.import_data_from_file.__name__)
            raise
        else:
            csvfile.close()
            self.data_mgr_log.log_info(method_name=self.import_data_from_file.__name__, msg='CSV File successfully imported.')

        if is_added and is_skipped_record:
            self.data_mgr_log.log_warn(method_name=self.import_data_from_file.__name__, msg='Partial Import Successful. Some records were skipped.')
        if is_skipped_record and not is_added:
            self.data_mgr_log.log_warn(method_name=self.import_data_from_file.__name__, msg='Import was unsuccessful.')
        return flash

    @measure_process_duration
    def remove_all_data_from_database(self):
        self.data_mgr_log.log_method_started(method_name=self.remove_all_data_from_database.__name__, msg=' Removing contents from database')
        try:
            self.cursor.execute(youtubePredictorConstants.CLEAR_TABLE)
            self.conn.commit()
        except YoutubePredictorError('Database unavailable') as e:
            self.reset_cursor()
            self.data_mgr_log.log_error(ex=e, method_name=self.remove_all_data_from_database.__name__)
            raise
        else:
            self.data_mgr_log.log_info(method_name=self.remove_all_data_from_database.__name__, msg='Contents removal completed')
