import csv
from datetime import date

def read_attendance(path):
    records = []
    with open(path, "r", newline="", encoding="utf-8") as file:
        for line_no, row in enumerate(csv.reader(file), start=1):
            if not row or not any(x.strip() for x in row):
                continue
            if len(row) != 3:
                raise ValueError(f"Line {line_no}: expected 3 fields")
            reg, day, status = (x.strip() for x in row)
            date.fromisoformat(day)
            if not reg or status not in {"P", "A"}:
                raise ValueError(f"Line {line_no}: invalid record")
            records.append((reg, day, status))
    return records
