import csv
import io
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

def inspect_csv_text(name, text, encoding="utf-8"):
    try:
        decoded = text.encode(encoding).decode(encoding)
        reader = csv.DictReader(io.StringIO(decoded))
        required = {"station", "date", "pm25"}
        if not reader.fieldnames:
            return f"{name}: EMPTY FILE / NO HEADER"
        missing = required - set(reader.fieldnames)
        if missing:
            return f"{name}: SCHEMA ERROR, missing {sorted(missing)}"
        return f"{name}: OK, columns={reader.fieldnames}"
    except UnicodeError as exc:
        return f"{name}: ENCODING ERROR: {exc}"

def sentiment_score(text):
    positive = {"good","clean","fast","helpful","improved"}
    negative = {"bad","dirty","slow","rude","smoke","broken"}
    negators = {"not","never","no"}
    words = text.lower().replace(".", " ").replace(",", " ").replace("!", " ").split()
    total = 0
    for i, word in enumerate(words):
        value = 1 if word in positive else -1 if word in negative else 0
        if i and words[i-1] in negators:
            value *= -1
        total += value
    return total

def main():
    print(inspect_csv_text("missing-column", "station,date\\nAdyar,2026-10-01"))
    print(inspect_csv_text("wrong-delimiter", "station;date;pm25\\nAdyar;2026-10-01;48"))
    print(inspect_csv_text("empty-file", ""))
    try:
        "station,date,pm25\\nAdyar,2026-10-01,48".encode("utf-8").decode("utf-8")
        print("encoding-test: UTF-8 input accepted")
        bytes([0xff, 0xfe]).decode("utf-8")
    except UnicodeDecodeError as exc:
        print("encoding-test: NON-UTF-8 bytes rejected:", type(exc).__name__)

    readings = [("Adyar","2026-10-01",48.0),("Guindy","2026-10-01",95.0),
                ("Guindy","2026-10-03",121.0),("Adyar","2026-10-04",60.0)]
    con = sqlite3.connect(":memory:")
    con.execute("CREATE TABLE aq (station TEXT, day TEXT, pm25 REAL)")
    con.executemany("INSERT INTO aq VALUES (?, ?, ?)", readings)
    con.commit()
    def station_average(name):
        row = con.execute("SELECT AVG(pm25) FROM aq WHERE station = ?", (name,)).fetchone()
        return row[0]
    print("SAFE QUERY AVERAGES:", station_average("Adyar"), station_average("Guindy"))
    print("PARAMETERISED INJECTION ATTEMPT:", station_average("Adyar' OR '1'='1"))
    malicious = "Adyar' OR '1'='1"
    unsafe_sql = "SELECT AVG(pm25) FROM aq WHERE station = '" + malicious + "'"
    print("UNSAFE CONCATENATED SQL:", unsafe_sql)
    print("UNSAFE CONCATENATED RESULT:", con.execute(unsafe_sql).fetchone()[0])
    con.close()

    cases = [
        "The road is not good.",
        "The service is not bad.",
        "The road is not not good.",
        "Great, another day of dirty air!",
        "The road is clean, but the factory smoke is bad.",
        "The bus was good but very slow."
    ]
    print("SENTIMENT ADVERSARIAL CASES:")
    for text in cases:
        s = sentiment_score(text)
        label = "positive" if s > 0 else "negative" if s < 0 else "neutral"
        print(f"{label:8} | score={s:2} | {text}")

if __name__ == "__main__":
    main()
