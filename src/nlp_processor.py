import pandas as pd
import re
from collections import Counter
from datetime import datetime, timedelta, timezone

def process_trends(json_data):
    """Calculates Momentum and extracts trending topics."""
    if not json_data:
        return None, []

    video_list = []
    
    # 1. Data Transformation
    for item in json_data:
        stats = item.get('statistics', {})
        snippet = item.get('snippet', {})
        
        video_list.append({
            'title': snippet.get('title', ''),
            'channel': snippet.get('channelTitle', ''),
            'published_date': snippet.get('publishedAt', ''),
            'views': int(stats.get('viewCount', 0)),
            'likes': int(stats.get('likeCount', 0))
        })
        
    df = pd.DataFrame(video_list)
    
    # 2. Momentum Calculation (Engagement per hour of life)
    df['published_date'] = pd.to_datetime(df['published_date'])
    now = pd.Timestamp.utcnow()
    
    # Calculate how many hours ago the video was published
    df['hours_alive'] = (now - df['published_date']).dt.total_seconds() / 3600
    df['hours_alive'] = df['hours_alive'].replace(0, 0.1) # Prevents DivisionByZero error
    
    # Vectorized calculation for the custom metric
    df['momentum_score'] = (
        (df['views'] / df['hours_alive']) * 1.5 +
        (df['likes'] / df['hours_alive']) * 2.0
    )
    
    # Sort by the "hottest" videos right now
    df = df.sort_values(by='momentum_score', ascending=False)
    
    # 3. Entity Extraction (Basic NLP)
    # Get the top 30% of videos with the highest momentum
    top_videos = df.head(max(3, int(len(df) * 0.3)))
    full_text = " ".join(top_videos['title'].tolist()).lower()
    
    # Regex to find words (alphanumeric and hyphens)
    words = re.findall(r'\b[a-z0-9-]+\b', full_text)

    # Bilingual Stopwords Dictionary + Jargon
    stopwords = {
        # Portuguese
        'de', 'para', 'com', 'em', 'um', 'uma', 'como', 'que', 'do', 'da', 'no', 'na', 'os', 'as', 'por', 'mais',
        # English
        'the', 'and', 'in', 'to', 'of', 'for', 'is', 'on', 'from', 'with', 'how', 'what', 'why', 'crash', 'course', 'build',
        # Generic video jargon
        'tutorial', 'curso', 'completo', 'video', 'parte', 'step'
    }

    # List comprehension to filter out stopwords and short artifacts
    cleaned_words = [w for w in words if w not in stopwords and len(w) > 2]
    
    trending_topics = Counter(cleaned_words).most_common(5)
    
    return df, trending_topics