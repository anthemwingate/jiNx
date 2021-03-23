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
from setuptools import setup

# Import DiTTo_YoutubePredictor Utilities
from ypTester import youtubePredictor_constants

DESCRIPTION='The team from DiTTo present a Youtube video analyzer implementation which predicts potential number of views for a video'
GITHUB_URL='https://github.com/ssw-695-spring-2021-group-afhk/DiTTo_YoutubePredictor'
AUTHOR='DiTTo Team Stevens Institute of Technology SSW 695A Spring 2021 Farnaz Sabetpour, HanQing Liu, Anthem Rukiya WIngate'
MAINTAINER='DiTTo Team'

INSTALL_REQUIRES = [
    'Flask',
    'psycopg2',
    'python-dotenv',
    'watson-develop,er-cloud',
    'Flask-WTF',
    'prettyTable',
    'Flask',
    'jinja2',
    'coverage',
    'beautifulsoup4',
    'os.path2',
    'requests',
    'flask-sockets',
    'pafy',
    'watson-streaming',
    'mockito',
]

TEST_REQUIRES = [
    # testing and coverage
    'unittest', 'coverage',
    # to be able to run `python setup.py checkdocs`
    'collective.checkdocs', 'pygments',
]

with open('README.md') as f:
    README = f.read()

setup(
    name='DiTTo_YoutubePredictor',
    packages=['DiTTo_YoutubePredictor',],
    version=youtubePredictor_constants.PACKAGE_VERSION,
    description=DESCRIPTION,
    url=GITHUB_URL,
    author=AUTHOR,
    maintainer=MAINTAINER,
    classifiers=[
        'Topic :: Machine Learning :: Video Analysis and Prediction',
        'Development Status :: ',
        'Environment :: Console',
        'License :: Public Domain',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: Implementation',
        'Topic :: Software Development :: Research',
        'Inteded Audience :: Developers',
    ],
)
