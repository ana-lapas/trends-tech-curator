import requests

def fetch_trending_reddit_posts():
    """Fetches top stories from Hacker News (Open API, no auth required)."""
    url = "https://hacker-news.firebaseio.com/v0/topstories.json"
    
    try:
        # Pega os IDs dos top posts
        ids = requests.get(url, timeout=10).json()[:5]
        posts = []
        for id in ids:
            item_url = f"https://hacker-news.firebaseio.com/v0/item/{id}.json"
            item = requests.get(item_url, timeout=10).json()
            posts.append({
                'title': item.get('title', ''),
                'channel': 'Hacker News',
                'url': item.get('url', f"https://news.ycombinator.com/item?id={id}"),
                'type': 'reddit_post'
            })
        return posts
    except Exception as e:
        print(f"❌ Error fetching Hacker News data: {e}")
        return []