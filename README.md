# 🚀 Tech Trends Curator: Data-Driven Content Strategy Pipeline

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Data Engineering](https://img.shields.io/badge/Data_Engineering-ETL-orange.svg)
![NLP](https://img.shields.io/badge/NLP-Entity_Extraction-green.svg)

## 📌 Overview
The technology ecosystem suffers from severe information overload. For tech communities—specifically those advocating for women in STEM—manually curating high-quality, up-to-date content requires immense cognitive load and hours of research. 

**Tech Trends Curator** is a stateless Data Engineering pipeline that automates this curation. It moves beyond "lagging indicators" (like raw view counts) by calculating the **Thermal Velocity (Momentum)** of recent publications and applying **Natural Language Processing (NLP)** to extract genuine technical trends before they become mainstream noise.

## 💡 Business Value
* **Reduces Cognitive Load:** Transforms hours of manual YouTube/forum research into an automated, actionable weekly email.
* **Noise Reduction (Data Quality):** Filters out generic tech news and clickbait by applying strict *Data Quality Gates* and *Shift-Left Filtering*.
* **Empowers Communities:** Delivers highly targeted, ready-to-use content triggers to community leadership, ensuring discussions remain deeply technical and relevant.

## 🏗️ Architecture & Fundamentals

The system is built on solid data architecture principles:

1. **Extraction (Shift-Left Filtering):**
   * Uses the YouTube Data API v3 but enforces metadata barriers (`videoCategoryId: 28` - Science & Technology) at the request level, preventing gossip/news channels from entering the pipeline and saving API quota.
   * Relies on a dynamic **Whitelist** of highly vetted global and local creators, ignoring the platform's standard (and biased) recommendation algorithm.

2. **Transformation (Vectorized Math & NLP):**
   * **Momentum Algorithm:** Uses `pandas` to calculate an engagement-per-hour score ($Score = \frac{Views}{Hours\_Alive} \times 1.5 + \frac{Likes}{Hours\_Alive} \times 2.0$), identifying what is gaining traction *right now*.
   * **Entity Extraction:** Uses regex and a custom bilingual stopword dictionary (English/Portuguese) to filter out common verbs and jargon, isolating the actual technologies (e.g., *Claude, Python, Kubernetes*).

3. **Load / Notification (Stateless SMTP):**
   * Packages the processed insights into a MIME/SMTP payload.
   * Securely dispatches the report to a distribution list via environment variables.

## ⚙️ Infrastructure & How to Run

This application is designed to be easily containerized and deployed in any cloud environment.

### Prerequisites
* Python 3.10+
* A valid YouTube Data API Key
* An App Password from a Gmail account

### Local Setup
1. Clone the repository:
   ```bash
     git clone [https://github.com/your-username/trends-tech-curator.git](https://github.com/your-username/trends-tech-curator.git)
     cd trends-tech-curator
   
2. Create and activate a virtual environment:
   ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use: venv\Scripts\activate

3. Install dependencies:
   ```bash
     pip install -r requirements.txt

4. Configure your .env file at the root of the project:
   ```bash
      YOUTUBE_API_KEY=your_api_key_here
      SENDER_EMAIL=your_email@gmail.com
      EMAIL_PASSWORD=your_16_digit_app_password
      RECEIVER_EMAILS=target1@email.com, target2@email.com
   ```

5. Run the orchestrator:  
   ```bash
    python -m src.main
## 🛤️ Future Roadmap

* **Dockerization:** Wrap the application in a `Dockerfile` and `docker-compose.yml` for isolated execution.
* **CI/CD Automation:** Implement GitHub Actions to trigger the pipeline automatically every Monday morning via cron jobs.
* **Stateful Architecture:** Integrate a PostgreSQL database to track time-series data and prove the longevity of a trend.

---

## 👩‍💻 About the Author

**Ana Paula Lapas Leão** | *Systems Architecture & Predictive Modeling*

Passionate about building scalable data pipelines, predictive models, and automating workflows. I actively maintain codebases, optimize data systems, and advocate for more women in the technology sector.

📫 **Let's connect:** [LinkedIn - Ana Paula Leão](https://www.linkedin.com/in/ana-paula-leao)
