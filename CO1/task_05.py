
def read_number(prompt):
    """Read a valid number, allowing decimal values."""
    while True:
        text = input(prompt).strip()

        try:
            return float(text)
        except ValueError:
            print("Invalid input! Enter a valid number (e.g., 8.5).")


farmer_id = input("Enter Farmer ID: ").strip()
litres = read_number("Enter litres: ")
fat = read_number("Enter fat percentage: ")
snf = read_number("Enter SNF percentage: ")
shift = input("Enter shift (Morning/Evening): ").strip()

if not farmer_id:
    print("Error: Farmer ID cannot be empty.")
elif litres < 0:
    print("Error: Litres cannot be negative.")
elif not 2.0 <= fat <= 7.0:
    print("Error: Fat must be between 2.0% and 7.0%.")
else:
    print("\nFARMER ENTRY")
    print("-" * 40)
    print(f"{'Farmer ID':<15}: {farmer_id}")
    print(f"{'Litres':<15}: {litres:8.2f}")
    print(f"{'Fat (%)':<15}: {fat:8.2f}")
    print(f"{'SNF (%)':<15}: {snf:8.2f}")
    print(f"{'Shift':<15}: {shift}")
