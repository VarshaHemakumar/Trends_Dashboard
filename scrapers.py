import requests
from bs4 import BeautifulSoup
import time

def scrape_huggingface_blog(limit=3):
    url = "https://huggingface.co/blog/feed.xml"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml-xml")
    articles = []
    items = soup.find_all("item", limit=limit)
    for item in items:
        title = item.title.text if item.title else "No title"
        link = item.link.text if item.link else "#"
        pub_date = item.pubDate.text if item.pubDate else "Unknown date"
        
        text = ""
        if link and link != "#":
            try:
                article_resp = requests.get(link, timeout=10)
                article_soup = BeautifulSoup(article_resp.text, "html.parser")
                paragraphs = article_soup.find_all("p")
                text = " ".join(p.get_text(strip=True) for p in paragraphs)
            except:
                text = "Content unavailable"
        articles.append({
            "title": title.strip(),
            "link": link.strip(),
            "date": pub_date.strip(),
            "text": text if text else "No content available."
        })
    return articles

def scrape_arxiv(limit=3):
    url = (
        "https://export.arxiv.org/api/query?"
        "search_query=cat:cs.AI&sortBy=submittedDate&sortOrder=descending&max_results=" + str(limit)
    )
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml-xml")
    articles = []
    entries = soup.find_all("entry", limit=limit)
    for entry in entries:
        title = entry.title.text if entry.title else "No title"
        link = entry.id.text if entry.id else "#"
        summary = entry.summary.text if entry.summary else "No summary available."
        pub_date = entry.published.text if entry.published else "Unknown date"
        articles.append({
            "title": title.strip(),
            "link": link.strip(),
            "date": pub_date.strip(),
            "text": summary.strip()
        })
    return articles

def scrape_techcrunch_ai(limit=3):
    url = "https://techcrunch.com/tag/artificial-intelligence/feed/"
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "xml")
        articles = []
        items = soup.find_all("item", limit=limit)
        for item in items:
            title = item.title.text if item.title else "No title"
            link = item.link.text if item.link else "#"
            description = item.description.text if item.description else "No description available."
            pub_date = item.pubDate.text if item.pubDate else "Unknown date"
            articles.append({
                "title": title.strip(),
                "link": link.strip(),
                "date": pub_date.strip(),
                "text": description.strip()
            })
        return articles
    except:
        return []


def scrape_openai_blog(limit=3):
    """Scrape OpenAI Blog RSS"""
    url = "https://openai.com/blog/rss.xml"
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "xml")
        articles = []
        items = soup.find_all("item", limit=limit)
        for item in items:
            title = item.title.text if item.title else "No title"
            link = item.link.text if item.link else "#"
            description = item.description.text if item.description else "No description available."
            pub_date = item.pubDate.text if item.pubDate else "Unknown date"
            articles.append({
                "title": title.strip(),
                "link": link.strip(),
                "date": pub_date.strip(),
                "text": description.strip()
            })
        return articles
    except Exception as e:
        print(f"Error scraping OpenAI: {e}")
        return []

def scrape_mit_news_ai(limit=3):
    """Scrape MIT News AI section"""
    url = "https://news.mit.edu/rss/topic/artificial-intelligence2"
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "xml")
        articles = []
        items = soup.find_all("item", limit=limit)
        for item in items:
            title = item.title.text if item.title else "No title"
            link = item.link.text if item.link else "#"
            description = item.description.text if item.description else "No description available."
            pub_date = item.pubDate.text if item.pubDate else "Unknown date"
            articles.append({
                "title": title.strip(),
                "link": link.strip(),
                "date": pub_date.strip(),
                "text": description.strip()
            })
        return articles
    except Exception as e:
        print(f"Error scraping MIT News: {e}")
        return []

