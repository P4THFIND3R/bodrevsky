from src.endpoints.exceptions import URLNotSupported
from src.schemas.stuff import UrlRecognizerResponses


def recognize(url: str) -> UrlRecognizerResponses:
    if "youtube" in url:
        return UrlRecognizerResponses.YOUTUBE
    if "instagram" in url:
        return UrlRecognizerResponses.INSTAGRAM

    raise URLNotSupported
