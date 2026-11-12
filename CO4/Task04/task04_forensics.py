
from pathlib import Path
from tempfile import TemporaryDirectory
from datetime import datetime

# Original defective program
open_handle = None


def save_returns_wrong(path, books):
    global open_handle

    open_handle = open(path, "w", encoding="utf-8")

    for book in books:
        open_handle.write(book)

    open_handle.close()


def process_wrong(day_file, log_file):
    try:
        books = open(day_file, encoding="utf-8").read().split("\n")
        save_returns_wrong(log_file, books)

    except FileNotFoundError:
        print("missing")


# Corrected program
def save_returns_correct(path, books):
    with open(path, "a", encoding="utf-8") as file:
        for book in books:
            file.write(book + "\n")


def log_error(path, error):
    with open(path, "a", encoding="utf-8") as file:
        file.write(
            f"{datetime.now().isoformat(timespec='seconds')} "
            f"{type(error).__name__}: {error}\n"
        )


def process_correct(day_file, log_file, error_file):
    try:
        with open(day_file, "r", encoding="utf-8") as file:
            books = file.read().splitlines()

        save_returns_correct(log_file, books)

    except (OSError, ValueError, TypeError) as error:
        log_error(error_file, error)


def main():
    with TemporaryDirectory() as temp:
        folder = Path(temp)

        day1 = folder / "day1.txt"
        day2 = folder / "day2.txt"
        day3 = folder / "day3.txt"

        wrong_log = folder / "wrong_returns.log"
        correct_log = folder / "correct_returns.log"
        error_log = folder / "errors.log"

        # Create three daily input files
        day1.write_text("Book A\nBook B", encoding="utf-8")
        day2.write_text("Book C\nBook D", encoding="utf-8")
        day3.write_text("Book E\nBook F", encoding="utf-8")

        print("1. DEMONSTRATING ORIGINAL DEFECTS")

        # Run original process for three days
        for day in (day1, day2, day3):
            process_wrong(day, wrong_log)

        print("\nOriginal log:")
        print(repr(wrong_log.read_text(encoding="utf-8")))

        print("\nOnly the last day's books remain because mode 'w' "
              "overwrites earlier contents.")

        print("Books are joined because write() has no newline.")

        # Demonstrate failed write and unclosed file
        try:
            save_returns_wrong(wrong_log, ["Book G", 123])

        except TypeError as error:
            print("\nWrite failure:", error)
            print("File closed after failure:", open_handle.closed)
            print("No error log was created:", not error_log.exists())

            # Close manually for safe cleanup
            open_handle.close()

        print("\n2. DEMONSTRATING CORRECTED PROGRAM")

        for day in (day1, day2, day3):
            process_correct(day, correct_log, error_log)

        # Demonstrate a missing file
        missing_file = folder / "missing_day.txt"
        process_correct(missing_file, correct_log, error_log)

        print("\nCorrected log:")
        print(correct_log.read_text(encoding="utf-8"))

        print("Error log:")
        print(error_log.read_text(encoding="utf-8"))

        print("All three days preserved:",
              len(correct_log.read_text(encoding="utf-8").splitlines()) == 6)

        print("\n3. FILE HANDLING RULES")
        print("1. Use append mode when adding records to an existing log.")
        print("2. Use with statements to close files automatically.")


if __name__ == "__main__":
    main()
