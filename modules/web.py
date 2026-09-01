# modules/web.py
import requests
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS

def web_search(query: str) -> str:
    """İnternette arama yapar ve ilk 3 sonucun başlık ile özetini getirir."""
    try:
        results = []
        with DDGS() as ddgs:
            search_results = list(ddgs.text(query, max_results=3))
            
            for res in search_results:
                title = res.get('title', '')
                snippet = res.get('body', '')
                url = res.get('href', '')
                results.append(f"Başlık: {title}\nLink: {url}\nÖzet: {snippet}")
                
        if not results:
            return "Arama sonucunda bilgi bulunamadı."
            
        return "\n\n---\n\n".join(results)
    except Exception as e:
        return f"Arama yapılırken hata oluştu: {e}"

def fetch_web_page(url: str) -> str:
    """Verilen spesifik bir web sayfasının başlığını ve içeriğini çeker."""
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.title.string if soup.title else "Başlık Yok"
        
        paragraphs = [p.get_text() for p in soup.find_all('p')[:3]]
        content = " ".join(paragraphs)
        
        return f"Sayfa Başlığı: {title}\nİçerik Özeti: {content[:500]}"
    except Exception as e:
        return f"Web sayfası okunamadı: {e}"