from dotenv import load_dotenv
from os import getenv
from src.helper import YouTubeAPIClient

load_dotenv()

key = getenv("YOUTUBE_API_KEY")
if not key:
    raise ValueError("API Key not setup")
client = YouTubeAPIClient(key)
