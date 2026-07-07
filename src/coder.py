import re
from src.config import call_llm
from src.file_writer import write_file


def write_code(project_name: str, tasks: list[dict]) -> list[str]:
    system_prompt = "You are a senior software engineer. Write clean, complete, working code."
    written = []
    for task in tasks:
        prompt = f"""Write the FULL code for the file "{task["filename"]}" in the project "{project_name}".

Description of what this file should do:
{task["description"]}

Respond with ONLY the raw code for this file. No markdown code fences, no explanation, no comments about what you're doing — just the file content exactly as it should be saved."""
        raw = call_llm(prompt, system_prompt)
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
