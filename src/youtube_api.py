from requests import get
from dotenv import load_dotenv
from os import getenv
from src.model import PlaylistItemsResponse
from src.simple_model import simplePlaylistResponse, simpleVideoResponse, channelDetails

from utils import get_logger


load_dotenv()
log = get_logger(__name__)


def getResponse(endpoint: str, params: dict, timeout=5000) -> dict | None:
    """
    Handles all the request to Youtube API
    """
    base_url = "https://youtube.googleapis.com/youtube/v3/"
    params["key"] = getenv("YOUTUBE_API_KEY")
    headers = {"Accept": "application/json"}

    # Todo : Add a caching method with expiry to reduce API Calls
    response = get(base_url + endpoint, params, headers=headers, timeout=timeout)

    if response.status_code == 200:
        try:
            return response.json()
        except Exception as e:
            log.error("%s sent error for %s, reason %s", endpoint, params, str(e))
            return None
    log.critical("%s with %s, failed for %s", endpoint, params, response.text)
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


def getPlaylistFromIdRaw(id: str) -> PlaylistItemsResponse | None:
    """
    Returns the required Playlist in RAW Format
    """

    params = {"part": "snippet,contentDetails", "maxResults": "50", "playlistId": id}

    resp = getResponse("playlistItems", params)

    if resp:
        try:
            return PlaylistItemsResponse(**resp)
        except TypeError as e:
            log.critical("Failed to parse playlist :%s \n %s", id, str(e))
    return None


def getPlaylistFromIdSimple(id: str) -> simplePlaylistResponse | None:
    """
    Returns the required Playlist in Simple Format
    """
    playlist_response = getPlaylistFromIdRaw(id)
    if playlist_response:
        videos = []

        playlist_title = "Extracted Playlist"
        playlist_description = "Details extracted from playlist items"

        for item in playlist_response.items:
            video_id = item.contentDetails.videoId
            title = item.snippet.title
            description = item.snippet.description
            channel_name = item.snippet.channelTitle
            channel_id = item.snippet.channelId
            channel_detail = getChannelInfobyId(channel_id)
            channel_image = ""
            if channel_detail:
                channel_image = channel_detail.thumbnails.default.url

            # Note: View count is not available in the playlist items response.
            # You would need to make a separate video API call for each video to get view counts.
            videos.append(
                simpleVideoResponse(
                    video_id=video_id,
                    title=title,
                    description=description,
                    channel_name=channel_name,
                    channel_id=channel_id,
                    channel_image_url=channel_image,
                    thumbnail=item.snippet.thumbnails,
                    date_upload=item.contentDetails.videoPublishedAt,
                )
            )

        return simplePlaylistResponse(
            playlist_id=(
                playlist_response.items[0].snippet.playlistId
                if playlist_response.items
                else "N/A"
            ),  # Using playlistId from the first item
            title=playlist_title,
            description=playlist_description,
            videos=videos,
        )

def test_playlists():
    id = "PLTWGH5orWwL1-W-t21jQOIWUO6GKsc0ir"
    assert getPlaylistFromIdSimple(id) is not None

