from attendance_utils import read_attendance, percentage, \
    absent_three_consecutive, write_reports

def main():
    records = read_attendance("../sample_data/attendance.csv")
    write_reports(records)
    print("Records processed:", len(records))
    print("Attendance percentages:", percentage(records))
    print("Three-day consecutive absences:",
          absent_three_consecutive(records))

if __name__ == "__main__":
    main()
