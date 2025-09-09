# AI Trends Dashboard

A comprehensive AI news aggregator that collects and summarizes articles from multiple sources including HuggingFace, arXiv, TechCrunch, OpenAI, MIT, VentureBeat, and Towards Data Science.

##  Features

- **Multi-source aggregation**: Pulls from 5+ AI news sources
- **AI-powered summaries**: Automatically summarizes articles using GPT-4o-mini
- **Beautiful responsive design**: Modern glassmorphism UI with animations
- **Real-time updates**: Fresh content every time you visit
- **Source attribution**: Clear source badges and links

##  Quick Start

### Prerequisites

- Python 3.8+
- OpenAI API key

### Installation

1. **Download all files to a folder**

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up OpenAI API key**
   
   Create a `.env` file and add your key:
   ```
   OPENAI_API_KEY=your_actual_openai_key_here
   ```
   
   Get your key from: https://platform.openai.com/api-keys

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open browser**
   ```
   http://localhost:8000
   ```

##  Dependencies (requirements.txt)

```
Flask==2.3.3
python-dateutil==2.8.2
beautifulsoup4==4.12.2
requests==2.31.0
openai==1.3.0
python-dotenv==1.0.0
lxml==4.9.3
urllib3==2.0.7
certifi==2023.11.17
streamlit
plotly
pandas
Pillow
```

##  File Structure

```
ai-trends-dashboard/
├── app.py              # Main Flask application
├── scrapers.py         # Web scraping functions
├── summarize.py        # AI summarization logic
├── requirements.txt    # Python dependencies
├── .env               # Your OpenAI API key
└── README.md          # This file
```

##  News Sources

| Source | Content Focus |
|--------|---------------|
| 🤗 HuggingFace | ML models, datasets |
| 📄 arXiv | Research papers (cs.AI) |
| 🚀 TechCrunch | AI industry news |
| 🧠 OpenAI | Company updates |
| 🎓 MIT News | Academic research |
| 💼 VentureBeat | Business & funding |
| 📊 Towards DS | Technical tutorials |

##  Performance Notes

- First load takes 30-90 seconds (scraping + AI summarization)
- Each visit fetches fresh content
- Works on desktop and mobile browsers

##  Customization

- **Change article limit**: Edit `limit_per_source=3` in `app.py`
- **Modify sources**: Add/remove scrapers in `scrapers.py`
- **Adjust summaries**: Change word limit in `summarize.py`



---

**Enjoy your AI news dashboard! 🎉**
