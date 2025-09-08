from flask import Flask, render_template_string
from scrapers import scrape_ai_news_aggregated
from summarize import summarize_text
from dateutil import parser
import json

app = Flask(__name__)

def format_date(date_str):
    try:
        dt = parser.parse(date_str)
        day = dt.day
        if 4 <= day <= 20 or 24 <= day <= 30:
            suffix = "th"
        else:
            suffix = ["st", "nd", "rd"][day % 10 - 1]
        formatted = dt.strftime(f"%B {day}{suffix}, %Y")
        if dt.hour or dt.minute:
            formatted += dt.strftime(" – %I:%M %p").lstrip("0")
        return formatted
    except Exception:
        return date_str

@app.route('/')
def dashboard():
    print(" Starting to collect articles from all AI sources...")
    
    
    articles = scrape_ai_news_aggregated(limit_per_source=3)
    
   
    processed_articles = []
    for article in articles:
        try:
           
            summary = summarize_text(article["text"][:1000])
            
            processed_articles.append({
                "title": article["title"],
                "link": article["link"],
                "date": format_date(article["date"]),
                "summary": summary,
                "source": article["source"],
                "gradient": article["gradient"],
                "bg_gradient": article["bg_gradient"],
                "icon": article["icon"]
            })
        except Exception as e:
            print(f"Error processing article: {e}")
            continue
    
    print(f" Successfully processed {len(processed_articles)} articles!")
    
   
    sources = list(set(article["source"] for article in processed_articles))
    
    return render_template_string(HTML_TEMPLATE, 
                                  articles=processed_articles, 
                                  total_articles=len(processed_articles),
                                  total_sources=len(sources))


HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Trends Dashboard - Multi-Source</title>
    <link href="https://fonts.googleapis.com/css2?family=Quicksand:wght@400;500;600;700&display=swap" rel="stylesheet">


    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

       body {
        font-family: 'Quicksand', sans-serif;
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #334155 100%);
        color: white;
        min-height: 100vh;
        overflow-x: hidden;
    }

        /* Animated Background */
        .bg-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: 
                radial-gradient(circle at 20% 80%, rgba(120, 119, 198, 0.3) 0%, transparent 50%),
                radial-gradient(circle at 80% 20%, rgba(255, 119, 198, 0.3) 0%, transparent 50%),
                radial-gradient(circle at 40% 40%, rgba(120, 219, 255, 0.2) 0%, transparent 50%);
            animation: bgFloat 20s ease-in-out infinite;
            pointer-events: none;
            z-index: -1;
        }

        @keyframes bgFloat {
            0%, 100% { transform: rotate(0deg) scale(1); }
            50% { transform: rotate(180deg) scale(1.1); }
        }

        /* Container */
        .container {
            max-width: 1600px;
            margin: 0 auto;
            padding: 2rem;
        }

        /* Hero Section */
        .hero {
            text-align: center;
            margin-bottom: 4rem;
            padding: 4rem 2rem;
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(20px);
            border-radius: 2rem;
            border: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: 0 25px 50px rgba(0, 0, 0, 0.3);
        }

        .hero h1 {
            font-size: clamp(2.5rem, 5vw, 4rem);
            font-weight: 800;
            margin-bottom: 1rem;
            background: linear-gradient(135deg, #fff 0%, #e2e8f0 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .hero p {
            font-size: 1.25rem;
            color: rgba(255, 255, 255, 0.8);
            max-width: 700px;
            margin: 0 auto 2rem auto;
            line-height: 1.6;
        }

        .stats {
            display: flex;
            justify-content: center;
            gap: 3rem;
            flex-wrap: wrap;
            margin-top: 2rem;
        }

        .stat {
            text-align: center;
        }

        .stat-number {
            font-size: 2.5rem;
            font-weight: 700;
            display: block;
            background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .stat-label {
            font-size: 0.875rem;
            color: rgba(255, 255, 255, 0.6);
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-top: 0.5rem;
        }

        /* Section Title */
        .section-title {
            text-align: center;
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 3rem;
            position: relative;
        }

        .section-title::after {
            content: '';
            display: block;
            width: 100px;
            height: 4px;
            background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
            margin: 1rem auto;
            border-radius: 2px;
        }

        /* RESPONSIVE GRID - More articles */
        .articles-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 2rem;
            margin: 2rem 0;
        }

        /* Ensure minimum 3 columns on large screens */
        @media (min-width: 1200px) {
            .articles-grid {
                grid-template-columns: repeat(3, 1fr);
            }
        }

        @media (min-width: 1600px) {
            .articles-grid {
                grid-template-columns: repeat(4, 1fr);
            }
        }

        @media (max-width: 768px) {
            .articles-grid {
                grid-template-columns: 1fr;
                gap: 1.5rem;
            }
            
            .container {
                padding: 1rem;
            }
            
            .hero {
                padding: 2rem 1rem;
            }
        }

        /* Article Cards */
        .card {
            background: rgba(255, 255, 255, 0.08);
            backdrop-filter: blur(20px);
            border-radius: 1.5rem;
            padding: 2rem;
            border: 1px solid rgba(255, 255, 255, 0.1);
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
            min-height: 400px;
            display: flex;
            flex-direction: column;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
            opacity: 0;
            transform: translateY(30px);
        }

        .card.animate {
            opacity: 1;
            transform: translateY(0);
        }

        .card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            border-radius: 1.5rem 1.5rem 0 0;
        }

        .card:hover {
            transform: translateY(-8px);
            box-shadow: 0 32px 60px rgba(0, 0, 0, 0.4);
            border-color: rgba(255, 255, 255, 0.2);
        }

        .card-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 1.5rem;
            flex-wrap: wrap;
            gap: 1rem;
        }

        .source-badge {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.75rem 1.25rem;
            border-radius: 2rem;
            font-size: 0.875rem;
            font-weight: 600;
            color: white;
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
        }

        .date {
            font-size: 0.875rem;
            color: rgba(255, 255, 255, 0.6);
            font-weight: 500;
        }

        .card-title {
            font-size: 1.25rem;
            font-weight: 600;
            line-height: 1.4;
            margin: 0 0 1rem 0;
            color: #fff;
            display: -webkit-box;
            -webkit-line-clamp: 3;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }

        .card-title a {
            text-decoration: none;
            color: inherit;
            transition: color 0.3s ease;
        }

        .card-title a:hover {
            color: #fbbf24;
        }

        .card-summary {
            flex: 1;
            font-size: 0.95rem;
            line-height: 1.6;
            color: rgba(255, 255, 255, 0.8);
            margin-bottom: 1.5rem;
            display: -webkit-box;
            -webkit-line-clamp: 4;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }

        .read-more {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.875rem 1.5rem;
            color: white;
            text-decoration: none;
            border-radius: 0.875rem;
            font-weight: 600;
            font-size: 0.875rem;
            transition: all 0.3s ease;
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
            align-self: flex-start;
        }

        .read-more:hover {
            transform: translateY(-2px);
            box-shadow: 0 12px 24px rgba(0, 0, 0, 0.4);
        }

        .arrow {
            transition: transform 0.3s ease;
        }

        .read-more:hover .arrow {
            transform: translateX(4px);
        }

        /* Loading state */
        .loading {
            text-align: center;
            padding: 4rem;
            color: rgba(255, 255, 255, 0.6);
        }
    </style>
