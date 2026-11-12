"""Validation functions for fest registration records."""

def valid_email(email):
    """Basic assignment-level e-mail validation using string methods."""
    email = email.strip()
    if not email or any(ch.isspace() for ch in email):
        return False
    if email.count("@") != 1:
        return False
    local, domain = email.split("@")
    if not local or not domain:
        return False
    if "." not in domain or domain.startswith(".") or domain.endswith("."):
        return False
    return True

def parse_record(line):
    """Parse reg_no,name,department,email,event1;event2."""
    fields = [part.strip() for part in line.rstrip("\\r\\n").split(",")]
    if len(fields) != 5:
        raise ValueError(f"expected 5 fields, found {len(fields)}")

    reg_no, name, department, email, event_text = fields
    if not all((reg_no, name, department, email, event_text)):
        raise ValueError("one or more required fields are empty")
    if not valid_email(email):
        raise ValueError(f"invalid e-mail address {email!r}")

    events = [event.strip() for event in event_text.split(";")
              if event.strip()]
    if not events:
        raise ValueError("no valid events selected")

    return {
        "register_number": reg_no,
        "name": name,
        "department": department,
        "email": email,
        "events": events,
    }
