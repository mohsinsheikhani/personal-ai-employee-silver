#!/usr/bin/env python3
"""Filesystem Watcher - monitors drop folder for new files."""
import time
import datetime
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Configuration
DROP_FOLDER = Path.home() / "Public" / "agents_factory" / "ai_employees" / "bronze_tier" / "employee-inbox"
VAULT_NEEDS_ACTION = Path.home() / "Public" / "agents_factory" / "ai_employees" / "bronze_tier" / "ai-vault" / "Needs_Action"

class InboxHandler(FileSystemEventHandler):
    """Handles file creation events in the drop folder."""
    def on_created(self, event):
        if event.is_directory:
            return
        src = Path(event.src_path)

        # Ignore hidden and temp files
        if src.name.startswith('.') or src.name.startswith('_'):
            return
        if src.suffix in ('.tmp', '.swp', '.bak'):
            return

        now = datetime.datetime.now()
        timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")

        # Create action file with metadata frontmatter
        action_filename = f"FILE_{src.stem}_{timestamp}.md"
        action_file = VAULT_NEEDS_ACTION / action_filename

        try:
            file_size = src.stat().st_size
        except OSError:
            file_size = 0

        action_file.write_text(
            f"---\n"
            f"type: file_received\n"
            f"source: {src}\n"
            f"detected: {now.isoformat()}\n"
            f"status: pending\n"
            f"---\n\n"
            f"# New File Received\n\n"
            f"- **File**: {src.name}\n"
            f"- **Size**: {file_size} bytes\n"
            f"- **Location**: {src}\n"
            f"- **Detected**: {now.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            f"## Action Required\n\n"
            f"Process this file according to vault rules.\n"
        )
        print(f"[WATCHER] Detected: {src.name} -> Created: {action_filename}")

if __name__ == "__main__":
    # Ensure directories exist
    DROP_FOLDER.mkdir(parents=True, exist_ok=True)
    VAULT_NEEDS_ACTION.mkdir(parents=True, exist_ok=True)

    # Set up the observer
    observer = Observer()
    observer.schedule(InboxHandler(), str(DROP_FOLDER), recursive=False)
    observer.start()

    print(f"[WATCHER] Monitoring: {DROP_FOLDER}")
    print(f"[WATCHER] Action files go to: {VAULT_NEEDS_ACTION}")
    print(f"[WATCHER] Press Ctrl+C to stop")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[WATCHER] Stopping...")
        observer.stop()
    observer.join()
    print("[WATCHER] Stopped.")
