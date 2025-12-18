"""
Unit tests for scheduler module.
"""

import unittest
from datetime import datetime, timedelta
from src.job import Job, Machine
from src.scheduler import FuzzyScheduler


class TestFuzzyScheduler(unittest.TestCase):
    """Test FuzzyScheduler class."""
    
    def setUp(self):
        """Set up test scheduler with jobs and machines."""
        self.scheduler = FuzzyScheduler()
        self.current_time = datetime.now()
        
        # Add machines
        self.machine1 = Machine("M1", "Machine 1")
        self.machine2 = Machine("M2", "Machine 2")
        self.scheduler.add_machine(self.machine1)
        self.scheduler.add_machine(self.machine2)
        
        # Add jobs
        self.jobs = [
            Job(
                job_id=f"J{i:03d}",
                name=f"Job {i}",
                processing_time=10.0 + i * 2,
                due_date=self.current_time + timedelta(hours=24 + i * 12),
                arrival_time=self.current_time + timedelta(hours=i),
                machine_required="M1" if i % 2 == 0 else "M2"
            )
            for i in range(1, 6)
        ]
        
        for job in self.jobs:
            self.scheduler.add_job(job)
    
    def test_scheduler_initialization(self):
        """Test scheduler initialization."""
        self.assertEqual(len(self.scheduler.machines), 2)
        self.assertEqual(len(self.scheduler.jobs), 5)
    
    def test_add_machine(self):
        """Test adding machine to scheduler."""
        machine3 = Machine("M3", "Machine 3")
        self.scheduler.add_machine(machine3)
        self.assertEqual(len(self.scheduler.machines), 3)
        self.assertIn("M3", self.scheduler.machines)
    
    def test_add_jobs(self):
        """Test adding multiple jobs."""
        new_jobs = [
            Job(
                job_id="J100",
                name="New Job",
                processing_time=5.0,
                due_date=self.current_time + timedelta(hours=12),
                arrival_time=self.current_time,
                machine_required="M1"
            )
        ]
        self.scheduler.add_jobs(new_jobs)
        self.assertEqual(len(self.scheduler.jobs), 6)
    
    def test_calculate_job_priority(self):
        """Test job priority calculation."""
        job = self.jobs[0]
        machine = self.machine1
        priority = self.scheduler.calculate_job_priority(job, machine)
        
        self.assertGreaterEqual(priority, 0)
        self.assertLessEqual(priority, 100)
    
    def test_schedule_fuzzy_priority(self):
        """Test fuzzy priority scheduling algorithm."""
        scheduled = self.scheduler.schedule_jobs(algorithm="fuzzy_priority")
        
        self.assertGreater(len(scheduled), 0)
        for job in scheduled:
            self.assertIsNotNone(job.assigned_machine)
            self.assertEqual(job.status, "scheduled")
    
    def test_schedule_fcfs(self):
        """Test First-Come-First-Served scheduling."""
        scheduled = self.scheduler.schedule_jobs(algorithm="fcfs")
        
        self.assertGreater(len(scheduled), 0)
        # Check jobs are scheduled in arrival order
        prev_arrival = None
        for job in scheduled:
            if prev_arrival:
                self.assertGreaterEqual(job.arrival_time, prev_arrival)
            prev_arrival = job.arrival_time
    
    def test_schedule_edd(self):
        """Test Earliest Due Date scheduling."""
        scheduled = self.scheduler.schedule_jobs(algorithm="edd")
        
        self.assertGreater(len(scheduled), 0)
        # Check jobs are scheduled in due date order
        prev_due = None
        for job in scheduled:
            if prev_due:
                self.assertGreaterEqual(job.due_date, prev_due)
            prev_due = job.due_date
    
    def test_invalid_algorithm(self):
        """Test scheduling with invalid algorithm."""
        with self.assertRaises(ValueError):
            self.scheduler.schedule_jobs(algorithm="invalid_algo")
    
    def test_get_schedule_summary(self):
        """Test schedule summary generation."""
        self.scheduler.schedule_jobs()
        summary = self.scheduler.get_schedule_summary()
        
        self.assertIn('total_jobs', summary)
        self.assertIn('scheduled_jobs', summary)
        self.assertIn('pending_jobs', summary)
        self.assertIn('total_machines', summary)
        self.assertIn('makespan_hours', summary)
        self.assertIn('average_priority', summary)
        self.assertIn('machine_utilization', summary)
        
        self.assertEqual(summary['total_jobs'], 5)
        self.assertEqual(summary['total_machines'], 2)
    
    def test_get_job_by_id(self):
        """Test finding job by ID."""
        job = self.scheduler.get_job_by_id("J001")
        self.assertIsNotNone(job)
        self.assertEqual(job.job_id, "J001")
        
        non_existent = self.scheduler.get_job_by_id("J999")
        self.assertIsNone(non_existent)
    
    def test_reschedule(self):
        """Test rescheduling jobs."""
        self.scheduler.schedule_jobs()
        initial_scheduled = len([j for j in self.scheduler.jobs if j.status == "scheduled"])
        
        self.scheduler.reschedule()
        rescheduled = len([j for j in self.scheduler.jobs if j.status == "scheduled"])
        
        self.assertEqual(initial_scheduled, rescheduled)


class TestSchedulingIntegration(unittest.TestCase):
    """Integration tests for scheduling system."""
    
    def test_complete_scheduling_workflow(self):
        """Test complete scheduling workflow."""
        scheduler = FuzzyScheduler()
        current_time = datetime.now()
        
        # Add machines
        machines = [
            Machine("M1", "CNC Machine"),
            Machine("M2", "Assembly Line")
        ]
        for machine in machines:
            scheduler.add_machine(machine)
        
        # Add diverse jobs
        jobs = [
            Job("J001", "Urgent Short Job", 5.0,
                current_time + timedelta(hours=8),
                current_time, "M1"),
            Job("J002", "Long Job", 20.0,
                current_time + timedelta(hours=48),
                current_time, "M2"),
            Job("J003", "Medium Job", 10.0,
                current_time + timedelta(hours=24),
                current_time, "M1"),
        ]
        scheduler.add_jobs(jobs)
        
        # Schedule
        scheduled = scheduler.schedule_jobs(algorithm="fuzzy_priority")
        
        # Verify all jobs scheduled
        self.assertEqual(len(scheduled), 3)
        
        # Verify priority ordering (urgent short job should have high priority)
        priorities = {job.job_id: job.priority_score for job in scheduled}
        # J001 is urgent and short, should have higher priority than J002 (long job)
        self.assertGreaterEqual(priorities["J001"], priorities["J002"])
        
        # Get summary
        summary = scheduler.get_schedule_summary()
        self.assertEqual(summary['scheduled_jobs'], 3)
        self.assertEqual(summary['pending_jobs'], 0)


if __name__ == '__main__':
    unittest.main()
