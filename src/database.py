"""
Database Module
Handles data persistence for jobs, machines, and schedules using SQLAlchemy.
"""

from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
from typing import List, Optional
import os

Base = declarative_base()


class JobModel(Base):
    """Database model for Job."""
    
    __tablename__ = 'jobs'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    job_id = Column(String, unique=True, nullable=False, index=True)
    name = Column(String, nullable=False)
    processing_time = Column(Float, nullable=False)
    due_date = Column(DateTime, nullable=False)
    arrival_time = Column(DateTime, nullable=False)
    machine_required = Column(String, nullable=False)
    priority_score = Column(Float, default=0.0)
    status = Column(String, default="pending")
    assigned_machine = Column(String, nullable=True)
    start_time = Column(DateTime, nullable=True)
    completion_time = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    def __repr__(self):
        return f"<JobModel(job_id='{self.job_id}', name='{self.name}', status='{self.status}')>"


class MachineModel(Base):
    """Database model for Machine."""
    
    __tablename__ = 'machines'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    machine_id = Column(String, unique=True, nullable=False, index=True)
    name = Column(String, nullable=False)
    capacity = Column(Float, default=1.0)
    total_processing_time = Column(Float, default=0.0)
    utilization = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    def __repr__(self):
        return f"<MachineModel(machine_id='{self.machine_id}', name='{self.name}')>"


class ScheduleHistoryModel(Base):
    """Database model for Schedule History."""
    
    __tablename__ = 'schedule_history'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    schedule_date = Column(DateTime, default=datetime.now)
    algorithm_used = Column(String, nullable=False)
    total_jobs = Column(Integer, default=0)
    total_makespan = Column(Float, default=0.0)
    average_priority = Column(Float, default=0.0)
    notes = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    
    def __repr__(self):
        return f"<ScheduleHistory(date='{self.schedule_date}', algorithm='{self.algorithm_used}')>"


class Database:
    """
    Database manager for the fuzzy scheduling system.
    """
    
    def __init__(self, db_path: str = "data/scheduling.db"):
        """
        Initialize database connection.
        
        Args:
            db_path: Path to SQLite database file
        """
        # Create data directory if it doesn't exist
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        self.db_path = db_path
        self.engine = create_engine(f'sqlite:///{db_path}', echo=False)
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
    
    def add_job(self, job) -> JobModel:
        """
        Add a job to the database.
        
        Args:
            job: Job object to add
            
        Returns:
            Created JobModel
        """
        job_model = JobModel(
            job_id=job.job_id,
            name=job.name,
            processing_time=job.processing_time,
            due_date=job.due_date,
            arrival_time=job.arrival_time,
            machine_required=job.machine_required,
            priority_score=job.priority_score,
            status=job.status,
            assigned_machine=job.assigned_machine,
            start_time=job.start_time,
            completion_time=job.completion_time
        )
        self.session.add(job_model)
        self.session.commit()
        return job_model
    
    def update_job(self, job) -> Optional[JobModel]:
        """
        Update an existing job in the database.
        
        Args:
            job: Job object with updated information
            
        Returns:
            Updated JobModel or None if not found
        """
        job_model = self.session.query(JobModel).filter_by(job_id=job.job_id).first()
        if job_model:
            job_model.name = job.name
            job_model.processing_time = job.processing_time
            job_model.due_date = job.due_date
            job_model.arrival_time = job.arrival_time
            job_model.machine_required = job.machine_required
            job_model.priority_score = job.priority_score
            job_model.status = job.status
            job_model.assigned_machine = job.assigned_machine
            job_model.start_time = job.start_time
            job_model.completion_time = job.completion_time
            job_model.updated_at = datetime.now()
            self.session.commit()
            return job_model
        return None
    
    def get_job(self, job_id: str) -> Optional[JobModel]:
        """
        Retrieve a job from the database.
        
        Args:
            job_id: Job identifier
            
        Returns:
            JobModel if found, None otherwise
        """
        return self.session.query(JobModel).filter_by(job_id=job_id).first()
    
    def get_all_jobs(self) -> List[JobModel]:
        """
        Retrieve all jobs from the database.
        
        Returns:
            List of all JobModels
        """
        return self.session.query(JobModel).all()
    
    def delete_job(self, job_id: str) -> bool:
        """
        Delete a job from the database.
        
        Args:
            job_id: Job identifier
            
        Returns:
            True if deleted, False if not found
        """
        job_model = self.session.query(JobModel).filter_by(job_id=job_id).first()
        if job_model:
            self.session.delete(job_model)
            self.session.commit()
            return True
        return False
    
    def add_machine(self, machine) -> MachineModel:
        """
        Add a machine to the database.
        
        Args:
            machine: Machine object to add
            
        Returns:
            Created MachineModel
        """
        machine_model = MachineModel(
            machine_id=machine.machine_id,
            name=machine.name,
            capacity=machine.capacity,
            total_processing_time=machine.total_processing_time,
            utilization=machine.utilization
        )
        self.session.add(machine_model)
        self.session.commit()
        return machine_model
    
    def update_machine(self, machine) -> Optional[MachineModel]:
        """
        Update an existing machine in the database.
        
        Args:
            machine: Machine object with updated information
            
        Returns:
            Updated MachineModel or None if not found
        """
        machine_model = self.session.query(MachineModel).filter_by(
            machine_id=machine.machine_id
        ).first()
        if machine_model:
            machine_model.name = machine.name
            machine_model.capacity = machine.capacity
            machine_model.total_processing_time = machine.total_processing_time
            machine_model.utilization = machine.utilization
            machine_model.updated_at = datetime.now()
            self.session.commit()
            return machine_model
        return None
    
    def get_all_machines(self) -> List[MachineModel]:
        """
        Retrieve all machines from the database.
        
        Returns:
            List of all MachineModels
        """
        return self.session.query(MachineModel).all()
    
    def save_schedule_history(self, schedule_info: dict) -> ScheduleHistoryModel:
        """
        Save schedule history to database.
        
        Args:
            schedule_info: Dictionary containing schedule information
            
        Returns:
            Created ScheduleHistoryModel
        """
        history = ScheduleHistoryModel(
            algorithm_used=schedule_info.get('algorithm', 'unknown'),
            total_jobs=schedule_info.get('total_jobs', 0),
            total_makespan=schedule_info.get('makespan_hours', 0.0),
            average_priority=schedule_info.get('average_priority', 0.0),
            notes=schedule_info.get('notes', '')
        )
        self.session.add(history)
        self.session.commit()
        return history
    
    def get_schedule_history(self, limit: int = 10) -> List[ScheduleHistoryModel]:
        """
        Retrieve recent schedule history.
        
        Args:
            limit: Maximum number of records to retrieve
            
        Returns:
            List of ScheduleHistoryModels
        """
        return self.session.query(ScheduleHistoryModel).order_by(
            ScheduleHistoryModel.created_at.desc()
        ).limit(limit).all()
    
    def close(self):
        """Close database connection."""
        self.session.close()
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
