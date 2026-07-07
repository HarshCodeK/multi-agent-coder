import json
import re
from src.config import call_llm


def create_plan(user_prompt: str) -> dict:
    system_prompt = "You are a software planner. Respond with STRICT JSON only."
    prompt = f"""Given this app description:
{user_prompt}

Respond with STRICT JSON only, no markdown, no code fences:
{{
  "project_name": "short_snake_case_name",
  "tech_stack": ["list", "of", "technologies"],
  "features": ["list", "of", "key", "features"],
  "file_list": ["list", "of", "files", "needed"]
}}
Base the file_list on what makes sense for the requested app type."""
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
