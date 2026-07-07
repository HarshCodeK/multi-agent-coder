import re
from src.config import call_llm
from src.file_writer import write_file


def write_code(project_name: str, tasks: list[dict], plan: dict = None, status_callback=None) -> list[str]:
    design_style = (plan or {}).get("design_style", "modern")
    written = []

    for task in tasks:
        if status_callback:
            status_callback(f"Writing {task['filename']}...")

        other_files = [t for t in tasks if t["filename"] != task["filename"]]
        other_context = ""
        for ot in other_files:
            contract = ot.get("shared_contract", {})
            classes = ", ".join(contract.get("css_classes", []))
            ids = ", ".join(contract.get("css_ids", []))
            data = ", ".join(contract.get("data_attributes", []))
            other_context += f"\n  - {ot['filename']}: {ot['description']}"
            if classes:
                other_context += f"\n    CSS classes: {classes}"
            if ids:
                other_context += f"\n    IDs: {ids}"
            if data:
                other_context += f"\n    Data attributes: {data}"

        prompt = f"""You are writing the file "{task["filename"]}" for the project "{project_name}".

Design style: {design_style}

Your file's task:
{task["description"]}

SHARED CONTRACT — these CSS classes/IDs must be used as specified (other files depend on them):
CSS classes: {", ".join(task.get("shared_contract", {}).get("css_classes", []))}
CSS IDs: {", ".join(task.get("shared_contract", {}).get("css_ids", []))}
Data attributes: {", ".join(task.get("shared_contract", {}).get("data_attributes", []))}

OTHER FILES IN THIS PROJECT (for reference — know what they expect from your file):
{other_context}

REQUIREMENTS:
1. Write COMPLETE, WORKING code — no placeholders, no TODOs, no "function goes here" comments
2. If this is an HTML file, make the UI look MODERN AND POLISHED — use a clean layout, good spacing, appealing colors
3. If this is a CSS file, write complete styles that make the app look professional — include hover effects, transitions, responsive design, and a cohesive color scheme
4. If this is a JS file, write complete working logic with proper event handling and DOM manipulation
5. ALL CSS classes, IDs, and data attributes from the shared contract MUST be used exactly as specified
6. Do NOT add extra CSS classes, IDs, or attributes that aren't in the shared contract (other files won't know about them)
7. COMMON PITFALLS TO AVOID: If you write HTML with a <form> and buttons inside it, add type="button" to each button OR call event.preventDefault() in the JS click handler — otherwise clicking a button will reload the page. If you write an input field, make sure the JS reads its .value property correctly. If you write a link (<a>), make sure it has a valid href or the JS prevents default.

Respond with ONLY the raw code for this file. No markdown code fences, no backticks, no explanation, no comments about what you're doing — just the file content exactly as it should be saved."""
        raw = call_llm(prompt)
        raw = raw.strip()
        if raw.startswith("```"):
            lines = raw.splitlines()
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]
            raw = "\n".join(lines).strip()
        path = write_file(project_name, task["filename"], raw)
        print(f"[OK] Wrote {task['filename']}")
        written.append(path)
    return written
