from pydantic import ValidationError
from typing import List, Optional
from datetime import datetime

from src.simple_model import (
    CreatorDetail,
    Course,
    LessonInCourseDetail,
    CourseDetailResponse,
    LessonDetail,
)
from src.helper import YouTubeAPIClient, parse_iso8601_duration
from utils import get_logger


log = get_logger(__name__)


def get_creator_details_by_id(
    client: YouTubeAPIClient, creator_id: str
) -> Optional[CreatorDetail]:
    """
    Fetches detailed information about a YouTube channel (creator).
    Maps to your 'Get creator detail' API.
    """
    params = {"part": "snippet,statistics", "id": creator_id}
    resp = client._make_request("channels", params)

    if resp and resp.get("items"):
        try:
            channel_item = resp["items"][0]
            snippet_data = channel_item.get("snippet", {})
            statistics_data = channel_item.get("statistics", {})

            # Clean and convert string numbers to int
            views_count = int(statistics_data.get("viewCount", "0"))
            subscriber_count = int(statistics_data.get("subscriberCount", "0"))
            video_count = int(statistics_data.get("videoCount", "0"))

            creator_data = {
                "creator_id": channel_item.get("id", creator_id),
                "creator_name": snippet_data.get("title", ""),
                "title": None,  # YouTube API 'channels' endpoint doesn't typically provide a separate 'title' field for the channel itself beyond its name.
                "description": snippet_data.get("description", ""),
                "thumbnail_small": snippet_data.get("thumbnails", {})
                .get("default", {})
                .get("url"),
                "thumbnail_big": snippet_data.get("thumbnails", {})
                .get("high", {})
                .get("url", ""),
                "views_count": views_count,
                "subscriber_count": subscriber_count,
                "lesson_count": video_count,  # Mapping YouTube's 'videoCount' to your 'lesson_count'
            }
            return CreatorDetail(**creator_data)
        except (KeyError, ValueError, ValidationError) as e:
            log.warning(
                f"Failed to parse creator data for ID {creator_id}: {e}. Raw response: {resp}"
            )
    log.warning(f"No creator found for ID: {creator_id}")
    return None


def search_courses(
    client: YouTubeAPIClient, query: str, region: str = "IN", pageToken: str = ""
) -> List[Course]:
    """
    Searches for YouTube playlists (which represent courses in your app).
    Maps to your 'Get relevant courses' API.
    """
    params = {
        "part": "snippet",
        "q": query,
        "type": "playlist",
        "maxResults": 50,
        "regionCode": region,
    }
    if pageToken != "":
        params["pageToken"] = pageToken

    resp = client._make_request("search", params)
    courses_list: List[Course] = []

    if resp and resp.get("items"):
        for item in resp["items"]:
            try:
                snippet = item.get("snippet", {})
                play_id = item.get('id',{}).get("playlistId", "")
                if not play_id:
                    continue
                course_data = {
                    "course_id": play_id,  # Extract playlistId from 'id' field
                    "course_name": snippet.get("title", ""),
                    "course_description": snippet.get("description", ""),
                    "thumbnail_small": snippet.get("thumbnails", {})
                    .get("default", {})
                    .get("url"),
                    "thumbnail_big": snippet.get("thumbnails", {})
                    .get("high", {})
                    .get("url", ""),
                    "creator_name": snippet.get("channelTitle", ""),
                    "creator_id": snippet.get("channelId", ""),
                    "published_date": (
                        datetime.fromisoformat(
                            snippet["publishedAt"].replace("Z", "+00:00")
                        ).date()
                        if snippet.get("publishedAt")
                        else None
                    ),
                }
                courses_list.append(Course(**course_data))
            except (KeyError, ValueError, ValidationError) as e:
                log.warning(
                    f"Failed to parse course item from search results: {e}. Item: {item}"
                )
                continue  # Skip malformed item and continue with others
    return { 'items':courses_list,
            'next':resp.get('nextPageToken')
    }


