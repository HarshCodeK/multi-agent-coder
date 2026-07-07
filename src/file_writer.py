import os
from src.config import GENERATED_PROJECTS_DIR


def write_file(project_name: str, relative_path: str, content: str) -> str:
    full_path = os.path.join(GENERATED_PROJECTS_DIR, project_name, relative_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
    return full_path
