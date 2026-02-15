# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## Smarter Scheduling Features

The PawPal+ scheduler now includes advanced features for intelligent task planning:

### Time-Based Sorting
- Tasks are sorted by scheduled time using efficient lambda-based sorting
- Query methods like `get_tasks_by_time()` return chronologically ordered schedules
- Supports HH:MM time format parsing and comparison

### Flexible Filtering
- **By Pet**: `get_tasks_by_pet(pet_id)` — view tasks for a specific pet
- **By Status**: `get_tasks_by_status(status)` — filter pending, in-progress, or completed tasks
- **By Time Range**: `get_tasks_in_time_range(start, end)` — find tasks within a window
- All filters return time-sorted results for easy scanning

### Recurring Tasks with Auto-Rescheduling
- Tasks can be marked as recurring (daily, weekly, every_other_day)
- When a recurring task is marked complete, the next due date is automatically calculated
- Uses Python's `timedelta` for accurate date arithmetic:
  - Daily tasks: next due = today + 1 day
  - Every-other-day: next due = today + 2 days
  - Weekly: next due = next matching weekday
- Next due date persists across sessions (saved/loaded with user data)

### Conflict Detection
- Identifies overlapping tasks using interval overlap logic
- Reports all conflicts with task names and time ranges
- Integrated into schedule explanations for transparency
- Enables manual resolution or future automated conflict prevention

### Advanced Scheduling
- Prioritizes medications first, then by task priority, then by time preference
- Respects user availability constraints
- Generates detailed explanations of scheduling decisions
- Tracks which tasks couldn't fit and why (insufficient time)
