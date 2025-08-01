from fastapi import APIRouter, HTTPException
from src.youtube_api import getChannelInfobyId

channel = APIRouter(
    prefix="/channel",
    tags=["Channel"],
)


@channel.get("/ChannelDetail")
def ChannelDetail(id: str):
    """
    Returns the Channel Details for the given Id
    """
    result = getChannelInfobyId(id)
    if result:
        return result.model_dump(mode="json")
    raise HTTPException(status_code=404, detail="Item not found")
