from pathlib import Path

import yt_dlp

from src.core.config import settings
from src.schemas.yb_schemas import YoutubeDownloaderResponse


class YoutubeDownloader:
    def __init__(self):
        self.catalog = Path.cwd() / settings.VIDEO_CATALOG

    def download_video(
        self,
        url: str,
        audio_only: bool,
    ):
        if audio_only:
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

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)

                if audio_only:
                    filepath = Path(self.catalog / f"{info['title']}.mp3")
                else:
                    filepath = Path(self.catalog / f"{info['title']}.mp4")

                return YoutubeDownloaderResponse(
                    status=True,
                    filepath=str(filepath),
                    filename=filepath.name,
                )

        except Exception as e:
            return YoutubeDownloaderResponse(status=False, desc=e.__str__())
