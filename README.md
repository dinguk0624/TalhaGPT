# TalhaGPT 🤖

> **A local AI assistant built on top of Qwen3:8B.**

**Current release: [v0.2.0](https://github.com/dinguk0624/TalhaGPT/releases/tag/v0.2.0)**

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
- 📸 Screen capture
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
| `capture_screen` | Screen capture |

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
py main.py
```

Full install notes for macOS/Linux are in earlier docs / same flow with `python3`.

## ⚙️ Configuration

`config.py` / env:

- `MODEL_NAME` (default `qwen3:8b`)
- `OLLAMA_HOST`
- `ENABLE_VOICE`
- `TTS_LANGUAGE`

## 🔒 Privacy

Runs locally. Memory and vector DB stay on your machine. Some tools (web, weather) need network.

## 🗺️ Roadmap

- [x] Local Qwen3:8B + agent loop + tools
- [x] RAG + memory
- [x] Streaming
- [x] File read / directory list
- [x] CI tests
- [ ] Tool permission system
- [ ] Multi-session conversations
- [ ] Real multimodal vision

## 📜 License

See `LICENSE` (MIT).

## ⭐ Support

Star the repo if useful. Issues and PRs welcome.
