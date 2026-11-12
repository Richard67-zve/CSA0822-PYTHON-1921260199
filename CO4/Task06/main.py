"""Main program for Task 6 – College Fest Registration Desk."""
from pathlib import Path

from fest_registration.reader import expected_department_files, iter_records
from fest_registration.validation import parse_record
from fest_registration.merge import merge_records
from fest_registration.errors import make_error
from fest_registration.writer import write_all

def main():
    input_dir = Path("input")
    output_dir = Path("output")
    errors = []
    valid_records = []

    files_expected = 5
    files_read = 0
    missing_files = 0
    unreadable_files = 0
    damaged_lines = 0
    invalid_emails = 0

    for file_path in expected_department_files(input_dir, files_expected):
        try:
            for line_number, raw_line in iter_records(file_path):
                if not raw_line.strip():
                    continue
                try:
                    record = parse_record(raw_line)
                    valid_records.append(record)
                except ValueError as exc:
                    message = str(exc)
                    if "e-mail" in message:
                        category = "INVALID_EMAIL"
                        invalid_emails += 1
                    else:
                        category = "DAMAGED_OR_INVALID_RECORD"
                        damaged_lines += 1
                    errors.append(make_error(
                        file_path.name, line_number, category,
                        raw_line.rstrip("\\r\\n"), message
                    ))
            files_read += 1
        except FileNotFoundError as exc:
            missing_files += 1
            errors.append(make_error(
                file_path.name, "-", "MISSING_FILE", "", exc
            ))
        except (PermissionError, UnicodeDecodeError, OSError) as exc:
            unreadable_files += 1
            errors.append(make_error(
                file_path.name, "-", "UNREADABLE_FILE", "", exc
            ))

    master, event_map, duplicates = merge_records(valid_records)

    for record in duplicates:
        errors.append(make_error(
            "multiple_department_files", "-", "DUPLICATE",
            record["register_number"],
            "register number was already accepted; first valid record retained"
        ))

    summary = {
        "Department files expected": files_expected,
        "Files successfully read": files_read,
        "Missing files": missing_files,
        "Unreadable files": unreadable_files,
        "Accepted unique registrations": len(master),
        "Duplicate registrations": len(duplicates),
        "Invalid e-mail rows": invalid_emails,
        "Damaged or otherwise invalid rows": damaged_lines,
        "Event-wise participant files created": len(event_map),
    }

    try:
        write_all(master, event_map, summary, errors, output_dir)
    except (PermissionError, OSError) as exc:
        print("OUTPUT ERROR:", type(exc).__name__, exc)
        print("Input processing completed, but one or more reports could not be written.")
        return 1

    print("College fest processing completed.")
    for key, value in summary.items():
        print(f"{key}: {value}")
    print(f"Reports saved in: {output_dir.resolve()}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
