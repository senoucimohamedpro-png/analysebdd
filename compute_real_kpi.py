import re, sys
sys.stdout.reconfigure(encoding='utf-8')

base = r"C:\Users\ITADMI~1\AppData\Local\Temp\xlsx_extract"
print("Lecture du fichier (peut prendre 30s)...")
sys.stdout.flush()

ss_data = open(base + r"\xl\sharedStrings.xml", encoding="utf-8").read()
items = re.findall(r"<si>(.*?)</si>", ss_data, re.S)
def txt(i):
    return re.sub("<[^>]*>", "", items[int(i)]).strip() if int(i) < len(items) else ""

sh_data = open(base + r"\xl\worksheets\sheet1.xml", encoding="utf-8").read()
print("Fichier lu. Extraction des colonnes D (qualif1) et AX (priorite)...")
sys.stdout.flush()

# Extraire toutes les paires (qualif1_idx, priorite_val) par ligne
# Colonne D = contact_qualif1 (shared string)
# Colonne AX = priorite (numeric)
# On extrait row par row via regex sur les cellules

# Extraire D et AX par numero de ligne
qualif_by_row = {}
prio_by_row = {}

for m in re.finditer(r'<c r="D(\d+)"[^>]*><v>(\d+)</v>', sh_data):
    row, idx = m.group(1), m.group(2)
    if row != "1":  # ignorer header
        qualif_by_row[row] = txt(idx)

for m in re.finditer(r'<c r="AX(\d+)"[^>]*><v>(-?\d+)</v>', sh_data):
    row, val = m.group(1), m.group(2)
    if row != "1":
        prio_by_row[row] = int(val)

print(f"Lignes avec qualif1: {len(qualif_by_row)}")
print(f"Lignes avec priorite: {len(prio_by_row)}")

# Classification
POSITIF = {"pa en ligne","don en ligne","don avec montant","pa","upgrade"}
TRAITE  = POSITIF | {"refus argumente","refus de repondre","indecis"}
BLOQUE_PRIOS = {-999,-800,-300,-50,-5}

all_rows = set(qualif_by_row.keys()) | set(prio_by_row.keys())
total = len(all_rows)

traite = positif = bloque = 0
qualif_counts = {}

for row in all_rows:
    q = qualif_by_row.get(row,"").lower().strip()
    p = prio_by_row.get(row, 1)
    qualif_counts[q] = qualif_counts.get(q,0) + 1
    blk = p in BLOQUE_PRIOS
    if blk:
        bloque += 1
    elif q in TRAITE:
        traite += 1
    if q in POSITIF and not blk:
        positif += 1

actif = total - bloque - traite

print(f"\n=== KPI REELS ===")
print(f"Total fiches    : {total:>8,}")
print(f"Traitées        : {traite:>8,}  ({traite/total*100:.1f}%)")
print(f"Positives       : {positif:>8,}  ({positif/total*100:.1f}%)")
print(f"Non traitées    : {total-traite:>8,}  ({(total-traite)/total*100:.1f}%)")
print(f"Bloquées        : {bloque:>8,}  ({bloque/total*100:.1f}%)")
print(f"Actives         : {actif:>8,}  ({actif/total*100:.1f}%)")

print(f"\n=== DISTRIBUTION QUALIF1 (réelle) ===")
for k,v in sorted(qualif_counts.items(), key=lambda x:-x[1])[:20]:
    print(f"  {v:6,}  '{k}'")

# Priorité distribution
prio_dist = {}
for p in prio_by_row.values():
    prio_dist[p] = prio_dist.get(p,0)+1
print(f"\n=== DISTRIBUTION PRIORITE ===")
for k,v in sorted(prio_dist.items()):
    flag = " <- BLOQUE" if k in BLOQUE_PRIOS else ""
    print(f"  priorite {k:5d} : {v:6,}{flag}")
