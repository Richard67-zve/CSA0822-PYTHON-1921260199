import random, time
from collections import Counter

STOP={"not","high","the","a","is","and"}
def frequencies(texts, stop):
    counts={}
    for text in texts:
        for word in ''.join(ch.lower() if ch.isalnum() else ' ' for ch in text).split():
            if word not in stop: counts[word]=counts.get(word,0)+1
    return counts

def top(counts,k):
    return sorted(counts.items(),key=lambda item:(-item[1],item[0]))[:k]

def main():
    calls=["seeds not received seeds delayed","fertiliser price high","seeds price high subsidy not received"]
    print("top words:",top(frequencies(calls,{"not","high"}),3))
    for n in (1000,10000,100000):
        data=[f"seeds price district{i%50} subsidy" for i in range(n)]
        start=time.perf_counter(); f=frequencies(data,STOP); t1=time.perf_counter()-start
        start=time.perf_counter(); c=Counter(w for line in data for w in line.lower().split() if w not in STOP); t2=time.perf_counter()-start
        start=time.perf_counter(); words=[w for line in data for w in line.lower().split() if w not in STOP]; d={w:words.count(w) for w in set(words)}; t3=time.perf_counter()-start
        print(f"n={n}: dict={t1:.5f}s Counter={t2:.5f}s list.count={t3:.5f}s")
    grouped={}
    records=[("North","seeds delayed"),("South","fertiliser issue"),("North","subsidy pending")]
    for district,complaint in records: grouped.setdefault(district,[]).append(complaint)
    print("by district:",grouped)
if __name__ == "__main__": main()
