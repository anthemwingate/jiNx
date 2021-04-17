
# Project                                                   : jiNx 
# Purpose                                                   : Capstone Project Stevens Institute of Tecchnology SSW 695A Spring 2021
# Author                                                    : Anthem Rukiya J. Wingate
# Revision History                                          : Version 1.0

# Import Data Handling Libraries
import logging

# Import DiTTo_YoutubePredictor Utilities
from youtubePredictor.youtubePredictor_frontend import youtubePredictor_constants as ypConstants

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
