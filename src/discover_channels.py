import os
import requests
import pandas as pd
from datetime import datetime, timedelta
from collections import Counter
from dotenv import load_dotenv

# Load environment variables (API Key)
load_dotenv()

def mine_channels_by_niche(queries, lookback_days=30, max_results_per_query=50):
    """
    Searches for the most relevant recent videos in a niche and extracts the creators' channels.
    """
    api_key = os.getenv("YOUTUBE_API_KEY")
    url_search = "https://www.googleapis.com/youtube/v3/search"
    
    # Calculate the temporal boundary
    cutoff_date = (datetime.utcnow() - timedelta(days=lookback_days)).strftime('%Y-%m-%dT%H:%M:%SZ')

    found_channels = []
    print("🔍 Starting Category-filtered mining (Tech)...")

    for query in queries:
        print(f"Searching for videos in the Tech category about: '{query}'")

        # Parameter dictionary updated with the metadata barrier
        params = {
            'part': 'snippet',
            'q': query,
            'maxResults': max_results_per_query,
            'publishedAfter': cutoff_date,
            'order': 'relevance',
            'type': 'video',
            'videoCategoryId': '28', # <- THE FILTER: Requires the video to be Science/Technology
            'key': api_key
        }
        
        response = requests.get(url_search, params=params)
        
        if response.status_code != 200:
            print(f"API Error when searching for '{query}': {response.status_code}")
            continue
            
        items = response.json().get('items', [])
        
        for item in items:
            channel_id = item['snippet']['channelId']
            channel_name = item['snippet']['channelTitle']
            found_channels.append((channel_id, channel_name))

    # Step 2: Consolidation and Ranking (The Mathematical Foundation)
    # Here we use Counter to count how many times each channel appeared in the results.
    # If a channel made 3 videos that ranked well for our queries, it is more relevant.
    channel_counts = Counter(found_channels)
    
    # Prepare data for visualization with Pandas
    ranking_data = []
    for (channel_id, channel_name), frequency in channel_counts.most_common():
        ranking_data.append({
            'Channel Name': channel_name,
            'Channel ID': channel_id,
            'Trending Videos in Niche': frequency,
            'Channel Link': f"https://www.youtube.com/channel/{channel_id}"
        })
        
    df_channels = pd.DataFrame(ranking_data)
    return df_channels

# ==========================================
# Script Execution Point
# ==========================================
if __name__ == "__main__":
    # We define the terms that matter to Developer Girls (Kept in Portuguese to target local creators)
    tech_terms = [
        "engenharia de dados",
        "backend python",
        "inteligência artificial generativa",
        "cloud computing aws",
        "mulheres na tecnologia"
    ]
    
    # Execute the function
    df_result = mine_channels_by_niche(queries=tech_terms, lookback_days=30)
    
    if not df_result.empty:
        print("\n🏆 TOP CHANNELS DISCOVERED FOR YOUR WHITELIST:")
        print("-" * 60)
        # Shows the 15 most recurring channels
        print(df_result.head(15).to_string(index=False))
        
        # Saves the result so you can analyze it calmly
        os.makedirs("data", exist_ok=True)

        # Updated filename to English
        df_result.to_csv("data/new_discovered_channels.csv", index=False)
        print("\n✅ Full report saved at: data/new_discovered_channels.csv")
    else:
        print("No data returned. Check your API Key and internet connection.")