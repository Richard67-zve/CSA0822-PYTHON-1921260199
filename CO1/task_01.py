
# Task 1: Understanding and storing farmer data

# Named constants from the assignment
BASE_RATE = 30.00
STANDARD_FAT = 3.5
STANDARD_SNF = 8.5
FAT_STEP_VALUE = 0.40
SNF_STEP_VALUE = 0.30

# Each tuple stores one farmer's entry:
# (farmer_id, litres, fat, snf, shift)

farmer_entries = [
    ("F001", 10.0, 3.5, 8.5, "Morning"),
    ("F002", 8.5, 4.2, 8.7, "Evening"),
    ("F003", 12.0, 3.1, 8.3, "Morning")
]

print("MILK CO-OPERATIVE: FARMER ENTRIES")
print("-" * 55)

for entry in farmer_entries:
    farmer_id, litres, fat, snf, shift = entry

    print(
        f"ID: {farmer_id} | Litres: {litres} | "
        f"Fat: {fat}% | SNF: {snf}% | Shift: {shift}"
    )

print("-" * 55)
print("Number of entries:", len(farmer_entries))

# Demonstrate the data types of one entry
sample = farmer_entries[0]

print("\nData types in the first entry:")
print("Farmer ID:", type(sample[0]).__name__)
print("Litres:", type(sample[1]).__name__)
print("Fat:", type(sample[2]).__name__)
print("SNF:", type(sample[3]).__name__)
print("Shift:", type(sample[4]).__name__)
