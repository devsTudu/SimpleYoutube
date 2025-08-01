from datetime import datetime
from pydantic import BaseModel

from pydantic import BaseModel, Field
from typing import List, Optional


# Data model for the thumbnail
class Image(BaseModel):
    url: str
    width: int
    height: int


# Data model for all thumbnails
class Thumbnails(BaseModel):
    default: Optional[Image] = None
    medium: Optional[Image] = None
    high: Optional[Image] = None
    standard: Optional[Image] = None
    maxres: Optional[Image] = None


# Data model for ResourceId in playlist items
class PlaylistItemResourceId(BaseModel):
    kind: str
    videoId: str


# Data model for snippet in playlist items
class PlaylistItemSnippet(BaseModel):
    publishedAt: datetime
    channelId: str
    title: str
    description: str
    thumbnails: Thumbnails
    channelTitle: str
    playlistId: str
    position: int
    resourceId: PlaylistItemResourceId
    videoOwnerChannelTitle: Optional[str] = None
    videoOwnerChannelId: Optional[str] = None


# Data model for contentDetails in playlist items
class PlaylistItemContentDetails(BaseModel):
    videoId: str
    videoPublishedAt: Optional[datetime] = None


# Data model for a single playlist item
class PlaylistItem(BaseModel):
    kind: str
    etag: str
    id: str
    snippet: PlaylistItemSnippet
    contentDetails: PlaylistItemContentDetails


# Data model for the entire playlist items response
class PlaylistItemsResponse(BaseModel):
    kind: str
    etag: str
    nextPageToken: Optional[str] = None
    items: List[PlaylistItem]
    pageInfo: dict  # Simplified as the structure is simple


# Data model for ResourceId in search results
class SearchResultResourceId(BaseModel):
    kind: str
    videoId: str


# Data model for snippet in search results
class SearchResultSnippet(BaseModel):
    publishedAt: datetime
    channelId: str
    title: str
    description: str
    thumbnails: Thumbnails
    channelTitle: str
    liveBroadcastContent: str
    publishTime: Optional[str] = None  # Optional based on the response


# Data model for a single search result item
class SearchResultItem(BaseModel):
    kind: str
    etag: str
    id: SearchResultResourceId
    snippet: SearchResultSnippet


# Data model for the entire search results response
class SearchResponse(BaseModel):
    kind: str
    etag: str
    nextPageToken: Optional[str] = None
    regionCode: Optional[str] = None  # Optional based on the response
    pageInfo: dict  # Simplified as the structure is simple
    items: List[SearchResultItem]


# Data model for snippet in channel response
class ChannelSnippet(BaseModel):
    title: str
    description: str
    customUrl: str
    publishedAt: datetime
    thumbnails: Thumbnails
    localized: dict  # Simplified as the structure is simple
    country: Optional[str] = None  # Optional based on the response


# Data model for statistics in channel response
class ChannelStatistics(BaseModel):
    viewCount: str
    subscriberCount: str
    hiddenSubscriberCount: bool
    videoCount: str


# Data model for a single channel item
class ChannelItem(BaseModel):
    kind: str
    etag: str
    id: str
    snippet: ChannelSnippet
    statistics: ChannelStatistics


# Data model for the entire channel response
class ChannelResponse(BaseModel):
    kind: str
    etag: str
    pageInfo: dict  # Simplified as the structure is simple
    items: List[ChannelItem]


# Data model for contentDetails in video response
class VideoContentDetails(BaseModel):
    duration: str
    dimension: str
    definition: str
    caption: str
    licensedContent: bool
    contentRating: dict  # Simplified as the structure is simple
    projection: str


# Data model for statistics in video response
class VideoStatistics(BaseModel):
    viewCount: str
    likeCount: str
    favoriteCount: str
    commentCount: str


# Data model for a single video item
class VideoItem(BaseModel):
    kind: str
    etag: str
    id: str
    snippet: SearchResultSnippet  # Reuse SearchResultSnippet as it has similar fields
    contentDetails: VideoContentDetails
    statistics: VideoStatistics


# Data model for the entire video response
class VideoResponse(BaseModel):
    kind: str
    etag: str
    items: List[VideoItem]
    pageInfo: dict  # Simplified as the structure is simple
