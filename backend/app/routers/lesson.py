from fastapi import APIRouter
from backend.engine.gpt import GPTClient

router = APIRouter()
gpt = GPTClient()


@router.get('/chat/{chatId}/lesson', status_code=200)
async def generate_lesson(
    chatId: str,
):

    lesson = gpt.generate_lesson(chatId=chatId)
    
    res = lesson
    return {"lesson": res, "success": True}