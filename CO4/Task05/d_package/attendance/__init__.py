"""Attendance processing package."""
from .reader import read_attendance
from .stats import percentage, absent_three_consecutive
from .report import write_reports

__all__ = ["read_attendance", "percentage",
           "absent_three_consecutive", "write_reports"]
