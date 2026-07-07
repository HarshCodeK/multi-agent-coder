from src.planner import create_plan
from src.architect import create_tasks
from src.coder import write_code


def run_pipeline(user_prompt: str) -> dict:
    print("[Plan] Planning...")
    plan = create_plan(user_prompt)

    print("[Arch] Creating architecture...")
    tasks = create_tasks(plan)

    print("[Code] Writing code...")
    files_written = write_code(plan["project_name"], tasks)

    return {
        "project_name": plan["project_name"],
        "plan": plan,
        "tasks": tasks,
        "files_written": files_written,
    }
