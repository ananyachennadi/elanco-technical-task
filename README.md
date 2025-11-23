# Elanco Technical Task - Backend
A FastAPI backend that processes and serves tick sighting data for public health awareness. It allows users and veterinarians to filter, search, and analyse tick sightings based on location and time.

## Technologies
- **Python**: chosen for its simplicity and readability
- **FastAPI**: provides a fast and modern framework for building APIs in Python and automatically generates interactive API documentation
- **Pandas**: used for reading and preprocessing Excel data

## Project Outline

1. **Input** → Excel file with tick sighting data (`id`, `date`, `location`, `species`, `latinName`)

2. **Processing** → Clean data with pandas, remove duplicates, validate rows  
   - **Valid data** → `sightings.json`  
   - **Invalid data** → `invalid.json`

3. **API** → FastAPI serves cleaned data with endpoints for:  
   - Filtering by location, date range, or both  
   - Aggregating sightings by region  
   - Monthly and weekly trend analysis

4. **Output** → JSON responses via API (with interactive docs at `/docs`)

5. **Error Handling** → Invalid dates return 400 errors; malformed data returns 500 errors; bad rows logged to `invalid.json`

6. **Future** → Database integration, ML predictions, frontend dashboard

## Available Endpoints

| Endpoint | Description |
|---|---|
| `/location/{location}` | Get sightings filtered by location |
| `/time_range` | Filter sightings by optional start and end timestamps |
| `/location/{location}/time_range` | Combine location and date filters |
| `/sightings` | Get total sightings per region |
| `/trends/monthly` | Monthly aggregation of sightings |
| `/trends/weekly` | Weekly (ISO) aggregation of sightings |


## Running the project

### 1. Install Dependencies
Make sure you have Python 3.10 or higher installed.

Install the required dependencies using:

```bash
pip install -r requirements.txt
```

### 2. Prepare the Data

Then process the Excel file and generate JSON output:

```bash
python process_data.py
```

### 3. Start the FastAPI Server

Run the API using Uvicorn:

```bash
uvicorn main:app --reload
```

### 4. Access the API

Once the server is running:

- **API Home:**  
  [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

- **Interactive Swagger Docs:**  
  [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)


## Author

**Ananya Chennadi**
