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
import logging

# Import DiTTo_YoutubePredictor Utilities
from youtubePredictor import youtubePredictor_constants as ypConstants


logging.basicConfig(filename=ypConstants.LOG_FILE_PATH,
                    format=ypConstants.LOGGING_FORMAT,
                    level=logging.DEBUG,
                    filemode="w+"
                    )


class YoutubePredictorLogger:
    def __init__(self):
        self.log = logging.getLogger(__name__)

    def log_method_started(self, method_name, msg):
        self.log.info('Starting method ' + method_name)
        self.log.info(msg)

    def log_method_completed(self, method_name, msg):
        self.log.info('Completed method ' + method_name)
        self.log.info(msg)

    def log_info(self, method_name, msg):
        self.log.info(f'{method_name}: ' + msg)

    def log_warn(self, method_name):
        self.log.warning(f'{method_name}: ' + ex.message)
        print(dir(ex))

    def log_error(self, ex, method_name):
        self.log.error(f'{method_name}: ' + ex.message)
        print(dir(ex))
