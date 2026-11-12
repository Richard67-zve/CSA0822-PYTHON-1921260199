def while_otp(entries, correct="246810", max_attempts=3):
    attempts = 0
    iterator = iter(entries)
    while attempts < max_attempts:
        entry = next(iterator, None)
        if entry is None:
            print("Input sequence ended before all attempts were used")
            break
        if entry == "":
            print("Blank entry: not counted")
            continue
        attempts += 1
        if entry == correct:
            print("OTP verified")
            break
        print("Wrong OTP")
    else:
        print("Account locked for 30 minutes")
        return True
    return False

def for_otp(entries, correct="246810", max_attempts=3):
    attempts_used = 0
    for entry in entries:
        if attempts_used >= max_attempts:
            break
        if entry == "":
            print("Blank entry: not counted")
            continue
        attempts_used += 1
        if entry == correct:
            print("OTP verified")
            break
        print("Wrong OTP")
    else:
        if attempts_used == max_attempts:
            print("Account locked for 30 minutes")
    print("Attempts counted:", attempts_used)

def security_extension(entries, security_answer, correct_answer="blue"):
    limit = 3 + (2 if security_answer.strip().lower() == correct_answer else 0)
    print("Allowed attempts:", limit)
    while_otp(entries, max_attempts=limit)

def main():
    print("WHILE:")
    while_otp(["", "111111", "222222", "333333"])
    print("\nFOR:")
    for_otp(["", "111111", "222222", "333333"])
    print("\nSecurity-question extension:")
    security_extension(["1","2","3","4","246810"], "blue")
    print("\npass demonstration: pass is a deliberate no-op placeholder.")
    if True: pass
if __name__ == "__main__": main()
