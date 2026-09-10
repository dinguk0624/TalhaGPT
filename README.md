# TalhaGPT 🤖

> **A local AI assistant built on top of Qwen3:8B.**

**Current version: [v0.3](https://github.com/dinguk0624/TalhaGPT/releases/tag/v0.3)**

TalhaGPT combines a local LLM with an agent loop, tool calling, persistent memory, RAG, web access, system tools, file reading, streaming output, image generation, and optional voice. 

**Qwen3:8B is the model. TalhaGPT is the assistant layer around it.**

## 🌐 Website

### [🚀 Try TalhaGPT Web Buddy](https://talha-gpt-web-buddy.lovable.app)
*Built with Loveable - Web UI for TalhaGPT*

---

## ✨ Highlights

- 🤖 Local AI through Ollama + Qwen3:8B
- ⚡ Streaming token output
- 🧠 Persistent conversation memory
- 🔎 ChromaDB + Sentence Transformers RAG
- 🛠️ Agent-based tool calling
- 📄 Read local files + list directories
- 🌐 Web search and page retrieval
- 🌤️ Weather and system monitoring
- 🚀 Application launching (Windows)
- 🖼️ Image generation (optional GPU)
- 📸 Screen capture + local vision analysis
- 🔐 Per-tool permissions (allow / ask / deny)
- 💬 Multi-session conversations
- 🔊 Optional text-to-speech
- 🧪 Automated tests and GitHub Actions

## 🛠️ Tools

| Tool | Purpose |
|---|---|
| `get_weather` | Weather information |
| `get_system_status` | CPU, RAM and system resources |
| `save_note` | Persistent notes |
| `launch_app` | Launch allowed apps (Windows) |
| `read_file` | Read a local text file |
| `list_directory` | List folder contents |
| `add_document_to_memory` | Index documents into RAG |
| `search_memory` | Semantic memory search |
| `generate_image` | Image generation |
| `web_search` | Internet search |
| `fetch_web_page` | Retrieve web page contents |
| `capture_screen` | Screen capture (optional vision analysis) |
| `analyze_image` | Describe a local image with a vision model |

## 🧰 Stack

- Python 3.12+
- Ollama + Qwen3:8B
- ChromaDB, Sentence Transformers
- Requests / BeautifulSoup

## 🚀 Quick start (Windows)

```powershell
git clone https://github.com/dinguk0624/TalhaGPT.git
cd TalhaGPT
py -m pip install -r requirements.txt
ollama pull qwen3:8b
ollama pull llava
py main.py
```

Full install notes for macOS/Linux are in earlier docs / same flow with `python3`.

## ⚙️ Configuration

`config.py` / env:

- `MODEL_NAME` (default `qwen3:8b`)
- `VISION_MODEL` (default `llava`)
- `OLLAMA_HOST`
- `ENABLE_VOICE`
- `TTS_LANGUAGE`
- `REQUIRE_TOOL_CONFIRM`

Slash commands: `/permissions`, `/allow`, `/ask`, `/deny`, `/sessions`, `/new`, `/switch`.

## 🔒 Privacy

Runs locally. Memory and vector DB stay on your machine. Some tools (web, weather) need network.

## 🗺️ Roadmap

v0.3.0 ile bu yol haritası **tamamlandı**.

- [x] Local Qwen3:8B + agent loop + tools
- [x] RAG + memory
- [x] Streaming
- [x] File read / directory list
- [x] CI tests
- [x] Tool permission system
- [x] Multi-session conversations
- [x] Real multimodal vision

Yeni fikirler için GitHub Issues kullanın.

## 📜 License

See `LICENSE` (MIT).

## ⭐ Support

Star the repo if useful. Issues and PRs welcome.

## 🐳 Docker ile çalıştırma

Docker ve Docker Compose kurulu bir makinede TalhaGPT ile Ollama'yı birlikte başlatabilirsiniz:

```bash
cp .env.example .env
docker compose up -d ollama
docker compose run --rm ollama ollama pull qwen3:8b
docker compose run --rm ollama ollama pull llava
docker compose run --rm talhGPT
```

Model indirmeleri `ollama_data` Docker volume'unda, konuşma hafızası ve vektör veritabanı ise ayrı kalıcı volume'larda tutulur. Ollama servisi Compose ağı içinde `http://ollama:11434` adresinden erişilir; bu nedenle konteyner içindeki `.env` dosyasında `OLLAMA_HOST` değerini değiştirmeyin. Etkileşimli arayüzü kapatmak için `q` yazın. Servisleri durdurmak için:

```bash
docker compose down
```

GPU kullanımı donanım ve Docker runtime yapılandırmasına bağlıdır. Bu Compose dosyası varsayılan olarak CPU uyumludur.
