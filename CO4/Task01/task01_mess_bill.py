from decimal import Decimal, InvalidOperation
from pathlib import Path

def process_bill_file(filename):
    total=Decimal("0.00"); report=[]; rejected=[]
    with open(filename,"r",encoding="utf-8") as file:
        for line_no,line in enumerate(file,1):
            if not line.strip(): continue
            parts=line.rstrip("\n").split(",")
            try:
                if len(parts)!=3: raise ValueError("expected register,name,amount")
                reg,name,amount=parts
                value=Decimal(amount.strip())
                if not value.is_finite(): raise InvalidOperation
                total += value
                report.append(f"{name.strip()} {value:.2f}")
            except (ValueError,InvalidOperation) as exc:
                rejected.append((line_no,line.rstrip("\n"),str(exc)))
    return report,total,rejected

def main():
    sample=Path(__file__).with_name("mess_oct_sample.txt")
    sample.write_text("192311001,Anu,1250.50\n192311002,Bala,900\nBAD LINE\n192311003,Chitra,abc\n\n",encoding="utf-8")
    report,total,rejected=process_bill_file(sample)
    print("\n".join(report)); print("Total",total); print("Rejected:",rejected)
    print("Design note: streaming uses O(one line + report/rejections) memory; storing the whole file uses O(file size).")
if __name__ == "__main__": main()
