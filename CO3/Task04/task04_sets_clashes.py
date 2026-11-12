import random,time

def main():
    ai={"192311001","192311004","192311007","192311009"}
    iot={"192311002","192311004","192311009","192311010"}
    all_students={f"1923110{i:02d}" for i in range(1,11)}
    both=ai & iot; exactly_one=ai ^ iot; neither=all_students-(ai|iot)
    print("clash      :",sorted(both))
    print("exactly one:",sorted(exactly_one))
    print("neither    :",sorted(neither))
    print("method check:",both==ai.intersection(iot), exactly_one==ai.symmetric_difference(iot))
    for n in (10000,100000,1000000):
        values=list(range(n)); target=n-1; value_set=set(values)
        start=time.perf_counter(); target in values; tl=time.perf_counter()-start
        start=time.perf_counter(); target in value_set; ts=time.perf_counter()-start
        print(f"n={n}: list membership={tl:.6f}s set membership={ts:.6f}s")
    print("empty:",set() & ai,"identical:",ai & ai)
if __name__ == "__main__": main()
