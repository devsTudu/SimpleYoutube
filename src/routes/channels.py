from fastapi import APIRouter, HTTPException
from src.youtube_api import (
    get_creator_details_by_id,
    get_lesson_details_by_id,
)

from src.routes.client import client


channel = APIRouter(
    prefix="/channel",
    tags=["Channel"],
)


@channel.get("/ChannelDetail")
def ChannelDetail(id: str):
    """
    Returns the Channel Details for the given Id
    """
    result = get_creator_details_by_id(client, id)
    if result:
        return result.model_dump(mode="json")
    raise HTTPException(status_code=404, detail="Item not found")


@channel.get("/videoDetail")
def getVideoDetail(id: str):
    """
    Return the video metadata for the application
    """
    resp = get_lesson_details_by_id(client, id)
    if resp:
        return resp
    raise HTTPException(status_code=404, detail="Item not found")
