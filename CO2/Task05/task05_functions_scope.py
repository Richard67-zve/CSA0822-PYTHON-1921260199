def add_item_buggy(item, order=[]):
    order.append(item)
    return order

def add_item(item, order=None):
    if order is None: order=[]
    order.append(item)
    return order

global_count = 0
def change_global():
    global global_count
    global_count += 1

def make_counter():
    count = 0
    def increment():
        nonlocal count
        count += 1
        return count
    return increment

def bill(amount, gst_rate=0.05, *, discount=0):
    subtotal = amount - discount
    gst = subtotal * gst_rate
    return subtotal + gst, gst

def main():
    print(add_item_buggy("Tea"), add_item_buggy("Vada"))
    print("buggy defaults:", add_item_buggy.__defaults__)
    print(add_item("Tea"), add_item("Vada"))
    print("bill total and GST:", bill(100, discount=10))
    change_global(); print("global_count:", global_count)
    counter=make_counter(); print("nonlocal:", counter(), counter(), counter())
if __name__ == "__main__": main()
