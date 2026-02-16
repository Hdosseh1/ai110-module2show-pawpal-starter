import streamlit as st

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

# Import core PawPal system classes for later integration
from pawpal_system import User, Pet, Task, TaskScheduler, UserDataManager
from datetime import datetime, time
import uuid

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input("Owner name", value="Jordan")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

st.markdown("### Pets")
st.caption("Create a pet profile that tasks can be attached to.")

# Ensure a User object exists in session_state
if 'pawpal_user' not in st.session_state:
    st.session_state['pawpal_user'] = User(username=owner_name, password='')
else:
    # keep username in sync with input
    if st.session_state['pawpal_user'].username != owner_name:
        st.session_state['pawpal_user'].username = owner_name

user: User = st.session_state['pawpal_user']

colp1, colp2 = st.columns(2)
with colp1:
    pet_age = st.number_input("Pet age", min_value=0, max_value=50, value=2)
with colp2:
    health_info = st.text_input("Health info", value="Healthy")

if st.button("Add pet"):
    pet_id = f"{user.username}-{pet_name}-{uuid.uuid4().hex[:6]}"
    pet = Pet(pet_id=pet_id, name=pet_name, species=species, age=int(pet_age), health_info=health_info)
    user.pets.append(pet)
    st.success(f"Added pet: {pet.name}")

st.markdown("### Tasks")
st.caption("Add a task and attach it to one of your pets.")

pet_options = [p.name for p in user.pets] if user.pets else [pet_name]
selected_pet_name = st.selectbox("Select pet", options=pet_options, index=0)

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority_str = st.selectbox("Priority", ["low", "medium", "high"], index=2)

priority_map = {"low": 2, "medium": 3, "high": 5}

if st.button("Add task"):
    # find pet object
    pet_obj = None
    for p in user.pets:
        if p.name == selected_pet_name:
            pet_obj = p
            break
    # if no pet exists yet, create one from quick inputs
    if pet_obj is None:
        pet_id = f"{user.username}-{selected_pet_name}-{uuid.uuid4().hex[:6]}"
        pet_obj = Pet(pet_id=pet_id, name=selected_pet_name, species=species, age=int(pet_age), health_info=health_info)
        user.pets.append(pet_obj)

    task_id = uuid.uuid4().hex
    task = Task(
        task_id=task_id,
        pet_id=pet_obj.pet_id,
        name=task_title,
        duration=int(duration),
        priority=priority_map.get(priority_str, 3),
        category="general",
    )
    pet_obj.add_task(task)
    st.success(f"Added task '{task.name}' to {pet_obj.name}")

# Display current tasks per pet
st.markdown("### Current Task Overview")
if user.pets:
    for p in user.pets:
        with st.expander(f"📋 {p.name} ({len(p.tasks)} tasks)", expanded=False):
            if p.tasks:
                # Sort and display tasks
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

st.subheader("Build Schedule")
st.caption("Generate a daily schedule based on your availability and pet tasks.")

col_avail1, col_avail2 = st.columns(2)
with col_avail1:
    avail_start = st.time_input("Available from", value=time(9, 0))
with col_avail2:
    avail_end = st.time_input("Available until", value=time(17, 0))

if st.button("Generate schedule", type="primary"):
    # ensure user exists in session
    user = st.session_state.get('pawpal_user')
    if not user or not user.pets:
        st.error("❌ No user or pets found. Please add a pet and tasks first.")
    elif not any(any(p.tasks) for p in user.pets):
        st.error("❌ No tasks found. Please add at least one task.")
    else:
        # Set user availability
        user.availability = [f"{avail_start.strftime('%H:%M')}-{avail_end.strftime('%H:%M')}"]
        
        scheduler = TaskScheduler(user)
        schedule = scheduler.schedule_tasks(datetime.now())
        
        # Show schedule results
        st.divider()
        st.markdown("## 📅 Generated Schedule")
        
        # Display scheduled tasks
        if schedule.scheduled_tasks:
            st.markdown("### Tasks Scheduled (sorted by time)")
            
            task_rows = []
            for st_task in schedule.get_tasks_by_time():
                task_rows.append({
                    "Time": f"{st_task.start_time.strftime('%H:%M')} - {st_task.end_time.strftime('%H:%M')}",
                    "Task": st_task.task.name,
                    "Pet": st_task.pet_id,
                    "Priority": "🔴 High" if st_task.task.priority >= 4 else "🟡 Medium" if st_task.task.priority >= 3 else "🟢 Low",
                    "Duration": f"{st_task.task.duration} min",
                    "Status": st_task.status
                })
            
            st.dataframe(task_rows, use_container_width=True, hide_index=True)
            st.success(f"✓ Successfully scheduled {len(schedule.scheduled_tasks)} task(s).")
        else:
            st.warning("⚠️ No tasks could be scheduled in the available time.")
        
        # Check for conflicts
        if schedule.has_conflicts():
            st.warning("⚠️ Schedule Conflicts Detected")
            conflict_text = schedule.get_conflict_summary()
            st.text(conflict_text)
        else:
            st.success("✓ No time conflicts detected.")
        
        # Show unscheduled tasks (if any)
        scheduled_ids = {t.task_id for t in schedule.scheduled_tasks}
        all_tasks = [t for p in user.pets for t in p.tasks]
        unscheduled = [t for t in all_tasks if t.task_id not in scheduled_ids]
        
        if unscheduled:
            st.info(f"ℹ️ {len(unscheduled)} task(s) could not fit in your available time")
            unscheduled_rows = [{
                "Task": t.name,
                "Pet": t.pet_id,
                "Duration (min)": t.duration,
                "Priority": "🔴 High" if t.priority >= 4 else "🟡 Medium" if t.priority >= 3 else "🟢 Low",
            } for t in unscheduled]
            st.dataframe(unscheduled_rows, use_container_width=True, hide_index=True)
        
        # Display full explanation
        with st.expander("📝 Detailed Explanation", expanded=False):
            st.text(schedule.get_explanation())
        
        # Persist schedule
        udm = UserDataManager()
        udm.save_user(user)
        udm.save_schedule(schedule)
        st.success("✓ Schedule generated and saved.")
