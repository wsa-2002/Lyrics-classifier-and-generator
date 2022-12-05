from fastapi import APIRouter, responses, Depends

from middleware.headers import get_auth_token

router = APIRouter(tags=['Public'], dependencies=[Depends(get_auth_token)])


@router.get("/", status_code=200, response_class=responses.HTMLResponse)
async def default_page():
    return "<a href=\"/docs\">/docs</a>"
