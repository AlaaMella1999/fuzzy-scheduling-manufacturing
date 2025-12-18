"""
Main Module
Entry point for the Fuzzy Scheduling Manufacturing System.
"""

import argparse
from datetime import datetime, timedelta
from src.job import Job, Machine
from src.scheduler import FuzzyScheduler
from src.database import Database
from src.utils import (export_jobs_to_csv, export_schedule_to_json, 
                       generate_schedule_report, calculate_performance_metrics)


def create_sample_data():
    """
    Create sample jobs and machines for demonstration.
    
    Returns:
        Tuple of (jobs list, machines dict)
    """
    current_time = datetime.now()
    
    # Create machines
    machines = {
        'M1': Machine('M1', 'CNC Machine 1', capacity=1.0),
        'M2': Machine('M2', 'CNC Machine 2', capacity=1.0),
        'M3': Machine('M3', 'Assembly Line 1', capacity=1.5)
    }
    
    # Create sample jobs
    jobs = [
        Job(
            job_id='J001',
            name='Engine Block Machining',
            processing_time=15.0,
            due_date=current_time + timedelta(hours=48),
            arrival_time=current_time,
            machine_required='M1'
        ),
        Job(
            job_id='J002',
            name='Gear Assembly',
            processing_time=8.0,
            due_date=current_time + timedelta(hours=24),
            arrival_time=current_time + timedelta(hours=2),
            machine_required='M3'
        ),
        Job(
            job_id='J003',
            name='Frame Welding',
            processing_time=20.0,
            due_date=current_time + timedelta(hours=72),
            arrival_time=current_time + timedelta(hours=1),
            machine_required='M2'
        ),
        Job(
            job_id='J004',
            name='Component Finishing',
            processing_time=5.0,
            due_date=current_time + timedelta(hours=16),
            arrival_time=current_time + timedelta(hours=3),
            machine_required='M1'
        ),
        Job(
            job_id='J005',
            name='Quality Inspection',
            processing_time=3.0,
            due_date=current_time + timedelta(hours=12),
            arrival_time=current_time + timedelta(hours=4),
            machine_required='M3'
        ),
        Job(
            job_id='J006',
            name='Precision Cutting',
            processing_time=12.0,
            due_date=current_time + timedelta(hours=36),
            arrival_time=current_time + timedelta(hours=5),
            machine_required='M1'
        ),
        Job(
            job_id='J007',
            name='Surface Treatment',
            processing_time=6.0,
            due_date=current_time + timedelta(hours=20),
            arrival_time=current_time + timedelta(hours=6),
            machine_required='M2'
        ),
        Job(
            job_id='J008',
            name='Final Assembly',
            processing_time=10.0,
            due_date=current_time + timedelta(hours=30),
            arrival_time=current_time + timedelta(hours=7),
            machine_required='M3'
        )
    ]
    
    return jobs, machines


