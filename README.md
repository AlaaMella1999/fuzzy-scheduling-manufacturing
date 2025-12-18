# Fuzzy Manufacturing Scheduler

This application helps manufacturing facilities schedule their production jobs efficiently using fuzzy logic. Instead of relying on rigid formulas, it makes decisions more like a human would - considering multiple factors like urgency, processing time, and machine availability to determine which job should run next.

## What This Project Does

In a manufacturing environment, you have multiple jobs waiting to be processed and several machines available. The challenge is figuring out the best order to run these jobs. Should you prioritize the urgent ones? The quick ones? The ones that fit best with available machines? This system uses fuzzy logic to balance all these factors and make smart scheduling decisions.

## Real Implementation

Here's what I actually built:

**Core Scheduling Engine:**

- Custom fuzzy logic system from scratch (not using pre-built fuzzy libraries for the core logic)
- Three different scheduling algorithms: Fuzzy Priority, FCFS (First-Come-First-Served), and EDD (Earliest Due Date)
- Real-time priority calculation based on job urgency, processing time, and machine load

**Two User Interfaces:**

- Command-line interface for quick operations and scripting
- Graphical interface (Tkinter) with interactive charts and real-time visualization

**Data Management:**

- SQLite database to store jobs, machines, and scheduling history
- Import/export functionality for CSV and JSON files
- Automatic generation of scheduling reports

**Testing & Quality:**

- 51 unit tests covering all major functionality
- Tests for fuzzy logic calculations, scheduling algorithms, and database operations

## Why Fuzzy Logic?

When you ask a production manager "which job should we run first?", they don't just look at one number. They'll say things like "this one is pretty urgent" or "that machine is getting heavily loaded." These are fuzzy terms - not precise numbers but ranges of possibility.

Traditional scheduling systems use hard rules: IF urgency > 8 THEN priority = HIGH. But what if urgency is 7.9? Is it really that different from 8.1? Fuzzy logic handles this naturally by allowing gradual transitions between states.

In this project, I implemented a Mamdani-style fuzzy inference system that:

- Takes three inputs: urgency (0-10), processing time (0-100 hours), and machine load (0-100%)
- Applies 13 fuzzy rules that mimic how a scheduler would think
- Outputs a priority score (0-100) for each job
- Uses centroid defuzzification to get a final decision

## How to Run It

### Installation

You'll need Python 3.8 or newer. Here's the setup:

```powershell
# Navigate to the project folder
cd "c:\Users\CATECH\OneDrive\Bureau\projet PFT"

# Activate the virtual environment (already created)
.\.venv\Scripts\Activate.ps1

# Install dependencies (if needed)
pip install -r requirements.txt
```

### Running the Application

**Option 1: Graphical Interface (Recommended for demos)**

```powershell
python -m src.gui
```

This opens a window where you can:

- Select which algorithm to use (Fuzzy, FCFS, or EDD)
- Click "Run Scheduling" to see results instantly
- View a Gantt chart showing job timelines
- Export results to CSV/JSON files

**Option 2: Command Line**

```powershell
# Run with fuzzy logic (default)
python -m src.main --no-db

# Try different algorithms
python -m src.main --algorithm fcfs --no-db
python -m src.main --algorithm edd --no-db
```

The `--no-db` flag skips database saving (useful for quick tests).

## What's Actually Implemented

Here's what this project contains (not just theory - actual working code):

**Core Implementation:**

- Custom fuzzy inference engine (not using pre-built libraries for inference)
- Three scheduling algorithms you can compare side-by-side
- Both CLI and GUI interfaces (your choice)
- Gantt chart visualization using matplotlib
- SQLite database for saving scheduling history
- CSV and JSON export for results

**The Fuzzy System:**

- Input 1: Urgency (how close is the due date?)
- Input 2: Processing Time (how long will the job take?)
- Input 3: Machine Load (how busy is the target machine?)
- Output: Priority Score (0-100, determines scheduling order)
- 13 fuzzy rules (e.g., "IF urgency is high AND processing time is short THEN priority is high")
- Triangular membership functions
- Centroid defuzzification method

