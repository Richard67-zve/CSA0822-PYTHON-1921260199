
# Task 05: Functions, Scope and Default Arguments

# 1. Demonstrating mutable default argument problem
def add_item_buggy(item, order=[]):
    order.append(item)
    return order


# 2. Correcting the mutable default argument problem
def add_item(item, order=None):
    if order is None:
        order = []
    order.append(item)
    return order


# 3. Demonstrating global variable
global_count = 0

def change_global():
    global global_count
    global_count += 1


# 4. Demonstrating nonlocal variable
def make_counter():
    count = 0

    def increment():
        nonlocal count
        count += 1
        return count

    return increment


# 5. Demonstrating keyword-only arguments
def bill(amount, gst_rate=0.05, *, discount=0):
    subtotal = amount - discount
    gst = subtotal * gst_rate
    return subtotal + gst, gst


# Main program
def main():

    print("----- Mutable Default Argument Bug -----")
    print("Buggy Order 1:", add_item_buggy("Tea"))
    print("Buggy Order 2:", add_item_buggy("Vada"))
    print("Shared Default:", add_item_buggy.__defaults__)

    print("\n----- Corrected Default Argument -----")

    customer1 = add_item("Tea")
    customer2 = add_item("Vada")
    customer3 = add_item("Coffee")

    print("Customer 1:", customer1)
    print("Customer 2:", customer2)
    print("Customer 3:", customer3)

    print("\n----- Keyword-only Argument -----")
    total, gst = bill(100, discount=10)
    print("Bill Total:", total)
    print("GST Amount:", gst)

    print("\n----- Global Variable -----")
    change_global()
    print("Global Count:", global_count)

    print("\n----- Nonlocal Variable -----")
    counter = make_counter()
    print("Counter:", counter())
    print("Counter:", counter())
    print("Counter:", counter())


if __name__ == "__main__":
    main()
