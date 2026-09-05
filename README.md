# TalhaGPT 🤖

> **A local AI assistant built on top of Qwen3:8B.**

TalhaGPT combines a local LLM with an agent loop, tool calling, persistent memory, RAG, web access, system tools, vision, image generation, and optional voice output.

**Qwen3:8B is the model. TalhaGPT is the assistant layer around it.**

## 🌐 Website

### [🚀 Try TalhaGPT Web Buddy](https://talha-gpt-web-buddy.lovable.app)
*Built with Loveable - Web UI for TalhaGPT*

---

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

TalhaGPT uses an agent loop rather than simply forwarding every prompt to the model. The model can decide when a registered tool is useful, receive the result, and continue reasoning toward a final answer.

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

TalhaGPT is not limited to Windows. The project can be installed on **Windows, macOS, and Linux**.

### Windows

#### 1. Install Python

Install Python 3.12 or newer and make sure Python is available in your PATH.

#### 2. Install Ollama

Download and install Ollama for Windows from the official Ollama website.

#### 3. Clone TalhaGPT

```powershell
git clone https://github.com/dinguk0624/TalhaGPT.git
cd TalhaGPT
```

#### 4. Install dependencies

```powershell
py -m pip install -r requirements.txt
```

#### 5. Install the model

```powershell
ollama pull qwen3:8b
```

#### 6. Run TalhaGPT

```powershell
py main.py
```

### macOS

#### 1. Install Python

Install Python 3.12 or newer. Homebrew users can run:

```bash
brew install python
```

#### 2. Install Ollama

Install Ollama for macOS from the official Ollama website and make sure the Ollama application/service is running.

#### 3. Clone TalhaGPT

```bash
git clone https://github.com/dinguk0624/TalhaGPT.git
cd TalhaGPT
```

#### 4. Install dependencies

```bash
python3 -m pip install -r requirements.txt
```

#### 5. Install the model

```bash
ollama pull qwen3:8b
```

#### 6. Run TalhaGPT

```bash
python3 main.py
```

### Linux

#### 1. Install Python

Install Python 3.12 or newer using your distribution's package manager or the official Python installation method.

#### 2. Install Ollama

Install Ollama using the official Linux installation instructions. For supported Linux systems:

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

Start Ollama if it is not already running:

```bash
ollama serve
```

#### 3. Clone TalhaGPT

```bash
git clone https://github.com/dinguk0624/TalhaGPT.git
cd TalhaGPT
```

#### 4. Install dependencies

```bash
python3 -m pip install -r requirements.txt
```

#### 5. Install the model

```bash
ollama pull qwen3:8b
```

#### 6. Run TalhaGPT

```bash
python3 main.py
```

### Run tests (all platforms)

```bash
python -m pytest -q
```

> **Note:** Some system-level tools may behave differently across operating systems. In particular, application launching, screen capture, and other OS-specific functionality may require platform-specific setup.

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

TalhaGPT is designed for local AI execution. The model, conversation memory, and vector database can run on the user's computer. Individual tools may still access external services or the local system depending on configuration.

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
