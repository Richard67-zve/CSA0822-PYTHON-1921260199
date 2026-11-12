from pathlib import Path
from collections import defaultdict
import csv

def process_folder(folder, output_folder):
    folder=Path(folder); output=Path(output_folder); output.mkdir(parents=True,exist_ok=True)
    counts=defaultdict(lambda:[0,0])  # reg -> [present, valid total]
    errors=[]
    for path in sorted(folder.glob("*.csv")):
        with path.open("r",encoding="utf-8") as f:
            for line_no,line in enumerate(f,1):
                fields=line.strip().split(",")
                if len(fields)!=3 or fields[2] not in ("P","A"):
                    errors.append((path.name,line_no,line.strip()))
                    continue
                reg,date,status=fields
                counts[reg][1]+=1
                if status=="P": counts[reg][0]+=1
    attendance=[]
    for reg,(present,total) in sorted(counts.items()):
        pct=present/total*100 if total else 0
        attendance.append((reg,present,total,round(pct,2)))
    with (output/"attendance_report.csv").open("w",newline="",encoding="utf-8") as f:
        w=csv.writer(f); w.writerow(["register","present","valid_days","percentage"]); w.writerows(attendance)
    with (output/"below_75.csv").open("w",newline="",encoding="utf-8") as f:
        w=csv.writer(f); w.writerow(["register","percentage"]); w.writerows((r,p) for r,_,_,p in attendance if p<75)
    with (output/"damaged_lines.csv").open("w",newline="",encoding="utf-8") as f:
        w=csv.writer(f); w.writerow(["filename","line_number","content"]); w.writerows(errors)
    return attendance,errors

def main():
    base=Path(__file__).parent/"sample_daily_files"; base.mkdir(exist_ok=True)
    (base/"day01.csv").write_text("192311001,2026-10-01,P\n192311002,2026-10-01,A\nbad,line\n",encoding="utf-8")
    (base/"day02.csv").write_text("192311001,2026-10-02,A\n192311002,2026-10-02,A\n",encoding="utf-8")
    print(process_folder(base,Path(__file__).parent/"reports"))
    print("Reports written to reports/ (attendance_report.csv, below_75.csv, damaged_lines.csv)")
if __name__ == "__main__": main()
