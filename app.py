import streamlit as st

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

# Import core PawPal system classes for later integration
from pawpal_system import User, Pet, Task, TaskScheduler, UserDataManager
from datetime import datetime
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
for p in user.pets:
    if p.tasks:
        st.write(f"Tasks for {p.name}:")
        st.table([t.get_details() for t in p.tasks])
    else:
        st.info(f"No tasks yet for {p.name}.")

st.divider()

st.subheader("Build Schedule")
st.caption("This button will generate a schedule using the backend scheduler.")

if st.button("Generate schedule"):
    # ensure user exists in session
    user = st.session_state.get('pawpal_user')
    if not user:
        st.error("No user found. Please set owner name and add a pet first.")
    else:
        scheduler = TaskScheduler(user)
        schedule = scheduler.schedule_tasks(datetime.now())
        st.subheader("Schedule Explanation")
        st.text(schedule.get_explanation())
        # Optionally persist schedule
        udm = UserDataManager()
        udm.save_user(user)
        udm.save_schedule(schedule)
        st.success("Schedule generated and saved.")
