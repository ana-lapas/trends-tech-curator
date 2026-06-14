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
        # Se for um item do GitHub ou Reddit, ele tem campos diferentes
        # Usamos .get() para evitar KeyError
        # Dentro do loop de Data Transformation no nlp_processor.py
        video_list.append({
            'title': item.get('title', ''),
            'channel': item.get('channel', 'Unknown'),
            'published_date': item.get('published_date', None),
            'views': int(item.get('statistics', {}).get('viewCount', 0)),
            'likes': int(item.get('statistics', {}).get('likeCount', 0)),
            'video_id': item.get('id', ''),
            'url': item.get('url', ''),        # <--- ESSENCIAL
            'type': item.get('type', 'youtube') # <--- ESSENCIAL
        })
        
    df = pd.DataFrame(video_list)
    
    # 2. Momentum Calculation (Engagement per hour of life)
    now = datetime.now(timezone.utc)
    
    # Converter para datetime, forçando fuso UTC
    df['published_date'] = pd.to_datetime(df['published_date'], utc=True)

    # Definir agora e preencher NaT com agora para itens sem data
    now = datetime.now(timezone.utc)
    df['published_date'] = df['published_date'].fillna(now)

    # Cálculo seguro da diferença em horas
    df['hours_alive'] = (now - df['published_date']).dt.total_seconds() / 3600
    
    # Evita divisão por zero em itens com o mesmo timestamp
    df['hours_alive'] = df['hours_alive'].replace(0, 0.1)

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