def scrape_venturebeat_ai(limit=3):
    """Scrape VentureBeat AI section - Updated with working RSS URL"""
    
    urls = [
        "https://feeds.feedburner.com/venturebeat/SZYF",  
        "https://venturebeat.com/feed/",  
        "https://venturebeat.com/category/ai/feed/"  
    ]
    
    for url in urls:
        try:
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.text, "xml")
            articles = []
            items = soup.find_all("item")[:limit] 
            
            ai_articles = []
            for item in items:
                title = item.title.text if item.title else "No title"
               
                if "ai/" in url or any(keyword in title.lower() for keyword in ['ai', 'artificial intelligence', 'machine learning', 'deep learning']):
                    link = item.link.text if item.link else "#"
                    description = item.description.text if item.description else "No description available."
                    pub_date = item.pubDate.text if item.pubDate else "Unknown date"
                    ai_articles.append({
                        "title": title.strip(),
                        "link": link.strip(),
                        "date": pub_date.strip(),
                        "text": description.strip()
                    })
                    if len(ai_articles) >= limit:
                        break
            
            if ai_articles: 
                return ai_articles
                
        except Exception as e:
            print(f"Error with VentureBeat URL {url}: {e}")
            continue
    
    print("All VentureBeat URLs failed")
    return []

def scrape_towards_data_science(limit=3):
    """Scrape Towards Data Science Medium feed (always returns latest N posts)"""
    url = "https://towardsdatascience.com/feed"
    try:
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/rss+xml, application/xml;q=0.9, */*;q=0.8"
        }
        response = requests.get(url, timeout=10, headers=headers)
        soup = BeautifulSoup(response.text, "xml")

        articles = []
        items = soup.find_all("item", limit=limit)

        for item in items:
            title = item.title.text if item.title else "No title"
            link = item.link.text if item.link else "#"
            description = item.description.text if item.description else "No description available."
            pub_date = item.pubDate.text if item.pubDate else "Unknown date"

            articles.append({
                "title": title.strip(),
                "link": link.strip(),
                "date": pub_date.strip(),
                "text": description.strip()
            })

        return articles
    except Exception as e:
        print(f"Error scraping TDS: {e}")
        return []


from dateutil import parser

def scrape_ai_news_aggregated(limit_per_source=2):
    """
    Aggregate AI news from all sources and sort by date
    """
    all_articles = []
    
    sources = [
        ("HuggingFace", scrape_huggingface_blog, "🤗", "linear-gradient(135deg, #FF6B35 0%, #FF8E53 100%)"),
        ("arXiv", scrape_arxiv, "📄", "linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)"),
        ("TechCrunch", scrape_techcrunch_ai, "🚀", "linear-gradient(135deg, #10b981 0%, #34d399 100%)"),
        ("OpenAI", scrape_openai_blog, "🧠", "linear-gradient(135deg, #00d4aa 0%, #00b4d8 100%)"),
        ("MIT News", scrape_mit_news_ai, "🎓", "linear-gradient(135deg, #8b0000 0%, #dc143c 100%)"),
        ("VentureBeat", scrape_venturebeat_ai, "💼", "linear-gradient(135deg, #ff6b6b 0%, #ffa500 100%)"),
        ("Towards DS", scrape_towards_data_science, "📊", "linear-gradient(135deg, #1a1a1a 0%, #333333 100%)")
    ]
    
    for source_name, scraper_func, icon, gradient in sources:
        try:
            print(f"Scraping {source_name}...")
            articles = scraper_func(limit_per_source)
            for article in articles:
                article['source'] = source_name
                article['icon'] = icon
                article['gradient'] = gradient
                article['bg_gradient'] = "linear-gradient(135deg, rgba(255,255,255,0.05) 0%, rgba(255,255,255,0.02) 100%)"
            all_articles.extend(articles)
            time.sleep(1)  
        except Exception as e:
            print(f"Failed to scrape {source_name}: {e}")
            continue
    
    
    def parse_date_safe(d):
        try:
            return parser.parse(d)
        except:
            return parser.parse("1970-01-01")  

    all_articles.sort(key=lambda x: parse_date_safe(x["date"]), reverse=True)
    
    return all_articles



def get_all_articles(limit_per_source=2):
    """Get all articles from all sources"""
    return scrape_ai_news_aggregated(limit_per_source)