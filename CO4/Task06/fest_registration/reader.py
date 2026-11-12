"""Input-file discovery and line-by-line reading."""
from pathlib import Path

def expected_department_files(input_dir, count=5):
    folder = Path(input_dir)
    return [folder / f"department{i}.txt" for i in range(1, count + 1)]

def iter_records(path):
    """Yield (physical_line_number, raw_line) from a UTF-8 text file."""
    with open(path, "r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            yield line_number, line
