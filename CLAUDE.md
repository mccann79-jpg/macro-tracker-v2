# Macro Tracker – working notes

## "Add X to food database" (frequent request)
1. Read the nutrition label image: serving size/unit, protein, carbs, fats, fiber, calories.
2. Append a row to `new-foods-import.csv` (columns: name,servingAmount,servingUnit,protein,carbs,fats,fiber,calories,customCalories,pieceGrams).
   - Set `customCalories` to true when label calories differ from 4P+4C+9F.
   - `pieceGrams` only for countable items (1 tortilla, 1 kiwi); leave blank otherwise.
   - Check the CSV first; don't add duplicates (import matches by name, case-insensitive, and updates).
3. Commit and push. Push to `main` only when the user says so.
4. Import it yourself, never hand the user a CSV to import:
   `python3 import-foods.py` (PIN defaults to 6625; `--dry-run` previews).
   It upserts by name into the user's Firebase foodDatabase via REST, touching only
   foodDatabase/_counts/_lastSync, backs up the cloud record to `backups_<pin>/pre-import-<ts>`,
   and verifies the foods landed. Open apps pick it up live.
   Requires the host `macro-tracker-v2-default-rtdb.firebaseio.com` in the environment's
   allowed network hosts (already added to the Default environment; if the request gets a
   403 proxy error, re-add it with update_environment).
5. Tell the user it's done and in the app. Re-running is safe (upsert by name).
