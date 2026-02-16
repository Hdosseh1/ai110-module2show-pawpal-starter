import streamlit as st

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

# Import core PawPal system classes for later integration
from pawpal_system import User, Pet, Task, TaskScheduler, UserDataManager
from datetime import datetime, time
import uuid

st.title("🐾 PawPal+")
st.divider()

# Ensure a User object exists in session_state
if 'pawpal_user' not in st.session_state:
    st.session_state['pawpal_user'] = User(username="Jordan", password='')

user: User = st.session_state['pawpal_user']

# Archived tasks store (in-memory session)
if 'archived_tasks' not in st.session_state:
    st.session_state['archived_tasks'] = []

st.subheader("Manage Pets & Tasks")

# -----------------------
# Add Pet
# -----------------------
with st.expander("Add Pet", expanded=False):
    new_pet_name = st.text_input("Pet name", key="form_pet_name")
    new_species = st.selectbox("Species", ["dog", "cat", "other"], key="form_pet_species")
    new_age = st.number_input("Age", min_value=0, max_value=50, value=2, key="form_pet_age")
    new_health = st.text_input("Health info", value="Healthy", key="form_pet_health")

    if st.button("Add Pet", key="form_add_pet"):
        pet_id = f"{user.username}-{new_pet_name}-{uuid.uuid4().hex[:6]}"
        pet = Pet(
            pet_id=pet_id,
            name=new_pet_name,
            species=new_species,
            age=int(new_age),
            health_info=new_health
        )
        user.pets.append(pet)
        st.success(f"Added pet: {pet.name}")

# -----------------------
# Add Task
# -----------------------
with st.expander("Add Task", expanded=False):

    if not user.pets:
        st.info("Add a pet first to attach tasks.")
    else:
        add_pet_options = [p.name for p in user.pets]
        add_selected_pet = st.selectbox("Select pet", options=add_pet_options, key="form_task_pet")
        add_title = st.text_input("Task title", value="Morning walk", key="form_task_title")
        add_duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20, key="form_task_duration")
        add_priority_str = st.selectbox("Priority", ["low", "medium", "high"], index=2, key="form_task_priority")
        add_is_med = st.checkbox("Is medication", value=False, key="form_task_med")
        add_pref_time = st.selectbox("Preferred time", ["flexible", "morning", "evening"], index=0, key="form_task_pref")
        add_recurring = st.checkbox("Recurring", value=False, key="form_task_recurring")

        priority_map = {"low": 2, "medium": 3, "high": 5}

        if st.button("Add Task", key="form_add_task"):
            pet_obj = next((p for p in user.pets if p.name == add_selected_pet), None)

            if pet_obj:
                task_id = uuid.uuid4().hex
                task = Task(
                    task_id=task_id,
                    pet_id=pet_obj.pet_id,
                    name=add_title,
                    duration=int(add_duration),
                    priority=priority_map.get(add_priority_str, 3),
                    category="general",
                    is_medication=add_is_med,
                    preferred_time=add_pref_time,
                    is_recurring=add_recurring,
                )
                pet_obj.add_task(task)
                st.success(f"Added task '{task.name}' to {pet_obj.name}")

# -----------------------
# Task Overview
# -----------------------
st.markdown("### Current Task Overview")

if user.pets:
    for p in user.pets:
        with st.expander(f"📋 {p.name} ({len(p.tasks)} tasks)", expanded=False):
            if p.tasks:
                task_data = []
                for t in p.tasks:
                    task_data.append({
                        "Task": t.name,
                        "Duration (min)": t.duration,
                        "Priority": "🔴 High" if t.priority >= 4 else "🟡 Medium" if t.priority >= 3 else "🟢 Low",
                        "Category": t.category,
                        "Medication": "✓" if t.is_medication else "✗",
                        "Recurring": "✓" if t.is_recurring else "✗"
                    })
                st.dataframe(task_data, use_container_width=True, hide_index=True)
            else:
                st.info(f"No tasks yet for {p.name}.")
else:
    st.info("No pets added yet. Add a pet to get started!")

st.divider()

# -----------------------
# Schedule Builder
# -----------------------
st.subheader("Build Schedule")
st.caption("Generate a daily schedule based on your availability and pet tasks.")

col_avail1, col_avail2 = st.columns(2)
with col_avail1:
    avail_start = st.time_input("Available from", value=time(9, 0))
with col_avail2:
    avail_end = st.time_input("Available until", value=time(17, 0))

if st.button("Generate schedule", type="primary"):

    if not user or not user.pets:
        st.error("❌ No user or pets found. Please add a pet and tasks first.")
    elif not any(p.tasks for p in user.pets):
        st.error("❌ No tasks found. Please add at least one task.")
    else:
        user.availability = [f"{avail_start.strftime('%H:%M')}-{avail_end.strftime('%H:%M')}"]
        scheduler = TaskScheduler(user)
        schedule = scheduler.schedule_tasks(datetime.now())

        st.session_state['last_schedule'] = schedule

        udm = UserDataManager()
        udm.save_user(user)

        try:
            udm.save_schedule(schedule)
        except Exception:
            pass

        st.success("✓ Schedule generated and saved.")

# -----------------------
# Display Schedule
# -----------------------
schedule = st.session_state.get('last_schedule')

if schedule:
    st.divider()
    st.markdown("## 📅 Generated Schedule")

    if schedule.scheduled_tasks:
        st.markdown("### Tasks Scheduled (sorted by time)")
        task_rows = []
