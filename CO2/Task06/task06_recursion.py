
from functools import lru_cache
import sys

calls = 0

def ways_naive(n):
    """Ways to climb n temple steps taking 1 or 2 steps at a time."""
    global calls
    calls += 1

    if n <= 1:
        return 1

    return ways_naive(n - 1) + ways_naive(n - 2)


@lru_cache(maxsize=None)
def ways_memo(n):
    global calls
    calls += 1

    if n <= 1:
        return 1

    return ways_memo(n - 1) + ways_memo(n - 2)


# Naive recursion
calls = 0
print("naive:", ways_naive(25), "calls =", calls)

# Memoised recursion
calls = 0
ways_memo.cache_clear()
print("memo :", ways_memo(25), "calls =", calls)

# Check answers for n = 1 to 6
print("\nWays for n = 1 to 6:")
for n in range(1, 7):
    print(n, ":", ways_memo(n))

# Recursion limit investigation
print("\nRecursion limit:", sys.getrecursionlimit())

try:
    print("ways(1000):", ways_memo(1000))
except RecursionError:
    print("RecursionError: Maximum recursion depth exceeded")

# Iterative solution - O(n) time and O(1) space
def ways_iterative(n):
    if n <= 1:
        return 1

    a, b = 1, 1

    for i in range(2, n + 1):
        a, b = b, a + b

    return b

print("\nIterative result for 1000:", ways_iterative(1000))
