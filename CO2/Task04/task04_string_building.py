import time

def build_plus(parts):
    text = ""
    for part in parts: text += part + ";"
    return text

def build_join(parts):
    return ";".join(parts) + (";" if parts else "")

def build_fstring(parts):
    return "".join(f"{part};" for part in parts)

def main():
    for n in (1000, 10000, 200000):
        items = [f"Item{i}:Rs{i % 50}" for i in range(n)]
        results = {}
        for name, fn in (("plus",build_plus),("join",build_join),("f-string",build_fstring)):
            samples=[]
            for _ in range(3):
                start=time.perf_counter(); output=fn(items); samples.append(time.perf_counter()-start)
            results[name]=(output, sum(samples)/len(samples))
        print(f"\n{n:,} items; outputs equal:", len({v[0] for v in results.values()}) == 1)
        for name,(_,avg) in results.items(): print(f"{name:9} average: {avg:.6f} s")
    print("\njoin constructs from an iterable in one operation; repeated += may copy growing strings.")
if __name__ == "__main__": main()
