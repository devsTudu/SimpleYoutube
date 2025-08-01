from datetime import datetime
from pydantic import BaseModel
from .model import Thumbnails


class simpleVideoResponse(BaseModel):
    video_id: str
    title: str
    description: str
    channel_name: str
    channel_id: str
    thumbnail: Thumbnails
    date_upload: datetime | None


class simplePlaylistResponse(BaseModel):
    playlist_id: str
    title: str
    description: str
    videos: list[simpleVideoResponse]


class channelDetails(BaseModel):
    title: str
    description: str
    thumbnails: Thumbnails
    viewsCount: int
    subscriberCount: int
    videoCount: int
