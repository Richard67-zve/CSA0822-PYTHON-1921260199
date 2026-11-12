import random, time

def moving_naive(values, window=7):
    return [sum(values[i:i+window])/window for i in range(len(values)-window+1)]

def moving_running(values, window=7):
    if len(values)<window: return []
    total=sum(values[:window]); result=[total/window]
    for i in range(window,len(values)):
        total += values[i]-values[i-window]
        result.append(total/window)
    return result

def main():
    random.seed(1)
    readings=[round(random.uniform(0,30),1) for _ in range(365)]
    weekly=[sum(readings[i:i+7]) for i in range(0,len(readings),7)]
    wet=max(range(len(weekly)),key=weekly.__getitem__); dry=min(range(len(weekly)),key=weekly.__getitem__)
    print("weekly totals:", weekly)
    print("wettest week:", wet+1, weekly[wet], "| driest week:", dry+1, weekly[dry])
    print("7-day average sample:", moving_running(readings)[:5])
    print("dry days (1-based):", [i+1 for i,x in enumerate(readings) if x==0])
    for n in (365,36500,365000):
        data=[random.random()*30 for _ in range(n)]
        times=[]
        for fn in (moving_naive,moving_running):
            start=time.perf_counter(); out=fn(data); times.append(time.perf_counter()-start)
        print(f"n={n}: naive={times[0]:.6f}s running={times[1]:.6f}s outputs={len(out)}")
    print("edge cases:", moving_running([]), moving_running([1,2,3]))
if __name__ == "__main__": main()
