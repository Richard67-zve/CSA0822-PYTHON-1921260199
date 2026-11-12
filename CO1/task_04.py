
import math

# Named constants
BASE_RATE = 30.00
STANDARD_FAT = 3.5
STANDARD_SNF = 8.5
FAT_STEP_VALUE = 0.40
SNF_STEP_VALUE = 0.30
STEP_SIZE = 0.1


def calculate_rate(fat, snf):
    """Calculate the rate per litre using rounded fat and SNF steps."""
    fat_steps = round((fat - STANDARD_FAT) / STEP_SIZE)
    snf_steps = round((snf - STANDARD_SNF) / STEP_SIZE)

    rate = (
        BASE_RATE
        + fat_steps * FAT_STEP_VALUE
        + snf_steps * SNF_STEP_VALUE
    )

    return round(rate, 2)


def calculate_payment(litres, fat, snf):
    """Calculate the payment for one milk entry."""
    rate = calculate_rate(fat, snf)
    return round(litres * rate, 2)


# Normal calculation
litres = 8.5
fat = 4.2
snf = 8.7

fat_steps = round((fat - STANDARD_FAT) / STEP_SIZE)
snf_steps = round((snf - STANDARD_SNF) / STEP_SIZE)
rate = calculate_rate(fat, snf)
amount = calculate_payment(litres, fat, snf)

print("NORMAL CALCULATION")
print("Fat steps:", fat_steps)
print("SNF steps:", snf_steps)
print(f"Rate per litre: Rs {rate:.2f}")
print(f"Payment: Rs {amount:.2f}")

# Validate fat and quantity
print("\nVALIDATION")
print("Fat valid:", 2.0 <= fat <= 7.0)
print("Quantity valid:", litres >= 0)
print("Both valid:", litres >= 0 and 2.0 <= fat <= 7.0)

# Unexpected result 1: floating-point arithmetic
print("\nFLOATING-POINT SURPRISES")
print("(4.2 - 3.5) / 0.1 =", (4.2 - 3.5) / 0.1)
print("0.1 + 0.2 =", 0.1 + 0.2)
print("0.1 + 0.2 == 0.3:", 0.1 + 0.2 == 0.3)

# Unexpected result 2: operator precedence
print("\nOPERATOR PRECEDENCE")
print("-2 ** 2 =", -2 ** 2)
print("(-2) ** 2 =", (-2) ** 2)
print("2 ** 3 ** 2 =", 2 ** 3 ** 2)

# Unexpected result 3: round, int and floor
print("\nROUNDING DIFFERENCES")
print("round(2.5) =", round(2.5))
print("round(3.5) =", round(3.5))
print("int(-3.5) =", int(-3.5))
print("floor(-3.5) =", math.floor(-3.5))

# Compare step-counting methods.
# Hold SNF at its standard value of 8.5%.
print("\nALTERNATIVE FAT STEP METHODS")
for fat_value in (4.2, 3.1):
    raw_steps = (fat_value - STANDARD_FAT) / STEP_SIZE

    rounded_steps = round(raw_steps)
    truncated_steps = int(raw_steps)
    floored_steps = math.floor(raw_steps)

    rounded_rate = round(
        BASE_RATE + rounded_steps * FAT_STEP_VALUE, 2
    )
    truncated_rate = round(
        BASE_RATE + truncated_steps * FAT_STEP_VALUE, 2
    )
    floored_rate = round(
        BASE_RATE + floored_steps * FAT_STEP_VALUE, 2
    )

    print(f"\nFat: {fat_value}%")
    print("Raw steps:", raw_steps)
    print("round():", rounded_steps, "Rate:", rounded_rate)
    print("int():", truncated_steps, "Rate:", truncated_rate)
    print("floor():", floored_steps, "Rate:", floored_rate)
