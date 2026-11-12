
import time

calls = 0

# ORIGINAL: Naive recursive solution
def ways_naive(n):
    global calls
    calls += 1

    if n <= 1:
        return 1

    return ways_naive(n - 1) + ways_naive(n - 2)


# REDESIGNED: Iterative solution using only two variables
def ways_iterative(n):
    if n <= 1:
        return 1, 0

    a, b = 1, 1
    iterations = 0

    for i in range(2, n + 1):
        a, b = b, a + b
        iterations += 1

    return b, iterations


def main():
    global calls

    print("STAIRCASE REDESIGN: ORIGINAL vs REDESIGNED")
    print("-" * 65)

    print(f"{'N':<8}{'Result':<15}{'Naive Calls':<15}"
          f"{'Loop Iterations':<18}")

    for n in (10, 20, 25, 30):

        # Original solution
        calls = 0
        start = time.perf_counter()
        original = ways_naive(n)
        naive_time = time.perf_counter() - start
        naive_calls = calls

        # Redesigned solution
        start = time.perf_counter()
        redesigned, iterations = ways_iterative(n)
        iterative_time = time.perf_counter() - start

        print(f"{n:<8}{original:<15}{naive_calls:<15}"
              f"{iterations:<18}")

        print("Same result:", original == redesigned)
        print(f"Naive time: {naive_time:.6f} seconds")
        print(f"Redesigned time: {iterative_time:.6f} seconds")
        print("-" * 65)

    print("\nDESIGN ANALYSIS")
    print("Original: O(2^n) time and O(n) stack space.")
    print("Redesigned: O(n) time and O(1) space.")
    print("The redesigned solution avoids repeated calculations.")
    print("It stores only the previous two results.")
    print("Trade-off: The iterative version does not directly show")
    print("the recursive relationship of the problem.")


if __name__ == "__main__":
    main()
