from functools import lru_cache
import sys, time

calls_naive=0
def ways_naive(n):
    global calls_naive
    calls_naive += 1
    if n <= 1: return 1
    return ways_naive(n-1) + ways_naive(n-2)

calls_memo=0
@lru_cache(maxsize=None)
def ways_memo(n):
    global calls_memo
    calls_memo += 1
    if n <= 1: return 1
    return ways_memo(n-1) + ways_memo(n-2)

def ways_loop(n):
    if n <= 1: return 1
    a,b=1,1
    for _ in range(2,n+1): a,b=b,a+b
    return b

def main():
    print("ways n=1..6:", [ways_loop(n) for n in range(1,7)])
    for n in (10,20,25,30):
        calls_naive=0; answer=ways_naive(n); naive_count=calls_naive
        ways_memo.cache_clear(); calls_memo=0; memo_answer=ways_memo(n)
        print(f"n={n}: answer={answer}, naive calls={naive_count}, memo calls={calls_memo}, equal={answer==memo_answer}")
    ways_memo.cache_clear()
    try: print("memo n=1000:", ways_memo(1000))
    except RecursionError as exc: print("RecursionError at n=1000:", exc, "| limit:", sys.getrecursionlimit())
    print("loop n=1000 has", len(str(ways_loop(1000))), "digits and no recursion stack.")
if __name__ == "__main__": main()
