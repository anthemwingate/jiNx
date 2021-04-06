import youtube_dl
import sys
import youtubePredictor_constants


def get_urls():
    try:
        urls = []
        with open('url_list.txt', "r") as f:
            urls_from_file = f.readlines()
            f.close()
        for line in urls_from_file:
            urls.append(line.strip('\n'))
        for url in urls:
            get_subtitles(url)
    except FileNotFoundError('Unable to open file') as e:
        raise


def get_subtitles(url):
    ydl_opts = youtubePredictor_constants.YOUTUBE_DOWNLOAD_OPTIONS
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


if __name__ == '__main__':
    get_urls()
    sys.exit()
