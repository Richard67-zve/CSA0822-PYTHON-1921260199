"""Day-4 redesign example: compare naive repeated counting with dictionary memoisation."""
import time, random

def count_naive(values):
    unique=set(values)
    return {x: values.count(x) for x in unique}

def count_dict(values):
    counts={}
    for value in values: counts[value]=counts.get(value,0)+1
    return counts

def main():
    random.seed(7)
    values=[random.randrange(1000) for _ in range(20000)]
    start=time.perf_counter(); a=count_naive(values); t1=time.perf_counter()-start
    start=time.perf_counter(); b=count_dict(values); t2=time.perf_counter()-start
    print("same result:", a==b)
    print(f"original list.count approach: {t1:.6f}s")
    print(f"redesigned dictionary approach: {t2:.6f}s")
    print("Diagnosis: list.count scans the full list once per distinct value (O(n*d)); dictionary counting is O(n) average.")
    print("Trade-off: dictionary uses O(d) extra memory; list.count is simple for tiny inputs.")
if __name__ == "__main__": main()
