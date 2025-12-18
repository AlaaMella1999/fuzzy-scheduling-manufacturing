"""
Utilities Module
Helper functions for data import/export, visualization, and reporting.
"""

import pandas as pd
import json
from datetime import datetime
from typing import List, Dict
from src.job import Job, Machine


def export_jobs_to_csv(jobs: List[Job], filename: str):
    """
    Export jobs to CSV file.
    
    Args:
        jobs: List of Job objects
        filename: Output CSV filename
    """
    data = []
    for job in jobs:
        data.append({
            'job_id': job.job_id,
            'name': job.name,
            'processing_time': job.processing_time,
            'due_date': job.due_date.isoformat(),
            'arrival_time': job.arrival_time.isoformat(),
            'machine_required': job.machine_required,
            'priority_score': job.priority_score,
            'status': job.status,
            'assigned_machine': job.assigned_machine,
            'start_time': job.start_time.isoformat() if job.start_time else None,
            'completion_time': job.completion_time.isoformat() if job.completion_time else None
        })
    
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"Exported {len(jobs)} jobs to {filename}")


def import_jobs_from_csv(filename: str) -> List[Job]:
    """
    Import jobs from CSV file.
    
    Args:
        filename: Input CSV filename
        
    Returns:
        List of Job objects
    """
    df = pd.read_csv(filename)
    jobs = []
    
    for _, row in df.iterrows():
        job = Job(
            job_id=row['job_id'],
            name=row['name'],
            processing_time=float(row['processing_time']),
            due_date=datetime.fromisoformat(row['due_date']),
            arrival_time=datetime.fromisoformat(row['arrival_time']),
            machine_required=row['machine_required'],
            priority_score=float(row.get('priority_score', 0.0)),
            status=row.get('status', 'pending'),
            assigned_machine=row.get('assigned_machine') if pd.notna(row.get('assigned_machine')) else None,
            start_time=datetime.fromisoformat(row['start_time']) if pd.notna(row.get('start_time')) else None,
            completion_time=datetime.fromisoformat(row['completion_time']) if pd.notna(row.get('completion_time')) else None
        )
        jobs.append(job)
    
    print(f"Imported {len(jobs)} jobs from {filename}")
    return jobs


def export_schedule_to_json(jobs: List[Job], machines: Dict[str, Machine], filename: str):
    """
    Export complete schedule to JSON file.
    
    Args:
        jobs: List of Job objects
        machines: Dictionary of Machine objects
        filename: Output JSON filename
    """
    schedule_data = {
        'export_time': datetime.now().isoformat(),
        'jobs': [],
        'machines': []
    }
    
    for job in jobs:
        schedule_data['jobs'].append({
            'job_id': job.job_id,
            'name': job.name,
            'processing_time': job.processing_time,
            'due_date': job.due_date.isoformat(),
            'arrival_time': job.arrival_time.isoformat(),
            'machine_required': job.machine_required,
            'priority_score': job.priority_score,
            'status': job.status,
            'assigned_machine': job.assigned_machine,
            'start_time': job.start_time.isoformat() if job.start_time else None,
            'completion_time': job.completion_time.isoformat() if job.completion_time else None
        })
    
    for machine_id, machine in machines.items():
        schedule_data['machines'].append({
            'machine_id': machine.machine_id,
            'name': machine.name,
            'capacity': machine.capacity,
            'total_processing_time': machine.total_processing_time,
            'utilization': machine.utilization,
            'current_load': machine.get_current_load(),
            'scheduled_jobs_count': len(machine.scheduled_jobs)
        })
    
    with open(filename, 'w') as f:
        json.dump(schedule_data, f, indent=2)
    
    print(f"Exported schedule to {filename}")


