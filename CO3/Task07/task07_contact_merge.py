import random,time,string

def normalise_phone(phone):
    digits=''.join(ch for ch in (phone or '') if ch.isdigit())
    if digits.startswith("91") and len(digits)==12: digits=digits[2:]
    return digits

def normalise_name(name):
    return " ".join((name or "").lower().replace(".","").split())

def merge_contacts(groups):
    merged={}
    for contact in groups:
        name=contact.get("name","").strip()
        phones={normalise_phone(p) for p in contact.get("phones",[]) if normalise_phone(p)}
        emails={e.strip().lower() for e in contact.get("emails",[]) if e.strip()}
        keys=phones or {"name:"+normalise_name(name)}
        for key in keys:
            record=merged.setdefault(key,{"names":set(),"phones":set(),"emails":set()})
            if name: record["names"].add(name)
            record["phones"].update(phones); record["emails"].update(emails)
    # Merge overlapping keys that belong to the same phone by canonical number.
    result={}
    for record in merged.values():
        key=min(record["phones"]) if record["phones"] else "name:"+min(record["names"])
        target=result.setdefault(key,{"names":set(),"phones":set(),"emails":set()})
        for field in target: target[field].update(record[field])
    return result

def main():
    contacts=[
      {"name":"Dr. Ravi","phones":["+91 98400 12345"],"emails":["RAVI@EXAMPLE.COM"]},
      {"name":"ravi kumar","phones":["9840012345","98400-12345"],"emails":["ravi.work@example.com"]},
      {"name":"Maya","phones":["+91 90000 11111"],"emails":[]},
      {"name":"Unknown","phones":[],"emails":["unknown@example.com"]},
      {"name":"Dr Ravi","phones":["9840012345"],"emails":["RAVI@EXAMPLE.COM"]}]
    print("merged:")
    for key,value in merge_contacts(contacts).items(): print(key,value)
    for n in (1000,100000):
        generated=[{"name":f"Person{i}","phones":[f"90000{i:05d}"],"emails":[]} for i in range(n)]
        start=time.perf_counter(); merged=merge_contacts(generated); elapsed=time.perf_counter()-start
        print(f"{n} contacts -> {len(merged)} groups in {elapsed:.4f}s")
    print("Limitation: matching by phone can incorrectly merge shared family numbers; name-only matching can also be ambiguous.")
if __name__ == "__main__": main()
