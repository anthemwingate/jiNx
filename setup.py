from distutils.core import setup

from setuptools import setup, find_packages

DESCRIPTION='The team from DiTTo present a Youtube video analyzer implementation which predicts potential number of views for a video'
GITHUB_URL='https://github.com/ssw-695-spring-2021-group-afhk/DiTTo_YoutubePredictor'
AUTHOR='DiTTo Team Stevens Institute of Technology SSW 695A Spring 2021 Farnaz Sabetpour, HanQing Liu, Anthem Rukiya WIngate'
MAINTAINER='DiTTo Team'
VERSION=0.0.1

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
    packages=['DiTTo_YoutubePredictor'],
    version=VERSION,
    description=DESCRIPTION,
    url=GITHUB_URL,
    author=AUTHOR,
    maintainer=MAINTAINER,
    LICENSE='Unlicense',
    classifiers=[
        'Topic :: Machine Learning :: Video Analysis and Prediction',
        'Development Status :: 1 - Development',
        'Environment :: Console',
        'License :: Public Domain',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: Implementation',
        'Topic :: Software Development :: Research',
        'Inteded Audience :: Developers',
    ],
)
