import csv
import re
import sqlite3
import time
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs"
DATA = ROOT / "data"
OUT.mkdir(exist_ok=True); DATA.mkdir(exist_ok=True)

POSITIVE = {"good","clean","fast","helpful","improved"}
NEGATIVE = {"bad","dirty","slow","rude","smoke","broken"}
NEGATORS = {"not","never","no"}
STOP = {"the","a","an","is","are","was","were","and","or","to","of","in","on","for","at","it","this","from","but"}

# Synthetic examples for demonstrating the pipeline. Replace with approved real complaints
# and manually reviewed reference labels for the final assignment submission.
SEED_COMPLAINTS = [
("Roads are clean and the bus was fast.", "positive"),
("Smoke from the factory makes the air bad.", "negative"),
("The staff were not helpful.", "negative"),
("Not bad, service improved.", "positive"),
("The road is dirty near the market.", "negative"),
("The bus service is good today.", "positive"),
("Air quality is bad near the factory.", "negative"),
("The street is clean after the workers arrived.", "positive"),
("The traffic is slow and the road is broken.", "negative"),
("The response team was helpful.", "positive"),
("The air is not clean near the school.", "negative"),
("The new bus route is fast and good.", "positive"),
("Smoke is making the neighbourhood dirty.", "negative"),
("The complaint service was rude.", "negative"),
("The situation improved and the road is clean.", "positive"),
("The road is not bad now.", "positive"),
("The bus is slow but the staff are helpful.", "neutral"),
("There is smoke outside my home.", "negative"),
("The road is clean but traffic is slow.", "neutral"),
("The repair work improved the broken road.", "positive"),
("The air smells bad every evening.", "negative"),
("The team was not rude and was helpful.", "positive"),
("The bus is good but the stop is dirty.", "neutral"),
("The factory smoke is bad for residents.", "negative"),
("The service improved this week.", "positive"),
]
def score(text):
    words = re.findall(r"[a-z']+", text.lower())
    total = 0
    for i, word in enumerate(words):
        value = 1 if word in POSITIVE else -1 if word in NEGATIVE else 0
        if i and words[i-1] in NEGATORS:
            value *= -1
        total += value
    return total

def label(text):
    s=score(text)
    return "positive" if s>0 else "negative" if s<0 else "neutral"

def summarise(text,k=2):
    sentences=[s.strip() for s in re.split(r"(?<=[.!?])\s+",text) if s.strip()]
    words=[w.lower() for w in re.findall(r"[A-Za-z]+",text) if w.lower() not in STOP]
    freq=Counter(words)
    ranked=sorted(enumerate(sentences),
        key=lambda pair: sum(freq[w.lower()] for w in re.findall(r"[A-Za-z]+",pair[1])),
        reverse=True)
    chosen=sorted(i for i,_ in ranked[:k])
    return " ".join(sentences[i] for i in chosen)

def create_dataset(path):
    rows=[]
    for i in range(50):
        text, human = SEED_COMPLAINTS[i % len(SEED_COMPLAINTS)]
        rows.append((i+1,text,human))
    with open(path,"w",newline="",encoding="utf-8") as f:
        w=csv.writer(f); w.writerow(["complaint_id","complaint","human_label"]); w.writerows(rows)

def index_test(db):
    con=sqlite3.connect(db)
    con.executescript("DROP TABLE IF EXISTS readings; CREATE TABLE readings(station TEXT, day TEXT, pm25 REAL);")
    rows=[]
    for s in range(120):
        for day in range(365):
            rows.append((f"Station{s:03}",f"2026-{day//30+1:02}-{day%30+1:02}",float((s*7+day)%180)))
    con.executemany("INSERT INTO readings VALUES (?,?,?)",rows); con.commit()
    sql="SELECT AVG(pm25) FROM readings WHERE station=? AND day>=? AND day<?"
    def measure():
        vals=[]
        for _ in range(100):
            t=time.perf_counter(); con.execute(sql,("Station020","2026-03-01","2026-04-01")).fetchone()
            vals.append((time.perf_counter()-t)*1000)
        return sorted(vals)[len(vals)//2]
    before=measure()
    con.execute("CREATE INDEX idx_readings_station_day ON readings(station,day)"); con.commit()
    after=measure()
    plan=con.execute("EXPLAIN QUERY PLAN "+sql,("Station020","2026-03-01","2026-04-01")).fetchall()
    con.close()
    return before,after,plan

def main():
    complaint_file=DATA/"complaints_synthetic.csv"
    create_dataset(complaint_file)
    predictions=[]; references=[]
    with open(complaint_file,encoding="utf-8",newline="") as f:
        rows=list(csv.DictReader(f))
    with (OUT/"b4_complaint_results.csv").open("w",encoding="utf-8",newline="") as f:
        w=csv.writer(f); w.writerow(["complaint_id","complaint","predicted_label","human_reference","summary"])
        for row in rows:
            pred=label(row["complaint"]); ref=row["human_label"]
            predictions.append(pred); references.append(ref)
            w.writerow([row["complaint_id"],row["complaint"],pred,ref,summarise(row["complaint"])])
    matches=sum(p==r for p,r in zip(predictions,references))
    pct=100*matches/len(references)
    print(f"COMPLAINTS REVIEWED: {len(references)} (synthetic demonstration set)")
    print(f"AGREEMENT: {matches}/{len(references)} = {pct:.1f}%")
    print("PREDICTED LABEL COUNTS:", {x:predictions.count(x) for x in sorted(set(predictions))})
    db=OUT/"b4_index_test.db"
    before,after,plan=index_test(db)
    print(f"QUERY MEDIAN BEFORE INDEX: {before:.4f} ms")
    print(f"QUERY MEDIAN AFTER INDEX:  {after:.4f} ms")
    print("QUERY PLAN AFTER INDEX:",plan)
    (OUT/"b4_observations.txt").write_text(
        f"Synthetic complaint agreement: {matches}/{len(references)} = {pct:.1f}%\\n"
        f"Median query before index: {before:.4f} ms\\n"
        f"Median query after index: {after:.4f} ms\\n"
        "Replace synthetic complaints and reference labels with approved manually reviewed data.\\n",
        encoding="utf-8")
    print("Complaint predictions/summaries saved to outputs/b4_complaint_results.csv")

if __name__=="__main__":
    main()
