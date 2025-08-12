from fastapi import APIRouter, HTTPException
from src.youtube_api import get_lessons_for_course, search_courses

from src.routes.client import client

playlist = APIRouter(prefix="/playlist", tags=["Playlist, Search"])


@playlist.get("/search/")
def search_for_playlist(query: str, pageToken:str=''):
    """
    Returns relevant playlist details for the query
    """
    return search_courses(client, query,
                          pageToken=pageToken)


@playlist.get("/details")
def PlaylistDetailsByID(playlistID: str):
    result = get_lessons_for_course(client, playlistID)
    if result:
        return result.model_dump(mode="json")
    raise HTTPException(status_code=404, detail="Item not found")
