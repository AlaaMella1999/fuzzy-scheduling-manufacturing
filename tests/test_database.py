"""
Unit tests for database module.
"""

import unittest
import os
from datetime import datetime, timedelta
from src.database import Database, JobModel, MachineModel
from src.job import Job, Machine


class TestDatabase(unittest.TestCase):
    """Test Database class."""
    
    def setUp(self):
        """Set up test database."""
        self.test_db_path = f"data/test_scheduling_{id(self)}.db"
        # Remove test database if exists
        if os.path.exists(self.test_db_path):
            try:
                os.remove(self.test_db_path)
            except PermissionError:
                pass
        self.db = Database(self.test_db_path)
        self.current_time = datetime.now()
    
    def tearDown(self):
        """Clean up test database."""
        self.db.close()
        if os.path.exists(self.test_db_path):
            try:
                os.remove(self.test_db_path)
            except PermissionError:
                pass
    
    def test_database_creation(self):
        """Test database file creation."""
        self.assertTrue(os.path.exists(self.test_db_path))
    
    def test_add_job(self):
        """Test adding job to database."""
        job = Job(
            job_id="J001",
            name="Test Job",
            processing_time=10.0,
            due_date=self.current_time + timedelta(hours=24),
            arrival_time=self.current_time,
            machine_required="M1"
        )
        
        job_model = self.db.add_job(job)
        self.assertIsNotNone(job_model)
        self.assertEqual(job_model.job_id, "J001")
    
    def test_get_job(self):
        """Test retrieving job from database."""
        job = Job(
            job_id="J002",
            name="Test Job 2",
            processing_time=15.0,
            due_date=self.current_time + timedelta(hours=36),
            arrival_time=self.current_time,
            machine_required="M2"
        )
        
        self.db.add_job(job)
        retrieved = self.db.get_job("J002")
        
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.job_id, "J002")
        self.assertEqual(retrieved.name, "Test Job 2")
    
    def test_update_job(self):
        """Test updating job in database."""
        job = Job(
            job_id="J003",
            name="Original Name",
            processing_time=10.0,
            due_date=self.current_time + timedelta(hours=24),
            arrival_time=self.current_time,
            machine_required="M1"
        )
        
        self.db.add_job(job)
        
        # Update job
        job.name = "Updated Name"
        job.priority_score = 75.0
        updated = self.db.update_job(job)
        
        self.assertIsNotNone(updated)
        self.assertEqual(updated.name, "Updated Name")
        self.assertEqual(updated.priority_score, 75.0)
    
    def test_delete_job(self):
        """Test deleting job from database."""
        job = Job(
            job_id="J004",
            name="To Delete",
            processing_time=10.0,
            due_date=self.current_time + timedelta(hours=24),
            arrival_time=self.current_time,
            machine_required="M1"
        )
        
        self.db.add_job(job)
        deleted = self.db.delete_job("J004")
        
        self.assertTrue(deleted)
        retrieved = self.db.get_job("J004")
        self.assertIsNone(retrieved)
    
    def test_get_all_jobs(self):
        """Test retrieving all jobs."""
        jobs = [
            Job(f"J{i:03d}", f"Job {i}", 10.0,
                self.current_time + timedelta(hours=24),
                self.current_time, "M1")
            for i in range(1, 4)
        ]
        
        for job in jobs:
            self.db.add_job(job)
        
        all_jobs = self.db.get_all_jobs()
        self.assertEqual(len(all_jobs), 3)
    
    def test_add_machine(self):
        """Test adding machine to database."""
        machine = Machine("M1", "Test Machine", capacity=1.0)
        machine_model = self.db.add_machine(machine)
        
        self.assertIsNotNone(machine_model)
        self.assertEqual(machine_model.machine_id, "M1")
    
    def test_update_machine(self):
        """Test updating machine in database."""
        machine = Machine("M2", "Original Machine")
        self.db.add_machine(machine)
        
        machine.name = "Updated Machine"
        machine.utilization = 0.75
        updated = self.db.update_machine(machine)
        
        self.assertIsNotNone(updated)
        self.assertEqual(updated.name, "Updated Machine")
        self.assertEqual(updated.utilization, 0.75)
    
    def test_get_all_machines(self):
        """Test retrieving all machines."""
        machines = [
            Machine(f"M{i}", f"Machine {i}")
            for i in range(1, 4)
        ]
        
        for machine in machines:
            self.db.add_machine(machine)
        
        all_machines = self.db.get_all_machines()
        self.assertEqual(len(all_machines), 3)
    
    def test_save_schedule_history(self):
        """Test saving schedule history."""
        schedule_info = {
            'algorithm': 'fuzzy_priority',
            'total_jobs': 10,
            'makespan_hours': 45.5,
            'average_priority': 65.3,
            'notes': 'Test schedule'
        }
        
        history = self.db.save_schedule_history(schedule_info)
        
        self.assertIsNotNone(history)
        self.assertEqual(history.algorithm_used, 'fuzzy_priority')
        self.assertEqual(history.total_jobs, 10)
    
    def test_get_schedule_history(self):
        """Test retrieving schedule history."""
        # Add multiple schedule records
        for i in range(5):
            schedule_info = {
                'algorithm': f'algo_{i}',
                'total_jobs': i * 10,
                'makespan_hours': i * 10.5,
                'average_priority': 50.0 + i * 5,
                'notes': f'Test {i}'
            }
            self.db.save_schedule_history(schedule_info)
        
        history = self.db.get_schedule_history(limit=3)
        self.assertEqual(len(history), 3)
        # Should be in descending order (most recent first)
        self.assertEqual(history[0].algorithm_used, 'algo_4')
    
    def test_context_manager(self):
        """Test database context manager."""
        with Database(self.test_db_path) as db:
            job = Job(
                job_id="J999",
                name="Context Job",
                processing_time=10.0,
                due_date=self.current_time + timedelta(hours=24),
                arrival_time=self.current_time,
                machine_required="M1"
            )
            db.add_job(job)
        
        # Verify job was saved
        with Database(self.test_db_path) as db:
            retrieved = db.get_job("J999")
            self.assertIsNotNone(retrieved)


if __name__ == '__main__':
    unittest.main()
