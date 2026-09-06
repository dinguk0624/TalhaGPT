# Changelog

All notable changes to TalhaGPT are documented here.

## [Unreleased]

- Improve agent reliability and tool execution safeguards.
- Add tool argument validation.
- Add automated tests for the tool registry and agent helpers.
- Continue improving local RAG, memory, and agent workflows.

## [0.1.1] - 2026-09-06

### Fixed
- `capture_screen`: Screenshot was being deleted immediately after capture. Now saved permanently under `screenshots/` with a timestamped filename and full path returned.
- `generate_image`: Hardcoded CUDA assumption removed. Now auto-detects CUDA and falls back to CPU with a clear warning.
- `launch_app`: Added explicit platform check. Returns a clear error on non-Windows systems instead of failing silently.
- CI: Lazy-import `pyautogui` so headless runners (no `DISPLAY`) no longer crash during test collection.
- Test: `test_limit_tool_output` now correctly forces a small truncation limit.
- CI: Suppress third-party `torch.jit.script` FutureWarning via `pytest.ini`.

### Added
- **Streaming responses**: Agent streams tokens live to the terminal via `on_token` callback (Ollama `stream=True`).

### Improved
- RAG: Added simple chunk overlap, raised default `n_results` from 2 → 4.
- Tool descriptions updated to reflect Windows-only launcher and new screenshot behavior.
- `.gitignore` now excludes `screenshots/` and `generated_images/`.

## [0.1.0]

- Initial TalhaGPT project structure.
- Qwen3:8B support through Ollama.
- Agent-based tool calling.
- Conversation memory and ChromaDB-backed RAG.
- Web, weather, system, application, vision, and image-generation tools.
