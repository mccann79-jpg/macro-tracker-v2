#!/usr/bin/env python3
"""Upsert foods from new-foods-import.csv straight into the app's Firebase DB.

Usage: python3 import-foods.py [--pin 6625] [--csv new-foods-import.csv] [--dry-run]

Mirrors the app's Import button (upsert by case-insensitive name, keep existing id,
blank CSV cells don't overwrite) but writes only foodDatabase, _counts/foodDatabase
and _lastSync, so no other data is touched. The cloud record is backed up to
backups_<pin>/pre-import-<timestamp> first. Open apps pick the change up live.
"""
import argparse, csv, json, time, urllib.request

BASE = "https://macro-tracker-v2-default-rtdb.firebaseio.com"
NUM = {"servingAmount", "protein", "carbs", "fats", "fiber", "calories"}
NUM_NULL = {"density", "volEqAmount", "volEqGrams", "pieceGrams"}

def call(method, path, body=None):
    req = urllib.request.Request(f"{BASE}/{path}.json", method=method,
        data=None if body is None else json.dumps(body).encode(),
        headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)

def num(v):
    try: return float(v)
    except ValueError: return 0

def clean(n):
    return int(n) if float(n).is_integer() else n

def parse_row(row):
    f = {}
    for k, v in row.items():
        v = (v or "").strip()
        if not k or v == "": continue
        if k == "id": f[k] = int(num(v))
        elif k in NUM: f[k] = clean(num(v))
        elif k in NUM_NULL:
            if num(v): f[k] = clean(num(v))
        elif k == "customCalories": f[k] = v.lower() in ("true", "1")
        else: f[k] = v
    return f

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pin", default="6625")
    ap.add_argument("--csv", default="new-foods-import.csv")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    with open(a.csv, newline="") as fh:
        incoming = [parse_row(r) for r in csv.DictReader(fh)]
    incoming = [f for f in incoming if f.get("name") and f.get("servingAmount") and f.get("servingUnit")]
    if not incoming: raise SystemExit("No valid rows in CSV")

    data = call("GET", a.pin) or {}
    foods = data.get("foodDatabase") or []
    if isinstance(foods, dict): foods = [v for v in foods.values() if v]
    print(f"Cloud has {len(foods)} foods; importing {len(incoming)} from CSV")

    ts = int(time.time() * 1000)
    max_id = max([f.get("id", 0) for f in foods] + [ts])
    added = updated = 0
    for nf in incoming:
        for k in ("protein", "carbs", "fats", "fiber"): nf.setdefault(k, 0)
        if not nf.get("calories"):
            nf["calories"] = clean(nf["protein"]*4 + nf["carbs"]*4 + nf["fats"]*9)
            nf["customCalories"] = False
        ex = next((f for f in foods if f.get("name", "").strip().lower() == nf["name"].lower()), None)
        if ex:
            keep = ex.get("id"); ex.update(nf); ex["id"] = keep; updated += 1
        else:
            max_id += 1; nf["id"] = max_id; foods.append(nf); added += 1
    print(f"Added {added}, updated {updated}, total {len(foods)}")
    if a.dry_run: return print("Dry run - nothing written")

    call("PUT", f"backups_{a.pin}/pre-import-{ts}", data)
    call("PATCH", a.pin, {"foodDatabase": foods, "_counts/foodDatabase": len(foods), "_lastSync": ts})
    after = call("GET", f"{a.pin}/foodDatabase") or []
    names = {f.get("name") for f in after if f}
    missing = [f["name"] for f in incoming if f["name"] not in names]
    if missing: raise SystemExit(f"VERIFY FAILED, missing: {missing}")
    print(f"Verified: all {len(incoming)} foods present in cloud ({len(after)} total)")

main()
