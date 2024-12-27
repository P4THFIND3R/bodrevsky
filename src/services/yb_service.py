from pathlib import Path

import yt_dlp

from src.core.config import settings
from src.schemas.stuff import UrlRecognizerResponses
from src.schemas.yb_schemas import YoutubeDownloaderResponse
from src.utils.randomizer import randomizer
from src.utils.url_recognizer import recognize


class Downloader:
    def __init__(self, url: str, audio_only: bool = False):
        self.url = url
        self.url_type = None
        self.audio_only = audio_only

        self.media_type = "audio/mpeg" if self.audio_only else "video/mp4"

        self.catalog = Path.cwd() / settings.VIDEO_CATALOG

    def check_url(self):
        self.url_type = recognize(self.url)

    def download_video(self):
        try:
            ydl_opts = self._get_ydl_opts()

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(self.url, download=True)

                filepath = self._get_filepath(info)
                filename = self._modify_filename(filepath.name)

                return YoutubeDownloaderResponse(
                    status=True,
                    filepath=str(filepath),
                    filename=filename,
                    media_type=self.media_type,
                )

        except Exception as e:
            return YoutubeDownloaderResponse(status=False, desc=e.__str__())

    def _get_ydl_opts(self):
        if self.audio_only:
            ydl_opts = {
                "format": "bestaudio/best",
                "postprocessors": [
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": "320",
                    }
                ],
                "merge_output_format": "mp3",
                "outtmpl": self.catalog.__str__() + "/%(title)s.%(ext)s",
            }
        else:
            ydl_opts = {
                "format": "bestvideo+bestaudio/best",
                "merge_output_format": "mp4",
                "outtmpl": self.catalog.__str__() + "/%(title)s.%(ext)s",
            }

        return ydl_opts

    def _get_filepath(self, info: dict) -> Path:
        filename = f"{info['title']}"

        if self.audio_only:
            filepath = Path(self.catalog / (filename + ".mp3"))
        else:
            filepath = Path(self.catalog / (filename + ".mp4"))

        return filepath

    def _modify_filename(self, filename) -> str:
        if self.url_type == UrlRecognizerResponses.INSTAGRAM:
            return randomizer.generate_random_string() + "_" + filename
        return filename
