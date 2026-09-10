# TalhaGPT

> **A local AI assistant built on top of Ollama and Qwen3:8B.**

TalhaGPT is a local, terminal-based AI assistant with an agent loop, tool calling, persistent memory, retrieval-augmented generation (RAG), web access, streaming responses, optional image generation, vision support, and optional text-to-speech.

**Qwen3:8B is the language model. TalhaGPT is the assistant layer around it.**

[![CI/CD](https://github.com/dinguk0624/TalhaGPT/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/dinguk0624/TalhaGPT/actions/workflows/ci-cd.yml)

## Features

- Local inference through [Ollama](https://ollama.com/) and Qwen3:8B
- Streaming assistant responses
- Persistent conversation memory and multiple sessions
- ChromaDB and Sentence Transformers-based RAG
- Agent-based tool calling with per-tool permissions
- Local file reading and directory browsing
- Web search and web page retrieval
- Weather and system resource information
- Optional image generation and vision analysis
- Optional text-to-speech
- Automated tests and GitHub Actions CI/CD

## Available tools

| Tool | Description |
|---|---|
| `get_weather` | Get weather information |
| `get_system_status` | Inspect CPU, memory, and system resources |
| `save_note` | Save a persistent note |
| `launch_app` | Launch an allowed local application |
| `read_file` | Read a local text-based file |
| `list_directory` | List files in a directory |
| `add_document_to_memory` | Index a document for RAG search |
| `search_memory` | Search saved memories semantically |
| `generate_image` | Generate an image when configured |
| `web_search` | Search the web |
| `fetch_web_page` | Retrieve the contents of a web page |
| `capture_screen` | Capture the local screen when supported |
| `analyze_image` | Analyze an image with the configured vision model |

## Requirements

### Native installation

- Python 3.12 or newer
- Ollama
- At least one Ollama model:
  - `qwen3:8b` for text conversations
  - `llava` for vision features
- Git

### Docker installation

- Docker Engine
- Docker Compose v2
- Enough disk space for Python dependencies and Ollama models

## Installation

### Windows, macOS, and Linux

Clone the repository and create a virtual environment:

```bash
git clone https://github.com/dinguk0624/TalhaGPT.git
cd TalhaGPT
python -m venv .venv
```

Activate the virtual environment:

**Windows PowerShell:**

```powershell
.\.venv\Scripts\Activate.ps1
```

**macOS/Linux:**

```bash
source .venv/bin/activate
```

Install the dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Install Ollama from [ollama.com/download](https://ollama.com/download), then download the recommended models:

```bash
ollama pull qwen3:8b
ollama pull llava
```

Create a local configuration file and start TalhaGPT:

```bash
cp .env.example .env
python main.py
```

On Windows, use `copy .env.example .env` in Command Prompt or copy the file manually in PowerShell.

### Docker Compose

Docker Compose starts both TalhaGPT and Ollama. The named volumes preserve models, conversations, RAG data, screenshots, and generated images across container recreation.

```bash
cp .env.example .env
docker compose up -d ollama
docker compose run --rm ollama ollama pull qwen3:8b
docker compose run --rm ollama ollama pull llava
docker compose run --rm talhGPT
```

The Compose network exposes Ollama to TalhaGPT at `http://ollama:11434`. Keep this value for `OLLAMA_HOST` inside the container; `localhost` would refer to the TalhaGPT container itself.

To stop the services:

```bash
docker compose down
```

To remove the services and all named volumes, including downloaded models and stored memory:

```bash
docker compose down -v
```

> **Warning:** `docker compose down -v` permanently deletes the Docker-managed application data and Ollama models.

The default Compose configuration is CPU-compatible. GPU acceleration requires compatible host hardware and Docker runtime configuration.

## Configuration

Copy `.env.example` to `.env` and adjust the values for your environment:

| Variable | Default | Description |
|---|---|---|
| `MODEL_NAME` | `qwen3:8b` | Ollama model used for text conversations |
| `VISION_MODEL` | `llava` | Ollama model used for image analysis |
| `OLLAMA_HOST` | `http://localhost:11434` | Ollama server URL; Compose overrides this to `http://ollama:11434` |
| `ENABLE_VOICE` | `False` | Enable startup text-to-speech |
| `TTS_LANGUAGE` | `tr` | Language used by text-to-speech |
| `REQUIRE_TOOL_CONFIRM` | `True` | Ask before running sensitive tools |
| `USER_ADDRESS` | empty | Optional preferred name or form of address |

Do not commit `.env` or API keys to the repository. The `.gitignore` file is configured to exclude local environment and runtime data.

## Interactive commands

During a conversation, use:

| Command | Description |
|---|---|
| `/help` | Show available commands |
| `/status` | Show model, host, session, and memory information |
| `/tools` | List registered tools |
| `/permissions` | Show tool permission policies |
| `/allow <tool>` | Always allow a tool |
| `/ask <tool>` | Ask for confirmation before using a tool |
| `/deny <tool>` | Deny a tool |
| `/sessions` | List conversation sessions |
| `/new [title]` | Create a new session |
| `/switch <id>` | Switch to another session |
| `/clear` | Clear the current session memory |
| `q` or `/exit` | Exit TalhaGPT |

Sensitive tools such as application launching and screen capture require confirmation by default. You can change this behavior with `REQUIRE_TOOL_CONFIRM` or the permission commands above.

## Testing

Install the test dependencies and run the test suite:

```bash
python -m pip install -r requirements-test.txt
python -m pytest -q
```

The GitHub Actions workflow also runs the tests on Python 3.11 and 3.12. Successful pushes to `main` build and publish a Docker image to GitHub Container Registry:

```text
ghcr.io/dinguk0624/talhagpt:latest
ghcr.io/dinguk0624/talhagpt:<short-commit-sha>
```

## Privacy and security

TalhaGPT is designed to run locally. Conversation memory and the vector database remain on the machine or Docker volumes where the application runs. Web search, page retrieval, and weather tools require network access. Review tool permissions before enabling actions that interact with the local system.

Never commit secrets, tokens, private documents, or `.env` files. See [SECURITY.md](SECURITY.md) for security guidance.

## Project structure

```text
.
├── core/                 # Agent loop and tool registry
├── modules/              # Memory, sessions, RAG, web, voice, and system tools
├── tests/                # Automated tests
├── main.py               # Interactive application entry point
├── config.py             # Environment-backed configuration
├── Dockerfile            # TalhaGPT container image
├── docker-compose.yml    # TalhaGPT and Ollama services
└── requirements.txt      # Runtime dependencies
```

## Contributing

Issues and pull requests are welcome. Before opening a pull request, run the test suite locally and describe the change, configuration requirements, and any platform-specific limitations.

## License

TalhaGPT is released under the [MIT License](LICENSE).

## Web version

A web interface is available at [TalhaGPT Web Buddy](https://talha-gpt-web-buddy.lovable.app).
