# modules/web.py
import ipaddress
import socket
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup
try:
    from duckduckgo_search import DDGS
except ImportError:  # package renamed to `ddgs` in recent releases
    from ddgs import DDGS


_BLOCKED_HOSTS = {"localhost", "localhost.localdomain"}


def _is_safe_url(url: str) -> bool:
    """Allow public HTTP(S) URLs and reject local/private network targets."""
    try:
        parsed = urlparse(url)
        if parsed.scheme not in {"http", "https"} or not parsed.hostname:
            return False

        hostname = parsed.hostname.rstrip(".").casefold()
        if hostname in _BLOCKED_HOSTS or hostname.endswith(".localhost"):
            return False

        # Resolve hostnames so private/loopback/link-local IPs cannot be reached.
        addresses = socket.getaddrinfo(hostname, None, type=socket.SOCK_STREAM)
        for address in {item[4][0] for item in addresses}:
            ip = ipaddress.ip_address(address)
            if (
                ip.is_private
                or ip.is_loopback
                or ip.is_link_local
                or ip.is_reserved
                or ip.is_multicast
                or ip.is_unspecified
            ):
                return False
        return True
    except (ValueError, socket.gaierror):
        return False


def web_search(query: str) -> str:
    """İnternette arama yapar ve ilk 3 sonucun başlık ile özetini getirir."""
    if not isinstance(query, str) or not query.strip():
        return "Arama sorgusu boş olamaz."

    try:
        results = []
        with DDGS() as ddgs:
            search_results = list(ddgs.text(query, max_results=3))
            for res in search_results:
                title = res.get("title", "")
                snippet = res.get("body", "")
                url = res.get("href", "")
                results.append(f"Başlık: {title}\nLink: {url}\nÖzet: {snippet}")

        if not results:
            return "Arama sonucunda bilgi bulunamadı."
        return "\n\n---\n\n".join(results)
    except Exception:
        return "Arama yapılırken bir hata oluştu."


def fetch_web_page(url: str) -> str:
    """Fetch a public HTTP(S) web page with SSRF protection."""
    if not isinstance(url, str) or not url.strip():
        return "Web sayfası okunamadı: Güvenlik nedeniyle bu URL'ye erişim engellendi."

    try:
        headers = {"User-Agent": "TalhaGPT/1.0"}
        current = url.strip()
        response = None
        max_redirects = 5

        for _ in range(max_redirects + 1):
            if not _is_safe_url(current):
                return (
                    "Web sayfası okunamadı: "
                    "Güvenlik nedeniyle bu URL'ye erişim engellendi."
                )
            response = requests.get(
                current,
                headers=headers,
                timeout=5,
                allow_redirects=False,
            )
            if response.is_redirect or response.is_permanent_redirect:
                location = response.headers.get("Location", "")
                if not location:
                    return "Web sayfası okunamadı: İstek başarısız oldu."
                current = urljoin(current, location)
                continue
            response.raise_for_status()
            break
        else:
            return "Web sayfası okunamadı: Çok fazla yönlendirme."

        if response is None:
            return "Web sayfası okunamadı: İstek başarısız oldu."

        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.title.string.strip() if soup.title and soup.title.string else "Başlık Yok"
        paragraphs = [p.get_text(" ", strip=True) for p in soup.find_all("p")[:3]]
        content = " ".join(paragraphs)

        return f"Sayfa Başlığı: {title}\nİçerik Özeti: {content[:500]}"
    except requests.RequestException:
        return "Web sayfası okunamadı: İstek başarısız oldu."
    except Exception:
        return "Web sayfası okunamadı: Beklenmeyen bir hata oluştu."
