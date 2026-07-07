import json
import re
from src.config import call_llm


def create_tasks(plan: dict) -> list[dict]:
    system_prompt = (
        "You are a senior software architect. You design precise, consistent, cross-file contracts. "
        "Every CSS class, ID, and data attribute used in HTML must be defined in CSS and referenced in JS. "
        "Respond with STRICT JSON only — no markdown, no code fences, no explanation."
    )
    prompt = f"""Given this project plan:
Project name: {plan["project_name"]}
Tech stack: {", ".join(plan["tech_stack"])}
Features: {", ".join(plan["features"])}
Files: {", ".join(plan["file_list"])}
Design style: {plan.get("design_style", "modern")}

For each file, provide:
1. A detailed description of what it contains and does
2. A "shared_contract" that lists all CSS class names, IDs, and data attributes that MULTIPLE files will use

CRITICAL RULE: Every CSS class, ID, or data attribute in the shared_contract must be used by ALL files that need it. HTML defines the structure, CSS styles those exact selectors, JS targets those exact selectors. They must all AGREE on names.

Respond with STRICT JSON only — an array of objects:
[
  {{
    "filename": "index.html",
    "description": "Detailed description of the HTML structure, what elements it contains, and how they connect to CSS/JS",
    "shared_contract": {{
      "css_classes": ["class-name-1", "class-name-2"],
      "css_ids": ["id-name-1"],
      "data_attributes": ["data-custom"]
    }}
  }},
  {{
    "filename": "style.css",
    "description": "Detailed styling description including layout, colors, typography, and interactive states",
    "shared_contract": {{
      "css_classes": ["class-name-1", "class-name-2"],
      "css_ids": ["id-name-1"],
      "data_attributes": []
    }}
  }},
  {{
    "filename": "script.js",
    "description": "Detailed description of all JavaScript functionality, event listeners, and DOM manipulations",
    "shared_contract": {{
      "css_classes": ["class-name-1", "class-name-2"],
      "css_ids": ["id-name-1"],
      "data_attributes": ["data-custom"]
    }}
  }}
]

IMPORTANT: The shared_contract for css_classes and css_ids must be IDENTICAL across all files that share those selectors. HTML defines the elements, CSS styles them, JS uses them — all with the same names."""
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