**Comparison Algorithms:**

- FCFS (First Come First Served) - schedule in arrival order
- EDD (Earliest Due Date) - schedule by deadline
- Fuzzy Priority - our main contribution using the fuzzy system

**Performance Metrics:**

- Makespan: Total time to complete all jobs
- Machine utilization: Percentage of time machines are working
- Average flow time: Time jobs spend in the system
- On-time delivery rate: Jobs completed before their due date

## Testing & Validation

The project includes 51 unit tests covering all major components. Run them with:

```powershell
pytest
```

Test coverage:

- Fuzzy logic engine: membership functions, rule evaluation, inference
- Scheduling algorithms: all three methods
- Job and machine models
- Database operations
- Utility functions

## More Usage Options

### Command Line Flags

```powershell
# Use different algorithms
python -m src.main --algorithm fcfs
python -m src.main --algorithm edd

# Skip database saving (faster for testing)
python -m src.main --no-db

# Skip file export
python -m src.main --no-export
```

### Using It in Your Own Code

Want to integrate this into another project? Here's a basic example:

```python
from datetime import datetime, timedelta
from src.job import Job, Machine
from src.scheduler import FuzzyScheduler

# Set up the scheduler
scheduler = FuzzyScheduler()

# Define your machines
scheduler.add_machine(Machine("M1", "CNC Machine 1"))
scheduler.add_machine(Machine("M2", "Assembly Line"))

# Create a job
job = Job(
    job_id="J001",
    name="Engine Block Machining",
    processing_time=15.0,  # hours
    due_date=datetime.now() + timedelta(hours=48),
    arrival_time=datetime.now(),
    machine_required="M1"
)
scheduler.add_job(job)

# Run the scheduling
scheduled = scheduler.schedule_jobs(algorithm="fuzzy_priority")

# Check the results
summary = scheduler.get_schedule_summary()
print(f"Scheduled {summary['scheduled_jobs']} jobs")
print(f"Total time needed: {summary['makespan_hours']:.2f} hours")
```

### Loading Jobs from a CSV File

If you have jobs in a spreadsheet, save it as CSV and load them:

```python
from src.utils import import_jobs_from_csv

jobs = import_jobs_from_csv("data/my_jobs.csv")
scheduler.add_jobs(jobs)
```

Your CSV should look like this:

```csv
job_id,name,processing_time,due_date,arrival_time,machine_required
J001,Job 1,10.0,2025-12-15T10:00:00,2025-12-13T08:00:00,M1
J002,Job 2,5.0,2025-12-14T16:00:00,2025-12-13T09:00:00,M2
```

## How the Code is Organized

The project structure is straightforward:

```
projet PFT/
│
├── src/                              # All the main code
│   ├── main.py                       # CLI entry point
│   ├── gui.py                        # GUI entry point (Tkinter)
│   ├── fuzzy_logic.py                # Fuzzy inference engine
│   ├── job.py                        # Job and Machine classes
│   ├── scheduler.py                  # Scheduling algorithms
│   ├── database.py                   # SQLite database handling
│   └── utils.py                      # Helper functions (CSV import/export)
│
├── tests/                            # 51 unit tests
│   ├── test_fuzzy_logic.py
│   ├── test_job.py
│   ├── test_scheduler.py
│   └── test_database.py
│
├── data/                             # Generated output files
│   ├── scheduling.db                 # Database (created on first run)
│   ├── scheduled_jobs.csv            # Exported results
│   ├── schedule.json                 # JSON format results
│   └── schedule_report.txt           # Human-readable report
│
└── requirements.txt                  # Python dependencies
```

## The Three Algorithms Explained

### 1. Fuzzy Priority (The Smart One)

This is the main algorithm. It evaluates each job based on:

- **Processing Time**: How long will it take? (0-100 hours)
- **Urgency**: How close is the deadline? (0-10 scale)
- **Machine Load**: How busy is the target machine? (0-100%)

These inputs go through 13 fuzzy rules. For example:

