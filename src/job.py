"""
Job Module
Defines Job and Machine classes for manufacturing scheduling.
"""

from datetime import datetime, timedelta
from typing import Optional, List
from dataclasses import dataclass


@dataclass
class Job:
    """
    Represents a manufacturing job with all relevant attributes.
    """
    
    job_id: str
    name: str
    processing_time: float  # in hours
    due_date: datetime
    arrival_time: datetime
    machine_required: str
    priority_score: float = 0.0
    status: str = "pending"  # pending, scheduled, in_progress, completed
    assigned_machine: Optional[str] = None
    start_time: Optional[datetime] = None
    completion_time: Optional[datetime] = None
    
    def __post_init__(self):
        """Validate job attributes after initialization."""
        if self.processing_time <= 0:
            raise ValueError("Processing time must be positive")
        if self.due_date < self.arrival_time:
            raise ValueError("Due date cannot be before arrival time")
    
    def calculate_urgency(self, current_time: Optional[datetime] = None) -> float:
        """
        Calculate urgency based on time remaining until due date.
        
        Args:
            current_time: Current time for calculation (defaults to now)
            
        Returns:
            Urgency score (0-10, where 10 is most urgent)
        """
        if current_time is None:
            current_time = datetime.now()
        
        time_remaining = (self.due_date - current_time).total_seconds() / 3600  # in hours
        
        # Normalize urgency: less time = higher urgency
        if time_remaining <= 0:
            return 10.0  # Overdue
        elif time_remaining <= self.processing_time:
            return 9.0  # Very urgent
        elif time_remaining <= 2 * self.processing_time:
            return 7.0  # Urgent
        elif time_remaining <= 5 * self.processing_time:
            return 5.0  # Moderate
        elif time_remaining <= 10 * self.processing_time:
            return 3.0  # Low urgency
        else:
            return 1.0  # Not urgent
    
    def is_overdue(self, current_time: Optional[datetime] = None) -> bool:
        """
        Check if job is overdue.
        
        Args:
            current_time: Current time for comparison
            
        Returns:
            True if job is overdue
        """
        if current_time is None:
            current_time = datetime.now()
        return current_time > self.due_date and self.status != "completed"
    
    def get_slack_time(self, current_time: Optional[datetime] = None) -> float:
        """
        Calculate slack time (time available beyond processing time).
        
        Args:
            current_time: Current time for calculation
            
        Returns:
            Slack time in hours (negative if overdue)
        """
        if current_time is None:
            current_time = datetime.now()
        
        time_to_due = (self.due_date - current_time).total_seconds() / 3600
        return time_to_due - self.processing_time
    
    def __str__(self) -> str:
        """String representation of job."""
        return (f"Job({self.job_id}: {self.name}, "
                f"PT={self.processing_time}h, "
                f"Priority={self.priority_score:.2f}, "
                f"Status={self.status})")
    
    def __repr__(self) -> str:
        """Detailed representation of job."""
        return self.__str__()


class Machine:
    """
    Represents a manufacturing machine with capacity and scheduling information.
    """
    
    def __init__(self, machine_id: str, name: str, capacity: float = 1.0):
        """
        Initialize machine.
        
        Args:
            machine_id: Unique machine identifier
            name: Machine name
            capacity: Machine capacity (jobs/hour or utilization factor)
        """
        self.machine_id = machine_id
        self.name = name
        self.capacity = capacity
        self.scheduled_jobs: List[Job] = []
        self.current_job: Optional[Job] = None
        self.total_processing_time: float = 0.0
        self.utilization: float = 0.0
    
    def add_job(self, job: Job):
        """
        Add a job to machine's schedule.
        
        Args:
            job: Job to add
        """
        self.scheduled_jobs.append(job)
        job.assigned_machine = self.machine_id
        job.status = "scheduled"
        self.total_processing_time += job.processing_time
        self._update_utilization()
    
    def remove_job(self, job_id: str) -> Optional[Job]:
        """
        Remove a job from machine's schedule.
        
        Args:
            job_id: ID of job to remove
            
        Returns:
            Removed job if found, None otherwise
        """
        for i, job in enumerate(self.scheduled_jobs):
            if job.job_id == job_id:
                removed_job = self.scheduled_jobs.pop(i)
                removed_job.assigned_machine = None
                removed_job.status = "pending"
                self.total_processing_time -= removed_job.processing_time
                self._update_utilization()
                return removed_job
        return None
    
    def get_current_load(self) -> float:
        """
        Get current machine load as percentage.
        
        Returns:
            Load percentage (0-100)
        """
        # Simple load calculation based on scheduled jobs
        # In real system, this would consider time windows
        max_capacity = 100.0  # hours of work capacity
        return min(100.0, (self.total_processing_time / max_capacity) * 100)
    
    def _update_utilization(self):
        """Update machine utilization metric."""
        # Simplified utilization calculation
        max_time = 40.0  # 40 hours work week
        self.utilization = min(1.0, self.total_processing_time / max_time)
    
    def get_available_slot(self, processing_time: float, 
                          earliest_start: datetime) -> Optional[datetime]:
        """
        Find the earliest available time slot for a job.
        
        Args:
            processing_time: Required processing time
            earliest_start: Earliest possible start time
            
        Returns:
            Available start time or None if not available
        """
        if not self.scheduled_jobs:
            return earliest_start
        
        # Sort jobs by start time
        sorted_jobs = sorted([j for j in self.scheduled_jobs if j.start_time], 
                           key=lambda x: x.start_time)
        
        current_time = earliest_start
        for job in sorted_jobs:
            if job.start_time and job.start_time >= current_time + timedelta(hours=processing_time):
                return current_time
            if job.completion_time:
                current_time = max(current_time, job.completion_time)
        
        return current_time
    
    def __str__(self) -> str:
        """String representation of machine."""
        return (f"Machine({self.machine_id}: {self.name}, "
                f"Jobs={len(self.scheduled_jobs)}, "
                f"Load={self.get_current_load():.1f}%, "
                f"Utilization={self.utilization:.2f})")
    
    def __repr__(self) -> str:
        """Detailed representation of machine."""
        return self.__str__()
