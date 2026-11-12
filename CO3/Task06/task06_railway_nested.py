import random,time

TIMETABLE={
 "12601":{"name":"Chennai Express","stops":[("Chennai","06:00","06:10"),("Vijayawada","12:00","12:05"),("Hyderabad","18:00","18:10")],"days":{"Mon","Wed","Fri"}},
 "12602":{"name":"Coastal Express","stops":[("Chennai","07:00","07:15"),("Nellore","10:00","10:05"),("Vijayawada","13:00","13:10")],"days":{"Tue","Thu","Sat"}},
 "12603":{"name":"City Link","stops":[("Bengaluru","05:00","05:10"),("Chennai","11:00","11:10")],"days":{"Mon","Tue","Wed","Thu","Fri","Sat","Sun"}},
 "12604":{"name":"Southern Mail","stops":[("Madurai","04:00","04:10"),("Trichy","07:00","07:05"),("Chennai","12:00","12:15")],"days":{"Sun","Tue"}},
 "12605":{"name":"Hill Route","stops":[("Coimbatore","06:30","06:40"),("Salem","09:00","09:05"),("Chennai","14:00","14:10")],"days":{"Wed","Sat"}}
}
def query(data,station,day):
    found=[]
    for number,train in data.items():
        if day in train["days"]:
            for stop in train["stops"]:
                if stop[0].lower()==station.lower(): found.append((stop[2],number,train["name"]))
    return sorted(found,key=lambda x:x[0])

def main():
    print("Trains stopping at Chennai on Wednesday:")
    for row in query(TIMETABLE,"Chennai","Wed"): print(row)
    print("\nTimetable:")
    for no,t in TIMETABLE.items(): print(no,t["name"],t["days"],t["stops"])
    print("third stop departure of 12601:",TIMETABLE["12601"]["stops"][2][2])
    index={}
    for no,t in TIMETABLE.items():
        for station,arr,dep in t["stops"]: index.setdefault(station,[]).append((no,t["days"],dep,t["name"]))
    print("indexed Chennai:",sorted([(dep,no,name) for no,days,dep,name in index.get("Chennai",[]) if "Wed" in days]))
    print("unknown station:",query(TIMETABLE,"Atlantis","Mon"))
    print("not running day:",query(TIMETABLE,"Chennai","Never"))
    for n in (100,1000,10000):
        data={}
        for i in range(n):
            data[str(i)]={"name":f"Train{i}","stops":[(f"Station{j%100}", "08:00","08:05") for j in range(10)],"days":{"Mon","Wed"}}
        idx={}
        for no,t in data.items():
            for s,_,dep in t["stops"]: idx.setdefault(s,[]).append((no,t["days"],dep))
        start=time.perf_counter(); [query(data,"Station5","Mon") for _ in range(20)]; t1=time.perf_counter()-start
        start=time.perf_counter(); [idx.get("Station5",[]) for _ in range(20)]; t2=time.perf_counter()-start
        print(f"{n} trains: scan={t1:.5f}s indexed lookup={t2:.5f}s index keys={len(idx)}")
if __name__ == "__main__": main()
