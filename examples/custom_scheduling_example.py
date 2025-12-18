"""
Custom Scheduling Example
Demonstrates how to use the fuzzy scheduling system with custom data.
"""

from datetime import datetime, timedelta
from src.job import Job, Machine
from src.scheduler import FuzzyScheduler
from src.database import Database
from src.utils import (export_jobs_to_csv, generate_schedule_report, 
                       calculate_performance_metrics)


def main():
    """Run custom scheduling example."""
    
    print("=" * 80)
    print("CUSTOM SCHEDULING EXAMPLE")
    print("=" * 80)
    print()
    
    # Initialize scheduler
    scheduler = FuzzyScheduler()
    current_time = datetime.now()
    
    # Define machines
    print("Setting up machines...")
    machines = [
        Machine("CNC-01", "CNC Milling Machine", capacity=1.0),
        Machine("CNC-02", "CNC Turning Machine", capacity=1.0),
        Machine("ASM-01", "Assembly Station 1", capacity=1.5),
        Machine("ASM-02", "Assembly Station 2", capacity=1.5),
        Machine("QC-01", "Quality Control Station", capacity=2.0)
    ]
    
    for machine in machines:
        scheduler.add_machine(machine)
    
    print(f"Added {len(machines)} machines")
    print()
    
    # Define custom jobs
    print("Creating custom jobs...")
    jobs = [
        # Critical urgent job
        Job(
            job_id="URGENT-001",
            name="Emergency Repair Part",
            processing_time=3.0,
            due_date=current_time + timedelta(hours=6),
            arrival_time=current_time,
            machine_required="CNC-01"
        ),
        
        # Large project jobs
        Job(
            job_id="PROJ-A-001",
            name="Project Alpha - Component 1",
            processing_time=25.0,
            due_date=current_time + timedelta(hours=120),
            arrival_time=current_time,
            machine_required="CNC-01"
        ),
        Job(
            job_id="PROJ-A-002",
            name="Project Alpha - Component 2",
            processing_time=18.0,
            due_date=current_time + timedelta(hours=120),
            arrival_time=current_time + timedelta(hours=2),
            machine_required="CNC-02"
        ),
        Job(
            job_id="PROJ-A-003",
            name="Project Alpha - Assembly",
            processing_time=12.0,
            due_date=current_time + timedelta(hours=132),
            arrival_time=current_time + timedelta(hours=48),
            machine_required="ASM-01"
        ),
        
        # Medium priority jobs
        Job(
            job_id="STD-001",
            name="Standard Order - Bracket",
            processing_time=8.0,
            due_date=current_time + timedelta(hours=48),
            arrival_time=current_time + timedelta(hours=1),
            machine_required="CNC-02"
        ),
        Job(
            job_id="STD-002",
            name="Standard Order - Housing",
            processing_time=15.0,
            due_date=current_time + timedelta(hours=72),
            arrival_time=current_time + timedelta(hours=3),
            machine_required="CNC-01"
        ),
        
        # Quality control jobs
        Job(
            job_id="QC-001",
            name="Batch Inspection - Set A",
            processing_time=4.0,
            due_date=current_time + timedelta(hours=24),
            arrival_time=current_time + timedelta(hours=4),
            machine_required="QC-01"
        ),
        Job(
            job_id="QC-002",
            name="Batch Inspection - Set B",
            processing_time=3.5,
            due_date=current_time + timedelta(hours=30),
            arrival_time=current_time + timedelta(hours=6),
            machine_required="QC-01"
        ),
        
        # Assembly jobs
        Job(
            job_id="ASM-001",
            name="Subassembly - Motor Mount",
            processing_time=6.0,
            due_date=current_time + timedelta(hours=36),
            arrival_time=current_time + timedelta(hours=5),
            machine_required="ASM-01"
        ),
        Job(
            job_id="ASM-002",
            name="Final Assembly - Unit 100",
            processing_time=10.0,
            due_date=current_time + timedelta(hours=60),
            arrival_time=current_time + timedelta(hours=12),
            machine_required="ASM-02"
        ),
        
        # Low priority maintenance jobs
        Job(
            job_id="MAINT-001",
            name="Spare Parts Production",
            processing_time=20.0,
            due_date=current_time + timedelta(hours=168),  # 1 week
            arrival_time=current_time + timedelta(hours=8),
            machine_required="CNC-02"
        ),
    ]
    
    scheduler.add_jobs(jobs)
    print(f"Added {len(jobs)} jobs")
    print()
    
    # Display job details before scheduling
    print("JOB DETAILS BEFORE SCHEDULING:")
    print("-" * 80)
    print(f"{'Job ID':<15} {'Name':<30} {'PT(h)':<8} {'Urgency':<10}")
    print("-" * 80)
    for job in jobs:
        urgency = job.calculate_urgency(current_time)
        print(f"{job.job_id:<15} {job.name:<30} {job.processing_time:<8.1f} {urgency:<10.2f}")
    print()
    
    # Run fuzzy priority scheduling
    print("Running FUZZY PRIORITY scheduling...")
    print()
    scheduled = scheduler.schedule_jobs(algorithm="fuzzy_priority")
    
    # Display results
    print("SCHEDULING RESULTS:")
    print("-" * 80)
    print(f"Successfully scheduled: {len(scheduled)} jobs")
    print()
    
    # Show top priority jobs
    print("TOP 5 PRIORITY JOBS:")
    print("-" * 80)
    sorted_jobs = sorted(scheduled, key=lambda j: j.priority_score, reverse=True)[:5]
    for i, job in enumerate(sorted_jobs, 1):
        print(f"{i}. {job.job_id} - {job.name}")
        print(f"   Priority: {job.priority_score:.2f}")
        print(f"   Machine: {job.assigned_machine}")
        print(f"   Start: {job.start_time.strftime('%Y-%m-%d %H:%M') if job.start_time else 'N/A'}")
        print()
    
    # Performance metrics
    metrics = calculate_performance_metrics(scheduler.jobs)
    print("PERFORMANCE METRICS:")
    print("-" * 80)
    print(f"Total Makespan: {metrics['makespan']:.2f} hours")
    print(f"Average Completion Time: {metrics['average_completion_time']:.2f} hours")
    print(f"Average Waiting Time: {metrics['average_waiting_time']:.2f} hours")
    print(f"On-Time Delivery Rate: {metrics['on_time_delivery_rate']:.1f}%")
    print()
    
    # Machine utilization
    summary = scheduler.get_schedule_summary()
    print("MACHINE UTILIZATION:")
    print("-" * 80)
    for machine_id, util in summary['machine_utilization'].items():
        machine = scheduler.machines[machine_id]
        print(f"{machine.name:<30} {util:>6.1%}  (Load: {machine.get_current_load():.1f}%)")
    print()
    
    # Compare with other algorithms
    print("ALGORITHM COMPARISON:")
    print("-" * 80)
    
    # Reset and try FCFS
    scheduler2 = FuzzyScheduler()
    for machine in machines:
        scheduler2.add_machine(machine)
    scheduler2.add_jobs(jobs)
    scheduler2.schedule_jobs(algorithm="fcfs")
    metrics_fcfs = calculate_performance_metrics(scheduler2.jobs)
    
    # Reset and try EDD
    scheduler3 = FuzzyScheduler()
    for machine in machines:
        scheduler3.add_machine(machine)
    scheduler3.add_jobs(jobs)
    scheduler3.schedule_jobs(algorithm="edd")
    metrics_edd = calculate_performance_metrics(scheduler3.jobs)
    
    print(f"{'Algorithm':<20} {'Makespan':<15} {'On-Time %':<12} {'Avg Wait':<12}")
    print("-" * 80)
    print(f"{'Fuzzy Priority':<20} {metrics['makespan']:<15.2f} {metrics['on_time_delivery_rate']:<12.1f} {metrics['average_waiting_time']:<12.2f}")
    print(f"{'FCFS':<20} {metrics_fcfs['makespan']:<15.2f} {metrics_fcfs['on_time_delivery_rate']:<12.1f} {metrics_fcfs['average_waiting_time']:<12.2f}")
    print(f"{'EDD':<20} {metrics_edd['makespan']:<15.2f} {metrics_edd['on_time_delivery_rate']:<12.1f} {metrics_edd['average_waiting_time']:<12.2f}")
    print()
    
    # Save results
    print("Saving results...")
    
    # Save to database
    with Database("data/custom_schedule.db") as db:
        for machine in scheduler.machines.values():
            db.add_machine(machine)
        for job in scheduler.jobs:
            db.add_job(job)
        db.save_schedule_history({
            'algorithm': 'fuzzy_priority',
            'total_jobs': len(scheduler.jobs),
            'makespan_hours': metrics['makespan'],
            'average_priority': summary['average_priority'],
            'notes': 'Custom example run'
        })
    
    # Export to CSV
    export_jobs_to_csv(scheduler.jobs, 'data/custom_schedule.csv')
    
    # Generate report
    report = generate_schedule_report(scheduler.jobs, scheduler.machines)
    with open('data/custom_schedule_report.txt', 'w') as f:
        f.write(report)
    
    print("Results saved to:")
    print("  - data/custom_schedule.db")
    print("  - data/custom_schedule.csv")
    print("  - data/custom_schedule_report.txt")
    print()
    
    print("=" * 80)
    print("EXAMPLE COMPLETED SUCCESSFULLY!")
    print("=" * 80)


if __name__ == '__main__':
    main()
