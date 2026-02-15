from dataclasses import dataclass, field
from datetime import datetime, time
from typing import List, Dict, Optional

# ==================== USER ====================
@dataclass
class User:
    username: str
    password: str
    availability: List[str] = field(default_factory=list)  # e.g., ["Mon-Fri: 9-5", "Sat: 10-12"]
    preferences: Dict[str, str] = field(default_factory=dict)
    pets: List['Pet'] = field(default_factory=list)
    
    def get_availability(self) -> List[str]:
        pass
    
    def update_profile(self) -> None:
        pass


# ==================== TASK ====================
@dataclass
class Task:
    task_id: str
    pet_id: str
    name: str
    duration: int  # in minutes
    priority: int  # 1-5, 5 being highest
    category: str  # e.g., "feeding", "walk", "medication"
    is_medication: bool = False
    
    def get_details(self) -> Dict:
        pass
    
    def update_priority(self, new_priority: int) -> None:
        pass


# ==================== PET ====================
@dataclass
class Pet:
    pet_id: str
    name: str
    species: str
    age: int
    health_info: str
    task_priorities: Dict[str, int] = field(default_factory=dict)  # task category -> priority
    user_preferences: Dict[str, str] = field(default_factory=dict)
    tasks: List[Task] = field(default_factory=list)
    
    def get_profile(self) -> Dict:
        pass
    
    def update_profile(self) -> None:
        pass
    
    def add_task(self, task: Task) -> None:
        pass


# ==================== SCHEDULED TASK ====================
@dataclass
class ScheduledTask:
    task_id: str
    start_time: time
    end_time: time
    pet_id: str
    task: Task = None
    status: str = "pending"  # pending, in_progress, completed
    
    def mark_complete(self) -> None:
        pass
    
    def reschedule(self, new_start: time, new_end: time) -> None:
        pass


# ==================== DAILY SCHEDULE ====================
@dataclass
class DailySchedule:
    user_id: str
    date: datetime
    scheduled_tasks: List[ScheduledTask] = field(default_factory=list)
    explanation: str = ""
    
    def get_tasks_by_time(self) -> List[ScheduledTask]:
        pass
    
    def get_explanation(self) -> str:
        pass


# ==================== TASK SCHEDULER ====================
class TaskScheduler:
    def __init__(self, user: User):
        self.user = user
        self.pets = user.pets
    
    def schedule_tasks(self, date: datetime) -> DailySchedule:
        pass
    
    def _prioritize_tasks(self) -> List[Task]:
        pass
    
    def _fit_tasks_in_schedule(self, prioritized_tasks: List[Task]) -> List[ScheduledTask]:
        pass
    
    def _generate_explanation(self, schedule: DailySchedule) -> str:
        pass


# ==================== USER DATA MANAGER ====================
class UserDataManager:
    def __init__(self, storage_path: str = "users/"):
        self.storage_path = storage_path
    
    def save_user(self, user: User) -> None:
        """Save user with all nested pets, tasks, and schedules."""
        pass
    
    def load_user(self, username: str) -> Optional[User]:
        """Load user with all nested pets and tasks."""
        pass
    
    def delete_user(self, username: str) -> None:
        pass
    
    def user_exists(self, username: str) -> bool:
        pass
    
    def save_schedule(self, schedule: DailySchedule) -> None:
        """Persist daily schedule to storage."""
        pass
    
    def load_schedule(self, user_id: str, date: datetime) -> Optional[DailySchedule]:
        """Load schedule for user on specific date."""
        pass
