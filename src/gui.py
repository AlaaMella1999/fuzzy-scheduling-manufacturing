"""
Fuzzy Scheduling Manufacturing System - GUI Application
A graphical user interface for the scheduling system using Tkinter.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import sys
import os

# Add parent directory to path to import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.job import Job, Machine
from src.scheduler import FuzzyScheduler
from src.fuzzy_logic import create_scheduling_fuzzy_system
from src.utils import export_jobs_to_csv, export_schedule_to_json, calculate_performance_metrics


class SchedulingGUI:
    """Main GUI application for the fuzzy scheduling system."""
    
    def __init__(self, root):
        """Initialize the GUI application."""
        self.root = root
        self.root.title("🏭 Fuzzy Manufacturing Scheduler")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')
        
        # Data storage
        self.jobs = []
        self.machines = []
        self.scheduler = None
        self.scheduled_jobs = []
        
        # Setup GUI
        self.setup_gui()
        
        # Load sample data
        self.load_sample_data()
    
    def setup_gui(self):
        """Setup the main GUI layout."""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Title
        title_label = tk.Label(
            main_frame, 
            text="🏭 Fuzzy Manufacturing Scheduler",
            font=("Arial", 20, "bold"),
            bg='#f0f0f0',
            fg='#2c3e50'
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=10)
        
        # Left panel - Controls
        self.setup_control_panel(main_frame)
        
        # Right panel - Results
        self.setup_results_panel(main_frame)
        
        # Bottom panel - Job list
        self.setup_job_list(main_frame)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(5, 0))
    
    def setup_control_panel(self, parent):
        """Setup the control panel with buttons and options."""
        control_frame = ttk.LabelFrame(parent, text="Control Panel", padding="10")
        control_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
        
        # Algorithm selection
        ttk.Label(control_frame, text="Algorithm:", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky=tk.W, pady=5)
        
        self.algorithm_var = tk.StringVar(value="fuzzy")
        algorithms = [
            ("Fuzzy Priority (Recommended)", "fuzzy"),
            ("FCFS (First Come First Served)", "fcfs"),
            ("EDD (Earliest Due Date)", "edd")
        ]
        
        for idx, (text, value) in enumerate(algorithms):
            ttk.Radiobutton(
                control_frame, 
                text=text, 
                variable=self.algorithm_var, 
                value=value
            ).grid(row=idx+1, column=0, sticky=tk.W, padx=20)
        
        # Buttons
        button_frame = ttk.Frame(control_frame)
        button_frame.grid(row=5, column=0, pady=20)
        
        ttk.Button(
            button_frame, 
            text="🚀 Run Scheduling", 
            command=self.run_scheduling,
            width=20
        ).grid(row=0, column=0, pady=5)
        
        ttk.Button(
            button_frame, 
            text="📊 Show Gantt Chart", 
            command=self.show_gantt_chart,
            width=20
        ).grid(row=1, column=0, pady=5)
        
        ttk.Button(
            button_frame, 
            text="💾 Export Results", 
            command=self.export_results,
            width=20
        ).grid(row=2, column=0, pady=5)
        
        ttk.Button(
            button_frame, 
            text="🔄 Reset Data", 
            command=self.load_sample_data,
            width=20
        ).grid(row=3, column=0, pady=5)
        
        # Statistics frame
        stats_frame = ttk.LabelFrame(control_frame, text="Statistics", padding="10")
        stats_frame.grid(row=6, column=0, pady=10, sticky=(tk.W, tk.E))
        
        self.stats_text = tk.Text(stats_frame, height=10, width=35, font=("Courier", 9))
        self.stats_text.grid(row=0, column=0)
        
        scrollbar = ttk.Scrollbar(stats_frame, orient="vertical", command=self.stats_text.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.stats_text.configure(yscrollcommand=scrollbar.set)
    
    def setup_results_panel(self, parent):
        """Setup the results panel with treeview."""
        results_frame = ttk.LabelFrame(parent, text="Scheduling Results", padding="10")
        results_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0))
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)
        
        # Create treeview
        columns = ("Job ID", "Name", "Priority", "Machine", "Start", "End", "Status")
        self.results_tree = ttk.Treeview(results_frame, columns=columns, show="headings", height=15)
        
        # Define column headings
        for col in columns:
            self.results_tree.heading(col, text=col)
            self.results_tree.column(col, width=100)
        
        # Add scrollbars
        vsb = ttk.Scrollbar(results_frame, orient="vertical", command=self.results_tree.yview)
        hsb = ttk.Scrollbar(results_frame, orient="horizontal", command=self.results_tree.xview)
        self.results_tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        # Grid layout
        self.results_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        vsb.grid(row=0, column=1, sticky=(tk.N, tk.S))
        hsb.grid(row=1, column=0, sticky=(tk.W, tk.E))
    
    def setup_job_list(self, parent):
        """Setup the job list panel."""
        job_frame = ttk.LabelFrame(parent, text="Available Jobs", padding="10")
        job_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        job_frame.columnconfigure(0, weight=1)
        job_frame.rowconfigure(0, weight=1)
        
        # Create treeview for jobs
        columns = ("Job ID", "Name", "Processing Time", "Due Date", "Machine", "Urgency")
        self.job_tree = ttk.Treeview(job_frame, columns=columns, show="headings", height=8)
        
        for col in columns:
            self.job_tree.heading(col, text=col)
            self.job_tree.column(col, width=150)
        
        # Add scrollbars
        vsb = ttk.Scrollbar(job_frame, orient="vertical", command=self.job_tree.yview)
        hsb = ttk.Scrollbar(job_frame, orient="horizontal", command=self.job_tree.xview)
        self.job_tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        # Grid layout
        self.job_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        vsb.grid(row=0, column=1, sticky=(tk.N, tk.S))
        hsb.grid(row=1, column=0, sticky=(tk.W, tk.E))
    
    def load_sample_data(self):
        """Load sample jobs and machines."""
        self.status_var.set("Loading sample data...")
        
        # Clear existing data
        self.jobs.clear()
        self.machines.clear()
        self.scheduled_jobs.clear()
        
        # Clear displays
        for item in self.job_tree.get_children():
            self.job_tree.delete(item)
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
        
        # Create machines
        self.machines = [
            Machine("M1", "CNC Machine 1", 1.0),
            Machine("M2", "Welding Station 1", 1.0),
            Machine("M3", "Assembly Line 1", 1.0)
        ]
        
        # Create sample jobs
        now = datetime.now()
        sample_jobs = [
            Job("J001", "Engine Block Machining", 15.0, now + timedelta(hours=48), now, "M1"),
            Job("J002", "Gear Assembly", 8.0, now + timedelta(hours=24), now, "M3"),
            Job("J003", "Frame Welding", 20.0, now + timedelta(hours=72), now, "M2"),
            Job("J004", "Component Finishing", 5.0, now + timedelta(hours=16), now, "M1"),
            Job("J005", "Quality Inspection", 3.0, now + timedelta(hours=12), now, "M3"),
            Job("J006", "Precision Cutting", 12.0, now + timedelta(hours=36), now, "M1"),
            Job("J007", "Surface Treatment", 6.0, now + timedelta(hours=20), now, "M2"),
            Job("J008", "Final Assembly", 10.0, now + timedelta(hours=30), now, "M3"),
        ]
        
        self.jobs = sample_jobs
        
        # Populate job tree
        for job in self.jobs:
            self.job_tree.insert("", "end", values=(
                job.job_id,
                job.name,
                f"{job.processing_time:.1f}h",
                job.due_date.strftime("%Y-%m-%d %H:%M"),
                job.machine_required,
                f"{job.calculate_urgency():.2f}/10"
            ))
        
        # Initialize scheduler
        self.scheduler = FuzzyScheduler()
        
        self.status_var.set(f"Loaded {len(self.jobs)} jobs and {len(self.machines)} machines")
        self.update_statistics()
    
    def run_scheduling(self):
        """Run the scheduling algorithm."""
        if not self.jobs:
            messagebox.showwarning("No Data", "Please load jobs first!")
            return
        
        self.status_var.set(f"Running {self.algorithm_var.get().upper()} scheduling...")
        self.root.update()
        
        try:
            # Run scheduling
            algorithm = self.algorithm_var.get()
            
            # Add jobs and machines to scheduler
            for machine in self.machines:
                self.scheduler.add_machine(machine)
            for job in self.jobs:
                self.scheduler.add_job(job)
            
            # Map algorithm names
            algo_map = {
                "fuzzy": "fuzzy_priority",
                "fcfs": "fcfs",
                "edd": "edd"
            }
            
            self.scheduled_jobs = self.scheduler.schedule_jobs(algorithm=algo_map.get(algorithm, "fuzzy_priority"))
            
            # Clear results tree
            for item in self.results_tree.get_children():
                self.results_tree.delete(item)
            
            # Populate results
            for job in self.scheduled_jobs:
                status = "✅ On Time" if not job.is_overdue() else "⚠️ Late"
                if job.start_time and job.completion_time:
                    self.results_tree.insert("", "end", values=(
                        job.job_id,
                        job.name,
                        f"{job.priority_score:.2f}",
                        job.assigned_machine,
                        job.start_time.strftime("%Y-%m-%d %H:%M"),
                        job.completion_time.strftime("%Y-%m-%d %H:%M"),
                        status
                    ))
            
            self.status_var.set(f"Scheduling completed: {len(self.scheduled_jobs)} jobs scheduled")
            self.update_statistics()
            
            messagebox.showinfo(
                "Success", 
                f"Successfully scheduled {len(self.scheduled_jobs)} jobs!\n\n"
                f"Algorithm: {algorithm.upper()}\n"
                f"Check the results table for details."
            )
            
        except Exception as e:
            messagebox.showerror("Error", f"Scheduling failed: {str(e)}")
            self.status_var.set("Error during scheduling")
    
    def update_statistics(self):
        """Update the statistics display."""
        self.stats_text.delete(1.0, tk.END)
        
        if not self.scheduled_jobs:
            self.stats_text.insert(tk.END, "No scheduling results yet.\n\n")
            self.stats_text.insert(tk.END, f"Available Jobs: {len(self.jobs)}\n")
            self.stats_text.insert(tk.END, f"Available Machines: {len(self.machines)}\n")
            return
        
        # Calculate metrics
        metrics = calculate_performance_metrics(self.scheduled_jobs)
        
        # Display statistics
        stats = f"""
