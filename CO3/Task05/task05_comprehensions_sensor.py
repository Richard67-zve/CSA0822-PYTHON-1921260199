import random,time,sys

def loop_clean(readings):
    c=[]
    for x in readings:
        if -50<=x<=50: c.append(x)
    f=[x*9/5+32 for x in c]
    alarms=[i for i,x in enumerate(c) if not 2<=x<=8]
    return c,f,alarms

def comp_clean(readings):
    c=[x for x in readings if -50<=x<=50]
    f=[x*9/5+32 for x in c]
    alarms=[i for i,x in enumerate(c) if not 2<=x<=8]
    return c,f,alarms

def map_filter_clean(readings):
    c=list(filter(lambda x:-50<=x<=50,readings))
    f=list(map(lambda x:x*9/5+32,c))
    alarms=[i for i,x in enumerate(c) if not 2<=x<=8]
    return c,f,alarms

def main():
    readings=[-60,2,5,9,51,7,0,55]
    a=loop_clean(readings); b=comp_clean(readings); c=map_filter_clean(readings)
    print("loop:",a); print("comprehension:",b); print("map/filter:",c)
    print("all equal:",a==b==c)
    for n in (10000,100000,1000000):
        data=[random.uniform(-60,60) for _ in range(n)]
        for fn in (loop_clean,comp_clean,map_filter_clean):
            start=time.perf_counter(); fn(data); print(f"{n} {fn.__name__}: {time.perf_counter()-start:.5f}s")
    gen=(x for x in readings if -50<=x<=50)
    print("list size vs generator size:",sys.getsizeof([x for x in readings]),sys.getsizeof(gen))
    print("all-valid/all-invalid:",len(comp_clean([3]*5)[0]),len(comp_clean([100]*5)[0]))
if __name__ == "__main__": main()
