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
from __future__ import unicode_literals
import csv
import psycopg2
from prettytable import from_db_cursor
from flask import jsonify, flash

# Import DiTTo_YoutubePredictor Utilities
from youtubePredictor.youtubePredictor_frontend import youtubePredictor_logger as ypLog, youtubePredictor_constants as youtubePredictorConstants


class YoutubePredictorError(Exception):
    def __init__(self, message):
        self.message = message


class DataManager:

    def __init__(self, POSTGRESQL_USERNAME, POSTGRESQL_PASSWORD, POSTGRESQL_HOST, POSTGRESQL_DBNAME, POSTGRESQL_PORT):
        self.conn_string = "host='{}' dbname='{}' user='{}' password={} port={}".format(POSTGRESQL_HOST,
                                                                                        POSTGRESQL_DBNAME,
                                                                                        POSTGRESQL_USERNAME,
                                                                                        POSTGRESQL_PASSWORD,
                                                                                        POSTGRESQL_PORT)

        self.conn = psycopg2.connect(self.conn_string)
        self.cursor = self.conn.cursor()
        self.column_headers = []
        self.transcript = ""
        self.data_mgr_log = ypLog.YoutubePredictorLogger()

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

    def reset_cursor(self):
        self.data_mgr_log.log_method_started(method_name=self.reset_cursor.__name__, msg='Resetting database cursor')
        self.conn = psycopg2.connect(self.conn_string)
        self.cursor = self.conn.cursor()

    def get_all_records_from_database(self):
        self.data_mgr_log.log_method_started(method_name=self.get_all_records_from_database.__name__,
                                             msg='Getting records')
        self.cursor.execute(youtubePredictorConstants.GET_TABLE)
        self.data_mgr_log.log_method_completed(method_name=self.get_all_records_from_database.__name__,
                                               msg="Get all records completed")
        return self.cursor.fetchall()

    def get_column_headers(self):
        self.data_mgr_log.log_method_started(method_name=self.get_column_headers.__name__, msg='Getting column headers')
        self.cursor.execute(youtubePredictorConstants.GET_COLUMN_HEADERS)
        return from_db_cursor(self.cursor.fetchall)

    def add_record_to_database(self, record):
        self.data_mgr_log.log_method_started(method_name=self.add_record_to_database().__name__, msg='Adding record to database')
        try:
            update_st = youtubePredictorConstants.ADD_RECORD
            self.cursor.execute(update_st, record)
            self.conn.commit()
            self.data_mgr_log.log_method_completed(method_name=self.add_video_stats.__name__, msg='Record added to database')
        except YoutubePredictorError('IBM Watson PostGreSQL Service connection failure') as e:
            self.reset_cursor()
            self.data_mgr_log.log_error(ex=e, method_name=self.add_video_stats.__name__)
            return None

    def get_record_from_database(self, i):
        self.data_mgr_log.log_method_started(method_name=self.get_record_from_database.__name__,
                                             msg=f'Getting record with id: {i}')
        try:
            update_st = youtubePredictorConstants.GET_SINGLE_RECORD
            self.cursor.execute(update_st, (i,))
            self.data_mgr_log.log_method_completed(method_name=self.get_all_records_from_database.__name__,
                                                   msg="Get record from database completed")
            return self.cursor.fetchone()
        except YoutubePredictorError('Record not found.') as e:
            self.reset_cursor()
            self.data_mgr_log.log_error(ex=e, method_name=self.get_record_from_database.__name__)

    def delete_record_from_database(self, i):
        self.data_mgr_log.log_method_started(method_name=self.delete_record_from_database.__name__,
                                             msg=f'Deleting record with id: {i}')
        try:
            update_st = youtubePredictorConstants.REMOVE_SINGLE_RECORD
            self.cursor.execute(update_st, (i,))
            self.conn.commit()
            self.data_mgr_log.log_method_completed(method_name=self.delete_record_from_database.__name__,
                                                   msg="Record deleted")
        except YoutubePredictorError('Record not found') as e:
            self.reset_cursor()
            self.data_mgr_log.log_error(ex=e, method_name=self.delete_record_from_database.__name__)
            raise
        else:
            self.data_mgr_log.log_info(method_name=self.delete_record_from_database.__name__, msg='Record deleted')

    def import_data_from_file(self, filename):
        self.data_mgr_log.log_method_started(method_name=self.import_data_from_file.__name__,
                                             msg=f'Importing data from file {filename}')
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
            self.data_mgr_log.log_method_completed(method_name=self.import_data_from_file.__name__,
                                                   msg='CSV File successfully imported.')

        if is_added and is_skipped_record:
            self.data_mgr_log.log_warn(method_name=self.import_data_from_file.__name__,
                                       msg='Partial Import Successful. Some records were skipped.')
        if is_skipped_record and not is_added:
            self.data_mgr_log.log_warn(method_name=self.import_data_from_file.__name__, msg='Import was unsuccessful.')
        return flash

    def remove_all_data_from_database(self):
        self.data_mgr_log.log_method_started(method_name=self.remove_all_data_from_database.__name__,
                                             msg=' Removing contents from database')
        try:
            self.cursor.execute(youtubePredictorConstants.CLEAR_TABLE)
            self.conn.commit()
        except YoutubePredictorError('Database unavailable') as e:
            self.reset_cursor()
            self.data_mgr_log.log_error(ex=e, method_name=self.remove_all_data_from_database.__name__)
            raise
        else:
            self.data_mgr_log.log_method_completed(method_name=self.remove_all_data_from_database.__name__,
                                                   msg='Contents removal completed')
