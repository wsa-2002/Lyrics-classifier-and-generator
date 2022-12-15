from typing import Sequence

from fastapi import APIRouter, responses

from base.enums import Genre
from service.lyrics_classifier import lyrics_classifier
from service.lyrics_generator import UserModel

router = APIRouter(tags=['Public'],
                   default_response_class=responses.JSONResponse)


@router.get("/", status_code=200, response_class=responses.HTMLResponse)
async def default_page():
    return "<a href=\"/docs\">/docs</a>"


@router.get("/genres-classify")
async def lyrics_to_genres(lyrics: str):
    genres = lyrics_classifier(lyrics)
    return genres


@router.get("/lyrics-generate")
async def lyrics_generator(lyrics: str, genres: Sequence[Genre] = None, lyrics_length: int = 100):
    if not genres:
        genres = lyrics_classifier(lyrics)
    generated_lyrics = [UserModel(genre.value).update(lyrics).generate_text(100) for genre in genres]
    # TODO: which lyric to return?
    return generated_lyrics
