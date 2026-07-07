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

        visual_notes = task.get("visual_notes", "")
        visual_section = f"\nDesign guidance: {visual_notes}" if visual_notes else ""

        prompt = f"""You are writing the file "{task["filename"]}" for the project "{project_name}".

Design style: {design_style}{visual_section}

Your file's task:
{task["description"]}

SHARED CONTRACT — these CSS classes/IDs are the CONNECTION POINTS between files. They MUST all appear in your code:
CSS classes: {", ".join(task.get("shared_contract", {}).get("css_classes", []))}
CSS IDs: {", ".join(task.get("shared_contract", {}).get("css_ids", []))}
Data attributes: {", ".join(task.get("shared_contract", {}).get("data_attributes", []))}

OTHER FILES IN THIS PROJECT (for reference — know what they expect from your file):
{other_context}

REQUIREMENTS:
1. Write COMPLETE, WORKING code — no placeholders, no TODOs, no "function goes here"
2. ALL items from the SHARED CONTRACT above MUST appear in your code (every class, ID, data attribute)
3. You MAY add extra classes/IDs beyond the shared contract if needed for styling, but keep it minimal
4. If writing HTML: structure it semantically (<header>, <main>, <section>, <footer>), use modern layout, nice spacing
5. If writing CSS: make it LOOK GOOD — use gradients, box-shadows, rounded corners, smooth hover transitions, a cohesive color palette, and responsive media queries. Style should feel polished like a real app.
6. If writing JS: make it work correctly — proper event listeners, DOM manipulation, handle edge cases. Use event.preventDefault() on form submit or add type="button" to form buttons.
7. COMMON PITFALL: Buttons inside a <form> will reload the page unless you add type="button" to them OR call event.preventDefault() in JS.

Respond with ONLY the raw code. No markdown fences, no backticks, no explanation — just the file content."""
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
