
# Task 3: Variables and Named Constants

# Rate card constants
BASE_RATE = 30.00
STANDARD_FAT = 3.5
STANDARD_SNF = 8.5
FAT_STEP_VALUE = 0.40
SNF_STEP_VALUE = 0.30

# Validation limits
MIN_FAT = 2.0
MAX_FAT = 7.0

# Other constants
TEN_DAY_PERIOD = 10

print("MILK PAYMENT RATE CARD")
print("-" * 35)
print(f"Base rate       : Rs {BASE_RATE:.2f}")
print(f"Standard fat    : {STANDARD_FAT:.1f}%")
print(f"Standard SNF    : {STANDARD_SNF:.1f}%")
print(f"Fat step value  : Rs {FAT_STEP_VALUE:.2f}")
print(f"SNF step value  : Rs {SNF_STEP_VALUE:.2f}")
print(f"Minimum fat     : {MIN_FAT:.1f}%")
print(f"Maximum fat     : {MAX_FAT:.1f}%")
print(f"Payment period  : {TEN_DAY_PERIOD} days")

# Dynamic typing
value = 100
print("\nDynamic typing demonstration:")
print("Value:", value, "| Type:", type(value).__name__)

value = "Milk"
print("Value:", value, "| Type:", type(value).__name__)

# Multiple assignment
a, b = 10, 20
print("\nBefore swapping:", "a =", a, "b =", b)

a, b = b, a
print("After swapping :", "a =", a, "b =", b)

# Dictionary alternative rate card
RATE_CARD = {
    "base": 30.00,
    "fat": 0.40,
    "snf": 0.30
}

print("\nDictionary rate card:", RATE_CARD)
