# Changelog

All notable changes to TalhaGPT are documented here.

## [0.3.0] - 2026-09-07

Roadmap complete: permissions, multi-session chats, and local vision.

### Added
- Per-tool permission policies (`allow` / `ask` / `deny`) with `/permissions`, `/allow`, `/ask`, `/deny`
- Multi-session chats: `/sessions`, `/new`, `/switch`
- `analyze_image` plus optional `capture_screen(analyze=true)` via `VISION_MODEL` (default `llava`)

## [0.2.3] - 2026-09-07

### Fixed
- Tool results now include `tool_name` so Ollama can bind them to the call
- Conversation memory no longer re-saves truncated history copies
- Restricted tools are denied when confirmation is required but no callback is set
- `save_note` indexes only the new note, not the whole `notes.txt` file
- Fast-path hints no longer match inside words like `program` / `karar`, and detect `yağmur`
- Agent/module logs go to the TalhaGPT log file
- Empty model replies retry without injecting a fake user message
- Qwen3 `thinking` tokens are used when `content` is empty
- Voice libraries load only when TTS is enabled
- Arbitrary Python execution in `executor.py` is disabled
- Empty weather city and empty memory search no longer look like success
- `fetch_web_page` follows up to 5 redirects with an SSRF check on each hop

### Improved
- Model `num_predict` raised from 256 to 1024

## [0.2.2] - 2026-09-07

### Fixed
- `launch_app` now accepts `app_name` (tool schema) instead of a mismatched `user_input` argument
- RAG document paths no longer strip Linux absolute paths, so `save_note` can index `data/notes.txt`
- Voice TTS cleanup no longer crashes if a temp file was never created
- Windows system status uses the current drive root instead of `/`
- GitHub Actions installs lightweight test deps instead of torch/chroma on every run

### Improved
- Image generation and ChromaDB load only when those tools are used
- `duckduckgo-search` / `ddgs` import fallback
- `.env` files are no longer readable via `read_file`

## [0.2.1] - 2026-09-06

### Added
- **Fast path**: Simple chat ("sa", short questions) skips tool schemas → much lower latency
- **Slash commands**: `/help`, `/clear`, `/status`, `/tools`
- **Tool confirmation** for `launch_app` and `capture_screen` (env `REQUIRE_TOOL_CONFIRM`, default on)
- Startup banner with version + model name

### Improved
- `VERSION` file wired into runtime via `config.VERSION`

## [0.2.0] - 2026-09-06

First public package release.

### Added
- Streaming responses
- `read_file` / `list_directory`
- Windows-safe UTF-8 logging
- Perf defaults for 8GB VRAM

### Fixed
- Screenshot persistence, CUDA fallback, CI pyautogui, syntax error

## [0.1.0]

- Initial structure, Qwen3:8B, agent tools, RAG, memory
