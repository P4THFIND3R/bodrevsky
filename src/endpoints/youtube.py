from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates

from src.endpoints.exceptions import URLNotSupported
from src.services.yb_service import Downloader

router = APIRouter(prefix="/youtube", tags=["youtube"])
templates = Jinja2Templates(directory="src/templates")


@router.get("/", response_class=HTMLResponse)
async def show_form(request: Request):
    return templates.TemplateResponse("download.html", {"request": request})


@router.get("/download", response_class=FileResponse)
async def download_video(url: str, audio_only: bool = False) -> FileResponse:
    downloader = Downloader(url, audio_only)

    try:
        downloader.check_url()

        response = downloader.download_video()
        if not response.status:
            raise HTTPException(status_code=500, detail=response.desc)

        return FileResponse(response.filepath, filename=response.filename, media_type=response.media_type)

    except URLNotSupported:
        raise HTTPException(status_code=400, detail="На текущий момент доступно скачивание лишь из youtube/instagram!")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
