
def separate_ifs(units, ration, elderly):
    decisions = []

    if units <= 100:
        decisions.append("Full subsidy")

    if 101 <= units <= 200 and ration:
        decisions.append("Partial subsidy")

    if units > 200 and elderly:
        decisions.append("Elderly exception subsidy")

    if not decisions:
        decisions.append("No subsidy")

    return decisions


def chained(units, ration, elderly):
    if units <= 100:
        return "Full subsidy"
    elif 101 <= units <= 200:
        if ration:
            return "Partial subsidy"
        else:
            return "No subsidy"
    elif units > 200 and elderly:
        return "Elderly exception subsidy"
    else:
        return "No subsidy"


def lookup_version(units, ration, elderly):
    slabs = [
        (100, "Full subsidy"),
        (200, "Partial subsidy"),
        (float("inf"), "No subsidy")
    ]

    for limit, decision in slabs:
        if units <= limit:
            if decision == "Partial subsidy" and not ration:
                return "No subsidy"

            if decision == "No subsidy" and elderly:
                return "Elderly exception subsidy"

            return decision


def main():
    households = [
        (100, False, False),
        (101, True, False),
        (101, False, False),
        (200, True, False),
        (201, False, True),
        (201, True, False),
        (80, True, True),
        (200, False, True)
    ]

    print("UNITS | RATION | ELDERLY | SEPARATE IF | IF-ELIF")
    print("-" * 75)

    for u, r, e in households:
        print(
            f"{u:5} | {str(r):6} | {str(e):7} | "
            f"{separate_ifs(u, r, e)} | {chained(u, r, e)}"
        )

    print("\nLOOKUP LIST IMPLEMENTATION")
    for u, r, e in households:
        print(u, r, e, ":", lookup_version(u, r, e))

    print("\nCOMPLEXITY ANALYSIS")
    print("Separate if: O(1) for this fixed set of conditions.")
    print("If-elif: O(1) for this fixed set of conditions.")
    print("Lookup list: O(k) worst-case for k subsidy slabs.")
    print("Lookup list space: O(k) for storing the slabs.")

    print("\nCONCLUSION")
    print("Separate if statements can execute multiple matching blocks.")
    print("If-elif-else executes only the first matching branch.")
    print("Nested conditions are useful when a second condition")
    print("needs to be checked only after the first condition is true.")


if __name__ == "__main__":
    main()
