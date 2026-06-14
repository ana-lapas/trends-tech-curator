import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def send_email_report(content_text):
    """Sends the formatted content triggers via SMTP connection to multiple receivers."""
    
    # Fetch credentials securely from the environment
    sender_email = os.getenv("SENDER_EMAIL")
    app_password = os.getenv("EMAIL_PASSWORD")
    
    # Puxa a string com todos os e-mails separados por vírgula
    receiver_emails = os.getenv("RECEIVER_EMAILS")

    if not sender_email or not app_password or not receiver_emails:
        print("Error: Email credentials or receivers missing in .env file.")
        return

    # MIME format structures the email payload
    message = MIMEMultipart()
    message['From'] = sender_email

    # O protocolo MIME aceita perfeitamente uma string separada por vírgulas aqui
    message['To'] = receiver_emails

    message['Subject'] = "🚀 Gatilhos de Conteúdo Tech - Curadoria Semanal"

    # Attach the plain text body to the email
    message.attach(MIMEText(content_text, 'plain'))

    try:
        # Connect to Gmail's SMTP server on secure port 587
        server = smtplib.SMTP('smtp.gmail.com', 587)
        
        # Establish a TLS (Transport Layer Security) encryption layer
        server.starttls() 
        
        # Authentication and sending
        server.login(sender_email, app_password)

        # O send_message lê automaticamente o campo 'To' e dispara para todos da lista
        server.send_message(message)
        server.quit()
        
        print("✅ Email successfully sent to the distribution list!")
        
    except Exception as e:
        print(f"❌ Failed to send email: {e}")