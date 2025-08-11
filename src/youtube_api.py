from requests import get
from dotenv import load_dotenv
from os import getenv
from src.model import PlaylistItemsResponse, BaseModel
from src.simple_model import simplePlaylistResponse, simpleVideoResponse, channelDetails

from utils import get_logger


load_dotenv()
log = get_logger(__name__)

# Simple cache dictionary
cache = {}


def getResponse(
    endpoint: str, params: dict, timeout=10, useCache=True
) -> dict | None:
    """
    Handles all the request to Youtube API with caching.
    """
    base_url = "https://youtube.googleapis.com/youtube/v3/"
    api_key = getenv("YOUTUBE_API_KEY")
    if not api_key:
        log.critical("YOUTUBE_API_KEY not set in environment variables.")
        return None
    params["key"] = api_key
    headers = {"Accept": "application/json"}

    # Create a unique cache key from endpoint and params
    cache_key = (endpoint, tuple(sorted(params.items())))

    # Check if response is in cache
    if cache_key in cache and useCache:
        log.info("Cache hit for %s", cache_key)
        return cache[cache_key]

    response = get(base_url + endpoint, params, headers=headers, timeout=timeout)

    if response.status_code == 200:
        try:
            response_json = response.json()
            # Store response in cache
            cache[cache_key] = response_json
            return response_json
        except Exception as e:
            log.error("%s sent error for %s, reason %s", endpoint, params, str(e))
            return None
    log.critical("%s failed %s for %s", endpoint,response.text, params)
    return None


def getChannelInfobyId(id: str) -> channelDetails | None:
    """
    Returns the Channel Details for a given Channel ID
    """

    resp = getResponse("channels", {"part": "snippet,statistics", "id": id})
    if resp:
        try:
            channel_data = resp.get("items", [])
            channel_item = channel_data[0]
            # Extract snippet and statistics data
            snippet_data = channel_item.get("snippet", {})
            statistics_data = channel_item.get("statistics", {})

            # Combine the data for the channelDetails model
            data = {
                "title": snippet_data.get("title", ""),
                "description": snippet_data.get("description", ""),
                "thumbnails": snippet_data.get("thumbnails", {}),
                "viewsCount": statistics_data.get("viewCount", "0"),
                "subscriberCount": statistics_data.get("subscriberCount", "0"),
                "videoCount": statistics_data.get("videoCount", "0"),
            }
            channel_details = channelDetails(**data)
            return channel_details
        except Exception as e:
            log.warning("Failed to parse channel data %s \n %s", resp, str(e))


def getPlaylistFromIdRaw(
    id: str, page_token: str = "", useCache=True
) -> PlaylistItemsResponse | None:
    """
    Returns the required Playlist in RAW Format
    """

    params = {"part": "snippet,contentDetails", "maxResults": "50", "playlistId": id}
    if page_token:
        params["pageToken"] = page_token

    resp = getResponse("playlistItems", params, useCache=useCache)

    if resp:
        try:
            return PlaylistItemsResponse(**resp)
        except TypeError as e:
            log.critical("Failed to parse playlist :%s \n %s", id, str(e))
    return None


def getPlaylistFromIdSimple(
    id: str, useCache=True, pl_title: str = "", pl_descr: str = ""
) -> simplePlaylistResponse | None:
    """
    Returns the required Playlist in Simple Format
    """
    playlist_response = getPlaylistFromIdRaw(id,useCache=useCache)
    videos = []
    while playlist_response:
        for item in playlist_response.items:
            video_id = item.contentDetails.videoId
            video_title = item.snippet.title
            video_description = item.snippet.description
            channel_name = item.snippet.channelTitle
            channel_id = item.snippet.channelId

            # Note: View count is not available in the playlist items response.
            videos.append(
                simpleVideoResponse(
                    video_id=video_id,
                    title=video_title,
                    description=video_description,
                    channel_name=channel_name,
                    channel_id=channel_id,
                    thumbnail=item.snippet.thumbnails,
                    date_upload=item.contentDetails.videoPublishedAt,
                )
            )
        page_next = playlist_response.nextPageToken
        if page_next:
            playlist_response = getPlaylistFromIdRaw(id, page_next, useCache=useCache)
        else:
            playlist_response = None
    return simplePlaylistResponse(
        playlist_id=id,
        title=pl_title,
        description=pl_descr,
        videos=videos,
    )


class playlistQuery(BaseModel):
    query: str
    max_results: int = 50
    pageToken: str = None
    regionCode: str = "IN"


def searchPlaylists(query: playlistQuery):
    """
    Searches for playlists using the YouTube API and returns a list of playlist

    Args:
        query: The search query.
        max_results: The maximum number of results to return (default is 10).
        pageToken: The page token for the next page of results.

    Returns:
        A list of playlist.
    """
    params = {
        "part": "snippet",
        "q": query.query,
        "type": "playlist",
        "maxResults": query.max_results,
        "regionCode": query.regionCode,
    }
    if query.pageToken:
        params["pageToken"] = query.pageToken

    resp = getResponse("search", params, useCache=False)

    return resp

def getVideoDetailsById(video_id: str, useCache=True) -> dict | None:
    """
    Returns the details about a video given its ID.
    """
    params = {
        "part": "snippet,contentDetails,statistics",
        "id": video_id,
    }
    resp = getResponse("videos", params, useCache=useCache)
    if resp and "items" in resp and len(resp["items"]) > 0:
        return resp["items"][0]
    else:
        log.warning("No video found for id: %s", video_id)
        return


def test_playlists():
    q_id = "PLTWGH5orWwL1-W-t21jQOIWUO6GKsc0ir"
    raw = getPlaylistFromIdRaw(q_id)
    assert raw is not None
    size = int(raw.pageInfo['totalResults'])
    simple = getPlaylistFromIdSimple(q_id)
    assert  simple is not None
    assert len(simple.videos)==size

def test_video_id():
    q_id = "gfhtaP5Wq7M"
    video_detail = getVideoDetailsById(q_id,False)
    print(video_detail)
    assert video_detail is not None
    assert video_detail['snippet']['title'] == "#39 Python Tutorial for Beginners | Factorial"