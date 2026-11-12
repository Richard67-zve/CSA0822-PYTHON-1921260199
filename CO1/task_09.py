
def rate_per_litre(fat, snf):
    fat_steps = round((fat - 3.5) / 0.1)
    snf_steps = round((snf - 8.5) / 0.1)
    rate = 30 + fat_steps * 0.40 + snf_steps * 0.30
    return round(rate, 2)


def payout(litres, fat, snf):
    return round(litres * rate_per_litre(fat, snf), 2)


def main():
    total = 0.0
    payments = []

    try:
        count = int(input("Enter number of farmers: "))

        if count <= 0:
            print("Error: Number of farmers must be positive.")
            return

        for i in range(count):
            print(f"\nFarmer {i + 1}")

            farmer_id = input("Enter Farmer ID: ").strip()
            litres = float(input("Enter litres: "))
            fat = float(input("Enter fat percentage: "))
            snf = float(input("Enter SNF percentage: "))

            if not farmer_id:
                print("Error: Farmer ID cannot be empty.")
                continue
            if litres < 0:
                print("Error: Litres cannot be negative.")
                continue
            if not 2 <= fat <= 7:
                print("Error: Fat must be between 2% and 7%.")
                continue
            if snf < 0:
                print("Error: SNF cannot be negative.")
                continue

            rate = rate_per_litre(fat, snf)
            amount = payout(litres, fat, snf)

            payments.append(amount)
            total += amount

            print(f"Rate per litre: Rs. {rate:.2f}")
            print(f"Payment: Rs. {amount:.2f}")

        print("\nPAYMENT SUMMARY")
        print(f"Valid entries: {len(payments)}")
        print(f"Total payment: Rs. {total:.2f}")

    except ValueError:
        print("Error: Please enter valid numeric values.")


if __name__ == "__main__":
    main()
