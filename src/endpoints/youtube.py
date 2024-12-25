from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse

from src.endpoints.deps import get_yb_downloader
from src.services.yb_service import YoutubeDownloader

router = APIRouter(prefix="/youtube", tags=["youtube"])


@router.get("/download")
async def download_video(
    url: str, audio_only: bool = False, youtube_downloader: YoutubeDownloader = Depends(get_yb_downloader)
):
    response = youtube_downloader.download_video(url, audio_only=audio_only)
    if not response.status:
        raise HTTPException(status_code=500, detail=response.desc)

    return FileResponse(response.filepath, filename=response.filename)
