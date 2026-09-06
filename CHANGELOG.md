# Changelog

All notable changes to TalhaGPT are documented here.

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
