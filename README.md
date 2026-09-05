# TalhaGPT 🤖

> **A local AI assistant built on top of Qwen3:8B.**

TalhaGPT combines a local LLM with an agent loop, tool calling, persistent memory, RAG, web access, system tools, vision, image generation, and optional voice output.

**Qwen3:8B is the model. TalhaGPT is the assistant layer around it.**

## ✨ Highlights

- 🤖 Local AI through Ollama + Qwen3:8B
- 🧠 Persistent conversation memory
- 🔎 ChromaDB + Sentence Transformers RAG
- 🛠️ Agent-based tool calling
- 🌐 Web search and page retrieval
- 🌤️ Weather and system monitoring
- 🚀 Application launching
- 📚 Document-to-RAG indexing
- 🖼️ Image generation
- 📸 Screen capture and vision support
- 🔊 Optional text-to-speech
- 🧪 Automated tests and GitHub Actions

## 🏗️ Architecture

```text
                         ┌──────────────────┐
                         │       User       │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │  TalhaGPT Agent  │
                         └────────┬─────────┘
                                  │
                    ┌─────────────┴─────────────┐
                    │                           │
                    ▼                           ▼
             Direct Response              Tool Selection
                                                │
                ┌───────────────┬──────────────┼───────────────┐
                ▼               ▼              ▼               ▼
              Web             RAG           System           Vision
                │               │              │               │
                └───────────────┴──────────────┴───────────────┘
                                                │
                                                ▼
                                      ┌──────────────────┐
                                      │   Tool Result    │
                                      └────────┬─────────┘
                                               │
                                               ▼
                                      ┌──────────────────┐
                                      │  Agent evaluates │
                                      └────────┬─────────┘
                                               │
                                               ▼
                                         Final answer
```

## 🧠 How It Works

TalhaGPT uses an agent loop rather than simply forwarding every prompt to the model. The model can decide when a registered tool is useful, receive the result, and continue reasoning toward a final response.

Long-term information can be stored in local RAG memory and retrieved through semantic similarity instead of relying only on the active conversation context.

## 🛠️ Tools

| Tool | Purpose |
|---|---|
| `get_weather` | Weather information |
| `get_system_status` | CPU, RAM and system resources |
| `save_note` | Persistent notes |
| `launch_app` | Launch allowed applications |
| `add_document_to_memory` | Index documents into RAG |
| `search_memory` | Semantic memory search |
| `generate_image` | Image generation |
| `web_search` | Internet search |
| `fetch_web_page` | Retrieve web page contents |
| `capture_screen` | Screen capture |

## 🧰 Stack

- Python 3.12+
- Ollama
- Qwen3:8B
- ChromaDB
- Sentence Transformers
- Transformers / PyTorch
- Requests / BeautifulSoup
- Pillow / Pygame

## 🚀 Installation

### 1. Clone

```bash
git clone https://github.com/dinguk0624/TalhaGPT.git
cd TalhaGPT
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Install the model

Install Ollama, then:

```bash
ollama pull qwen3:8b
```

### 4. Run

```bash
python main.py
```

### 5. Run tests

```bash
pytest -q
```

## ⚙️ Configuration

Configuration lives in `config.py` and environment variables can be used for deployment-specific settings.

Important settings include:

- `MODEL_NAME`
- `OLLAMA_HOST`
- `ENABLE_VOICE`
- `TTS_LANGUAGE`

Do not commit API keys, tokens, passwords, or private data.

## 🔊 Voice

Voice output is optional and disabled by default. Set `ENABLE_VOICE=True` when the required dependencies are installed.

## 🔒 Privacy & Security

TalhaGPT is designed for local AI execution. The model, conversation memory, and vector database can run on the user's computer. Individual tools may still access external services or the local system, so review their behavior before using TalhaGPT with sensitive data.

## 🧪 Development

The repository includes automated tests for core agent and tool-registry behavior. GitHub Actions runs the test suite on pushes and pull requests.

See `CONTRIBUTING.md` for development guidelines and `CHANGELOG.md` for project history.

## 🗺️ Roadmap

- [x] Local Qwen3:8B integration
- [x] Agent loop
- [x] Tool calling
- [x] Conversation memory
- [x] RAG
- [x] Web tools
- [x] System tools
- [x] Vision / image capabilities
- [x] Automated tests
- [ ] Streaming responses
- [ ] Tool permission system
- [ ] Multi-session conversations
- [ ] More comprehensive integration tests
- [ ] Public demo

## 📜 License

This project is released under the license included in `LICENSE`.

## ⭐ Support

If TalhaGPT is useful or interesting, consider starring the repository. Ideas, issues, and contributions are welcome.
