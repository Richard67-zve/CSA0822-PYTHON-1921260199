import copy, sys, time

def main():
    rows,cols=3,4
    bad=[[0]*cols]*rows; bad[0][1]=7
    good=[[0 for _ in range(cols)] for _ in range(rows)]; good[0][1]=7
    print("bad :",bad); print("good:",good)
    print("row identity:",bad[0] is bad[1],good[0] is good[1])
    stops={(13.0827,80.2707):"Chennai Central",(13.0418,80.2341):"T. Nagar"}
    print(stops[(13.0418,80.2341)])
    original=[[1,2],[3,4]]
    alias=original; shallow=copy.copy(original); sliced=original[:]; deep=copy.deepcopy(original)
    original[0][0]=99
    print("alias/shallow/slice/deep:",alias,shallow,sliced,deep)
    coords=(13.0,80.0)
    for lat,lon in [coords]: print("unpacked:",lat,lon)
    try: stops[[13.0418,80.2341]]="invalid"
    except TypeError as e: print("list key error:",e)
    million=list(range(1_000_000)); tuple_million=tuple(million)
    print("container sizes:",sys.getsizeof(million),sys.getsizeof(tuple_million))
    for obj in (million,tuple_million):
        start=time.perf_counter(); _=obj[500000]; print(type(obj).__name__,"index time:",time.perf_counter()-start)
    nested=(["mutable"],)
    nested[0].append("inside tuple"); print("tuple containing list:",nested)
if __name__ == "__main__": main()
