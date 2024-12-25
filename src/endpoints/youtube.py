from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from src.endpoints.exceptions import URLNotSupported
from src.services.yb_service import Downloader

router = APIRouter(prefix="/youtube", tags=["youtube"])


@router.get("/download")
async def download_video(url: str, audio_only: bool = False):
    downloader = Downloader(url, audio_only)

    try:
        downloader.check_url()

        response = downloader.download_video(url, audio_only=audio_only)
        if not response.status:
            raise HTTPException(status_code=500, detail=response.desc)

        return FileResponse(response.filepath, filename=response.filename)

    except URLNotSupported:
        raise HTTPException(status_code=400, detail="На текущий момент доступно скачивание лишь из youtube/instagram!")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
