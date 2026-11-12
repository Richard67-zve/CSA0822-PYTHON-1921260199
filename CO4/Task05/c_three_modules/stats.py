from collections import defaultdict
from datetime import date, timedelta

def percentage(records):
    counts = defaultdict(lambda: {"P": 0, "A": 0})
    for reg, _day, status in records:
        counts[reg][status] += 1
    return {reg: round(v["P"] * 100 / (v["P"] + v["A"]), 2)
            for reg, v in counts.items()}

def absent_three_consecutive(records):
    by_student = defaultdict(dict)
    for reg, day_text, status in records:
        by_student[reg][date.fromisoformat(day_text)] = status
    result = []
    for reg, days in by_student.items():
        dates = sorted(days)
        for i in range(len(dates) - 2):
            a, b, c = dates[i:i + 3]
            if (b-a == timedelta(days=1) and c-b == timedelta(days=1)
                and days[a] == days[b] == days[c] == "A"):
                result.append((reg, a.isoformat(), c.isoformat()))
                break
    return result
