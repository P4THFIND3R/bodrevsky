from typing import Optional

from pydantic import BaseModel


class YoutubeDownloaderResponse(BaseModel):
    status: bool
    desc: Optional[str] = None
    filepath: Optional[str] = None
    filename: Optional[str] = None
