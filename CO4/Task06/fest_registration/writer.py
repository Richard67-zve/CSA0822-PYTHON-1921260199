"""Write master, event-wise, summary and error reports."""
import csv
from pathlib import Path

def write_master(records, output_dir):
    path = Path(output_dir) / "master.csv"
    with open(path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["register_number", "name", "department",
                         "email", "events"])
        for record in records:
            writer.writerow([
                record["register_number"], record["name"],
                record["department"], record["email"],
                ";".join(record["events"])
            ])
    return path

def write_event_files(event_map, output_dir):
    event_dir = Path(output_dir) / "events"
    event_dir.mkdir(parents=True, exist_ok=True)
    paths = []
    for event, records in sorted(event_map.items()):
        # Keep output names predictable and filesystem-safe.
        safe_name = "".join(ch if ch.isalnum() or ch in "-_" else "_"
                            for ch in event.strip()).strip("_")
        if not safe_name:
            safe_name = "unnamed_event"
        path = event_dir / f"{safe_name}.csv"
        with open(path, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["register_number", "name", "department",
                             "email"])
            for record in records:
                writer.writerow([
                    record["register_number"], record["name"],
                    record["department"], record["email"]
                ])
        paths.append(path)
    return paths

def write_summary(summary, output_dir):
    path = Path(output_dir) / "summary.txt"
    with open(path, "w", encoding="utf-8") as file:
        file.write("COLLEGE FEST REGISTRATION SUMMARY\\n")
        file.write("----------------------------------\\n")
        for key, value in summary.items():
            file.write(f"{key}: {value}\\n")
    return path

def write_error_log(errors, output_dir):
    path = Path(output_dir) / "errors.log"
    with open(path, "w", encoding="utf-8") as file:
        if not errors:
            file.write("No errors.\\n")
        for item in errors:
            file.write(
                f'{item["file"]}, line {item["line"]}, '
                f'{item["category"]}: {item["message"]} | '
                f'RECORD={item["original"]}\\n'
            )
    return path

def write_all(master, event_map, summary, errors, output_dir):
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    write_master(master, output)
    write_event_files(event_map, output)
    write_summary(summary, output)
    write_error_log(errors, output)
