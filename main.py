from datetime import datetime
from fastapi import FastAPI, Query
from typing import Optional
import json

app = FastAPI()

def filter_by_location(location: str, data: list):
    location = location.capitalize()
    ticks_in_location = []

    for tick in data:
        if tick['location'] == location:
            ticks_in_location.append(tick)
    return ticks_in_location

def filter_by_time_range(
    start_datetime: str,
    end_datetime: str,
):
    try:
        start_dt = datetime.fromisoformat(start_datetime) if start_datetime else None
        end_dt = datetime.fromisoformat(end_datetime) if end_datetime else None
    except ValueError:
        return {"error": "invalid datetime format; use ISO format like 2023-05-01T12:30:00"}

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
    with open("sightings.json") as ticks:
        data = json.load(ticks)
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
    time_filtered_data = filter_by_time_range(start_datetime=start_datetime, end_datetime=end_datetime)
    return filter_by_location(location=location,data=time_filtered_data)

@app.get("/sightings")
def sightings_per_region():
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

@app.get("/trends/monthly")
def get_monthly_trends():
    with open("sightings.json") as ticks:
        data = json.load(ticks)
        monthly = {}

        for tick in data:
            ts_str = tick.get("datetime") or tick.get("timestamp") or tick.get("date")
            if not ts_str:
                continue
            try:
                ts = datetime.fromisoformat(ts_str)
            except ValueError:
                continue
            key = f"{ts.year}-{ts.month:02d}"
            monthly[key] = monthly.get(key, 0) + 1

        return monthly

@app.get("/trends/weekly")
def get_weekly_trends():
    with open("sightings.json") as ticks:
        data = json.load(ticks)
        weekly = {}

        for tick in data:
            ts_str = tick.get("datetime") or tick.get("timestamp") or tick.get("date")
            if not ts_str:
                continue
            try:
                ts = datetime.fromisoformat(ts_str)
            except ValueError:
                continue
            iso = ts.isocalendar()  # (year, week, weekday)
            key = f"{iso[0]}-W{iso[1]:02d}"
            weekly[key] = weekly.get(key, 0) + 1

        return weekly