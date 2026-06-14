import os
import requests
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

# Importing the centralized and validated list of channels
from src.config import CONSOLIDATED_TARGET_CHANNELS

load_dotenv()

def fetch_recent_whitelist_videos():
    """Fetches videos from the last 7 days from the selected channels."""
    api_key = os.getenv("YOUTUBE_API_KEY")
    url_search = "https://www.googleapis.com/youtube/v3/search"
    
    cutoff_date = (datetime.now(timezone.utc) - timedelta(days=7)).strftime('%Y-%m-%dT%H:%M:%SZ')
    found_videos = []

    # Phase 1: Discovery (Fetch the video IDs)
    for channel_id in CONSOLIDATED_TARGET_CHANNELS:
        params = {
            'part': 'snippet',
            'channelId': channel_id,
            'publishedAfter': cutoff_date,
            'maxResults': 5, # Fetches up to 5 recent videos per channel
            'order': 'date', # Chronological order, not relevance
            'type': 'video',
            'key': api_key
        }

        response = requests.get(url_search, params=params)
        if response.status_code == 200:
            items = response.json().get('items', [])
            for item in items:
                found_videos.append(item['id']['videoId'])

    # Phase 2: Enrichment (Fetch engagement metrics)
    if not found_videos:
        return []

    url_videos = "https://www.googleapis.com/youtube/v3/videos"

    # The API allows fetching up to 50 IDs at once, separated by commas
    ids_string = ",".join(found_videos[:50])

    params_stats = {
        'part': 'snippet,statistics',
        'id': ids_string,
        'key': api_key
    }
    
    resp_stats = requests.get(url_videos, params_stats)
    return resp_stats.json().get('items', [])