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
## 📌 Overview
**Tech Trends Curator** is a robust, **stateful Data Engineering pipeline** that automates content curation. It identifies technical trends by calculating **Thermal Velocity (Momentum)** and provides **comparative growth insights** by leveraging historical data stored in a local SQLite database. It moves beyond raw view counts to highlight technologies that are *accelerating* in the developer community.

## 🏗️ Architecture & Fundamentals
The system is built on solid data engineering principles:

1. **Extraction (Shift-Left Filtering):**
   * Aggregates multi-source data from **YouTube** (via whitelist), **GitHub** (Trending Repos), and the **Hacker News API** (Top Stories).
   * Enforces metadata barriers to prioritize high-signal technical content.

2. **Stateful Transformation (Persistence & Math):**
   * **Persistence Layer:** Uses `SQLite` to maintain a local knowledge base (`curator_data.db`) of processed items. This enables **stateful deduplication**, ensuring unique items are reported only once within a 7-day window.
   * **Momentum & Velocity:** Calculates engagement velocity ($Momentum$) and compares current metrics against historical averages to generate growth insights (e.g., *🚀 Rising Fast*).

3. **NLP & Insight Generation:**
   * Uses regex-based entity extraction and a bilingual stopword dictionary to isolate relevant tech stacks from generic content titles.

## 🛤️ Future Roadmap
* **Advanced Analytics:** Integrate a dashboard (e.g., Streamlit) to visualize long-term trends from the SQLite database.
* **AI Summarization:** Leverage an LLM API to generate human-readable technical summaries for each trending repo/video.
* **Cloud Native:** Deploy via containerization (Docker) on serverless infrastructure.

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
---

## 👩‍💻 About the Author

**Ana Paula Lapas Leão** | *Systems Architecture & Predictive Modeling*

Passionate about building scalable data pipelines, predictive models, and automating workflows. I actively maintain codebases, optimize data systems, and advocate for more women in the technology sector.

📫 **Let's connect:** [LinkedIn - Ana Paula Leão](https://www.linkedin.com/in/ana-paula-leao)
