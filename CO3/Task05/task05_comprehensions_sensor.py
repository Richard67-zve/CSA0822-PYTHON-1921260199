
import random
import time
import sys


# 1. Using a for loop with append()
def loop_clean(readings):
    c = []
    f = []

    for x in readings:
        if -50 <= x <= 50:
            c.append(x)
            f.append(x * 9 / 5 + 32)

    # Use original reading positions (minute numbers start from 1)
    alarms = [
        minute
        for minute, x in enumerate(readings, start=1)
        if -50 <= x <= 50 and not 2 <= x <= 8
    ]

    return c, f, alarms


# 2. Using list comprehensions
def comp_clean(readings):
    c = [x for x in readings if -50 <= x <= 50]
    f = [x * 9 / 5 + 32 for x in c]

    # Preserve original minute numbers
    alarms = [
        minute
        for minute, x in enumerate(readings, start=1)
        if -50 <= x <= 50 and not 2 <= x <= 8
    ]

    return c, f, alarms


# 3. Using map() and filter()
def map_filter_clean(readings):
    c = list(filter(lambda x: -50 <= x <= 50, readings))
    f = list(map(lambda x: x * 9 / 5 + 32, c))

    # Preserve original minute numbers
    alarms = [
        minute
        for minute, x in enumerate(readings, start=1)
        if -50 <= x <= 50 and not 2 <= x <= 8
    ]

    return c, f, alarms


def main():

    print("----- SENSOR READING CLEANING -----")

    readings = [-60, 2, 5, 9, 51, 7, 0, 55]

    a = loop_clean(readings)
    b = comp_clean(readings)
    c = map_filter_clean(readings)

    print("Original readings:", readings)
    print("For loop:", a)
    print("List comprehension:", b)
    print("Map/filter:", c)

    print("All results equal:", a == b == c)

    print("\n----- PERFORMANCE INVESTIGATION -----")

    rng = random.Random(42)

    for n in (10000, 100000, 1000000):

        data = [rng.uniform(-60, 60) for _ in range(n)]

        # Time the loop version
        start = time.perf_counter()
        baseline = loop_clean(data)
        t1 = time.perf_counter() - start

        # Time the comprehension version
        start = time.perf_counter()
        result2 = comp_clean(data)
        t2 = time.perf_counter() - start

        # Time the map/filter version
        start = time.perf_counter()
        result3 = map_filter_clean(data)
        t3 = time.perf_counter() - start

        print(f"\nReadings: {n}")
        print(f"For loop: {t1:.5f} seconds")
        print(f"List comprehension: {t2:.5f} seconds")
        print(f"Map/filter: {t3:.5f} seconds")
        print("All versions produce identical results:",
              baseline == result2 == result3)

    print("\n----- MEMORY COMPARISON -----")

    sample = [2, 5, 9, 7, 0]

    valid_list = [x for x in sample if -50 <= x <= 50]
    valid_generator = (
        x for x in sample if -50 <= x <= 50
    )

    print("List size:", sys.getsizeof(valid_list), "bytes")
    print("Generator size:", sys.getsizeof(valid_generator), "bytes")

    print("\n----- EDGE CASE TESTING -----")

    all_valid = comp_clean([3, 4, 5, 6, 7])
    all_invalid = comp_clean([100, -100, 200, -200, 150])

    print("All-valid readings:", all_valid)
    print("All-invalid readings:", all_invalid)


if __name__ == "__main__":
    main()
