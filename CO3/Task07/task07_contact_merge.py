
import time


# 1. Normalize phone numbers
def normalise_phone(phone):
    digits = ''.join(ch for ch in str(phone or '') if ch.isdigit())

    # Remove India's +91 country code
    if digits.startswith("91") and len(digits) == 12:
        digits = digits[2:]

    # Accept only 10-digit Indian mobile numbers
    return digits if len(digits) == 10 else ""


# 2. Normalize names
def normalise_name(name):
    return " ".join(
        (name or "").lower().replace(".", "").split()
    )


# 3. Normalize email addresses
def normalise_email(email):
    return str(email or "").strip().lower()


# 4. Merge contacts using dictionaries and sets
def merge_contacts(contacts):

    groups = {}
    owner = {}

    for index, contact in enumerate(contacts):

        name = (contact.get("name") or "").strip()

        raw_phones = contact.get("phones") or []
        raw_emails = contact.get("emails") or []

        if isinstance(raw_phones, str):
            raw_phones = [raw_phones]

        if isinstance(raw_emails, str):
            raw_emails = [raw_emails]

        phones = {
            normalise_phone(p)
            for p in raw_phones
            if normalise_phone(p)
        }

        emails = {
            normalise_email(e)
            for e in raw_emails
            if normalise_email(e)
        }

        # Phone numbers and emails identify matching contacts
        identifiers = (
            {("phone", p) for p in phones}
            | {("email", e) for e in emails}
        )

        existing_groups = {
            owner[key]
            for key in identifiers
            if key in owner
        }

        if not existing_groups:
            group_id = index

            groups[group_id] = {
                "names": set(),
                "display_names": set(),
                "phones": set(),
                "emails": set()
            }

        else:
            # Select one existing group
            group_id = min(existing_groups)

            # Merge every other matching group into it
            for other_id in sorted(existing_groups - {group_id}):

                old = groups.pop(other_id)
                target = groups[group_id]

                for field in target:
                    target[field].update(old[field])

                # Redirect all old identifiers to the surviving group
                for p in old["phones"]:
                    owner[("phone", p)] = group_id

                for e in old["emails"]:
                    owner[("email", e)] = group_id

        target = groups[group_id]

        if name:
            target["names"].add(normalise_name(name))
            target["display_names"].add(name)

        target["phones"].update(phones)
        target["emails"].update(emails)

        # Update the identifier-to-group dictionary
        for p in target["phones"]:
            owner[("phone", p)] = group_id

        for e in target["emails"]:
            owner[("email", e)] = group_id

    # Build final dictionary using normalized phone numbers as keys
    merged = {}

    for group_id, record in groups.items():

        if record["phones"]:
            key = min(record["phones"])

        elif record["emails"]:
            key = "email:" + min(record["emails"])

        else:
            # Contacts without phone or email remain separate
            key = f"contact:{group_id + 1}"

        merged[key] = record

    return merged


# 5. Alternative: compare every pair of contacts
def pairwise_duplicate_pairs(contacts):

    prepared = []

    for contact in contacts:

        phones = {
            normalise_phone(p)
            for p in (contact.get("phones") or [])
            if normalise_phone(p)
        }

        emails = {
            normalise_email(e)
            for e in (contact.get("emails") or [])
            if normalise_email(e)
        }

        prepared.append((phones, emails))

    matches = []

    for i in range(len(prepared)):
        for j in range(i + 1, len(prepared)):

            phones_i, emails_i = prepared[i]
            phones_j, emails_j = prepared[j]

            if phones_i & phones_j or emails_i & emails_j:
                matches.append((i, j))

    return matches


# 6. Generate test contacts for performance measurement
def generate_contacts(n):

    return [
        {
            "name": f"Person {i}",
            "phones": [f"90000{i:05d}"],
            "emails": [f"person{i}@example.com"]
        }
        for i in range(n)
    ]


def main():

    print("========== CONTACT MERGING ==========")

    contacts = [
        {
            "name": "Dr. Ravi",
            "phones": ["+91 98400 12345"],
            "emails": ["RAVI@EXAMPLE.COM"]
        },
        {
            "name": "ravi kumar",
            "phones": ["9840012345", "98400-12345"],
            "emails": ["ravi.work@example.com"]
        },
        {
            "name": "Maya",
            "phones": ["+91 90000 11111"],
            "emails": []
        },
        {
            "name": "Unknown",
            "phones": [],
            "emails": ["unknown@example.com"]
        },
        {
            "name": "Dr Ravi",
            "phones": ["9840012345"],
            "emails": ["RAVI@EXAMPLE.COM"]
        }
    ]

    merged = merge_contacts(contacts)

    print("\nMerged contacts:")

    for key, value in sorted(merged.items()):
        print("\nKey:", key)
        print("Names:", sorted(value["display_names"]))
        print("Normalized names:", sorted(value["names"]))
        print("Phone numbers:", sorted(value["phones"]))
        print("Emails:", sorted(value["emails"]))

    print("\n========== OVERLAPPING NUMBER TEST ==========")

    overlapping = [
        {
            "name": "Person A",
            "phones": ["9000011111", "9000022222"],
            "emails": []
        },
        {
            "name": "Person B",
            "phones": ["9000022222", "9000033333"],
            "emails": []
        }
    ]

    overlap_result = merge_contacts(overlapping)

    print("Number of merged groups:", len(overlap_result))
    print("Merged phone numbers:",
          sorted(next(iter(overlap_result.values()))["phones"]))

    print("\n========== SAME NAME TEST ==========")

    same_name = [
        {"name": "Ravi", "phones": ["9000012345"], "emails": []},
        {"name": "Ravi", "phones": ["9000067890"], "emails": []}
    ]

    print("Same name, different numbers:",
          len(merge_contacts(same_name)), "separate contacts")

    print("\n========== MISSING FIELD TEST ==========")

    missing = [
        {"name": "No Number"},
        {}
    ]

    print("Contacts without phone/email:",
          len(merge_contacts(missing)), "separate records")

    print("\n========== PERFORMANCE TEST ==========")

    efficient_times = {}

    for n in (1000, 100000):

        data = generate_contacts(n)

        start = time.perf_counter()
        result = merge_contacts(data)
        elapsed = time.perf_counter() - start

        efficient_times[n] = elapsed

        print(f"\nContacts: {n}")
        print(f"Dictionary merging: {elapsed:.6f} seconds")
        print("Merged groups:", len(result))

    # Pairwise comparison is practical to demonstrate at 1,000 contacts
    data = generate_contacts(1000)

    start = time.perf_counter()
    pairs = pairwise_duplicate_pairs(data)
    pairwise_time = time.perf_counter() - start

    print("\nPairwise comparison for 1,000 contacts:")
    print(f"Time: {pairwise_time:.6f} seconds")
    print("Matching pairs:", len(pairs))
    print("Pairs checked:", 1000 * 999 // 2)

    # Estimate, do not execute, the 100,000-contact pairwise version
    estimated_time = pairwise_time * (
        (100000 * 99999) / (1000 * 999)
    )

    print("\nEstimated pairwise time for 100,000 contacts:")
    print(f"{estimated_time:.2f} seconds (rough estimate, not measured)")

    print("\n========== DESIGN CONCLUSION ==========")
    print("Dictionary merging uses average O(n) time.")
    print("Pairwise comparison uses O(n^2) time.")
    print("Sets prevent duplicate phone numbers and emails.")
    print("Contacts with the same name but different numbers remain separate.")

    print("\nLimitation:")
    print("Shared phone numbers or emails can incorrectly merge")
    print("different people, such as family members.")


if __name__ == "__main__":
    main()
