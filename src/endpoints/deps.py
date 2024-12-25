from functools import lru_cache

from src.services.yb_service import YoutubeDownloader


@lru_cache()
def get_yb_downloader():
    return YoutubeDownloader()
