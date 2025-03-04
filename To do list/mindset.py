import streamlit as st
from streamlit_extras.stylable_container import stylable_container

# App title
st.title("📝 To-Do List App")

# Initialize session state for tasks
if "tasks" not in st.session_state:
    st.session_state.tasks = []

# Sidebar for adding tasks
st.sidebar.header("📌 Manage Your Tasks")
new_task = st.sidebar.text_input("Add a new task:", placeholder="Enter your task here...")

if st.sidebar.button("➕ Add Task"):
    if new_task.strip():
        st.session_state.tasks.append({"task": new_task, "completed": False})
        st.sidebar.success("✅ Task added successfully!")
    else:
        st.sidebar.warning("⚠️ Task cannot be empty!")

# Display tasks
st.subheader("📋 Your To-Do List")
if not st.session_state.tasks:
    st.info("No tasks added yet! Start by adding a task from the sidebar.")
else:
    for index, task in enumerate(st.session_state.tasks):
        with stylable_container("task_container", css_styles="padding: 10px; margin: 5px; border-radius: 10px; background-color: #f0f2f6;"):
            col1, col2, col3 = st.columns([0.7, 0.15, 0.15])
            
            # Mark task as complete
            completed = col1.checkbox(f"**{task['task']}**", task["completed"], key=f"check_{index}")
            st.session_state.tasks[index]["completed"] = completed
            
            # Edit task
            if col2.button("✏️", key=f"edit_{index}"):
                new_task_value = st.text_input("Edit task", task["task"], key=f'edit_input_{index}')
                if st.button("💾 Save", key=f'save_{index}'):
                    st.session_state.tasks[index]["task"] = new_task_value
                    st.experimental_rerun()
            
            # Delete task
            if col3.button("❌", key=f"delete_{index}"):
                del st.session_state.tasks[index]
                st.experimental_rerun()

# Clear all tasks
if st.button("🗑️ Clear All Tasks"):
    st.session_state.tasks = []
    st.success("🧹 All tasks deleted successfully!")

# Footer
st.markdown('---')
st.caption("🚀 Stay organized & productive with this simple to-do list app.")