- "IF urgency is HIGH AND processing time is SHORT → priority is VERY HIGH"
- "IF urgency is LOW AND processing time is LONG → priority is VERY LOW"
- "IF urgency is MEDIUM AND machine load is HEAVY → priority is LOW"

The fuzzy system outputs a priority score (0-100), and jobs are scheduled in priority order.

**Why it works better:** Traditional algorithms look at one factor. This considers multiple factors simultaneously and handles uncertain values gracefully.

### 2. FCFS (First Come First Served)

Simply schedules jobs in the order they arrive. Easy to understand but doesn't consider deadlines or processing times.

### 3. EDD (Earliest Due Date)

Schedules jobs by their due dates - earliest deadline first. Good for meeting deadlines but ignores job lengths and machine availability.

**You can compare all three** using either the GUI (dropdown menu) or CLI (`--algorithm` flag) to see which performs best for your scenario.

## 🧪 Testing

Run all tests:

```powershell
python -m pytest tests/
```

Run with coverage report:

```powershell
python -m pytest tests/ --cov=src --cov-report=html
```

Run specific test file:

```powershell
python -m pytest tests/test_fuzzy_logic.py -v
```

### Test Coverage

- `test_fuzzy_logic.py`: Tests membership functions, fuzzification, inference
- `test_job.py`: Tests Job and Machine classes
- `test_scheduler.py`: Tests scheduling algorithms and integration
- `test_database.py`: Tests database operations and persistence

**Test Coverage**: Over 85% of the code is covered by tests.

## Performance Metrics

The application tracks several useful metrics to evaluate schedule quality:

- **Makespan**: Total time needed to complete all jobs
- **Average Completion Time**: How long jobs spend in the system on average
- **Average Waiting Time**: Time jobs wait before starting
- **On-Time Delivery Rate**: What percentage of jobs finish before their deadline
- **Machine Utilization**: How much of the time machines are actually working

You can see these in the GUI statistics panel, or access them programmatically:

```python
from src.utils import calculate_performance_metrics

metrics = calculate_performance_metrics(scheduler.jobs)
print(f"On-time delivery: {metrics['on_time_delivery_rate']:.1f}%")
```

## Quick Demo for Presentation

If you need to show this to a professor or committee:

**Graphical Demo (Recommended):**

```powershell
.\.venv\Scripts\Activate.ps1
python -m src.gui
```

Then:

1. Click "Run Scheduling" (uses Fuzzy by default)
2. Click "Show Gantt Chart" to see the visual timeline
3. Try different algorithms (FCFS, EDD) and compare results
4. Click "Export Results" to save output files

**Command Line Demo:**

```powershell
python -m src.main --no-db
```

Creates 8 sample jobs, schedules them, prints detailed report.

## Key Files to Review

- `src/fuzzy_logic.py` (400 lines) - Custom fuzzy inference engine
- `src/scheduler.py` (277 lines) - All three scheduling algorithms
- `src/gui.py` (455 lines) - Tkinter interface
- `tests/` folder - 51 unit tests

Verify everything works: `pytest` (should show 51 passed)

## Future Work Ideas

These are NOT currently implemented but could be added:

- Real-time rescheduling when new jobs arrive
- Machine learning to tune fuzzy parameters from historical data
- Web-based interface instead of desktop GUI
- Job dependencies and setup time constraints
- Multi-objective optimization (balance multiple goals)

The current version focuses on core fuzzy scheduling with working interfaces and comparison benchmarks.

## Known Limitations

- The fuzzy system uses 100 discretization points (good balance between accuracy and speed)
- Scheduling assumes continuous operation (no shift breaks or maintenance windows)
- Best tested with up to ~100 jobs (larger datasets work but may be slower)
- Database is SQLite (sufficient for demos, would use PostgreSQL for production)

## About This Project

This was developed for the PhD Fundamentals of Programming course requirement. The goal was to implement a practical fuzzy logic application in manufacturing scheduling, demonstrating both theoretical understanding and practical implementation skills.

The fuzzy inference system is custom-built (not using pre-made fuzzy logic libraries for the core inference) to show mastery of the underlying mathematics.

---

**Happy Scheduling! 🏭✨**
