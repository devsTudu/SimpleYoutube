from typing import Any, Optional
import requests
import re

from utils import get_logger

log = get_logger(__name__)


class YouTubeAPIClient:
    """
    A client for interacting with the YouTube Data API.
    Handles API key management and base request logic.
    """

    BASE_URL = "https://www.googleapis.com/youtube/v3/"

    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("YouTube API Key must be provided.")
        self.api_key = api_key

    def _make_request(
        self, endpoint: str, params: dict[str, Any]
    ) -> Optional[dict[str, Any]]:
        """
        Internal method to make a request to the YouTube API.
        """
        full_url = f"{self.BASE_URL}{endpoint}"
        all_params = {**params, "key": self.api_key}

        try:
            response = requests.get(full_url, params=all_params, timeout=10)
            response.raise_for_status()  # Raise an HTTPError
            return response.json()
        except requests.exceptions.RequestException as e:
            log.error("API request failed to %s : %s", endpoint, e)
            return None


# --- Helper Function for ISO 8601 Duration Parsing ---
def parse_iso8601_duration(iso_duration: str) -> int:
    """
    Parses an ISO 8601 duration string (e.g., 'PT1H30M15S') to total minutes.
    Handles 'PT' prefix and extracts H, M, S components.
    """
    if not iso_duration:
        return 0

    # Regex to capture hours (H), minutes (M), and seconds (S)
    match = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", iso_duration)
    if not match:
        return 0  # Or raise an error for invalid format

    hours = int(match.group(1)) if match.group(1) else 0
    minutes = int(match.group(2)) if match.group(2) else 0
    seconds = int(match.group(3)) if match.group(3) else 0

    total_seconds = (hours * 3600) + (minutes * 60) + seconds
    return round(total_seconds / 60)  # Convert to minutes, rounded
