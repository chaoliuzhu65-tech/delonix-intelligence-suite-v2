---
name: notebooklm
description: |
  Complete API for Google NotebookLM - full programmatic access including features not in the web UI. Create notebooks, add sources, generate all artifact types, download in multiple formats. Activates on explicit /notebooklm or intent like "create a podcast about X"
---

# NotebookLM Automation

Complete programmatic access to Google NotebookLM—including capabilities not exposed in the web UI. Create notebooks, add sources (URLs, YouTube, PDFs, audio, video, images), chat with content, generate all artifact types, and download results in multiple formats.

## Installation

**From PyPI (Recommended):**
```bash
pip install notebooklm-py
```

**From GitHub (use latest release tag, NOT main branch):**
```bash
LATEST_TAG=$(curl -s https://api.github.com/repos/teng-lin/notebooklm-py/releases/latest | grep '"tag_name"' | cut -d'"' -f4)
pip install "git+https://github.com/teng-lin/notebooklm-py@${LATEST_TAG}"
```

**Skill install:**
```bash
notebooklm skill install
```

## 认证

**IMPORTANT:** Before using any command, you MUST authenticate:

```bash
notebooklm login          # Opens browser for Google OAuth
notebooklm list           # Verify authentication works
```

## When This Skill Activates

**Explicit:** User says "/notebooklm", "use notebooklm", or mentions the tool by name

**Intent detection:** Recognize requests like:
- "Create a podcast about [topic]"
- "Summarize these URLs/documents"
- "Generate a quiz from my research"
- "Turn this into an audio overview"
- "Create flashcards for studying"
- "Generate a video explainer"
- "Make an infographic"
- "Create a mind map of the concepts"
- "Download the quiz as markdown"
- "Add these sources to NotebookLM"

## Autonomy Rules

**Run automatically (no confirmation):**
- `notebooklm status` - check context
- `notebooklm auth check` - diagnose auth issues
- `notebooklm list` - list notebooks
- `notebooklm source list` - list sources
- `notebooklm artifact list` - list artifacts
- `notebooklm language list` - list supported languages
- `notebooklm create` - create notebook
- `notebooklm ask "..."` - chat queries
- `notebooklm source add` - add sources

**Ask before running:**
- `notebooklm delete` - destructive
- `notebooklm generate *` - long-running
- `notebooklm download *` - writes to filesystem

## Quick Reference

| Task | Command |
|------|---------|
| Authenticate | `notebooklm login` |
| List notebooks | `notebooklm list` |
| Create notebook | `notebooklm create "Title"` |
| Add URL source | `notebooklm source add "https://..."` |
| Add file | `notebooklm source add ./file.pdf` |
| Add YouTube | `notebooklm source add "https://youtube.com/..."` |
| Chat | `notebooklm ask "question"` |
| Generate podcast | `notebooklm generate audio "instructions"` |
| Generate video | `notebooklm generate video "instructions"` |
| Generate quiz | `notebooklm generate quiz` |
| Generate flashcards | `notebooklm generate flashcards` |
| Generate mind map | `notebooklm generate mind-map` |
| Generate report | `notebooklm generate report --format briefing-doc` |
| Download audio | `notebooklm download audio ./output.mp3` |
| Download video | `notebooklm download video ./output.mp4` |
| Download quiz | `notebooklm download quiz quiz.json` |
| Delete notebook | `notebooklm notebook delete <id>` |

## Generation Types

| Type | Command | Download |
|------|---------|----------|
| Podcast | `generate audio` | .mp3 |
| Video | `generate video` | .mp4 |
| Slide Deck | `generate slide-deck` | .pdf / .pptx |
| Infographic | `generate infographic` | .png |
| Report | `generate report` | .md |
| Mind Map | `generate mind-map` | .json |
| Data Table | `generate data-table` | .csv |
| Quiz | `generate quiz` | .json/.md/.html |
| Flashcards | `generate flashcards` | .json/.md/.html |

## Features Beyond Web UI

| Feature | Command |
|---------|---------|
| Quiz/Flashcard export (JSON) | `download quiz --format json` |
| Mind map JSON export | `download mind-map` |
| Slide deck as PPTX | `download slide-deck --format pptx` |
| Source fulltext | `source fulltext <id>` |
| Save chat to note | `ask "..." --save-as-note` |

## Language

```bash
# List languages
notebooklm language list

# Set Chinese
notebooklm language set zh_Hans

# Set Japanese
notebooklm language set ja
```

## Troubleshooting

```bash
notebooklm auth check          # Diagnose auth issues
notebooklm login               # Re-authenticate
notebooklm --help              # All commands
```
