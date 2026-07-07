from src.planner import create_plan
from src.architect import create_tasks
from src.coder import write_code


def run_pipeline(user_prompt: str, status_callback=None) -> dict:
    if status_callback:
        status_callback("Planning...")
    plan = create_plan(user_prompt)

    if status_callback:
        status_callback("Creating architecture...")
    tasks = create_tasks(plan)

    if status_callback:
        status_callback("Writing code...")
    files_written = write_code(plan["project_name"], tasks, status_callback)

    return {
        "project_name": plan["project_name"],
        "plan": plan,
        "tasks": tasks,
        "files_written": files_written,
    }
