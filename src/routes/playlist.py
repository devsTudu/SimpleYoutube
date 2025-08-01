from fastapi import APIRouter, HTTPException
from src.youtube_api import (playlistQuery,
                             searchPlaylists,
                             getPlaylistFromIdSimple)


playlist = APIRouter(prefix="/playlist", tags=["Playlist, Search"])


@playlist.post("/search/")
def search_for_playlist(query: playlistQuery):
    """
    Returns relevant playlist details for the query
    """
    return searchPlaylists(query)


@playlist.get("/details")
def PlaylistDetailsByID(id: str):
    result = getPlaylistFromIdSimple(id)
    if result:
        return result.model_dump(mode="json")
    raise HTTPException(status_code=404, detail="Item not found")
