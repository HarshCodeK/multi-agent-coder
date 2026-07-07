import os
import shutil
import streamlit as st
from src.pipeline import run_pipeline
from src.config import GENERATED_PROJECTS_DIR


st.set_page_config(page_title="Multi-Agent Coder", layout="wide")
st.title("Multi-Agent Coder")
st.markdown("Describe the app you want to build, and 3 AI agents will plan, architect, and code it.")

user_prompt = st.text_area(
    "Describe the app you want to build",
    placeholder="e.g. Build a calculator web app with add, subtract, multiply and divide buttons",
    height=100,
)

if st.button("Generate Project", type="primary") and user_prompt:
    status_placeholder = st.empty()
    with status_placeholder.status("Starting...", expanded=True) as status_box:
        logs = []

        def status_callback(msg):
            logs.append(msg)
            status_box.update(label=msg, state="running")

        result = run_pipeline(user_prompt, status_callback)
        status_box.update(
            label=f"Project '{result['project_name']}' generated!",
            state="complete",
        )

    st.success(f"Project **{result['project_name']}** generated successfully!")

    with st.expander("View Plan"):
        st.subheader("Tech Stack")
        st.write(", ".join(result["plan"]["tech_stack"]))
        st.subheader("Features")
        for f in result["plan"]["features"]:
            st.write(f"- {f}")
        st.subheader("File List")
        for f in result["plan"]["file_list"]:
            st.write(f"- {f}")

    st.subheader("Generated Files")
    for filepath in result["files_written"]:
        rel_path = os.path.relpath(filepath, GENERATED_PROJECTS_DIR)
        st.write(f"**{rel_path}**")
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            st.code(content, language=os.path.splitext(rel_path)[1].lstrip(".") or "text")
        except Exception as e:
            st.error(f"Could not read file: {e}")

    project_dir = os.path.join(GENERATED_PROJECTS_DIR, result["project_name"])
    zip_path = shutil.make_archive(
        result["project_name"],
        "zip",
        root_dir=project_dir,
    )
    with open(zip_path, "rb") as f:
        st.download_button(
            label="Download as ZIP",
            data=f,
            file_name=f"{result['project_name']}.zip",
            mime="application/zip",
        )
    os.remove(zip_path)
