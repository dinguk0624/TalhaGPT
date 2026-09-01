# TalhaGPT 🤖

> **Tired of using Qwen3:8B by itself?**
>
> **Meet TalhaGPT — a more capable AI assistant built on top of Qwen3:8B.**
>
> TalhaGPT combines Qwen3:8B with persistent memory, Retrieval-Augmented Generation (RAG), tool calling, web access, system monitoring, application control, image generation, screen capture, and optional voice output.
>
> **Qwen3:8B is the model. TalhaGPT is the complete AI assistant.**

TalhaGPT is a local AI assistant built with Python and powered by the Qwen3:8B model through Ollama.

## ✨ Features

* 🤖 Local AI powered by Qwen3:8B
* 🧠 Persistent conversation memory
* 🔎 Retrieval-Augmented Generation (RAG)
* 🛠️ Function and tool calling
* 🌐 Web search
* 📄 Web page retrieval
* 🌤️ Weather information
* 🖥️ System resource monitoring
* 🚀 Application launcher
* 📝 Persistent notes
* 📚 Document indexing into RAG memory
* 🖼️ AI image generation
* 📸 Screen capture
* 🔊 Optional text-to-speech
* 💾 Local vector database with ChromaDB

## 🏗️ Architecture

```text
TalhaGPT
│
├── main.py
├── config.py
│
├── core/
│   ├── agent.py
│   ├── tools.py
│   └── tool_registry.py
│
├── modules/
│   ├── api_tools.py
│   ├── app_launcher.py
│   ├── image_gen.py
│   ├── journal.py
│   ├── memory.py
│   ├── rag.py
│   ├── system.py
│   ├── vision.py
│   ├── voice.py
│   └── web.py
│
├── data/
│   └── conversations/
│
├── vector_db/
│
├── requirements.txt
└── README.md
```

## 🧠 How It Works

TalhaGPT uses an agent-based architecture.

```text
User
 │
 ▼
TalhaGPT Agent
 │
 ├── Direct Answer
 │
 └── Tool Selection
       │
       ├── Weather
       ├── Web Search
       ├── System Status
       ├── App Launcher
       ├── RAG Memory
       ├── Image Generation
       └── Screen Capture
              │
              ▼
         Tool Result
              │
              ▼
       Agent Evaluation
              │
              ▼
        Final Response
```

When long-term information is needed, TalhaGPT can store information in its local RAG memory and retrieve it later using semantic similarity search.

## 🧰 Technologies

* Python
* Ollama
* Qwen3:8B
* ChromaDB
* Sentence Transformers
* Transformers
* PyTorch
* Requests
* BeautifulSoup
* Pygame
* Pillow

## 💻 Requirements

Recommended:

* Python 3.12+
* Ollama
* NVIDIA GPU with sufficient VRAM
* At least 16 GB of system RAM

TalhaGPT can also run without a GPU, although model performance may be significantly slower.

## 🚀 Installation

### 1. Clone the repository

```bash
git clone <YOUR_REPOSITORY_URL>
cd TalhaGPT
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Install Qwen3:8B

Make sure Ollama is installed, then run:

```bash
ollama pull qwen3:8b
```

### 4. Start TalhaGPT

```bash
python main.py
```

## ⚙️ Configuration

The main configuration is located in:

```text
config.py
```

You can configure:

* AI model
* Ollama host
* Voice language
* Voice output
* System prompt

## 🔊 Voice Output

Voice output is disabled by default.

In `config.py`:

```python
ENABLE_VOICE = False
```

Set it to:

```python
ENABLE_VOICE = True
```

to enable voice output if the required dependencies are available.

## 🧠 RAG Memory

TalhaGPT uses ChromaDB and Sentence Transformers for semantic memory.

Information can be:

* Saved as persistent notes
* Added from documents
* Retrieved using semantic similarity search

This allows TalhaGPT to retrieve relevant information without relying only on the current conversation context.

## 🛠️ Available Tools

| Tool                     | Purpose                               |
| ------------------------ | ------------------------------------- |
| `get_weather`            | Retrieves weather information         |
| `get_system_status`      | Checks computer resources             |
| `save_note`              | Saves information to long-term memory |
| `launch_app`             | Launches an allowed application       |
| `add_document_to_memory` | Adds a document to RAG memory         |
| `search_memory`          | Searches long-term memory             |
| `generate_image`         | Generates an image                    |
| `web_search`             | Searches the internet                 |
| `fetch_web_page`         | Reads a web page                      |
| `capture_screen`         | Captures the screen                   |

## 🔒 Privacy

TalhaGPT is designed around local AI execution.

The language model runs through Ollama on the user's computer.

Local memory and the ChromaDB vector database are stored locally.

Users should review individual tools and dependencies before deploying the project in environments where sensitive information may be present.

## ⚠️ Project Status

TalhaGPT is an actively developed personal AI assistant project.

Features and architecture may change as development continues.

## 📜 License

License information will be added before the first public release.

## ⭐ Contributing

Contributions, ideas, bug reports, and improvements are welcome.

If you find the project interesting, consider giving it a ⭐ on GitHub.
