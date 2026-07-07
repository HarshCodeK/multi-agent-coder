import json
import re
from src.config import call_llm


def create_tasks(plan: dict) -> list[dict]:
    system_prompt = "You are a software architect. Respond with STRICT JSON only."
    prompt = f"""Given this project plan:
Project name: {plan["project_name"]}
Tech stack: {", ".join(plan["tech_stack"])}
Features: {", ".join(plan["features"])}
Files: {", ".join(plan["file_list"])}

Break each file into a specific task with a detailed description of exactly what that file should contain and do.

Respond with STRICT JSON only, no markdown, no code fences:
[
  {{
    "filename": "index.html",
    "description": "detailed description of exactly what this file should contain and do"
  }},
  ...
]"""
    raw = call_llm(prompt, system_prompt)
    raw = raw.strip()
    raw = re.sub(r"^```(?:json)?\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)
    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        raise ValueError(
            f"Failed to parse tasks JSON. Raw response:\n{raw}\n\nError: {e}"
        )
