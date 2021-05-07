import os
import sys
import youtube_dl
import youtubePredictor.youtubePredictor_frontend.youtubePredictor_constants as youtubePredictorConstants


def get_video_info(url):  # Process Step 2
    try:
        with youtube_dl.YoutubeDL(params=youtubePredictorConstants.YOUTUBE_DOWNLOAD_OPTIONS) as ydl:
            extraction_info = ydl.extract_info(url=url,
                                               download=False,
                                               ie_key=youtubePredictorConstants.YOUTUBE_EXTRACTOR_KEY)
            print(2021 - int(extraction_info.get("upload_date")[:4]))
    except youtube_dl.utils.ExtractorError as e:
        print(e)


if __name__ == '__main__':
    # Place test code here and run for testing line by line
    get_video_info("https://www.youtube.com/watch?v=IASLPrX3AmM")
    sys.exit()
