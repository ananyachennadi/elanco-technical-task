from datetime import datetime
from fastapi import FastAPI, Query, HTTPException
from typing import Optional
import json

app = FastAPI()

def filter_by_location(location: str, data: list):
    """
    This function filters a list of tick sightings and returns only those reported in the specified location.

    Args:
        location (str): The location to filter by (case-insensitive)
        data (List[Dict]): A list of tick sightings, where each sighting is a dictionary

    Returns:
        List: A list of ticks reported in the specified location
    """

    location = location.capitalize()
    ticks_in_location = []

    for tick in data:
        if tick.get("location") == location:
            ticks_in_location.append(tick)
    return ticks_in_location

def filter_by_time_range(
    start_datetime: str,
    end_datetime: str,
):
    """
    This function filters a list of tick sightings and returns only those reported in the specified time range. If a time range is not specified then all tick sightings are returned. 

    Args:
        start_datetime (Optional[str]): Start date/time in ISO format (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS)
        end_datetime (Optional[str]): End date/time in ISO format

    Returns:
        List[Dict]: A list of dictionaries representing ticks reported in the specified location.
                    Returns an empty list if no sightings match the location.
    """

    try:
        start_dt = datetime.fromisoformat(start_datetime) if start_datetime else None
        end_dt = datetime.fromisoformat(end_datetime) if end_datetime else None
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid datetime format. Use ISO format like 2023-05-01T12:30:00"
        )

    with open("sightings.json") as ticks:
        data = json.load(ticks)
        results = []

        for tick in data:
            try:
                ts = datetime.fromisoformat(tick["date"])
            except ValueError:
                continue

            if start_dt and ts < start_dt:
                continue
            if end_dt and ts > end_dt:
                continue
            results.append(tick)

        return results

@app.get("/location/{location}")
def ticks_by_location(location: str):
    try:
        with open("sightings.json") as ticks:
            data = json.load(ticks)
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Data file not found")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Data file is invalid JSON")

    return filter_by_location(location=location, data=data)

@app.get("/time_range")
def ticks_by_time(
    start_datetime: Optional[str] = Query(None, description="start date/time in ISO format"),
    end_datetime: Optional[str] = Query(None, description="end date/time in ISO format"),
):
    return filter_by_time_range(start_datetime=start_datetime, end_datetime=end_datetime)

@app.get("/location/{location}/time_range")
def ticks_by_location_time(
    location: str,
    start_datetime: Optional[str] = Query(None, description="start date/time in ISO format"),
    end_datetime: Optional[str] = Query(None, description="end date/time in ISO format"),
):
    """
    Filters sightings by an optional time range.

    Args:
        start_datetime (Optional[str]): Start date/time in ISO format (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS)
        end_datetime (Optional[str]): End date/time in ISO format

    Returns:
        List[Dict]: List of sightings within the specified time range
    """
    time_filtered_data = filter_by_time_range(start_datetime=start_datetime, end_datetime=end_datetime)
    return filter_by_location(location=location,data=time_filtered_data)

@app.get("/sightings")
def sightings_per_region():
    """
    Returns the number of tick sightings per region.

    Reads the 'sightings.json' file and counts how many sightings
    occurred in each location. Location names are capitalized for
    consistency.

    Returns:
        dict: A dictionary where keys are location names (str) and
              values are the number of sightings (int).
        If the data cannot be loaded, an error dictionary is returned:
              {"error": "unable to load ticks data"}
    """

    with open("sightings.json") as ticks:
        data = json.load(ticks)
        sightings = {}

        for tick in data:
            location = tick["location"].capitalize()
            if location in sightings:
                sightings[location] += 1
                continue
            sightings[location] = 1
        
        return sightings
    return{"error": "unable to load ticks data"}

from fastapi import HTTPException

@app.get("/trends/monthly")
def get_monthly_trends():
    """
    Returns the number of tick sightings per month.

    Reads 'sightings.json' and counts sightings for each month.
    Invalid or missing dates are skipped.

    Returns:
        dict: Keys are months ('YYYY-MM'), values are counts of sightings.
    """
    try:
        with open("sightings.json") as ticks:
            data = json.load(ticks)
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Data file not found")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Data file is invalid JSON")

    monthly = {}
    for tick in data:
        ts_str = tick.get("date")
        try:
            ts = datetime.fromisoformat(ts_str)
        except (TypeError, ValueError):
            continue  # skip invalid or missing dates
        key = f"{ts.year}-{ts.month:02d}"
        monthly[key] = monthly.get(key, 0) + 1

    return dict(sorted(monthly.items()))

@app.get("/trends/weekly")
def get_weekly_trends():
    """
    Returns the number of tick sightings per ISO week.

    Reads 'sightings.json' and counts sightings for each week.
    Weeks are formatted as 'YYYY-Www'. Invalid or missing dates are skipped.

    Returns:
        dict: Keys are weeks ('YYYY-Www'), values are counts of sightings.
    """
    try:
        with open("sightings.json") as ticks:
            data = json.load(ticks)
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Data file not found")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Data file is invalid JSON")

    weekly = {}
    for tick in data:
        ts_str = tick.get("date")
        try:
            ts = datetime.fromisoformat(ts_str)
        except (TypeError, ValueError):
            continue  # skip invalid or missing dates
        iso = ts.isocalendar()
        key = f"{iso[0]}-W{iso[1]:02d}"
        weekly[key] = weekly.get(key, 0) + 1

    return dict(sorted(weekly.items()))