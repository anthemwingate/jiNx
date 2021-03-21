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
import argparse
import contextlib
import time
import pafy
import fluteline

# Import DiTTo_YoutubePredictor Utilities
import youtubePredictor_constants

# Import APIs
import watson_streaming
import watson_streaming.utilities


def initialize_websocket(videoURL, credentials):
    input_video = pafy.new(videoURL)
    input_audio_stream_url = input_video._audiostreams[youtubePredictor_constants.AUDIO_STREAM_QUALITY].url
    settings = {
        'content_type': 'audio/webm',
        'timestamps': False,
        'word_confidence': False,
        'continuous': True,
        'interim_results': True,
    }

    nodes = [
        watson_streaming.utilities.FileAudioGen(input_audio_stream_url),
        watson_streaming.Transcriber(settings, credentials),
        watson_streaming.utilities.Printer(),
    ]

    fluteline.connect(nodes)
    fluteline.start(nodes)

    try:
        with contextlib.closing(?.open(input_audio_stream_url)) as f: # @TODO identify a library to open webm files
            audio_chunk_length = f.getnframes() / f.getnchannels() / f.getframerate()
        # Sleep till the end of the file + some seconds slack
        time.sleep(audio_chunk_length + 5)
    finally:
        fluteline.stop(nodes)
