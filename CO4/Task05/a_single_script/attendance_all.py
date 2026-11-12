"""Task 5(a): all attendance functions in one Python script."""
import csv
from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path

def read_attendance(path):
    records = []
    with open(path, "r", newline="", encoding="utf-8") as file:
        for line_no, row in enumerate(csv.reader(file), start=1):
            if not row or not any(value.strip() for value in row):
                continue
            if len(row) != 3:
                raise ValueError(f"Line {line_no}: expected 3 fields")
            reg, date_text, status = (value.strip() for value in row)
            date.fromisoformat(date_text)
            if not reg or status not in {"P", "A"}:
                raise ValueError(f"Line {line_no}: invalid attendance record")
            records.append((reg, date_text, status))
    return records

def percentage(records):
    counts = defaultdict(lambda: {"P": 0, "A": 0})
    for reg, _day, status in records:
        counts[reg][status] += 1
    return {
        reg: round(values["P"] * 100 / (values["P"] + values["A"]), 2)
        for reg, values in counts.items()
    }

def absent_three_consecutive(records):
    by_student = defaultdict(dict)
    for reg, day_text, status in records:
        by_student[reg][date.fromisoformat(day_text)] = status
    result = []
    for reg, days in by_student.items():
        dates = sorted(days)
        for index in range(len(dates) - 2):
            window = dates[index:index + 3]
            if (window[1] - window[0] == timedelta(days=1)
                and window[2] - window[1] == timedelta(days=1)
                and all(days[d] == "A" for d in window)):
                result.append((reg, window[0].isoformat(),
                               window[-1].isoformat()))
                break
    return result

def write_reports(records, output_dir="output"):
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    percentages = percentage(records)
    consecutive = absent_three_consecutive(records)
    with open(output / "attendance_percentage.csv", "w",
              newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["register_number", "attendance_percentage"])
        for reg, value in sorted(percentages.items()):
            writer.writerow([reg, f"{value:.2f}"])
    with open(output / "absent_three_consecutive.csv", "w",
              newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["register_number", "first_absent_date",
                         "third_absent_date"])
        writer.writerows(consecutive)

def main():
    records = read_attendance("../sample_data/attendance.csv")
    write_reports(records)
    print("Records processed:", len(records))
    print("Attendance percentages:", percentage(records))
    print("Absent for 3 consecutive days:", absent_three_consecutive(records))
    print("Reports written to output/")

if __name__ == "__main__":
    main()
