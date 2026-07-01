import shutil
from pathlib import Path
from datetime import datetime
from path_config import LEARNING_SYS_DIR, LESSONS_DIR, TRACKER_PATH

# Architecture definitions
base_dir = LEARNING_SYS_DIR
lessons_dir = LESSONS_DIR
archive_dir = LEARNING_SYS_DIR / "archive"
tracker_file = TRACKER_PATH

def archive_environment():
    # 1. Create Archive folder if it doesn't exist
    archive_dir.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    current_archive = archive_dir / f"session_{timestamp}"
    current_archive.mkdir(exist_ok=True)

    # 2. Move files to Archive instead of deleting
    moved_count = 0
    for file in lessons_dir.glob("*"):
        if file.is_file():
            shutil.move(str(file), str(current_archive / file.name))
            moved_count += 1
            print(f"Archived: {file.name}")
    
    # 3. Archive the Tracker and start a fresh one
    if tracker_file.exists():
        shutil.move(str(tracker_file), str(current_archive / "LEARNING_TRACKER.md"))
        with open(tracker_file, "w", encoding="utf-8") as f:
            f.write("# Learning Tracker\n\n## Status: Environment Reset - Production Ready")
        print("Archived: LEARNING_TRACKER.md and created fresh tracker.")

if __name__ == "__main__":
    archive_environment()
    print(f"--- Archive complete. {moved_count} items moved to {current_archive.name} ---")