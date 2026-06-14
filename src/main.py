from src.youtube_api import fetch_recent_whitelist_videos
from src.nlp_processor import process_trends
from src.email_notifier import send_email_report

def format_email_report(df_trends, topics):
    """Transforms the DataFrames into a friendly text payload for the email."""

    text = "Olá, Liderança da Developer Girls! 💜\n"
    text += "Aqui estão os gatilhos de conteúdo mapeados nesta semana:\n\n"

    text += "🔥 TERMOS MAIS QUENTES (Keywords):\n"
    for theme, freq in topics:
        text += f" - {theme.upper()} (apareceu em {freq} vídeos de alto engajamento)\n"

    text += "\n🎬 TOP 3 VÍDEOS (Maior Momentum / Velocidade de Engajamento):\n"
    top_3 = df_trends.head(3)

    for _, row in top_3.iterrows():
        text += f"\n📌 Título: {row['title']}\n"
        text += f"👩‍💻 Canal: {row['channel']}\n"
        text += f"⚡ Score de Momentum: {row['momentum_score']:.1f}\n"
        text += f"📊 Views: {row['views']} | Likes: {row['likes']}\n"
        text += "-" * 40

    text += "\n\nRelatório gerado automaticamente pelo seu Curador de Dados."
    return text

def execute_pipeline():
    # System logs in English for developers/DevOps
    print("Starting Whitelist scan...")
    raw_data = fetch_recent_whitelist_videos()
    
    if not raw_data:
        print("No new videos found in the mapped channels.")
        return
        
    print(f"Extracted {len(raw_data)} videos. Analyzing Momentum and Topics...")
    df_trends, topics = process_trends(raw_data)
    
    # Format the data into an email body
    print("Formatting email payload...")
    email_body = format_email_report(df_trends, topics)

    # Print to terminal for debugging
    print(email_body)

    # Trigger the email module
    print("Sending email to leadership...")
    send_email_report(email_body)

# Python's standard entry point
if __name__ == "__main__":
    execute_pipeline()