def get_lessons_for_course(
    client: YouTubeAPIClient, course_playlist_id: str
) -> CourseDetailResponse:
    """
    Fetches all lessons (videos) within a specific YouTube playlist (course).
    Handles pagination to get all items. Maps to your 'Get Course Detail' API.
    """
    lessons_list: List[LessonInCourseDetail] = []
    page_token: Optional[str] = ""

    while True:
        params = {
            "part": "snippet,contentDetails",
            "maxResults": "50",
            "playlistId": course_playlist_id,
        }
        if page_token:
            params["pageToken"] = page_token

        playlist_response = client._make_request("playlistItems", params)

        if not playlist_response or not playlist_response.get("items"):
            break

        for item in playlist_response["items"]:
            try:
                snippet = item.get("snippet", {})
                content_details = item.get("contentDetails", {})

                # YouTube's playlistItems endpoint gives videoId inside
                # resourceId if not directly in contentDetails
                video_id = content_details.get("videoId") or snippet.get(
                    "resourceId", {}
                ).get("videoId")

                if not video_id:  # Skip if no video ID found for the item
                    log.warning(f"Skipping playlist item without videoId: {item}")
                    continue

                lesson_data = {
                    "lesson_id": video_id,  # Using video_id as lesson_id
                    "lesson_title": snippet.get("title", ""),
                    "lesson_description": snippet.get("description", ""),
                    "creator_name": snippet.get("channelTitle", ""),
                    "creator_id": snippet.get("channelId", ""),
                    "published_date": (
                        datetime.fromisoformat(
                            snippet["publishedAt"].replace("Z", "+00:00")
                        ).date()
                        if snippet.get("publishedAt")
                        else None
                    ),
                    "thumbnail_small": snippet.get("thumbnails", {})
                    .get("default", {})
                    .get("url"),
                    "thumbnail_big": snippet.get("thumbnails", {})
                    .get("high", {})
                    .get("url", ""),
                }
                lessons_list.append(LessonInCourseDetail(**lesson_data))
            except (KeyError, ValueError, ValidationError) as e:
                log.warning(
                    f"Failed to parse lesson item from playlist {course_playlist_id}: {e}. Item: {item}"
                )
                continue

        page_token = playlist_response.get("nextPageToken")
        if not page_token:
            break

    return CourseDetailResponse(lessons=lessons_list)


def get_lesson_details_by_id(
    client: YouTubeAPIClient, video_id: str
) -> Optional[LessonDetail]:
    """
    Fetches comprehensive details for a single video (lesson).
    Maps to your 'Get lesson detail' API.
    """
    params = {
        "part": "snippet,contentDetails,statistics",
        "id": video_id,
    }
    resp = client._make_request("videos", params)

    if resp and resp.get("items"):
        try:
            video_item = resp["items"][0]
            snippet = video_item.get("snippet", {})
            content_details = video_item.get("contentDetails", {})
            statistics = video_item.get("statistics", {})

            # Convert string numbers to int, handling potential missing keys
            views_count = int(statistics.get("viewCount", "0"))
            like_count = int(statistics.get("likeCount", "0"))
            comment_count = int(statistics.get("commentCount", "0"))

            lesson_data = {
                "lesson_id": video_item.get("id", video_id),
                "video_id": video_item.get("id", video_id),
                "creator_id": snippet.get("channelId", ""),
                "creator_name": snippet.get("channelTitle", ""),
                "lesson_title": snippet.get("title", ""),
                "lesson_description": snippet.get("description", ""),
                "publish_date": (
                    datetime.fromisoformat(
                        snippet["publishedAt"].replace("Z", "+00:00")
                    ).date()
                    if snippet.get("publishedAt")
                    else None
                ),
                "thumbnail_small": snippet.get("thumbnails", {})
                .get("default", {})
                .get("url"),
                "thumbnail_big": snippet.get("thumbnails", {})
                .get("high", {})
                .get("url", ""),
                "category_id": snippet.get("categoryId"),
                "duration_minutes": parse_iso8601_duration(
                    content_details.get("duration", "")
                ),
                "views_count": views_count,
                "like_count": like_count,
                "comment_count": comment_count,
            }
            return LessonDetail(**lesson_data)
        except (KeyError, ValueError, ValidationError) as e:
            log.warning(
                "Failed to parse video details for ID %s: %s. Raw response: %s",
                video_id,
                e,
                resp,
            )
    else:
        log.warning(f"No video found for ID: {video_id}")
    return None

