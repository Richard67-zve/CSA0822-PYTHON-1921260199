
from decimal import Decimal, ROUND_HALF_UP

STANDARD_FAT = Decimal("3.5")
STANDARD_SNF = Decimal("8.5")
STEP_SIZE = Decimal("0.1")
SNF_STEP_VALUE = Decimal("0.30")
BONUS_RATE = Decimal("0.50")
BONUS_LIMIT = Decimal("500")


def money(value):
    """Round money to two decimal places."""
    return value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def get_rate_card(month):
    """Return the applicable seasonal rate card."""
    if 4 <= month <= 6:
        return Decimal("32.00"), Decimal("0.45")
    return Decimal("30.00"), Decimal("0.40")


def rate_per_litre(fat, snf, month):
    """Calculate rate using two-decimal analyser readings."""
    fat = Decimal(str(fat))
    snf = Decimal(str(snf))

    base_rate, fat_step_value = get_rate_card(month)

    fat_steps = ((fat - STANDARD_FAT) / STEP_SIZE).quantize(
        Decimal("1"), rounding=ROUND_HALF_UP
    )
    snf_steps = ((snf - STANDARD_SNF) / STEP_SIZE).quantize(
        Decimal("1"), rounding=ROUND_HALF_UP
    )

    rate = (
        base_rate
        + fat_steps * fat_step_value
        + snf_steps * SNF_STEP_VALUE
    )
    return money(rate)


def calculate_ten_day_payment(litres, fat, snf, month):
    """Calculate ten-day payment, including any eligible bonus."""
    litres = Decimal(str(litres))

    rate = rate_per_litre(fat, snf, month)
    milk_payment = money(litres * rate)

    bonus = (
        money(litres * BONUS_RATE)
        if litres > BONUS_LIMIT
        else Decimal("0.00")
    )

    return rate, milk_payment, bonus, money(milk_payment + bonus)


def run_tests():
    """Test both seasons and the bonus threshold."""
    tests = [
        ("March, no bonus", "300", "4.20", "8.70", 3),
        ("May, no bonus", "300", "4.20", "8.70", 5),
        ("May, bonus", "501", "4.20", "8.70", 5),
        ("May, exactly 500", "500", "4.20", "8.70", 5),
    ]

    for name, litres, fat, snf, month in tests:
        rate, milk, bonus, total = calculate_ten_day_payment(
            litres, fat, snf, month
        )
        print(
            f"{name}: rate Rs.{rate:.2f}, "
            f"milk Rs.{milk:.2f}, bonus Rs.{bonus:.2f}, "
            f"total Rs.{total:.2f}"
        )


if __name__ == "__main__":
    run_tests()
