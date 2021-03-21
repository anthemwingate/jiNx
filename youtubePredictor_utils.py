# Project           : DiTTo Yoututbe Predictor
# Author            : Team DiTTo Stevens Institute of Tecchnology SSW 695A Spring 2021
# Debugger         : Farnaz Sabetpour
# Purpose           : Flask APP to run Youtube Predictor Implementation
# Revision History  : Version 1.0
# Notes:  youtubepredictor_utils.py is obtained in its entirety from https://github.com/Nagasaki45/watson-streaming.git
#
#
#

import json
import wave

import fluteline
import sounddevice

AUDIO_OPTS = {
    'dtype': 'int16',
    'samplerate': 44100,
    'channels': 1,
}
BUFFER_SIZE = 2048


class MicAudioGen(fluteline.Producer):
    '''
    Producer that spits out audio samples from your microphone.
    '''

    def enter(self):
        self.stream = sounddevice.RawInputStream(**AUDIO_OPTS)
        self.stream.start()

    def exit(self):
        self.stream.stop()
        self.stream.close()

    def produce(self):
        chunk, _ = self.stream.read(BUFFER_SIZE)
        self.output.put(chunk[:])  # To get the bytes out of the CFFI buffer


class FileAudioGen(fluteline.Producer):
    '''
    Producer that spits out audio samples from a file.
    '''

    def __init__(self, audio_file):
        '''
        :param string audio_file: Path to a ``.wav`` file.
        '''
        super(FileAudioGen, self).__init__()
        self.audio_file = audio_file

    def enter(self):
        self.file_ = wave.open(self.audio_file)

    def exit(self):
        self.file_.close()

    def produce(self):
        samples = self.file_.readframes(BUFFER_SIZE)
        if samples:
            self.output.put(samples)
        else:
            self.stop()


class Printer(fluteline.Consumer):
    '''
    End-of-chain consumer to print the transcript received from
    IBM Watson.
    '''
    def consume(self, item):
        if 'results' in item:
            print(item['results'][0]['alternatives'][0]['transcript'])