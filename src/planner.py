import json
import re
from src.config import call_llm


def create_plan(user_prompt: str) -> dict:
    system_prompt = (
        "You are a senior software planner. You design practical, complete projects. "
        "For web apps, prefer simple HTML/CSS/JS unless a framework is explicitly requested. "
        "Respond with STRICT JSON only — no markdown, no code fences, no explanation."
    )
    prompt = f"""Given this app description:
{user_prompt}

Design a complete project plan. Choose a practical tech stack (for simple web apps use HTML + CSS + JavaScript).

Respond with EXACTLY this JSON structure, no extra fields:
{{
  "project_name": "short_snake_case_name",
  "tech_stack": ["html", "css", "javascript"],
  "features": ["list", "of", "key", "features"],
  "file_list": ["index.html", "style.css", "script.js"],
  "design_style": "modern" or "minimal" or "dark"
}}

Rules for file_list:
- For a web app with UI: ["index.html", "style.css", "script.js"]
- For a CLI tool: ["main.py"] or ["main.js"]
- For an API: ["server.py", "requirements.txt"] or ["server.js", "package.json"]
"""
    raw = call_llm(prompt, system_prompt)
    raw = raw.strip()
    raw = re.sub(r"^```(?:json)?\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)
    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        raise ValueError(
            f"Failed to parse plan JSON. Raw response:\n{raw}\n\nError: {e}"
        )
