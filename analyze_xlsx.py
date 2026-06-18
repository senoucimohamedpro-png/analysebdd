import re, sys

base = r"C:\Users\ITADMI~1\AppData\Local\Temp\xlsx_extract"

data_ss = open(base + r"\xl\sharedStrings.xml", encoding="utf-8").read()
items = re.findall(r"<si>(.*?)</si>", data_ss, re.S)
def txt(i): return re.sub("<[^>]*>","", items[i]).strip() if i < len(items) else ""

qualif_idx = {54:"No More CallBack Rules",136:"Call Back Disable",
 4268:"Answering Machine",18200:"refus argumente",21793:"rappel personnel",
 28202:"recycled record",32503:"refus de repondre",65021:"Wrong Number System",
 81455:"Not Qualified",81624:"Callback - abandoned",94442:"faux numero machine",
 95126:"hors cible",96144:"doublon",96370:"pa en ligne",109826:"don en ligne"}

print("Reading sheet... (may take ~20s)")
sys.stdout.flush()
data_sh = open(base + r"\xl\worksheets\sheet1.xml", encoding="utf-8").read()

print("Counting qualif1 values...")
counts = {}
for idx, label in qualif_idx.items():
    n = data_sh.count(f"<v>{idx}</v>")
    if n: counts[label] = n
total = sum(counts.values())
print(f"Total: {total}")
for k,v in sorted(counts.items(), key=lambda x:-x[1]):
    print(f"  {v:6d}  {k}")

print("\ncode_marketing:")
code_matches = re.findall(r'<c r="Z\d+"[^>]*><v>(\d+)</v>', data_sh)
code_idx = set(int(x) for x in code_matches)
for i in sorted(code_idx)[:20]: print(f"  {code_matches.count(str(i)):5d}  {txt(i)}")

print("\npriority distinct:")
prio = sorted(set(int(x) for x in re.findall(r'<c r="AX\d+"[^>]*><v>(-?\d+)</v>', data_sh)))
print(prio[:30])

print("\ndate_chargement (raw serial, first 5 unique):")
dc = sorted(set(re.findall(r'<c r="C\d+" s="\d+"><v>(\d+\.?\d*)</v>', data_sh)))[:5]
print(dc)
