"""Error-record helpers."""
def make_error(file_name, line_number, category, original, message):
    return {
        "file": str(file_name),
        "line": str(line_number),
        "category": category,
        "original": original,
        "message": str(message),
    }