</head>
<body>
    <div class="bg-overlay"></div>
    
    <div class="container">
        <!-- Hero Section -->
        <div class="hero">
            <h1> AI Trends Dashboard</h1>
            <p>Comprehensive AI insights from HuggingFace, arXiv, TechCrunch, OpenAI, MIT, VentureBeat & Towards DS</p>
            <div class="stats">
                <div class="stat">
                    <span class="stat-number" data-target="{{ total_articles }}">0</span>
                    <span class="stat-label">Articles</span>
                </div>
                <div class="stat">
                    <span class="stat-number" data-target="{{ total_sources }}">0</span>
                    <span class="stat-label">Sources</span>
                </div>
                <div class="stat">
                    <span class="stat-number">Live</span>
                    <span class="stat-label">Updates</span>
                </div>
            </div>
        </div>

        <!-- Section Title -->
        <h2 class="section-title">Latest AI Insights from Multiple Sources</h2>

        {% if articles %}
        <!-- Articles Grid -->
        <div class="articles-grid" id="articles-grid">
            {% for article in articles %}
            <div class="card">
                <div style="position: absolute; top: 0; left: 0; right: 0; height: 4px; background: {{ article.gradient }}; border-radius: 1.5rem 1.5rem 0 0;"></div>
                
                <div class="card-header">
                    <div class="source-badge" style="background: {{ article.gradient }};">
                        <span>{{ article.icon }}</span>
                        <span>{{ article.source }}</span>
                    </div>
                    <div class="date">{{ article.date }}</div>
                </div>
                
                <h3 class="card-title">
                    <a href="{{ article.link }}" target="_blank">{{ article.title }}</a>
                </h3>
                
                <p class="card-summary">{{ article.summary }}</p>
                
                <a href="{{ article.link }}" target="_blank" class="read-more" style="background: {{ article.gradient }};">
                    Read Full Article
                    <span class="arrow">→</span>
                </a>
            </div>
            {% endfor %}
        </div>
        {% else %}
        <div class="loading">
            <h3> Loading articles from all AI sources...</h3>
            <p>This might take a moment as we gather the latest insights.</p>
        </div>
        {% endif %}
    </div>

    <script>
        // Animate counter
        function animateCounter(element, target) {
            let current = 0;
            const increment = target / 40;
            const timer = setInterval(() => {
                current += increment;
                if (current >= target) {
                    element.textContent = target;
                    clearInterval(timer);
                } else {
                    element.textContent = Math.ceil(current);
                }
            }, 30);
        }

        // Initialize animations
        document.addEventListener('DOMContentLoaded', function() {
            // Animate cards with staggered timing
            const cards = document.querySelectorAll('.card');
            cards.forEach((card, index) => {
                setTimeout(() => {
                    card.classList.add('animate');
                }, index * 100);
            });
            
            // Animate counters
            setTimeout(() => {
                document.querySelectorAll('[data-target]').forEach(el => {
                    const target = parseInt(el.dataset.target);
                    if (!isNaN(target)) {
                        animateCounter(el, target);
                    }
                });
            }, 500);
        });
    </script>
</body>
</html>
'''

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)