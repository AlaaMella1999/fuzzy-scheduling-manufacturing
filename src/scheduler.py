"""
Scheduler Module
Implements fuzzy logic-based scheduling algorithms for manufacturing.
"""

from datetime import datetime, timedelta
from typing import List, Dict, Optional
from src.job import Job, Machine
from src.fuzzy_logic import FuzzyInferenceSystem, create_scheduling_fuzzy_system


class FuzzyScheduler:
    """
    Fuzzy logic-based scheduler for manufacturing jobs.
    """
    
    def __init__(self):
        """Initialize fuzzy scheduler."""
        self.fuzzy_system: FuzzyInferenceSystem = create_scheduling_fuzzy_system()
        self.machines: Dict[str, Machine] = {}
        self.jobs: List[Job] = []
        self.scheduled_jobs: List[Job] = []
        self.current_time: datetime = datetime.now()
    
    def add_machine(self, machine: Machine):
        """
        Add a machine to the scheduler.
        
        Args:
            machine: Machine to add
        """
        self.machines[machine.machine_id] = machine
    
    def add_job(self, job: Job):
        """
        Add a job to the scheduler.
        
        Args:
            job: Job to add
        """
        self.jobs.append(job)
    
    def add_jobs(self, jobs: List[Job]):
        """
        Add multiple jobs to the scheduler.
        
        Args:
            jobs: List of jobs to add
        """
        self.jobs.extend(jobs)
    
    def calculate_job_priority(self, job: Job, machine: Machine) -> float:
        """
        Calculate job priority using fuzzy inference system.
        
        Args:
            job: Job to evaluate
            machine: Target machine for the job
            
        Returns:
            Priority score (0-100)
        """
        urgency = job.calculate_urgency(self.current_time)
        processing_time = job.processing_time
        machine_load = machine.get_current_load()
        
        inputs = {
            "urgency": urgency,
            "processing_time": processing_time,
            "machine_load": machine_load
        }
        
        priority = self.fuzzy_system.infer(inputs)
        return priority
    
    def schedule_jobs(self, algorithm: str = "fuzzy_priority") -> List[Job]:
        """
        Schedule all pending jobs using specified algorithm.
        
        Args:
            algorithm: Scheduling algorithm to use
                      - 'fuzzy_priority': Fuzzy logic-based priority
                      - 'fcfs': First-Come-First-Served
                      - 'edd': Earliest Due Date
                      
        Returns:
            List of scheduled jobs in execution order
        """
        pending_jobs = [job for job in self.jobs if job.status == "pending"]
        
        if algorithm == "fuzzy_priority":
            return self._schedule_fuzzy_priority(pending_jobs)
        elif algorithm == "fcfs":
            return self._schedule_fcfs(pending_jobs)
        elif algorithm == "edd":
            return self._schedule_edd(pending_jobs)
        else:
            raise ValueError(f"Unknown algorithm: {algorithm}")
    
    def _schedule_fuzzy_priority(self, jobs: List[Job]) -> List[Job]:
        """
        Schedule jobs using fuzzy priority-based algorithm.
        
        Args:
            jobs: List of jobs to schedule
            
        Returns:
            Scheduled jobs
        """
        # Calculate priorities for all jobs
        for job in jobs:
            if job.machine_required in self.machines:
                machine = self.machines[job.machine_required]
                job.priority_score = self.calculate_job_priority(job, machine)
            else:
                # If specific machine not found, use first available
                machine = list(self.machines.values())[0] if self.machines else None
                if machine:
                    job.priority_score = self.calculate_job_priority(job, machine)
                else:
                    job.priority_score = 50.0  # Default medium priority
        
        # Sort jobs by priority (descending)
        sorted_jobs = sorted(jobs, key=lambda j: j.priority_score, reverse=True)
        
        # Assign jobs to machines
        scheduled = []
        for job in sorted_jobs:
            assigned = self._assign_job_to_machine(job)
            if assigned:
                scheduled.append(job)
        
        self.scheduled_jobs.extend(scheduled)
        return scheduled
    
    def _schedule_fcfs(self, jobs: List[Job]) -> List[Job]:
        """
        Schedule jobs using First-Come-First-Served algorithm.
        
        Args:
            jobs: List of jobs to schedule
            
        Returns:
            Scheduled jobs
        """
        sorted_jobs = sorted(jobs, key=lambda j: j.arrival_time)
        scheduled = []
        
        for job in sorted_jobs:
            job.priority_score = 50.0  # Neutral priority for FCFS
            assigned = self._assign_job_to_machine(job)
            if assigned:
                scheduled.append(job)
        
        self.scheduled_jobs.extend(scheduled)
        return scheduled
    
    def _schedule_edd(self, jobs: List[Job]) -> List[Job]:
        """
        Schedule jobs using Earliest Due Date algorithm.
        
        Args:
            jobs: List of jobs to schedule
            
        Returns:
            Scheduled jobs
        """
        sorted_jobs = sorted(jobs, key=lambda j: j.due_date)
        scheduled = []
        
        for job in sorted_jobs:
            # Priority based on urgency
            job.priority_score = job.calculate_urgency(self.current_time) * 10
            assigned = self._assign_job_to_machine(job)
            if assigned:
                scheduled.append(job)
        
        self.scheduled_jobs.extend(scheduled)
        return scheduled
    
    def _assign_job_to_machine(self, job: Job) -> bool:
        """
        Assign a job to an appropriate machine.
        
        Args:
            job: Job to assign
            
        Returns:
            True if successfully assigned
        """
        # Try to assign to required machine
        if job.machine_required in self.machines:
            machine = self.machines[job.machine_required]
            start_time = machine.get_available_slot(job.processing_time, 
                                                    max(self.current_time, job.arrival_time))
            if start_time:
                job.start_time = start_time
                job.completion_time = start_time + timedelta(hours=job.processing_time)
                machine.add_job(job)
                return True
        
        # Try to assign to any available machine
        for machine in self.machines.values():
            start_time = machine.get_available_slot(job.processing_time,
                                                    max(self.current_time, job.arrival_time))
            if start_time:
                job.start_time = start_time
                job.completion_time = start_time + timedelta(hours=job.processing_time)
                machine.add_job(job)
                return True
        
        return False
    
    def get_schedule_summary(self) -> Dict:
        """
        Get summary of current schedule.
        
        Returns:
            Dictionary containing schedule statistics
        """
        total_jobs = len(self.jobs)
        scheduled = len([j for j in self.jobs if j.status in ["scheduled", "in_progress", "completed"]])
        pending = len([j for j in self.jobs if j.status == "pending"])
        
        total_makespan = 0.0
        if self.scheduled_jobs:
            completion_times = [j.completion_time for j in self.scheduled_jobs if j.completion_time]
            if completion_times:
                latest_completion = max(completion_times)
                total_makespan = (latest_completion - self.current_time).total_seconds() / 3600
        
        avg_priority = sum(j.priority_score for j in self.jobs) / total_jobs if total_jobs > 0 else 0
        
        machine_utilization = {
            machine_id: machine.utilization 
            for machine_id, machine in self.machines.items()
        }
        
        return {
            "total_jobs": total_jobs,
            "scheduled_jobs": scheduled,
            "pending_jobs": pending,
            "total_machines": len(self.machines),
            "makespan_hours": total_makespan,
            "average_priority": avg_priority,
            "machine_utilization": machine_utilization
        }
    
    def get_job_by_id(self, job_id: str) -> Optional[Job]:
        """
        Find job by ID.
        
        Args:
            job_id: Job identifier
            
        Returns:
            Job if found, None otherwise
        """
        for job in self.jobs:
            if job.job_id == job_id:
                return job
        return None
    
    def reschedule(self):
        """
        Reschedule all pending jobs (useful after changes).
        """
        # Reset scheduled jobs
        for job in self.jobs:
            if job.status == "scheduled":
                if job.assigned_machine and job.assigned_machine in self.machines:
                    self.machines[job.assigned_machine].remove_job(job.job_id)
        
        # Clear scheduled list and reschedule
        self.scheduled_jobs.clear()
        self.schedule_jobs()
