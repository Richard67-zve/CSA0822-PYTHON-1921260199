import os,tempfile
class InvalidRecord(Exception):
    """Attendance record does not match the required format."""

def parse_line(line):
    parts=line.strip().split(",")
    if len(parts)!=3: raise InvalidRecord(f"expected 3 fields, found {len(parts)}")
    reg,date,status=parts
    if status not in ("P","A"): raise InvalidRecord(f"invalid status {status!r}")
    if not reg or not date: raise InvalidRecord("register number/date cannot be empty")
    return reg,date,status

def summarise(path):
    present=absent=0; errors=[]
    try:
        with open(path,"r",encoding="utf-8") as file:
            for line_no,line in enumerate(file,1):
                try:
                    _,_,status=parse_line(line)
                except InvalidRecord as exc:
                    errors.append((line_no,str(exc)))
                else:
                    if status=="P": present+=1
                    else: absent+=1
    except (FileNotFoundError,PermissionError,UnicodeDecodeError) as exc:
        raise RuntimeError(f"Could not process attendance file: {path}") from exc
    finally:
        print("Finished attempting to read:",path)
    return present,absent,errors

def main():
    data=("192311001,2026-10-08,P\n192311002,2026-10-08,A\n"
          "192311003,2026-10-08\n192311004,2026-10-08,L\n")
    with tempfile.NamedTemporaryFile("w",suffix=".csv",delete=False,encoding="utf-8") as tmp:
        tmp.write(data); path=tmp.name
    try:
        print(summarise(path))
        try: summarise(path+"_missing")
        except RuntimeError as exc: print(type(exc.__cause__).__name__,":",exc)
    finally: os.remove(path)
    print("Specific exceptions preserve diagnostics; `except Exception: pass` would hide programming errors too.")
if __name__ == "__main__": main()
