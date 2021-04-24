# Project                                                  : jiNx
# Architect/Core Implementation                            : Anthem Rukiya J. Wingate
# Purpose                                                  : Flask APP to run Youtube Predictor Implementation
# Revision History                                         : Version 1.0

# Notes:
#
#
#

# Import Data Handling Libraries
from setuptools import setup


DESCRIPTION='The team from jiNx present a Youtube video analyzer implementation which predicts potential number of views for a video'
GITHUB_URL='https://github.com/anthemwingate/jiNx'
AUTHOR='Anthem Rukiya WIngate Stevens Institute of Technology SSW 695A Spring 2021'
MAINTAINER='DiTTo Team'

INSTALL_REQUIRES = [
    'Flask',
    'psycopg2',
    'python-dotenv',
    'ibm-watson',
    'ibm-cloud-sdk-core'
    'watson-developer-cloud',
    'Flask-WTF',
    'prettyTable',
    'Flask',
    'jinja2',
    'coverage',
    'codecov',
    'beautifulsoup4',
    'os.path2',
    'requests',
    'flask-sockets',
    'pafy',
    'watson-streaming',
    'mockito',
    'Flask-Bcrypt',
    'Flask-Login',
    'Flask-Migrate',
    'Flask-SQLAlchemy', ''
    'Flask-Script',
    'Flask-Testing',
    'SQLAlchemy',
    'Mako',
    'MarkupSafe',
    'alembic',
    'gunicorn',
    'itsdangerous',
    'sqlite3-api',
    'python-vlc',
    'urllib3',
    'pymedia2-pyrana',
    'fluteline',
    'setuptools',
    'Werkzeug',
    'gevent',
    'WTForms',
    'fluteline',
    'sqlite3',
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
    name='',
    packages=['',],
    version=0,
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
