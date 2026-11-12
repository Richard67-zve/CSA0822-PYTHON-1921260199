
from decimal import Decimal, ROUND_HALF_UP

# Rate card constants
BASE_RATE = Decimal("30.00")
FAT_STEP_VALUE = Decimal("0.40")
SNF_STEP_VALUE = Decimal("0.30")
STANDARD_FAT = Decimal("3.5")
STANDARD_SNF = Decimal("8.5")
STEP_SIZE = Decimal("0.1")


def money(value):
    """Round a monetary value to two decimal places."""
    return value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def rate_per_litre(fat, snf):
    """Calculate the rate per litre."""
    fat = Decimal(str(fat))
    snf = Decimal(str(snf))

    fat_steps = ((fat - STANDARD_FAT) / STEP_SIZE).quantize(
        Decimal("1"), rounding=ROUND_HALF_UP
    )
    snf_steps = ((snf - STANDARD_SNF) / STEP_SIZE).quantize(
        Decimal("1"), rounding=ROUND_HALF_UP
    )

    rate = BASE_RATE + fat_steps * FAT_STEP_VALUE + snf_steps * SNF_STEP_VALUE
    return money(rate)


def payout(litres, fat, snf):
    """Calculate the payment for milk supplied."""
    litres = Decimal(str(litres))
    return money(litres * rate_per_litre(fat, snf))


# Sample calculation
litres = input("Enter litres: ")
fat = input("Enter fat percentage: ")
snf = input("Enter SNF percentage: ")

try:
    if Decimal(litres) < 0:
        raise ValueError("Litres cannot be negative.")

    if not Decimal("2.0") <= Decimal(fat) <= Decimal("7.0"):
        raise ValueError("Fat must be between 2.0% and 7.0%.")

    if Decimal(snf) < 0:
        raise ValueError("SNF cannot be negative.")

    rate = rate_per_litre(fat, snf)
    amount = payout(litres, fat, snf)

    print(f"Rate per litre: Rs. {rate:.2f}")
    print(f"Payment: Rs. {amount:.2f}")

except Exception as error:
    print("Invalid entry:", error)
