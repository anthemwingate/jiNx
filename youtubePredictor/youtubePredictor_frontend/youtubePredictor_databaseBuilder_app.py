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
import sys
from prettytable import PrettyTable
import os
import pickle

# Import DiTTo_YoutubePredictor Utilities
import youtubePredictor_constants as youtubePredictorConstants

# Import APIs
import youtube_dl
from ibm_watson import ToneAnalyzerV3, SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
#import gpt_2_simple as gpt2


# @TODO add yplogger_info and yplogger_error statements
# @TODO configure log files to be readable

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
        self.column_names = youtubePredictorConstants.CSV_FROM_DATABASE_FILE_COLUMN_NAMES
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
        self.average_tones_data = []
        self.urls = []
        self.ytdl_stt_info = []
        self.video_info = []
        self.youtube_downloads_folder = Path("audio_files/").rglob('*.mp3')
        self.audio_files = [x for x in self.youtube_downloads_folder]
        self.ydl_opts = youtubePredictorConstants.YOUTUBE_DOWNLOAD_OPTIONS
        self.ydl_alt_opts = youtubePredictorConstants.YOUTUBE_DOWNLOAD_ALTERNATIVE_OPTIONS
        self.model = {}
        self.record_table = PrettyTable()
        self.record_table.field_names = youtubePredictorConstants.CSV_FROM_DATABASE_FILE_COLUMN_NAMES

    def get_urls(self, url):  # Process Step 1
        # test_url = 'https://www.youtube.com/watch?v=ojhTu9aAa_Y&t=8s'
        # self.urls.append(test_url.strip('\n'))
        self.urls.append(url.strip('\n'))

    def get_video_info(self):  # Process Step 2
        for url in self.urls:
            is_not_playlist = 'playlist' not in url
            if is_not_playlist:
                with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
                    extraction_info = ydl.extract_info(url=url,
                                                       download=False,
                                                       ie_key=youtubePredictorConstants.YOUTUBE_EXTRACTOR_KEY)
                    video_info = {
                        'url': url,
                        'views': extraction_info.get("view_count"),
                        'video_id': extraction_info.get("id"),
                    }

                    if 'subtitles' in extraction_info:
                        video_info['subtitles'] = extraction_info.get("subtitles")
                    else:
                        self.get_video(url)
                        filename = str(os.getcwd() + "\\audio_files\\" + video_info['video_id'] + '.mp3')
                        video_info['subtitles'] = self.get_transcript_from_stt(filename)

                    self.video_info.append(video_info)
            else:  # @TODO Implementation if user submits a playlist
                print("Maybe write some code here before you try to do the thing!")
                # @TODO Write an implementation for users who decide to input a playlist instead of a single url

    def get_tone_analysis(self, transcript):
        results = []
        for chunk in transcript:
            results.append(self.tone_analyzer.tone(chunk).result)
        return results

    def get_video(self, url):
        with youtube_dl.YoutubeDL(self.ydl_alt_opts) as ydl:
            ydl.download([url])
            print('download complete')

    def get_transcript_from_stt(self, filename):
        transcript = []
        with open(filename, 'rb') as f:
            try:
                response = self.speech_to_text.recognize(audio=f, content_type="audio/mp3",
                                                         model="en-US_NarrowbandModel").get_result()
                for chunk in response['results']:
                    transcript.append(str(chunk['alternatives'][0]['transcript']))
            except ConnectionError(
                    'Unable to get transcript from IBM Watson Speech to Text for filename ' + filename) as e:
                raise
        f.close()
        os.remove(filename)
        return transcript

    def api_manager(self):
        for info in self.video_info:
            self.ytp_record_helper(info=info)

    def ytp_record_helper(self, info):
        ytp_record = YoutubePredictorRecord()
        self.record_id += 1
        ytp_record.initialize(record_id=self.record_id,
                              views=info.get('views'),
                              url=info.get('url'),
                              result=self.get_tone_analysis(info.get('subtitles')))
        self.average_tones_data.append(ytp_record.get_record())

    """def open_model(self):
        model_file = open(youtubePredictorConstants.ML_MODEL, 'rb')
        self.model = pickle.load(model_file)
        model_file.close()
        # @TODO when tensorflow issue is resolved, move the gpt2 implementation to get_prediction()
        sess = gpt2.start_tf_sess()
        gpt2.load_gpt2(sess, model_name=self.model, run_name='youtubePredictor_viewPrediction')
        predicted_views = gpt2.generate(sess,
                                        model_name=model,
                                        prefix="What do you call an entrepreneur",
                                        length=50,
                                        temperature=0.7,
                                        top_p=0.9,
                                        nsamples=5,
                                        batch_size=5,
                                        return_as_list=True)[0]"""

    def get_prediction(self, record):
        # self.open_model()
        # @TODO resolve issue with deprecated module tensorflow.contrib utilized by gpt-2-simple
        predicted_views = "gpt2 prediction goes here"
        return predicted_views

    def display_results(self):
        for record in self.average_tones_data:
            prediction = self.get_prediction(record)
            record.append(prediction)
            self.record_table.add_row(record)
        return self.record_table


if __name__ == '__main__':
    # In app testing
    data_bldr = DataBuilder()
    data_bldr.get_urls()
    data_bldr.get_video_info()
    data_bldr.api_manager()
    data_bldr.display_results()
    sys.exit()
