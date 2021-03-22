from distutils.core import setup

from requests import __version__

DESCRIPTION='The team from DiTTo present a Youtube video analyzer implementation which predicts potential number of views for a video'
GITHUB_URL='https://github.com/ssw-695-spring-2021-group-afhk/DiTTo_YoutubePredictor'
AUTHOR='DiTTo Team Stevens Institute of Technology SSW 695A Spring 2021 Farnaz Sabetpour, HanQing Liu, Anthem Rukiya WIngate'
MAINTAINER='DiTTo Team'

setup(
    name='DiTTo_YoutubePredictor',
    packages=['DiTTo_YoutubePredictor'],
    version=__version__,
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
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: IronPython',
        'Programming Language :: Python :: Implementation :: Jython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
)
