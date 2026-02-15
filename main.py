from datetime import datetime, time
from pawpal_system import User, Pet, Task, TaskScheduler, UserDataManager

def main():
    """Test the PawPal+ system by creating users, pets, tasks, and generating a schedule."""
    
    print("=" * 60)
    print("PawPal+ System Test")
    print("=" * 60)
    
    # ==================== CREATE USER ====================
    print("\n1. Creating user...")
    user = User(
        username="johndoe",
        password="secure123",
        availability=["9:00-17:00"],  # Available 9 AM to 5 PM
        preferences={"pet_care_style": "balanced", "preferred_times": "morning"}
    )
    print(f"   ✓ User created: {user.username}")
    print(f"   ✓ Availability: {user.availability}")
    
    # ==================== CREATE PETS ====================
    print("\n2. Creating pets...")
    
    # Pet 1: Dog
    dog = Pet(
        pet_id="pet_001",
        name="Max",
        species="Dog",
        age=3,
        health_info="Healthy, needs daily walks",
        task_priorities={"walk": 5, "feeding": 4, "play": 3},
        user_preferences={"preferred_walk_time": "morning", "frequency": "2x daily"}
    )
    print(f"   ✓ Pet created: {dog.name} ({dog.species})")
    
    # Pet 2: Cat
    cat = Pet(
        pet_id="pet_002",
        name="Whiskers",
        species="Cat",
        age=5,
        health_info="Healthy, on medication",
        task_priorities={"feeding": 5, "medication": 5, "play": 2},
        user_preferences={"preferred_feeding_time": "morning and evening"}
    )
    print(f"   ✓ Pet created: {cat.name} ({cat.species})")
    
    # Add pets to user
    user.pets = [dog, cat]
    
    # ==================== CREATE TASKS ====================
    print("\n3. Adding tasks to pets...")
    
    # Dog tasks
    dog_walk_morning = Task(
        task_id="task_001",
        pet_id="pet_001",
        name="Morning Walk",
        duration=30,  # 30 minutes
        priority=5,
        category="walk",
        is_medication=False,
        preferred_time="morning"
    )
    dog.add_task(dog_walk_morning)
    print(f"   ✓ Task added to {dog.name}: {dog_walk_morning.name} ({dog_walk_morning.duration} min, priority {dog_walk_morning.priority})")
    
    dog_feeding = Task(
        task_id="task_002",
        pet_id="pet_001",
        name="Feeding",
        duration=15,
        priority=4,
        category="feeding",
        is_medication=False,
        preferred_time="flexible"
    )
    dog.add_task(dog_feeding)
    print(f"   ✓ Task added to {dog.name}: {dog_feeding.name} ({dog_feeding.duration} min, priority {dog_feeding.priority})")
    
    dog_evening_walk = Task(
        task_id="task_003",
        pet_id="pet_001",
        name="Evening Walk",
        duration=30,
        priority=5,
        category="walk",
        is_medication=False,
        preferred_time="evening"
    )
    dog.add_task(dog_evening_walk)
    print(f"   ✓ Task added to {dog.name}: {dog_evening_walk.name} ({dog_evening_walk.duration} min, priority {dog_evening_walk.priority})")
    
    # Cat tasks
    cat_medication = Task(
        task_id="task_004",
        pet_id="pet_002",
        name="Morning Medication",
        duration=5,
        priority=5,
        category="medication",
        is_medication=True,
        preferred_time="morning"
    )
    cat.add_task(cat_medication)
    print(f"   ✓ Task added to {cat.name}: {cat_medication.name} ({cat_medication.duration} min, priority {cat_medication.priority}, MEDICATION)")
    
    cat_feeding_morning = Task(
        task_id="task_005",
        pet_id="pet_002",
        name="Morning Feeding",
        duration=10,
        priority=5,
        category="feeding",
        is_medication=False,
        preferred_time="morning"
    )
    cat.add_task(cat_feeding_morning)
    print(f"   ✓ Task added to {cat.name}: {cat_feeding_morning.name} ({cat_feeding_morning.duration} min, priority {cat_feeding_morning.priority})")
    
    cat_play = Task(
        task_id="task_006",
        pet_id="pet_002",
        name="Playtime",
        duration=20,
        priority=2,
        category="play",
        is_medication=False,
        preferred_time="flexible"
    )
    cat.add_task(cat_play)
    print(f"   ✓ Task added to {cat.name}: {cat_play.name} ({cat_play.duration} min, priority {cat_play.priority})")
    
    # ==================== GENERATE SCHEDULE ====================
    print("\n4. Generating daily schedule...")
    scheduler = TaskScheduler(user)
    today = datetime.now()
    schedule = scheduler.schedule_tasks(today)
    
    print(f"   ✓ Schedule generated for {today.strftime('%A, %B %d, %Y')}")
    
    # ==================== DISPLAY SCHEDULE ====================
    print("\n" + "=" * 60)
    print("TODAY'S SCHEDULE")
    print("=" * 60)
    
    print(f"\nUser: {user.username}")
    print(f"Date: {today.strftime('%A, %B %d, %Y')}")
    print(f"Available: {', '.join(user.availability)}")
    
    print("\n" + "-" * 60)
    print("SCHEDULED TASKS (in order):")
    print("-" * 60)
    
    tasks_by_time = schedule.get_tasks_by_time()
    if tasks_by_time:
        for i, scheduled_task in enumerate(tasks_by_time, 1):
            pet_name = next((p.name for p in user.pets if p.pet_id == scheduled_task.pet_id), "Unknown Pet")
            print(f"\n{i}. {scheduled_task.task.name}")
            print(f"   Pet: {pet_name} ({scheduled_task.pet_id})")
            print(f"   Time: {scheduled_task.start_time.strftime('%H:%M')} - {scheduled_task.end_time.strftime('%H:%M')}")
            print(f"   Duration: {scheduled_task.task.duration} minutes")
            print(f"   Priority: {scheduled_task.task.priority}/5")
            print(f"   Category: {scheduled_task.task.category}")
            if scheduled_task.task.is_medication:
                print(f"   ⚠️  MEDICATION")
    else:
        print("No tasks scheduled!")
    
    print("\n" + "-" * 60)
    print("SCHEDULING EXPLANATION:")
    print("-" * 60)
    print(schedule.get_explanation())
    
    # ==================== SAVE USER DATA ====================
    print("\n" + "=" * 60)
    print("5. Saving user data to storage...")
    data_manager = UserDataManager()
    data_manager.save_user(user)
    print(f"   ✓ User data saved for '{user.username}'")
    
    # ==================== LOAD USER DATA ====================
    print("\n6. Testing data persistence (loading user)...")
    loaded_user = data_manager.load_user(user.username)
    if loaded_user:
        print(f"   ✓ User loaded: {loaded_user.username}")
        print(f"   ✓ Pets: {', '.join(pet.name for pet in loaded_user.pets)}")
        total_tasks = sum(len(pet.tasks) for pet in loaded_user.pets)
        print(f"   ✓ Total tasks: {total_tasks}")
    else:
        print("   ✗ Failed to load user")
    
    # ==================== SAVE SCHEDULE ====================
    print("\n7. Saving schedule to storage...")
    data_manager.save_schedule(schedule)
    print(f"   ✓ Schedule saved for {today.strftime('%Y-%m-%d')}")
    
    print("\n" + "=" * 60)
    print("Test Complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
