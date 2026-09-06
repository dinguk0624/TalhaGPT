# Changelog

All notable changes to TalhaGPT are documented here.

## [0.2.0] - 2026-09-06

First public package release.

### Added
- Streaming responses (live token output via Ollama `stream=True`)
- `read_file` tool — safe local text file reading (project-scoped)
- `list_directory` tool — browse project folders
- Windows-safe UTF-8 logging (emoji / cp1254 crash fixed)
- Performance defaults for 8GB VRAM: `num_ctx=4096`, `num_predict=512`, `keep_alive=30m`
- History trimming and tool-output caps for faster turns

### Fixed
- `capture_screen` now keeps screenshots under `screenshots/`
- `generate_image` CUDA auto-detect + CPU fallback
- `launch_app` explicit Windows-only guard
- CI: lazy `pyautogui` import (no `DISPLAY` crash)
- CI: `torch.jit.script` FutureWarning filtered

### Improved
- RAG chunk overlap + default `n_results=4`
- Agent `max_steps` 4, memory history 12
- Tests green on GitHub Actions

## [0.1.1] - 2026-09-06

### Fixed
- Screenshot deletion bug, CUDA hardcode, platform check, CI import crash

### Added
- Streaming responses (initial)

## [0.1.0]

- Initial TalhaGPT structure
- Qwen3:8B via Ollama
- Agent tool calling, memory, RAG, web/system tools
