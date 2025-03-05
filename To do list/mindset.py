import streamlit as st
from streamlit_extras.stylable_container import stylable_container
import json

# App title
st.title("📝 Enhanced To-Do List App")

# Initialize session state for tasks
if "tasks" not in st.session_state:
    st.session_state.tasks = []
if "show_completed" not in st.session_state:
    st.session_state.show_completed = True
if "editing_index" not in st.session_state:
    st.session_state.editing_index = None

# Sidebar for adding tasks
st.sidebar.header("📌 Manage Your Tasks")
new_task = st.sidebar.text_input("Add a new task:", placeholder="Enter your task here...")
priority = st.sidebar.selectbox("Priority", ["Low", "Medium", "High"], index=1)

def add_task():
    if new_task.strip():
        st.session_state.tasks.append({"task": new_task, "completed": False, "priority": priority})
        st.sidebar.success("✅ Task added successfully!")
    else:
        st.sidebar.warning("⚠️ Task cannot be empty!")

st.sidebar.button("➕ Add Task", on_click=add_task)

# Toggle completed tasks visibility
st.sidebar.markdown("---")
st.session_state.show_completed = st.sidebar.checkbox("Show Completed Tasks", st.session_state.show_completed)

# Sort tasks by priority
priority_order = {"High": 0, "Medium": 1, "Low": 2}
st.session_state.tasks.sort(key=lambda x: priority_order[x["priority"]])

# Display tasks
st.subheader("📋 Your To-Do List")
active_tasks = [task for task in st.session_state.tasks if not task["completed"]]
completed_tasks = [task for task in st.session_state.tasks if task["completed"]]

def save_edit(index, new_task_value, new_priority):
    st.session_state.tasks[index]["task"] = new_task_value
    st.session_state.tasks[index]["priority"] = new_priority
    st.session_state.editing_index = None
    st.rerun()

if not active_tasks:
    st.info("No pending tasks! Add new tasks from the sidebar.")
else:
    for index, task in enumerate(active_tasks):
        with stylable_container("task_container", css_styles="padding: 10px; margin: 5px; border-radius: 10px; background-color: #f0f2f6;"):
            col1, col2, col3, col4 = st.columns([0.6, 0.1, 0.15, 0.15])
            
            # Mark task as complete
            completed = col1.checkbox(f"**{task['task']}** ({task['priority']})", task["completed"], key=f"check_{index}")
            if completed:
                st.session_state.tasks[index]["completed"] = True
                st.success(f"✅ Task '{task['task']}' marked as completed!")
                st.rerun()
            
            # Edit task
            if col2.button("✏️", key=f"edit_{index}"):
                st.session_state.editing_index = index
                st.rerun()
            
            # Delete task
            if col3.button("❌", key=f"delete_{index}"):
                deleted_task = st.session_state.tasks[index]["task"]
                del st.session_state.tasks[index]
                st.warning(f"🗑️ Task '{deleted_task}' deleted!")
                st.rerun()

# Edit mode
if st.session_state.editing_index is not None:
    index = st.session_state.editing_index
    task = st.session_state.tasks[index]
    new_task_value = st.text_input("Edit task", task["task"], key='edit_task')
    new_priority = st.selectbox("Priority", ["Low", "Medium", "High"], index=["Low", "Medium", "High"].index(task["priority"]), key='edit_priority')
    if st.button("💾 Save", key='save_edit'):
        save_edit(index, new_task_value, new_priority)

# Display completed tasks separately if enabled
if st.session_state.show_completed:
    st.subheader("✅ Completed Tasks")
    if completed_tasks:
        for index, task in enumerate(completed_tasks):
            with stylable_container("completed_task_container", css_styles="padding: 10px; margin: 5px; border-radius: 10px; background-color: #d4edda;"):
                col1, col2, col3 = st.columns([0.7, 0.15, 0.15])
                col1.write(f"- {task['task']} ({task['priority']})")
                
                # Mark completed task as incomplete
                if col2.button("🔄", key=f"restore_{index}"):
                    st.session_state.tasks[index]["completed"] = False
                    st.info(f"🔄 Task '{task['task']}' moved back to active list!")
                    st.rerun()
                
                # Delete completed task
                if col3.button("🗑️", key=f"delete_completed_{index}"):
                    st.session_state.tasks.remove(task)
                    st.warning(f"🗑️ Completed task '{task['task']}' deleted!")
                    st.rerun()
    else:
        st.info("No completed tasks yet!")

# Save all tasks
if st.button("💾 Save All Tasks"):
    with open("tasks.json", "w") as f:
        json.dump(st.session_state.tasks, f)
    st.session_state.tasks = []  # Clear all tasks after saving
    st.success("💾 All tasks saved successfully!")
    st.rerun()

# Clear all tasks
if st.button("🗑️ Clear All Tasks"):
    st.session_state.tasks = []
    st.success("🧹 All tasks deleted successfully!")

# Footer
st.markdown('---')
st.caption("🚀 Stay organized & productive with this enhanced to-do list app.")
