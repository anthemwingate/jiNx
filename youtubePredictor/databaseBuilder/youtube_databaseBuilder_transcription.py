import youtube_dl
import sys


def get_urls():
    try:
        urls = []
        with open('../url_list.txt', "r") as f:
            urls_from_file = f.readlines()
            f.close()
        for line in urls_from_file:
            urls.append(line.strip('\n'))
        for url in urls:
            get_subtitles(url)
    except FileNotFoundError('Unable to open file') as e:
        raise


def get_subtitles(url):
    ydl_opts = {
        'ignoreerrors': True,
        'skip_download': True,
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'writesubtitles': True,
        'writeautomaticsub': True,
        'subtitleslangs': ['en'],
        'outtmpl': 'subtitles_files/%(id)s.%(ext)s',
        'quiet': True,
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


if __name__ == '__main__':
    get_urls()
    sys.exit()
