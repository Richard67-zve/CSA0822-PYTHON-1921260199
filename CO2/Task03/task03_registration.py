def normalise(text):
    return text.strip().replace(" ", "").replace("-", "").upper()

def is_valid(reg):
    if len(reg) not in (9, 10): return False
    return (reg[0:2].isalpha() and reg[2:4].isdigit()
            and reg[4:-4].isalpha() and len(reg[4:-4]) in (1,2)
            and reg[-4:].isdigit())

def format_registration(reg):
    if not is_valid(reg): raise ValueError("Invalid registration number")
    return f"{reg[:2]} {reg[2:4]} {reg[4:-4]} {reg[-4:]}"

def main():
    samples = ["tn 09 ab 1234", "KA-01-M-0007", "TN9AB1234",
               "TN 22 1234 AB", "mh 12 xyz 9999", "XX-00-A-0001"]
    for raw in samples:
        reg = normalise(raw)
        print(f"{raw:17} -> {reg:11} {'valid' if is_valid(reg) else 'INVALID'}")
        if is_valid(reg): print("  receipt:", format_registration(reg))
    print("\nFor a valid 9-char code, s[-4:] is its final 4 digits and s[4:-4] is one series letter.")
    print("For a valid 10-char code, s[-4:] is its final 4 digits and s[4:-4] is two series letters.")
if __name__ == "__main__": main()
