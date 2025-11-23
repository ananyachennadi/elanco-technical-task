# uses pandas to read an Excel file, remove duplicates and validate rows and store them in two json files:
# sightings.json (valid data)
# invalid.json (invalid rows for future debugging)

import pandas as pd
import json

excel_file_path = "Tick Sightings.xlsx"
df = pd.read_excel(excel_file_path)

df = df.drop_duplicates()

data = df.to_dict(orient="records")

valid = []
invalid = []

for row in data:
    errors = []

    if "id" not in row:
        errors.append("missing id")
    if "date" not in row:
        errors.append("missing date")
    if "location" not in row:
        errors.append("missing location")
    if "species" not in row:
        errors.append("missing species")
    if "latinName" not in row:
        errors.append("missing latinName")
    
    if len(errors) != 0:
        row["errors"] = errors
        invalid.append(row)
    else:
        valid.append(row)

with open("sightings.json", "w") as f:
    json.dump(valid, f, indent=2)

with open("invalid.json", "w") as f:
    json.dump(invalid, f, indent=2)