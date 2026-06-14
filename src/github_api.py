import requests

def fetch_trending_github_repos():
    """Fetches trending repositories from GitHub API."""
    url = "https://api.github.com/search/repositories"
    # Busca repositórios criados nos últimos 7 dias com mais estrelas
    params = {
        'q': 'created:>2026-06-07',
        'sort': 'stars',
        'order': 'desc'
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        repos = []
        for item in data.get('items', [])[:5]:
            repos.append({
                'title': item.get('name', ''),
                'channel': item.get('owner', {}).get('login', ''),
                'url': item.get('html_url', ''),
                'type': 'github_repo'
            })
        return repos
    except Exception as e:
        print(f"❌ Error fetching GitHub data: {e}")
        return []