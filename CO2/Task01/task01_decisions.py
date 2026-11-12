def separate_ifs(units, ration, elderly):
    decisions = []
    if units <= 100:
        decisions.append("Full subsidy")
    if 101 <= units <= 200 and ration:
        decisions.append("Partial subsidy")
    if units > 200 and elderly:
        decisions.append("Elderly exception subsidy")
    if not decisions:
        decisions.append("No subsidy")
    return decisions

def chained(units, ration, elderly):
    if units <= 100:
        return "Full subsidy"
    elif 101 <= units <= 200:
        return "Partial subsidy" if ration else "No subsidy"
    elif units > 200 and elderly:
        return "Elderly exception subsidy"
    else:
        return "No subsidy"

def lookup_version(units, ration, elderly):
    if units <= 100: return "Full subsidy"
    if units <= 200: return "Partial subsidy" if ration else "No subsidy"
    return "Elderly exception subsidy" if elderly else "No subsidy"

def main():
    households = [(100,False,False),(101,True,False),(101,False,False),
                  (200,True,False),(201,False,True),(201,True,False),
                  (80,True,True),(200,False,True)]
    print("units ration elderly | separate-if result | if-elif result")
    for u,r,e in households:
        print(f"{u:5} {str(r):6} {str(e):7} | {separate_ifs(u,r,e)} | {chained(u,r,e)}")
    print("\nAlternative lookup implementation:")
    for u,r,e in households:
        print(u, lookup_version(u,r,e))
    print("\nFor k slabs, ordered lookup is O(k) worst-case; direct chained conditions are O(k) worst-case and O(1) extra space.")
if __name__ == "__main__": main()
