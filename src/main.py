import sqlite3
from datetime import datetime, timedelta
from src.youtube_api import fetch_recent_whitelist_videos
from src.github_api import fetch_trending_github_repos
from src.hackernews_api import fetch_trending_hackernews_posts
from src.nlp_processor import process_trends
from src.email_notifier import send_email_report

def init_db():
    conn = sqlite3.connect('curator_data.db')
    cursor = conn.cursor()
    # Using 'trend_logs' to store title, source, metrics, and timestamp
    cursor.execute('''CREATE TABLE IF NOT EXISTS trend_logs
                      (title TEXT, source TEXT, views INTEGER, likes INTEGER, sent_at TEXT)''')
    conn.commit()
    conn.close()

def is_already_sent(title):
    conn = sqlite3.connect('curator_data.db')
    cursor = conn.cursor()
    seven_days_ago = (datetime.now() - timedelta(days=7)).isoformat()
    # Querying the same table we log into: 'trend_logs'
    cursor.execute('SELECT 1 FROM trend_logs WHERE title=? AND sent_at > ?', (title, seven_days_ago))
    exists = cursor.fetchone()
    conn.close()
    return exists is not None

def log_sent_item(item):
    conn = sqlite3.connect('curator_data.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO trend_logs (title, source, views, likes, sent_at)
                      VALUES (?, ?, ?, ?, ?)''',
                   (item.get('title'), item.get('type', 'unknown'),
                    item.get('views', 0), item.get('likes', 0),
                    datetime.now().isoformat()))
    conn.commit()
    conn.close()

def format_email_report(df_trends, topics, gh_data, rd_data):
    text = "Olá, Liderança da Developer Girls! 💜\n"
    text += "Aqui está o radar técnico desta semana.\n\n"

    text += "🔥 PALAVRAS-CHAVE EM ALTA:\n"
    for theme, freq in topics:
        text += f" - {theme.upper()} (Mencionada em {freq} fontes)\n"

    text += "\n🎬 TOP 3 ITENS DE ALTO MOMENTUM:\n"
    for _, row in df_trends.head(3).iterrows():
        status = get_growth_status(row['title'], row.get('views', 0))
        item_type = row.get('type', 'youtube')
        link = row.get('url', 'N/A') if item_type != 'youtube' else f"[https://youtu.be/](https://youtu.be/){row.get('video_id', '')}"

        text += f"\n📌 Assunto: {row['title']} [{status}]\n"
        text += f"👩‍💻 Fonte: {row['channel']} | 🔗 Acessar: {link}\n"
        text += "-" * 40

    text += "\n\nRelatório gerado automaticamente pelo seu Tech Trends Curator. Mande sugestões e tire dúvidas a partir de https://www.linkedin.com/in/ana-paula-leao/"
    return text

def get_growth_status(title, current_views):
    avg_views = get_historical_stats(title)
    if avg_views == 0:
        return "🆕 New Trend"

    growth = ((current_views - avg_views) / avg_views) * 100
    if growth > 20:
        return f"🚀 Rising Fast (+{int(growth)}%)"
    elif growth < -20:
        return "📉 Cooling Down"
    return "📈 Steady"

def execute_pipeline():
    init_db()
    print("Starting data ingestion...")

    # 1. Collect
    raw_data = fetch_recent_whitelist_videos() + fetch_trending_github_repos() + fetch_trending_hackernews_posts()

    # 2. Filter using Database
    curated_data = [item for item in raw_data if item.get('title') and not is_already_sent(item['title'])]

    if not curated_data:
        print("No new unique items found.")
        return
        
    # 3. Process & Report
    df_trends, topics = process_trends(curated_data)
    email_body = format_email_report(df_trends, topics, fetch_trending_github_repos(), fetch_trending_hackernews_posts())
    send_email_report(email_body)

    # 4. Log to DB
    for item in curated_data:
        log_sent_item(item)
    print("Items successfully logged to database.")

if __name__ == "__main__":
    execute_pipeline()