import pytest
from datetime import time
from pawpal_system import Pet, Task, ScheduledTask


def test_add_task_increases_count():
    pet = Pet(pet_id="p1", name="Buddy", species="Dog", age=2, health_info="")
    assert len(pet.tasks) == 0

    t = Task(task_id="t1", pet_id="p1", name="Feed", duration=10, priority=3, category="feeding")
    pet.add_task(t)

    assert len(pet.tasks) == 1
    assert pet.tasks[0] is t


def test_mark_complete_sets_status_completed():
    st = ScheduledTask(task_id="t1", start_time=time(9, 0), end_time=time(9, 10), pet_id="p1", task=None, status="pending")
    assert st.status == "pending"
    st.mark_complete()
    assert st.status == "completed"
