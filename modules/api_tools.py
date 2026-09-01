# modules/api_tools.py

import urllib.request
import urllib.parse
import json


def get_weather(city: str = "Ankara") -> str:
    """wttr.in servisinden hava durumunu alır ve temiz metin döndürür."""

    try:
        url = f"https://wttr.in/{urllib.parse.quote(city)}?format=j1&lang=tr"

        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "TalhaGPT/1.0"
            }
        )

        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(
                response.read().decode("utf-8")
            )

        current = data["current_condition"][0]

        temp = current.get("temp_C", "?")
        feels = current.get("FeelsLikeC", "?")
        humidity = current.get("humidity", "?")

        weather_desc = current.get(
            "lang_tr",
            current.get(
                "weatherDesc",
                [{"value": "Bilinmiyor"}]
            )
        )

        if isinstance(weather_desc, list):
            description = weather_desc[0].get(
                "value",
                "Bilinmiyor"
            )
        else:
            description = str(weather_desc)

        return (
            f"[Hava Durumu]\n"
            f"Şehir: {city}\n"
            f"Sıcaklık: {temp}°C\n"
            f"Hissedilen: {feels}°C\n"
            f"Durum: {description}\n"
            f"Nem: %{humidity}"
        )

    except Exception as e:
        return (
            f"[Hava Durumu Hatası]: "
            f"Hava durumu alınamadı: {e}"
        )