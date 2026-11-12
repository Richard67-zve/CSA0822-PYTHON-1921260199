"""Duplicate removal and event-wise grouping."""
def merge_records(records):
    # Policy: first valid registration for a register number is retained.
    seen_register_numbers = set()
    master_records = []
    event_participants = {}
    duplicate_records = []

    for record in records:
        reg_no = record["register_number"]
        if reg_no in seen_register_numbers:
            duplicate_records.append(record)
            continue

        seen_register_numbers.add(reg_no)
        master_records.append(record)

        for event in record["events"]:
            event_participants.setdefault(event, []).append(record)

    return master_records, event_participants, duplicate_records
