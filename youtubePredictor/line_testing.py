import os
import sys

if __name__ == '__main__':
    url = 'https://www.youtube.com/playlist?list=PLua6pzs27dr-8LcGht9GjkjAlidA_JCNT'
    is_playlist = False
    is_playlist = 'playlist' in url
    if is_playlist:
        print('works')
    else:
        print('doggone it')
    sys.exit()