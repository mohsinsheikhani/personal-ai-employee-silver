#!/usr/bin/env python3
"""Approval Watcher - monitors /Approved/ folder for approved actions.
Workflow:
1. Scans /Approved/ for .md files
2. Logs each approved action with timestamp
3. Moves processed files to /Done/
4. Repeats every 5 seconds
Also scans /Rejected/ to log rejections (no action taken).
"""
import time
import datetime
import shutil
from pathlib import Path

# Configure paths relative to your vault
VAULT = Path.home() / "Public" / "agents_factory" / "ai_employees" / "bronze_tier" / "ai-vault"
APPROVED_DIR = VAULT / "Approved"
REJECTED_DIR = VAULT / "Rejected"
DONE_DIR = VAULT / "Done"
LOGS_DIR = VAULT / "Logs"

def log_action(filename: str, status: str, details: str = "") -> None:
    """Append a timestamped entry to today's log file."""
    log_file = LOGS_DIR / f"{datetime.date.today()}.log"
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {status}: {filename}"
    if details:
        entry += f" | {details}"
    with open(log_file, "a") as f:
        f.write(entry + "\n")
    print(entry)

def process_approved() -> None:
    """Process all files in /Approved/ directory."""
    for filepath in APPROVED_DIR.glob("*.md"):
        log_action(filepath.name, "APPROVED_AND_EXECUTED")
        # Move to Done
        dest = DONE_DIR / filepath.name
        shutil.move(str(filepath), str(dest))
        print(f"  -> Archived to Done/{filepath.name}")

def process_rejected() -> None:
    """Log all files in /Rejected/ directory (no action taken)."""
    for filepath in REJECTED_DIR.glob("*.md"):
        log_action(filepath.name, "REJECTED_NOT_EXECUTED")
        # Move to Done (with rejection prefix for audit trail)
        dest = DONE_DIR / f"REJECTED_{filepath.name}"
        shutil.move(str(filepath), str(dest))
        print(f"  -> Archived to Done/REJECTED_{filepath.name}")

def main() -> None:
    """Main loop: ensure directories exist, then poll."""
    for d in [APPROVED_DIR, REJECTED_DIR, DONE_DIR, LOGS_DIR]:
        d.mkdir(parents=True, exist_ok=True)
    print(f"[HITL Watcher] Monitoring:")
    print(f"  Approved: {APPROVED_DIR}")
    print(f"  Rejected: {REJECTED_DIR}")
    print(f"  Logs:     {LOGS_DIR}")
    print(f"  Archive:  {DONE_DIR}")
    print(f"  Polling every 5 seconds. Press Ctrl+C to stop.\n")
    while True:
        process_approved()
        process_rejected()
        time.sleep(5)

if __name__ == "__main__":
    main()