╔═══════════════════════════╗
║   PERFORMANCE METRICS     ║
╚═══════════════════════════╝

Total Jobs: {len(self.scheduled_jobs)}
Algorithm: {self.algorithm_var.get().upper()}

⏱️  Makespan: {metrics['makespan']:.2f}h
📊 Avg Completion: {metrics['average_completion_time']:.2f}h
⏳ Avg Waiting: {metrics['average_waiting_time']:.2f}h
✅ On-Time Rate: {metrics['on_time_delivery_rate']:.1f}%

🏭 MACHINE UTILIZATION:
"""
        
        for machine in self.machines:
            utilization = (machine.total_processing_time / metrics['makespan'] * 100) if metrics['makespan'] > 0 else 0
            stats += f"   {machine.machine_id}: {utilization:.1f}%\n"
        
        self.stats_text.insert(tk.END, stats)
    
    def show_gantt_chart(self):
        """Display a Gantt chart of the scheduled jobs."""
        if not self.scheduled_jobs:
            messagebox.showwarning("No Results", "Please run scheduling first!")
            return
        
        # Create new window for Gantt chart
        gantt_window = tk.Toplevel(self.root)
        gantt_window.title("📊 Gantt Chart - Job Schedule")
        gantt_window.geometry("1000x600")
        
        # Create figure
        fig = Figure(figsize=(10, 6), dpi=100)
        ax = fig.add_subplot(111)
        
        # Organize jobs by machine
        machine_jobs = {}
        for job in self.scheduled_jobs:
            if job.assigned_machine and job.start_time and job.completion_time:
                if job.assigned_machine not in machine_jobs:
                    machine_jobs[job.assigned_machine] = []
                machine_jobs[job.assigned_machine].append(job)
        
        # Sort machines
        machines_sorted = sorted(machine_jobs.keys())
        
        # Find time range
        if self.scheduled_jobs:
            min_time = min(job.start_time for job in self.scheduled_jobs if job.start_time)
            max_time = max(job.completion_time for job in self.scheduled_jobs if job.completion_time)
        else:
            min_time = datetime.now()
            max_time = datetime.now()
        
        # Plot bars
        colors = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6', '#1abc9c', '#e67e22', '#34495e']
        
        for idx, machine_id in enumerate(machines_sorted):
            for job in machine_jobs[machine_id]:
                start = (job.start_time - min_time).total_seconds() / 3600
                duration = job.processing_time
                
                color = colors[hash(job.job_id) % len(colors)]
                ax.barh(idx, duration, left=start, height=0.5, 
                       color=color, edgecolor='black', alpha=0.8)
                
                # Add job label
                ax.text(start + duration/2, idx, job.job_id, 
                       ha='center', va='center', fontsize=8, fontweight='bold')
        
        # Formatting
        ax.set_yticks(range(len(machines_sorted)))
        ax.set_yticklabels(machines_sorted)
        ax.set_xlabel('Time (hours)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Machines', fontsize=12, fontweight='bold')
        ax.set_title('Job Schedule - Gantt Chart', fontsize=14, fontweight='bold', pad=20)
        ax.grid(True, axis='x', alpha=0.3)
        
        fig.tight_layout()
        
        # Embed in Tkinter
        canvas = FigureCanvasTkAgg(fig, master=gantt_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Add close button
        ttk.Button(gantt_window, text="Close", command=gantt_window.destroy).pack(pady=10)
    
    def export_results(self):
        """Export scheduling results to files."""
        if not self.scheduled_jobs:
            messagebox.showwarning("No Results", "Please run scheduling first!")
            return
        
        try:
            # Export to CSV
            csv_path = "data/scheduled_jobs_gui.csv"
            export_jobs_to_csv(self.scheduled_jobs, csv_path)
            
            # Export to JSON
            json_path = "data/schedule_gui.json"
            export_schedule_to_json(self.scheduled_jobs, self.scheduler.machines, json_path)
            
            messagebox.showinfo(
                "Export Successful",
                f"Results exported successfully!\n\n"
                f"CSV: {csv_path}\n"
                f"JSON: {json_path}"
            )
            
            self.status_var.set("Results exported successfully")
            
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export results: {str(e)}")


def main():
    """Main entry point for the GUI application."""
    root = tk.Tk()
    app = SchedulingGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
