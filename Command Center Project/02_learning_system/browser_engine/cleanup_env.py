from pathlib import Path
import shutil
from datetime import datetime

def archive_files(source_dir, archive_root, pattern="*"):
    """
    Move files from source_dir into a dated archive folder under archive_root.
    Returns (moved_count, current_archive_path).
    """
    source = Path(source_dir)
    archive_root = Path(archive_root)
    archive_root.mkdir(parents=True, exist_ok=True)

    # Create a timestamped archive folder
    current_archive = archive_root / datetime.utcnow().strftime("archive_%Y%m%dT%H%M%SZ")
    current_archive.mkdir(parents=True, exist_ok=True)

    # Initialize moved_count before use
    moved_count = 0

    # Iterate and move matching files
    for item in source.glob(pattern):
        # Skip directories if you only want files; remove this check to move dirs too
        if item.is_dir():
            continue
        try:
            target = current_archive / item.name
            shutil.move(str(item), str(target))
            moved_count += 1
        except Exception as exc:
            # Keep process robust: log and continue
            print(f"Failed to move {item}: {exc}")

    print(f"--- Archive complete. {moved_count} items moved to {current_archive.name} ---")
    return moved_count, current_archive