def run_scheduling_demo(algorithm='fuzzy_priority', save_to_db=True, export_files=True):
    """
    Run a complete scheduling demonstration.
    
    Args:
        algorithm: Scheduling algorithm to use
        save_to_db: Whether to save results to database
        export_files: Whether to export results to files
    """
    print("=" * 80)
    print("FUZZY SCHEDULING MANUFACTURING SYSTEM")
    print("=" * 80)
    print()
    
    # Create sample data
    print("Creating sample jobs and machines...")
    jobs, machines = create_sample_data()
    print(f"Created {len(jobs)} jobs and {len(machines)} machines")
    print()
    
    # Initialize scheduler
    scheduler = FuzzyScheduler()
    
    # Add machines
    for machine in machines.values():
        scheduler.add_machine(machine)
    
    # Add jobs
    scheduler.add_jobs(jobs)
    
    # Display jobs before scheduling
    print("JOBS BEFORE SCHEDULING:")
    print("-" * 80)
    for job in jobs:
        urgency = job.calculate_urgency()
        print(f"{job.job_id}: {job.name}")
        print(f"  Processing Time: {job.processing_time}h")
        print(f"  Due Date: {job.due_date.strftime('%Y-%m-%d %H:%M')}")
        print(f"  Machine Required: {job.machine_required}")
        print(f"  Urgency: {urgency:.2f}/10")
        print()
    
    # Run scheduling
    print(f"Running {algorithm.upper()} scheduling algorithm...")
    print()
    scheduled_jobs = scheduler.schedule_jobs(algorithm=algorithm)
    
    # Display schedule summary
    summary = scheduler.get_schedule_summary()
    print("SCHEDULING SUMMARY:")
    print("-" * 80)
    print(f"Total Jobs: {summary['total_jobs']}")
    print(f"Scheduled Jobs: {summary['scheduled_jobs']}")
    print(f"Pending Jobs: {summary['pending_jobs']}")
    print(f"Total Makespan: {summary['makespan_hours']:.2f} hours")
    print(f"Average Priority: {summary['average_priority']:.2f}")
    print()
    print("Machine Utilization:")
    for machine_id, util in summary['machine_utilization'].items():
        print(f"  {machine_id}: {util:.2%}")
    print()
    
    # Display scheduled jobs
    print("SCHEDULED JOBS (Priority Order):")
    print("-" * 80)
    for job in sorted(scheduled_jobs, key=lambda j: j.priority_score, reverse=True):
        print(f"{job.job_id}: {job.name}")
        print(f"  Priority Score: {job.priority_score:.2f}")
        print(f"  Assigned Machine: {job.assigned_machine}")
        if job.start_time:
            print(f"  Start Time: {job.start_time.strftime('%Y-%m-%d %H:%M')}")
            print(f"  Completion Time: {job.completion_time.strftime('%Y-%m-%d %H:%M')}")
        print()
    
    # Calculate performance metrics
    metrics = calculate_performance_metrics(scheduler.jobs)
    print("PERFORMANCE METRICS:")
    print("-" * 80)
    print(f"Average Completion Time: {metrics['average_completion_time']:.2f} hours")
    print(f"Average Waiting Time: {metrics['average_waiting_time']:.2f} hours")
    print(f"On-Time Delivery Rate: {metrics['on_time_delivery_rate']:.1f}%")
    print(f"Total Makespan: {metrics['makespan']:.2f} hours")
    print()
    
    # Save to database
    if save_to_db:
        print("Saving to database...")
        with Database() as db:
            # Save machines
            for machine in machines.values():
                db.add_machine(machine)
            
            # Save jobs
            for job in scheduler.jobs:
                db.add_job(job)
            
            # Save schedule history
            schedule_info = {
                'algorithm': algorithm,
                'total_jobs': summary['total_jobs'],
                'makespan_hours': summary['makespan_hours'],
                'average_priority': summary['average_priority'],
                'notes': f"Demo run with {len(jobs)} jobs"
            }
            db.save_schedule_history(schedule_info)
        print("Data saved to database successfully!")
        print()
    
    # Export files
    if export_files:
        print("Exporting results to files...")
        export_jobs_to_csv(scheduler.jobs, 'data/scheduled_jobs.csv')
        export_schedule_to_json(scheduler.jobs, scheduler.machines, 'data/schedule.json')
        
        # Generate and save report
        report = generate_schedule_report(scheduler.jobs, scheduler.machines)
        with open('data/schedule_report.txt', 'w') as f:
            f.write(report)
        print("Report saved to data/schedule_report.txt")
        print()
    
    print("=" * 80)
    print("Scheduling completed successfully!")
    print("=" * 80)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Fuzzy Scheduling Manufacturing System'
    )
    parser.add_argument(
        '--algorithm',
        choices=['fuzzy_priority', 'fcfs', 'edd'],
        default='fuzzy_priority',
        help='Scheduling algorithm to use (default: fuzzy_priority)'
    )
    parser.add_argument(
        '--no-db',
        action='store_true',
        help='Do not save results to database'
    )
    parser.add_argument(
        '--no-export',
        action='store_true',
        help='Do not export results to files'
    )
    
    args = parser.parse_args()
    
    run_scheduling_demo(
        algorithm=args.algorithm,
        save_to_db=not args.no_db,
        export_files=not args.no_export
    )


if __name__ == '__main__':
    main()
