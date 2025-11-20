import pandas as pd

excel_file_path = "Tick Sightings.xlsx"
db = pd.read_excel(excel_file_path)

json_data = db.to_json(orient="records")

json_file_path = "data.json"
with open(json_file_path, 'w') as json_file:
    json_file.write(json_data)