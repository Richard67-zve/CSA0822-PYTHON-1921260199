
import random
import time
import sys

TIMETABLE = {
    "12601": {
        "name": "Chennai Express",
        "stops": [
            ("Chennai", "06:00", "06:10"),
            ("Vijayawada", "12:00", "12:05"),
            ("Hyderabad", "18:00", "18:10")
        ],
        "days": {"Mon", "Wed", "Fri"}
    },
    "12602": {
        "name": "Coastal Express",
        "stops": [
            ("Chennai", "07:00", "07:15"),
            ("Nellore", "10:00", "10:05"),
            ("Vijayawada", "13:00", "13:10")
        ],
        "days": {"Tue", "Thu", "Sat"}
    },
    "12603": {
        "name": "City Link",
        "stops": [
            ("Bengaluru", "05:00", "05:10"),
            ("Chennai", "11:00", "11:10")
        ],
        "days": {"Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"}
    },
    "12604": {
        "name": "Southern Mail",
        "stops": [
            ("Madurai", "04:00", "04:10"),
            ("Trichy", "07:00", "07:05"),
            ("Chennai", "12:00", "12:15")
        ],
        "days": {"Sun", "Tue"}
    },
    "12605": {
        "name": "Hill Route",
        "stops": [
            ("Coimbatore", "06:30", "06:40"),
            ("Salem", "09:00", "09:05"),
            ("Chennai", "14:00", "14:10")
        ],
        "days": {"Wed", "Sat"}
    }
}


# Normal station query
def query(data, station, day):
    found = []

    for number, train in data.items():
        if day in train["days"]:
            for stop, arrival, departure in train["stops"]:
                if stop.lower() == station.lower():
                    found.append(
                        (departure, number, train["name"])
                    )

    return sorted(found, key=lambda x: x[0])


# Create station index
def build_index(data):
    index = {}

    for number, train in data.items():
        for station, arrival, departure in train["stops"]:
            index.setdefault(station.lower(), []).append(
                (number, arrival, departure,
                 train["days"], train["name"])
            )

    return index


# Indexed station query
def indexed_query(index, station, day):
    found = []

    for number, arrival, departure, days, name in index.get(
        station.lower(), []
    ):
        if day in days:
            found.append((departure, number, name))

    return sorted(found, key=lambda x: x[0])


# Estimate additional memory used by the index
def index_memory(index):
    size = sys.getsizeof(index)

    for entries in index.values():
        size += sys.getsizeof(entries)

        for entry in entries:
            size += sys.getsizeof(entry)

    return size


def main():

    print("TRAINS STOPPING AT CHENNAI ON WEDNESDAY:")

    for row in query(TIMETABLE, "Chennai", "Wed"):
        print(row)

    print("\nCOMPLETE TIMETABLE:")

    for number, train in TIMETABLE.items():
        print(
            number,
            train["name"],
            train["days"],
            train["stops"]
        )

    # Access departure time of third station
    print(
        "\nThird stop departure of 12601:",
        TIMETABLE["12601"]["stops"][2][2]
    )

    # Build index
    index = build_index(TIMETABLE)

    print("\nINDEXED CHENNAI:")

    print(indexed_query(index, "Chennai", "Wed"))

    # Edge case tests
    print("\nUNKNOWN STATION:")
    print(query(TIMETABLE, "Atlantis", "Mon"))

    print("\nTRAIN NOT RUNNING ON REQUESTED DAY:")
    print(query(TIMETABLE, "Chennai", "Never"))

    # Verify both query methods give identical results
    print("\nQUERY VERIFICATION:")
    print(
        query(TIMETABLE, "Chennai", "Wed")
        == indexed_query(index, "Chennai", "Wed")
    )

    # Experimental investigation
    print("\nPERFORMANCE INVESTIGATION:")

    for n in (100, 1000, 10000):

        data = {}

        for i in range(n):
            data[str(i)] = {
                "name": f"Train{i}",
                "stops": [
                    (
                        f"Station{j % 100}",
                        "08:00",
                        "08:05"
                    )
                    for j in range(10)
                ],
                "days": {"Mon", "Wed"}
            }

        # Build station index
        start = time.perf_counter()
        idx = build_index(data)
        build_time = time.perf_counter() - start

        # Normal query timing
        start = time.perf_counter()

        for _ in range(20):
            normal_result = query(data, "Station5", "Mon")

        scan_time = time.perf_counter() - start

        # Indexed query timing
        start = time.perf_counter()

        for _ in range(20):
            indexed_result = indexed_query(
                idx, "Station5", "Mon"
            )

        indexed_time = time.perf_counter() - start

        # Verify equivalent results
        print(
            f"\n{n} trains:"
        )
        print(f"Normal query: {scan_time:.6f} seconds")
        print(f"Indexed query: {indexed_time:.6f} seconds")
        print(f"Index creation: {build_time:.6f} seconds")
        print(
            f"Index memory: {index_memory(idx)} bytes"
        )
        print(
            "Results identical:",
            normal_result == indexed_result
        )


if __name__ == "__main__":
    main()
