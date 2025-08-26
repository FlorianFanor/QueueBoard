# Scripts

This directory contains utility scripts for the QueueBoard project.

## Setup

To set up the Python environment and install dependencies:

```bash
./scripts/setup.sh
```

Or manually:

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r scripts/requirements.txt
```

## Available Scripts

### create_issues_from_yaml.py

Creates GitHub issues from a YAML backlog file.

**Usage:**
```bash
# Activate virtual environment first
source venv/bin/activate

# Set required environment variables
export REPO=owner/repo
export PROJECT_OWNER=owner  # Optional: for adding to projects
export PROJECT_NUMBER=123   # Optional: for adding to projects

# Run the script
python scripts/create_issues_from_yaml.py backlog.yml
```

**Required Environment Variables:**
- `REPO`: GitHub repository in format `owner/repo` (e.g., `FlorianFanor/QueueBoard`)

**Optional Environment Variables:**
- `PROJECT_OWNER`: GitHub username for adding issues to projects
- `PROJECT_NUMBER`: Project number for adding issues to projects

**YAML Format:**
```yaml
epics:
  - id: epic-foundation
    title: "EPIC: Foundation & DevOps"
    labels: ["epic", "priority:P1"]
    body: "Description of the epic"

issues:
  - parent: epic-foundation
    title: "Bootstrap monorepo"
    labels: ["type:chore", "priority:P1"]
    body: "Description of the issue"
```

The script will:
1. Create epic issues first
2. Create child issues and link them to epics
3. Update epic bodies with checklists of child issues
4. Add issues to GitHub projects (if PROJECT_OWNER and PROJECT_NUMBER are set)
