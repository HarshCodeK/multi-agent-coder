> **Archived 2026-09.** A learning slice: practice in multi-agent orchestration that emits file trees, built in a single session. Superseded by [regent](https://github.com/HarshCodeK/regent) - the AI control plane, where the same pipeline idea now has tests, CI, an append-only ledger and measured numbers. Kept for history, not presented as portfolio work.

# Multi-Agent Coder

A production-style multi-agent code generator: three Groq LLaMA 3.3 70B agents — Planner, Architect, Coder — turn a plain-English app description into a complete, downloadable project on disk.

## What it does

- Converts a free-text prompt into a structured project plan (tech stack, features, `file_list`, design style) via a strict-JSON planner agent (`src/planner.py`)
- Decomposes the plan into per-file implementation tasks with a separate architect agent (`src/architect.py`)
- Generates and writes real code files to `generated_projects/<project_name>/` (`src/coder.py`, `src/file_writer.py`)
- Streams live pipeline status and renders generated files, plan, and features in a Streamlit UI (`app.py`)
- Packages each generated project as a downloadable ZIP from the UI

## Architecture

```
User prompt (Streamlit app.py)
        |
src/pipeline.py — run_pipeline() orchestrator
        |
  +-----+------------------+
  |            |           |
Planner     Architect    Coder
(planner)   (architect)  (coder)
JSON plan → per-file    → files written
            tasks         to disk (file_writer)
        |
generated_projects/<name>/ + ZIP download
```

Shared LLM client in `src/config.py` (Groq, model `llama-3.3-70b-versatile`).

## Stack

![Python](https://img.shields.io/badge/Python-3.10%2B-blue) ![Groq](https://img.shields.io/badge/Groq-LLaMA%203.3%2070B-orange) ![Streamlit](https://img.shields.io/badge/Streamlit-UI-red) ![python--dotenv](https://img.shields.io/badge/python--dotenv-config-green)

## Quickstart

```bash
git clone https://github.com/HarshCodeK/multi-agent-coder.git
cd multi-agent-coder
python -m venv .venv
source .venv/Scripts/activate   # .venv\Scripts\activate on Windows cmd
pip install -r requirements.txt
```

Create `.env` from the example:

```bash
cp .env.example .env
# .env contents:
GROQ_API_KEY=your-key-here   # from https://console.groq.com
```

Run:

```bash
streamlit run app.py
```

Then type an app description (e.g. *"Build a calculator web app with add, subtract, multiply and divide buttons"*) and click **Generate Project**.

## Example / Demo

Prompt: *"Build a calculator web app with add, subtract, multiply and divide buttons"*

Planner agent output:

```json
{
  "project_name": "calculator_web_app",
  "tech_stack": ["html", "css", "javascript"],
  "features": ["add", "subtract", "multiply", "divide"],
  "file_list": ["index.html", "style.css", "script.js"],
  "design_style": "modern"
}
```

Result: `generated_projects/calculator_web_app/` containing the three generated files, previewed in the UI and downloadable as a ZIP.

## Status / Roadmap

Status: working — sequential 3-agent pipeline, JSON-contract prompts, file writing, and Streamlit UI all functional.

Next steps:

1. Add validation/retry loop when a coder-agent file fails to parse or write
2. Add evals: smoke-run generated web apps and score feature presence against the planner's `features` list
3. Support follow-up edits ("add a history panel") against an already-generated project
