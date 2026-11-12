"""Illustrative forensics based ONLY on the visible Task 4 scenario in the supplied document.
The source file ends before Task 4's sub-questions, so verify the complete task sheet with faculty."""
from pathlib import Path
from datetime import datetime

def write_wrong(path, books):
    # 'w' truncates the existing file each time: only the last day's data remains.
    with open(path,"w",encoding="utf-8") as f:
        for book in books: f.write(book+"\n")

def append_correct(path, books):
    with open(path,"a",encoding="utf-8") as f:
        for book in books: f.write(book+"\n")

def log_error(path, exc):
    with open(path,"a",encoding="utf-8") as f:
        f.write(f"{datetime.now().isoformat(timespec='seconds')} ERROR {type(exc).__name__}: {exc}\n")

def main():
    folder=Path(__file__).parent; wrong=folder/"wrong_log.txt"; good=folder/"correct_log.txt"; errors=folder/"error_log.txt"
    for p in (wrong,good,errors):
        if p.exists(): p.unlink()
    write_wrong(wrong,["Book A","Book B"]); write_wrong(wrong,["Book C"])
    append_correct(good,["Book A","Book B"]); append_correct(good,["Book C"])
    try: int("not-a-number")
    except ValueError as exc: log_error(errors,exc)
    print("Using w (bug):",wrong.read_text(encoding="utf-8").splitlines())
    print("Using a (fixed):",good.read_text(encoding="utf-8").splitlines())
    print("Saved error log:",errors.read_text(encoding="utf-8").strip())
if __name__ == "__main__": main()