def generate_schedule_report(jobs: List[Job], machines: Dict[str, Machine]) -> str:
    """
    Generate a text report of the current schedule.
    
    Args:
        jobs: List of Job objects
        machines: Dictionary of Machine objects
        
    Returns:
        Formatted schedule report as string
    """
    report = []
    report.append("=" * 80)
    report.append("FUZZY SCHEDULING MANUFACTURING SYSTEM - SCHEDULE REPORT")
    report.append("=" * 80)
    report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("")
    
    # Job summary
    report.append("JOB SUMMARY")
    report.append("-" * 80)
    total_jobs = len(jobs)
    scheduled = len([j for j in jobs if j.status == "scheduled"])
    pending = len([j for j in jobs if j.status == "pending"])
    completed = len([j for j in jobs if j.status == "completed"])
    
    report.append(f"Total Jobs: {total_jobs}")
    report.append(f"  - Scheduled: {scheduled}")
    report.append(f"  - Pending: {pending}")
    report.append(f"  - Completed: {completed}")
    report.append("")
    
    # Machine summary
    report.append("MACHINE SUMMARY")
    report.append("-" * 80)
    report.append(f"Total Machines: {len(machines)}")
    for machine in machines.values():
        report.append(f"  {machine.machine_id} ({machine.name})")
        report.append(f"    - Jobs: {len(machine.scheduled_jobs)}")
        report.append(f"    - Load: {machine.get_current_load():.1f}%")
        report.append(f"    - Utilization: {machine.utilization:.2%}")
    report.append("")
    
    # Scheduled jobs detail
    report.append("SCHEDULED JOBS DETAIL")
    report.append("-" * 80)
    scheduled_jobs = [j for j in jobs if j.status == "scheduled" and j.start_time]
    scheduled_jobs.sort(key=lambda x: x.start_time)
    
    for job in scheduled_jobs:
        report.append(f"Job: {job.job_id} - {job.name}")
        report.append(f"  Machine: {job.assigned_machine}")
        report.append(f"  Priority: {job.priority_score:.2f}")
        report.append(f"  Processing Time: {job.processing_time}h")
        report.append(f"  Start: {job.start_time.strftime('%Y-%m-%d %H:%M')}")
        report.append(f"  Completion: {job.completion_time.strftime('%Y-%m-%d %H:%M')}")
        report.append(f"  Due Date: {job.due_date.strftime('%Y-%m-%d %H:%M')}")
        slack = job.get_slack_time(job.start_time)
        report.append(f"  Slack Time: {slack:.1f}h")
        report.append("")
    
    report.append("=" * 80)
    return "\n".join(report)


def calculate_performance_metrics(jobs: List[Job]) -> Dict:
    """
    Calculate scheduling performance metrics.
    
    Args:
        jobs: List of scheduled Job objects
        
    Returns:
        Dictionary of performance metrics
    """
    scheduled_jobs = [j for j in jobs if j.start_time and j.completion_time]
    
    if not scheduled_jobs:
        return {
            'total_jobs': len(jobs),
            'scheduled_jobs': 0,
            'average_completion_time': 0,
            'average_waiting_time': 0,
            'on_time_delivery_rate': 0,
            'makespan': 0
        }
    
    # Calculate metrics
    completion_times = [(j.completion_time - j.arrival_time).total_seconds() / 3600 
                       for j in scheduled_jobs]
    waiting_times = [(j.start_time - j.arrival_time).total_seconds() / 3600 
                    for j in scheduled_jobs]
    
    on_time = len([j for j in scheduled_jobs if j.completion_time <= j.due_date])
    on_time_rate = (on_time / len(scheduled_jobs)) * 100
    
    earliest_start = min(j.start_time for j in scheduled_jobs)
    latest_completion = max(j.completion_time for j in scheduled_jobs)
    makespan = (latest_completion - earliest_start).total_seconds() / 3600
    
    return {
        'total_jobs': len(jobs),
        'scheduled_jobs': len(scheduled_jobs),
        'average_completion_time': sum(completion_times) / len(completion_times),
        'average_waiting_time': sum(waiting_times) / len(waiting_times),
        'on_time_delivery_rate': on_time_rate,
        'makespan': makespan
    }


def format_duration(hours: float) -> str:
    """
    Format duration in hours to readable string.
    
    Args:
        hours: Duration in hours
        
    Returns:
        Formatted string (e.g., "2h 30m")
    """
    h = int(hours)
    m = int((hours - h) * 60)
    return f"{h}h {m}m"
