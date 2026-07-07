import json
import re
from src.config import call_llm


def create_tasks(plan: dict) -> list[dict]:
    system_prompt = (
        "You are a senior software architect. You design precise, consistent cross-file contracts. "
        "Every CSS class/ID in shared_contract must appear in HTML, CSS, and JS identically. "
        "Respond with STRICT JSON only."
    )
    prompt = f"""Given this project plan:
Project name: {plan["project_name"]}
Tech stack: {", ".join(plan["tech_stack"])}
Features: {", ".join(plan["features"])}
Files: {", ".join(plan["file_list"])}
Design style: {plan.get("design_style", "modern")}

For EACH file, provide:
1. A description of what it contains
2. A shared_contract listing CSS classes/IDs/data attributes that MULTIPLE files share
3. visual_notes describing the look and feel (colors, layout, vibe)

CRITICAL: The css_classes and css_ids in shared_contract must be IDENTICAL across HTML, CSS, and JS. HTML uses them as selectors, CSS styles them, JS targets them. Names must match exactly.

Respond with STRICT JSON only:
[
  {{
    "filename": "index.html",
    "description": "HTML structure of the page",
    "shared_contract": {{
      "css_classes": ["class-name", "class-name-2"],
      "css_ids": ["id-name"],
      "data_attributes": ["data-custom"]
    }},
    "visual_notes": "color palette, layout type, UI feel"
  }},
  {{
    "filename": "style.css",
    "description": "CSS styling of the page",
    "shared_contract": {{
      "css_classes": ["class-name", "class-name-2"],
      "css_ids": ["id-name"],
      "data_attributes": []
    }},
    "visual_notes": "specific colors, fonts, effects to use"
  }},
  {{
    "filename": "script.js",
    "description": "JS functionality of the page",
    "shared_contract": {{
      "css_classes": ["class-name", "class-name-2"],
      "css_ids": ["id-name"],
      "data_attributes": ["data-custom"]
    }},
    "visual_notes": ""
  }}
]

List 4-8 css_classes to give enough for a well-styled page. Include layout classes (e.g. container, header, main, card) and interactive classes (e.g. button, input)."""
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
