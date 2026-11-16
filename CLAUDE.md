# Macro Tracker – working notes

## "Add X to food database" (frequent request)
1. Read the nutrition label image: serving size/unit, protein, carbs, fats, fiber, calories.
2. Append a row to `new-foods-import.csv` (columns: name,servingAmount,servingUnit,protein,carbs,fats,fiber,calories,customCalories,pieceGrams).
   - Set `customCalories` to true when label calories differ from 4P+4C+9F.
   - `pieceGrams` only for countable items (1 tortilla, 1 kiwi); leave blank otherwise.
   - Check the CSV first; don't add duplicates (import matches by name, case-insensitive, and updates).
3. Commit and push. Push to `main` only when the user says so.
4. Editing the CSV does NOT add the food to the app. Foods live in the user's Firebase
   (keyed by their 4-digit PIN) and localStorage. The user must tap Food Database -> Import
   in the app and pick the CSV (it upserts by name). Always tell them this explicitly.
   Writing to Firebase directly needs their PIN and a read-merge-write
   (`set()` replaces the whole object), so ask before doing that.
