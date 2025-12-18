"""
Unit tests for job module.
"""

import unittest
from datetime import datetime, timedelta
from src.job import Job, Machine


class TestJob(unittest.TestCase):
    """Test Job class."""
    
    def setUp(self):
        """Set up test job."""
        self.current_time = datetime.now()
        self.job = Job(
            job_id="J001",
            name="Test Job",
            processing_time=10.0,
            due_date=self.current_time + timedelta(hours=24),
            arrival_time=self.current_time,
            machine_required="M1"
        )
    
    def test_job_creation(self):
        """Test job creation with valid data."""
        self.assertEqual(self.job.job_id, "J001")
        self.assertEqual(self.job.name, "Test Job")
        self.assertEqual(self.job.processing_time, 10.0)
        self.assertEqual(self.job.status, "pending")
    
    def test_invalid_processing_time(self):
        """Test job creation with invalid processing time."""
        with self.assertRaises(ValueError):
            Job(
                job_id="J002",
                name="Invalid Job",
                processing_time=-5.0,
                due_date=self.current_time + timedelta(hours=24),
                arrival_time=self.current_time,
                machine_required="M1"
            )
    
    def test_invalid_due_date(self):
        """Test job creation with due date before arrival."""
        with self.assertRaises(ValueError):
            Job(
                job_id="J003",
                name="Invalid Job",
                processing_time=10.0,
                due_date=self.current_time - timedelta(hours=1),
                arrival_time=self.current_time,
                machine_required="M1"
            )
    
    def test_calculate_urgency_high(self):
        """Test urgency calculation for urgent job."""
        urgent_job = Job(
            job_id="J004",
            name="Urgent Job",
            processing_time=10.0,
            due_date=self.current_time + timedelta(hours=5),
            arrival_time=self.current_time,
            machine_required="M1"
        )
        urgency = urgent_job.calculate_urgency(self.current_time)
        self.assertGreater(urgency, 5.0)
    
    def test_calculate_urgency_low(self):
        """Test urgency calculation for non-urgent job."""
        non_urgent_job = Job(
            job_id="J005",
            name="Non-urgent Job",
            processing_time=10.0,
            due_date=self.current_time + timedelta(hours=200),
            arrival_time=self.current_time,
            machine_required="M1"
        )
        urgency = non_urgent_job.calculate_urgency(self.current_time)
        self.assertLess(urgency, 3.0)
    
    def test_is_overdue(self):
        """Test overdue detection."""
        overdue_job = Job(
            job_id="J006",
            name="Overdue Job",
            processing_time=10.0,
            due_date=self.current_time - timedelta(hours=1),
            arrival_time=self.current_time - timedelta(hours=5),
            machine_required="M1"
        )
        self.assertTrue(overdue_job.is_overdue(self.current_time))
        self.assertFalse(self.job.is_overdue(self.current_time))
    
    def test_slack_time_positive(self):
        """Test slack time calculation (positive)."""
        slack = self.job.get_slack_time(self.current_time)
        self.assertGreater(slack, 0)
    
    def test_slack_time_negative(self):
        """Test slack time calculation (negative)."""
        tight_job = Job(
            job_id="J007",
            name="Tight Job",
            processing_time=20.0,
            due_date=self.current_time + timedelta(hours=10),
            arrival_time=self.current_time,
            machine_required="M1"
        )
        slack = tight_job.get_slack_time(self.current_time)
        self.assertLess(slack, 0)


class TestMachine(unittest.TestCase):
    """Test Machine class."""
    
    def setUp(self):
        """Set up test machine and jobs."""
        self.machine = Machine("M1", "Test Machine", capacity=1.0)
        self.current_time = datetime.now()
        self.job1 = Job(
            job_id="J001",
            name="Job 1",
            processing_time=10.0,
            due_date=self.current_time + timedelta(hours=24),
            arrival_time=self.current_time,
            machine_required="M1"
        )
        self.job2 = Job(
            job_id="J002",
            name="Job 2",
            processing_time=5.0,
            due_date=self.current_time + timedelta(hours=12),
            arrival_time=self.current_time,
            machine_required="M1"
        )
    
    def test_machine_creation(self):
        """Test machine creation."""
        self.assertEqual(self.machine.machine_id, "M1")
        self.assertEqual(self.machine.name, "Test Machine")
        self.assertEqual(len(self.machine.scheduled_jobs), 0)
    
    def test_add_job(self):
        """Test adding job to machine."""
        self.machine.add_job(self.job1)
        self.assertEqual(len(self.machine.scheduled_jobs), 1)
        self.assertEqual(self.job1.assigned_machine, "M1")
        self.assertEqual(self.job1.status, "scheduled")
    
    def test_remove_job(self):
        """Test removing job from machine."""
        self.machine.add_job(self.job1)
        removed = self.machine.remove_job("J001")
        self.assertIsNotNone(removed)
        self.assertEqual(len(self.machine.scheduled_jobs), 0)
        self.assertIsNone(removed.assigned_machine)
        self.assertEqual(removed.status, "pending")
    
    def test_remove_nonexistent_job(self):
        """Test removing non-existent job."""
        removed = self.machine.remove_job("J999")
        self.assertIsNone(removed)
    
    def test_current_load(self):
        """Test machine load calculation."""
        self.machine.add_job(self.job1)
        self.machine.add_job(self.job2)
        load = self.machine.get_current_load()
        self.assertGreater(load, 0)
        self.assertLessEqual(load, 100)
    
    def test_utilization_update(self):
        """Test utilization update when adding jobs."""
        initial_utilization = self.machine.utilization
        self.machine.add_job(self.job1)
        self.assertGreater(self.machine.utilization, initial_utilization)


if __name__ == '__main__':
    unittest.main()
