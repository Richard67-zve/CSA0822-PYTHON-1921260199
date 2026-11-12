import csv
import io
import sqlite3
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs"
DATA = ROOT / "data"
OUT.mkdir(exist_ok=True)
DATA.mkdir(exist_ok=True)

RAW = """station,date,hour,pm25,pm10,no2,temperature,temperature_unit
Adyar,2026-10-01,08:00,48,82,21,86,F
Adyar,2026-10-01,12:00,52,90,23,30,C
Adyar,2026-10-02,08:00,NA,85,20,29,C
Adyar,2026-10-02,12:00,,88,22,31,C
Guindy,2026-10-01,08:00,95,140,34,87,F
Guindy,2026-10-01,12:00,-5,130,30,32,C
Guindy,2026-10-02,08:00,121,160,40,33,C
Guindy,2026-10-02,12:00,1500,170,45,34,C
Adyar,2026-10-03,08:00,48,80,19,28,C
Guindy,2026-10-03,08:00,110,150,37,33,C
"""

def load_clean(text):
    rows, rejected = [], []
    reader = csv.DictReader(io.StringIO(text))
    required = {"station", "date", "hour", "pm25", "pm10", "no2",
                "temperature", "temperature_unit"}
    if not reader.fieldnames or not required.issubset(reader.fieldnames):
        missing = required - set(reader.fieldnames or [])
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    seen = set()
    for line_no, row in enumerate(reader, start=2):
        station = (row.get("station") or "").strip().title()
        day = (row.get("date") or "").strip()
        hour = (row.get("hour") or "").strip()
        key = (station, day, hour)
        try:
            pm_raw = (row.get("pm25") or "").strip()
            if pm_raw.upper() in {"", "NA", "NULL"}:
                raise ValueError("missing pm25")
            pm25 = float(pm_raw)
            if pm25 < 0 or pm25 > 999:
                raise ValueError("pm25 outside accepted range 0..999")
            pm10 = float(row["pm10"])
            no2 = float(row["no2"])
            temp = float(row["temperature"])
            unit = row["temperature_unit"].strip().upper()
            if unit == "F":
                temp = (temp - 32) * 5 / 9
            elif unit != "C":
                raise ValueError(f"unknown temperature unit {unit}")
            if key in seen:
                raise ValueError("duplicate station/date/hour")
            seen.add(key)
            rows.append((station, day, hour, pm25, pm10, no2, round(temp, 3)))
        except (ValueError, TypeError, KeyError) as exc:
            rejected.append((line_no, station, day, hour, str(exc)))
    return rows, rejected

def main():
    raw_path = DATA / "raw_readings.csv"
    raw_path.write_text(RAW, encoding="utf-8")
    clean, rejected = load_clean(RAW)
    with (OUT / "cleaned_readings.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["station","date","hour","pm25","pm10","no2","temperature_c"])
        w.writerows(clean)
    with (OUT / "rejected_rows.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(["line","station","date","hour","reason"]); w.writerows(rejected)

    db = OUT / "air_quality.db"
    if db.exists(): db.unlink()
    con = sqlite3.connect(db)
    con.executescript("""
    CREATE TABLE stations (
        station_id INTEGER PRIMARY KEY,
        station_name TEXT UNIQUE NOT NULL
    );
    CREATE TABLE readings (
        station_id INTEGER NOT NULL,
        reading_date TEXT NOT NULL,
        reading_hour TEXT NOT NULL,
        pm25 REAL, pm10 REAL, no2 REAL, temperature_c REAL,
        PRIMARY KEY(station_id, reading_date, reading_hour),
        FOREIGN KEY(station_id) REFERENCES stations(station_id)
    );
    """)
    names = sorted({r[0] for r in clean})
    con.executemany("INSERT INTO stations(station_name) VALUES (?)", [(n,) for n in names])
    ids = {name: station_id for name, station_id in con.execute("SELECT station_name, station_id FROM stations")}
    con.executemany(
        "INSERT INTO readings VALUES (?, ?, ?, ?, ?, ?, ?)",
        [(ids[r[0]], *r[1:]) for r in clean])
    con.commit()
    print("CLEANED ROWS:", len(clean))
    print("REJECTED ROWS:", len(rejected))
    print("REJECT REASONS:", [r[-1] for r in rejected])
    queries = {
        "Adyar October mean": ("SELECT AVG(pm25) FROM readings JOIN stations USING(station_id) WHERE station_name=? AND reading_date>=? AND reading_date<?",
                               ("Adyar","2026-10-01","2026-11-01")),
        "Highest reading": ("SELECT station_name, MAX(pm25) FROM readings JOIN stations USING(station_id) GROUP BY station_name ORDER BY MAX(pm25) DESC LIMIT 1", ()),
        "Valid readings by station": ("SELECT station_name, COUNT(pm25) FROM readings JOIN stations USING(station_id) GROUP BY station_name", ())
    }
    for label, (sql, params) in queries.items():
        print(label + ":", con.execute(sql, params).fetchall())
    df = pd.read_sql_query("""
        SELECT s.station_name AS station, r.reading_date AS day, r.reading_hour AS hour,
               r.pm25, r.temperature_c
        FROM readings r JOIN stations s USING(station_id)
    """, con)
    df["day"] = pd.to_datetime(df["day"])
    daily = df.groupby("day", as_index=False)["pm25"].mean()
    plt.figure()
    plt.plot(daily["day"], daily["pm25"], marker="o")
    plt.title("Daily Mean PM2.5 Trend"); plt.xlabel("Date"); plt.ylabel("PM2.5 (µg/m³)")
    plt.tight_layout(); plt.savefig(OUT / "b1_daily_trend.png"); plt.close()
    means = df.groupby("station")["pm25"].mean()
    plt.figure(); means.plot(kind="bar")
    plt.title("Mean PM2.5 by Station"); plt.xlabel("Station"); plt.ylabel("PM2.5 (µg/m³)")
    plt.tight_layout(); plt.savefig(OUT / "b1_station_comparison.png"); plt.close()
    plt.figure()
    plt.scatter(df["temperature_c"], df["pm25"])
    plt.title("Temperature vs PM2.5"); plt.xlabel("Temperature (°C)"); plt.ylabel("PM2.5 (µg/m³)")
    plt.tight_layout(); plt.savefig(OUT / "b1_temperature_scatter.png"); plt.close()
    df["hour_label"] = df["hour"].str.slice(0,2)
    groups = [g["pm25"].tolist() for _,g in df.groupby("hour_label")]
    labels = [k for k,_ in df.groupby("hour_label")]
    plt.figure(); plt.boxplot(groups, labels=labels)
    plt.title("PM2.5 Distribution by Hour"); plt.xlabel("Hour"); plt.ylabel("PM2.5 (µg/m³)")
    plt.tight_layout(); plt.savefig(OUT / "b1_hourly_boxplot.png"); plt.close()
    print("CHARTS SAVED: 4 files in outputs/")
    con.close()

if __name__ == "__main__":
    main()
