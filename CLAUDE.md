# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

OpenTypeless is a cross-platform desktop AI voice input app built with Tauri v2. A Rust backend handles audio capture, STT, LLM polishing, and keyboard output; a React+TypeScript frontend provides the UI.

## Build & Run Commands

```bash
npm install           # Install frontend dependencies
npm run tauri dev     # Development mode (hot-reload frontend + Rust rebuild)
npm run tauri build   # Production build → src-tauri/target/release/bundle/
```

### Environment Variables

| Variable | Default | Purpose |
|---|---|---|
| `VITE_API_BASE_URL` | `https://www.opentypeless.com` | Frontend cloud API base URL |
| `API_BASE_URL` | `https://www.opentypeless.com` | Rust backend cloud API base URL |

Set both when building against a custom backend.

## Architecture

**Core data flow pipeline:**
```
Microphone → Audio Capture → STT Provider → Raw Transcript → LLM Polish → Keyboard/Clipboard Output
```

### Frontend (`src/`)

- `components/` — UI components (Settings, History, Capsule, etc.)
- `hooks/` — React hooks (recording, theme, Tauri events)
- `lib/` — Utilities (API client, router, constants)
- `stores/` — Zustand state management

### Backend (`src-tauri/src/`)

- `audio/` — Audio capture via cpal
- `stt/` — STT providers (Deepgram, AssemblyAI, Whisper-compat, Groq, GLM-ASR, SiliconFlow, Cloud)
- `llm/` — LLM providers (OpenAI-compat, Cloud)
- `output/` — Text output (keyboard simulation, clipboard paste)
- `storage/` — Config (tauri-plugin-store) + history/dictionary (SQLite)
- `app_detector/` — Detect active application for per-app formatting context
- `pipeline.rs` — Core orchestration: Recording → STT → LLM → Output
- `lib.rs` — Tauri app setup, commands, hotkey handling

### Key Design Decisions

- **BYOK vs Cloud**: The app supports two modes — Bring Your Own Key (requests go directly to user's provider) and Cloud/Pro (proxied through opentypeless.com). All core features work without cloud dependency.
- **Streaming output**: LLM responses stream to the output target as they're generated.
- **Config storage**: API keys stored locally via `tauri-plugin-store`; history/dictionary in SQLite. No keys are sent to OpenTypeless servers in BYOK mode.
- **STT providers** share a common trait/interface in `stt/`; similarly for LLM providers in `llm/`. Adding a new provider means implementing the relevant trait and wiring it into the pipeline.

## Prerequisites

- Node.js 20+
- Rust stable toolchain
- Platform-specific Tauri v2 dependencies: https://v2.tauri.app/start/prerequisites/
