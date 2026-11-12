
BASE_RATE = 30.00
FAT_STEP_VALUE = 0.40
SNF_STEP_VALUE = 0.30


def rate_per_litre(fat, snf):
    """Calculate the milk rate per litre."""
    fat_steps = round((fat - 3.5) / 0.1)
    snf_steps = round((snf - 8.5) / 0.1)

    rate = BASE_RATE + (fat_steps * FAT_STEP_VALUE) + (snf_steps * SNF_STEP_VALUE)
    return round(rate, 2)


def payout(litres, fat, snf):
    """Calculate the payment for the supplied milk."""
    rate = rate_per_litre(fat, snf)
    return round(litres * rate, 2)


def ten_day_total(payments):
    """Calculate the total payment for ten days."""
    return round(sum(payments), 2)


# Main program
litres = float(input("Enter litres: "))
fat = float(input("Enter fat percentage: "))
snf = float(input("Enter SNF percentage: "))

rate = rate_per_litre(fat, snf)
amount = payout(litres, fat, snf)

payments = [amount] * 10
total = ten_day_total(payments)

print(f"Rate per litre : Rs. {rate:.2f}")
print(f"Today's payment: Rs. {amount:.2f}")
print(f"Ten-day total  : Rs. {total:.2f}")
