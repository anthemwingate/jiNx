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


# Import Data Handling Libraries
from pathlib import Path
import csv
import sys
import vtt2text
import requests
from bs4 import BeautifulSoup
import time

# Import DiTTo_YoutubePredictor Utilities
import youtubePredictor_logger as ypLogger
import youtubePredictor_constants as youtubePredictorConstants

# Import APIs
import youtube_dl
from ibm_watson import ToneAnalyzerV3, SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


# @TODO add yplogger_info and yplogger_error statements
# @TODO remove skipped lines from init.csv
# @TODO get better Tone analyser results

class YoutubePredictorError(Exception):
    def __init__(self, message):
        self.message = message


class YoutubePredictorRecord:
    def __init__(self):
        self.anger_scores = []
        self.disgust_scores = []
        self.fear_scores = []
        self.joy_scores = []
        self.sadness_scores = []
        self.tentative_scores = []
        self.analytical_scores = []
        self.confident_scores = []
        self.sentence_ids = []
        self.record_id = 0
        self.views = 0
        self.url = ""
        self.tone_analyzer_result = []
        self.column_names = youtubePredictorConstants.CSV_FILE_COLUMN_NAMES
        self.record = []

    def initialize(self, record_id, views, url, result):
        self.record_id = record_id
        self.views = views
        self.url = url
        self.tone_analyzer_result = result
        self.set_tones_helper()

    def set_tones_helper(self):
        for result in self.tone_analyzer_result:
            if result.get('sentences_tone') is not None:
                for sentence in result['sentences_tone']:
                    if sentence['tones']:
                        for tone in sentence['tones']:
                            self.set_tones(tone)

            else:
                if result["document_tone"]["tones"]:
                    for tone in result["document_tone"]["tones"]:
                        self.set_tones(tone)

        self.record = [self.record_id,
                       self.get_average_tone(self.anger_scores),
                       self.get_average_tone(self.disgust_scores),
                       self.get_average_tone(self.fear_scores),
                       self.get_average_tone(self.joy_scores),
                       self.get_average_tone(self.sadness_scores),
                       self.get_average_tone(self.tentative_scores),
                       self.get_average_tone(self.analytical_scores),
                       self.get_average_tone(self.confident_scores),
                       self.views,
                       self.url]

    def set_tones(self, tone_dict):
        tone_id = tone_dict["tone_id"]
        if tone_id == self.column_names[1].lower():
            self.anger_scores.append(tone_dict["score"])
        if tone_id == self.column_names[2].lower():
            self.disgust_scores.append(tone_dict["score"])
        if tone_id == self.column_names[3].lower():
            self.fear_scores.append(tone_dict["score"])
        if tone_id == self.column_names[4].lower():
            self.joy_scores.append(tone_dict["score"])
        if tone_id == self.column_names[5].lower():
            self.sadness_scores.append(tone_dict["score"])
        if tone_id == self.column_names[6].lower():
            self.tentative_scores.append(tone_dict["score"])
        if tone_id == self.column_names[7].lower():
            self.analytical_scores.append(tone_dict["score"])
        if tone_id == self.column_names[8].lower():
            self.confident_scores.append(tone_dict["score"])

    def get_average_tone(self, scores):  # Called from process step 4
        if len(scores) > 0:
            return sum(scores) / len(scores)
        else:
            return 0

    def get_record(self):
        return self.record


class DataBuilder:
    def __init__(self):
        # Speech To Text Service Initialization
        self.speech_to_text_authenticator = IAMAuthenticator(youtubePredictorConstants.SPEECH_TO_TEXT_API_KEY)
        self.speech_to_text = SpeechToTextV1(authenticator=self.speech_to_text_authenticator)
        self.speech_to_text.set_service_url(youtubePredictorConstants.SPEECH_TO_TEXT_API_URL)

        # Tone Analyzer Service Initialization
        self.tone_analyzer_authenticator = IAMAuthenticator(apikey=youtubePredictorConstants.TONE_ANALYZER_API_KEY)
        self.tone_analyzer = ToneAnalyzerV3(version=youtubePredictorConstants.TONE_ANALYZER_VERSION,
                                            authenticator=self.tone_analyzer_authenticator)
        self.tone_analyzer.set_service_url(youtubePredictorConstants.TONE_ANALYZER_API_URL)

        # Variables
        self.record_id = 0
        self.db_builder_log = ypLogger.YoutubePredictorLogger()
        self.url_list_file = 'test_urls.txt'
        self.download_archive_file = 'downloaded_files.txt'
        self.average_tones_data = []
        self.urls = []
        self.video_info = []
        self.subtitles_folder = Path("subtitles_files/").rglob('*')
        self.subtitles_files = [x for x in self.subtitles_folder]
        self.ydl_opts = {
            'ignoreerrors': True,
            'skip_download': True,
            'download_archive': self.download_archive_file,
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'writesubtitles': True,
            'writeautomaticsub': True,
            'subtitleslangs': ['en'],
            'outtmpl': 'subtitles_files/%(id)s.%(ext)s',
            'quiet': True,
        }
        self.get_urls()

    def get_urls(self):  # Process Step 1
        try:
            with open(self.url_list_file, "r") as f:
                urls_from_file = f.readlines()
                f.close()
            for line in urls_from_file:
                self.urls.append(line.strip('\n'))
        except FileNotFoundError('Unable to open file') as e:
            raise

    def get_subtitles(self, url):
        with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
            ydl.download([url])
            time.sleep(30)

    def get_view_count(self):
        print(self.subtitles_files)
        for filename in self.subtitles_files:
            a, b = str(filename).split("\\")
            c, d = str(b).split(".", 1)
            sep = ""
            url = sep.join([youtubePredictorConstants.YOUTUBE_URL_PREFIX, c])
            print(url)
            soup = BeautifulSoup(requests.get(url).text, 'lxml')
            views = soup.select_one('meta[itemprop="interactionCount"][content]')['content']
            print(views)
            subtitle_file_contents = str(vtt2text.clean(filename))
            print(subtitle_file_contents)
            result = self.get_tone_analysis(subtitle_file_contents)
            print(result)
            self.video_info.append({'result': result,
                                    'views': views,
                                    'url': url})

    def get_tone_analysis(self, transcript):
        results = []
        for chunk in transcript:
            results.append(self.tone_analyzer.tone(chunk).result)
        return results

    def api_manager(self):
        for url in self.urls:
            self.get_subtitles(url)
            self.get_view_count()
            for info in self.video_info:
                self.ytp_record_helper(info)

    def ytp_record_helper(self, info):
        ytp_record = YoutubePredictorRecord()
        self.record_id += 1
        ytp_record.initialize(record_id=self.record_id,
                              views=info.get('views'),
                              url=info.get('url'),
                              result=info.get('result'))
        self.average_tones_data.append(ytp_record.get_record())

    def create_csv_file(self):  # Process Step 5
        try:
            training_file = open("init.csv", "w+")
            csv_writer = csv.writer(training_file)

            csv_writer.writerow(youtubePredictorConstants.CSV_FILE_COLUMN_NAMES)
            csv_writer.writerows(self.average_tones_data)

            training_file.close()

        except FileNotFoundError('Unable to write to file') as e:
            raise


if __name__ == '__main__':
    data_bldr = DataBuilder()
    data_bldr.api_manager()
    data_bldr.create_csv_file()
    sys.exit()
