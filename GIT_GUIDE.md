# Git Setup and Submission Guide

## Initial Git Setup

### 1. Initialize Git Repository

```powershell
cd "c:\Users\CATECH\OneDrive\Bureau\projet PFT"
git init
```

### 2. Configure Git (if not already done)

```powershell
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### 3. Add All Files

```powershell
git add .
```

### 4. Create Initial Commit

```powershell
git commit -m "feat: Initial commit - Fuzzy Scheduling Manufacturing System

- Implement fuzzy logic inference system with triangular and trapezoidal membership functions
- Add Job and Machine domain models with scheduling attributes
- Implement three scheduling algorithms (Fuzzy Priority, FCFS, EDD)
- Add SQLAlchemy database integration for persistence
- Implement data import/export (CSV, JSON)
- Add 51 comprehensive unit tests with 100% pass rate
- Include complete documentation (README, technical report)
- Add example scripts and sample data
"
```

## Recommended Commit History

If you want to show development progression, you can create multiple commits:

### Commit 1: Project Structure

```powershell
git add .gitignore requirements.txt src/__init__.py
git commit -m "feat: Initialize project structure and dependencies"
```

### Commit 2: Fuzzy Logic Core

```powershell
git add src/fuzzy_logic.py tests/test_fuzzy_logic.py
git commit -m "feat: Implement fuzzy logic inference system

- Add triangular and trapezoidal membership functions
- Implement Mamdani inference with centroid defuzzification
- Add fuzzy variables, rules, and inference system
- Include 12 unit tests for fuzzy logic module
"
```

### Commit 3: Domain Models

```powershell
git add src/job.py tests/test_job.py
git commit -m "feat: Add Job and Machine domain models

- Implement Job class with scheduling attributes
- Add urgency calculation and slack time methods
- Implement Machine class with load management
- Include 12 unit tests for job module
"
```

### Commit 4: Scheduling Algorithms

```powershell
git add src/scheduler.py tests/test_scheduler.py
git commit -m "feat: Implement scheduling algorithms

- Add FuzzyScheduler with three algorithms
- Implement fuzzy priority scheduling using FIS
- Add FCFS and EDD baseline algorithms
- Include 11 unit tests and integration tests
"
```

### Commit 5: Database Integration

```powershell
git add src/database.py tests/test_database.py
git commit -m "feat: Add database persistence layer

- Implement SQLAlchemy ORM models
- Add CRUD operations for jobs and machines
- Include schedule history tracking
- Add 12 unit tests for database module
"
```

### Commit 6: Utilities and I/O

```powershell
git add src/utils.py src/main.py
git commit -m "feat: Add utilities and main application

- Implement CSV/JSON import/export
- Add report generation and performance metrics
- Create main entry point with CLI
- Add sample data files
"
```

### Commit 7: Documentation

```powershell
git add README.md docs/ QUICKSTART.md PROJECT_SUMMARY.md
git commit -m "docs: Add comprehensive documentation

- Add detailed README with usage instructions
- Include technical report with algorithm analysis
- Add quick start guide
- Include project summary and metrics
"
```

### Commit 8: Examples

```powershell
git add examples/ data/sample_jobs.csv
git commit -m "feat: Add example scripts and sample data

- Add custom scheduling example
- Include sample jobs CSV file
- Add usage demonstrations
"
```

### Final Commit (if needed)

```powershell
git add .
git commit -m "test: Fix test edge cases and improve coverage

- Fix database test cleanup for Windows
- Adjust fuzzy logic test assertions
- Improve test isolation
- Achieve 100% test pass rate (51/51)
"
```

## Creating GitHub Repository

### Option 1: GitHub CLI

```powershell
gh repo create fuzzy-scheduling-manufacturing --public --source=. --remote=origin
git push -u origin main
```

### Option 2: Manual Setup

1. Go to https://github.com/new
2. Create a new repository named `fuzzy-scheduling-manufacturing`
3. Don't initialize with README (you already have one)
4. Copy the repository URL

```powershell
git remote add origin https://github.com/YOUR_USERNAME/fuzzy-scheduling-manufacturing.git
git branch -M main
git push -u origin main
```

## Commit Message Conventions

This project follows conventional commits:

- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `test:` - Test additions or modifications
- `refactor:` - Code refactoring
- `style:` - Code style changes (formatting)
- `chore:` - Build process or auxiliary tool changes

## Tagging a Release

```powershell
git tag -a v1.0.0 -m "Release v1.0.0: Complete Fuzzy Scheduling System

Features:
- Fuzzy logic inference system
- Multiple scheduling algorithms
- Database integration
- 51 passing unit tests
- Complete documentation
"

git push origin v1.0.0
```

## Checking Your Repository

```powershell
# View commit history
git log --oneline --graph

# View repository status
git status

# View remote URL
git remote -v

# View all files tracked
git ls-files
```

## Submission Checklist

Before submitting:

- [ ] All files committed
- [ ] No uncommitted changes (`git status` is clean)
- [ ] Repository pushed to GitHub
- [ ] README.md displays correctly on GitHub
- [ ] All tests pass locally
- [ ] .gitignore excludes unnecessary files
- [ ] Repository is public or accessible to instructor

## Repository URL Format

Your submission should include:

```
Repository URL: https://github.com/YOUR_USERNAME/fuzzy-scheduling-manufacturing
```

## Verifying Your Submission

Clone your repository in a different location to verify:

```powershell
cd C:\temp
git clone https://github.com/YOUR_USERNAME/fuzzy-scheduling-manufacturing
cd fuzzy-scheduling-manufacturing
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m pytest tests/
python -m src.main
```

If all commands succeed, your submission is ready! ✅

## Alternative: ZIP File Submission

If submitting as ZIP file instead of Git:

```powershell
# Create zip excluding unnecessary files
Compress-Archive -Path src,tests,data,docs,examples,README.md,requirements.txt,QUICKSTART.md,PROJECT_SUMMARY.md,.gitignore -DestinationPath "LastName_FirstName_FTP_Project.zip"
```

---

**Note**: Replace `YOUR_USERNAME` with your actual GitHub username and `LastName_FirstName` with your actual name when submitting.
