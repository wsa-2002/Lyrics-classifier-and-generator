from typing import Sequence

from fastapi import APIRouter, responses

from base.enums import Genre
from service.lyrics_classifier import classifier
from service.lyrics_generator import UserModel

router = APIRouter(tags=['Public'],
                   default_response_class=responses.JSONResponse)


@router.get("/", status_code=200, response_class=responses.HTMLResponse)
async def default_page():
    return "<a href=\"/docs\">/docs</a>"


@router.get("/genres-classify")
async def lyrics_to_genres(lyrics: str):
    genres = classifier.classification(lyrics)
    return genres


@router.post("/lyrics-generate")
async def lyrics_generator(lyrics: str, genres: Sequence[Genre] = None, lyrics_length: int = 100):
    """
    lyrics: user input, used for lyrics generation
    genres: user input, may be list of genres, if genres is provided, the function will return the lyrics with genres appointed.
    """
    if not genres:
        genres = classifier.classification(lyrics)
    generated_lyrics = UserModel(genres).update(lyrics).generate_text(lyrics_length)
    return generated_lyrics.replace('.', '\n')
