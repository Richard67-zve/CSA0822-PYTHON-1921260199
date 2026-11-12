import csv
from pathlib import Path
from stats import percentage, absent_three_consecutive

def write_reports(records, output_dir="output"):
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    with open(output / "attendance_percentage.csv", "w",
              newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["register_number", "attendance_percentage"])
        for reg, value in sorted(percentage(records).items()):
            w.writerow([reg, f"{value:.2f}"])
    with open(output / "absent_three_consecutive.csv", "w",
              newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["register_number", "first_absent_date",
                    "third_absent_date"])
        w.writerows(absent_three_consecutive(records))
