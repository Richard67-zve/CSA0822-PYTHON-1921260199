import csv
import cProfile
import io
import random
import sqlite3
import statistics
import time
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs"
DATA = ROOT / "data"
OUT.mkdir(exist_ok=True); DATA.mkdir(exist_ok=True)
SEED = 20261005

def generate_csv(path, station_count):
    rng = random.Random(SEED + station_count)
    start = datetime(2026, 1, 1)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(["station","date","hour","pm25"])
        for s in range(station_count):
            station = f"Station{s+1:03}"
            for i in range(365 * 24):
                dt = start + timedelta(hours=i)
                w.writerow([station, dt.date().isoformat(), dt.strftime("%H:%M"),
                            round(rng.uniform(5,180), 2)])

def python_loop(path):
    sums, counts = defaultdict(float), defaultdict(int)
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            key = (row["station"], row["date"])
            sums[key] += float(row["pm25"]); counts[key] += 1
    return {k: sums[k]/counts[k] for k in sums}

def pandas_groupby(path):
    df = pd.read_csv(path)
    result = df.groupby(["station","date"])["pm25"].mean()
    return {k: float(v) for k,v in result.items()}

def sql_groupby(path, db_path):
    if db_path.exists(): db_path.unlink()
    con = sqlite3.connect(db_path)
    con.execute("CREATE TABLE readings(station TEXT, day TEXT, pm25 REAL)")
    batch = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            batch.append((row["station"], row["date"], float(row["pm25"])))
            if len(batch) >= 20000:
                con.executemany("INSERT INTO readings VALUES (?,?,?)", batch); batch.clear()
    if batch: con.executemany("INSERT INTO readings VALUES (?,?,?)", batch)
    con.commit()
    result = {(s,d): float(v) for s,d,v in con.execute(
        "SELECT station, day, AVG(pm25) FROM readings GROUP BY station, day")}
    con.close()
    return result

def median_time(fn, repeats=3):
    times=[]; result=None
    for _ in range(repeats):
        start=time.perf_counter(); result=fn(); times.append(time.perf_counter()-start)
    return statistics.median(times), result

def main():
    rows=[]
    for count in (1,12,120):
        path=DATA / f"benchmark_{count}_stations.csv"
        print(f"Generating {count} station dataset...")
        generate_csv(path,count)
        db=OUT / f"benchmark_{count}.db"
        t_loop, r_loop = median_time(lambda: python_loop(path))
        t_pd, r_pd = median_time(lambda: pandas_groupby(path))
        t_sql, r_sql = median_time(lambda: sql_groupby(path,db))
        assert r_loop.keys()==r_pd.keys()==r_sql.keys()
        assert all(abs(r_loop[k]-r_pd[k]) < 1e-8 and abs(r_loop[k]-r_sql[k]) < 1e-8 for k in r_loop)
        n=count*365*24
        rows.append((count,n,t_loop,t_pd,t_sql))
        print(f"{count} stations, {n:,} rows | loop={t_loop:.4f}s pandas={t_pd:.4f}s SQL(end-to-end load+group)={t_sql:.4f}s")
        if count==1:
            profiler=cProfile.Profile(); profiler.enable(); python_loop(path); profiler.disable()
            stream=io.StringIO()
            import pstats
            pstats.Stats(profiler,stream=stream).sort_stats("cumulative").print_stats(20)
            (OUT/"b3_cprofile.txt").write_text(stream.getvalue(),encoding="utf-8")
    with (OUT/"b3_benchmark_results.csv").open("w",newline="",encoding="utf-8") as f:
        w=csv.writer(f); w.writerow(["stations","rows","python_loop_seconds","pandas_seconds","sql_end_to_end_seconds"]); w.writerows(rows)
    print("All three methods agree for every generated dataset.")
    print("Timing table saved to outputs/b3_benchmark_results.csv")
    print("Profile saved to outputs/b3_cprofile.txt")
    print("Note: SQL timing includes loading the generated CSV into a fresh database plus GROUP BY.")

if __name__=="__main__":
    main()
