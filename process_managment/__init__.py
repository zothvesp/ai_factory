#!/usr/bin/env python3

import argparse
import ast
import concurrent.futures
import re
import shutil
from pathlib import Path

IMPORT_PATTERN = re.compile(
    r'^\s*(?:import\s+\w+|from\s+\S+\s+import\s+.+)',
    re.MULTILINE
)


def read_file(path: Path):
    for encoding in ("utf-8", "latin1"):
        try:
            return path.read_text(encoding=encoding), encoding
        except UnicodeDecodeError:
            pass
    raise UnicodeDecodeError("Unable to decode file")


def process_file(file_path: Path, root: Path, backup_dir: Path | None, dry_run: bool):

    try:
        text, encoding = read_file(file_path)
    except Exception as e:
        return ("FAILED", file_path, str(e), 0)

    match = IMPORT_PATTERN.search(text)

    if not match:
        return ("SKIPPED", file_path, "No imports found", 0)

    cleaned = text[match.start():]

    if cleaned == text:
        return ("UNCHANGED", file_path, "", 0)

    try:
        ast.parse(cleaned)
    except SyntaxError as e:
        return ("FAILED", file_path, f"Invalid after cleanup: {e}", 0)

    removed_lines = text[:match.start()].count("\n")

    if not dry_run:

        if backup_dir:
            backup_file = backup_dir / file_path.relative_to(root)
            backup_file.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(file_path, backup_file)

        file_path.write_text(cleaned, encoding=encoding)

    return ("MODIFIED", file_path, "", removed_lines)


def main():

    parser = argparse.ArgumentParser(
        description="Remove all text before first Python import."
    )

    parser.add_argument(
        "root",
        help="Root directory to scan"
    )

    parser.add_argument(
        "--log",
        default="cleanup_log.txt",
        help="Log filename"
    )

    parser.add_argument(
        "--backup-dir",
        help="Directory where backups will be stored"
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without modifying files"
    )

    parser.add_argument(
        "--workers",
        type=int,
        default=8,
        help="Number of worker threads"
    )

    args = parser.parse_args()

    root = Path(args.root).resolve()

    backup_dir = (
        Path(args.backup_dir).resolve()
        if args.backup_dir
        else None
    )

    log_file = Path(args.log).resolve()

    python_files = list(root.rglob("*.py"))

    modified = []
    skipped = []
    unchanged = []
    failed = []

    with concurrent.futures.ThreadPoolExecutor(
        max_workers=args.workers
    ) as executor:

        futures = [
            executor.submit(
                process_file,
                file,
                root,
                backup_dir,
                args.dry_run
            )
            for file in python_files
        ]

        for future in concurrent.futures.as_completed(futures):

            status, path, info, removed = future.result()

            if status == "MODIFIED":
                modified.append((path, removed))

            elif status == "SKIPPED":
                skipped.append((path, info))

            elif status == "UNCHANGED":
                unchanged.append(path)

            else:
                failed.append((path, info))

    with log_file.open("w", encoding="utf-8") as log:

        log.write("=" * 80 + "\n")
        log.write("Python Cleanup Report\n")
        log.write("=" * 80 + "\n\n")

        log.write(f"Root: {root}\n")
        log.write(f"Dry Run: {args.dry_run}\n\n")

        log.write(f"Modified ({len(modified)})\n")
        log.write("-" * 80 + "\n")

        for path, removed in sorted(modified):
            log.write(f"{path} | Removed {removed} lines\n")

        log.write("\n")

        log.write(f"Skipped ({len(skipped)})\n")
        log.write("-" * 80 + "\n")

        for path, reason in sorted(skipped):
            log.write(f"{path} | {reason}\n")

        log.write("\n")

        log.write(f"Unchanged ({len(unchanged)})\n")
        log.write("-" * 80 + "\n")

        for path in sorted(unchanged):
            log.write(f"{path}\n")

        log.write("\n")

        log.write(f"Failed ({len(failed)})\n")
        log.write("-" * 80 + "\n")

        for path, reason in sorted(failed):
            log.write(f"{path} | {reason}\n")

        log.write("\n")

        log.write("=" * 80 + "\n")
        log.write("Summary\n")
        log.write("=" * 80 + "\n")

        log.write(f"Total Files : {len(python_files)}\n")
        log.write(f"Modified    : {len(modified)}\n")
        log.write(f"Skipped     : {len(skipped)}\n")
        log.write(f"Unchanged   : {len(unchanged)}\n")
        log.write(f"Failed      : {len(failed)}\n")

    print("\nCleanup Complete")
    print(f"Scanned    : {len(python_files)}")
    print(f"Modified   : {len(modified)}")
    print(f"Skipped    : {len(skipped)}")
    print(f"Unchanged  : {len(unchanged)}")
    print(f"Failed     : {len(failed)}")
    print(f"Log File   : {log_file}")


if __name__ == "__main__":
    main()