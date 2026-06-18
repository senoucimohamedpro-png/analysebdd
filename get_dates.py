import re, sys
sys.stdout.reconfigure(encoding='utf-8')

base = r"C:\Users\ITADMI~1\AppData\Local\Temp\xlsx_extract"
data = open(base + r"\xl\worksheets\sheet1.xml", encoding="utf-8").read()

# date_chargement = colonne C, stockee comme shared string (t="s")
vals = re.findall(r'<c r="C\d+"[^>]*><v>(\d+)</v>', data)
print(f"Valeurs col C: {len(vals)}")
unique_idx = sorted(set(int(x) for x in vals))
print(f"Indices uniques: {unique_idx}")

ss = open(base + r"\xl\sharedStrings.xml", encoding="utf-8").read()
items = re.findall(r"<si>(.*?)</si>", ss, re.S)
def txt(i): return re.sub("<[^>]*>","", items[i]).strip() if i < len(items) else ""

print("\nVraies dates de chargement dans le fichier:")
for i in unique_idx:
    val = txt(i)
    if val:
        print(f"  idx {i:6d} -> '{val}'")
