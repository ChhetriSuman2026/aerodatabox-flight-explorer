import requests
import json
import time
from datetime import datetime, timedelta

from config.config import API_CONFIG

# =========================
# Configuration
# =========================

BASE_URL = f"https://{API_CONFIG['host']}"

HEADERS = {
    "x-rapidapi-key": API_CONFIG["key"],
    "x-rapidapi-host": API_CONFIG["host"]
}

AIRPORT_IATA_CODES = [
    "DEL", "BOM", "BLR", "HYD", "MAA",
    "DXB", "LHR", "JFK", "SIN", "CDG",
    "FRA", "HKG"
]

PAST_DAYS = 5

RAW_DATA_PATHS = {
    "airports": "data/raw/airports.json",
    "flights": "data/raw/flights.json"
}


# =========================
# Helper Functions
# =========================

def save_json(filepath, data):
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"Saved → {filepath}")


# =========================
# Fetch Airport Data
# =========================

def fetch_airport_data():
    print("Fetching airport data...")
    airports = []

    for code in AIRPORT_IATA_CODES:
        print(f"Fetching airport info for {code}...")
        url = f"{BASE_URL}/airports/iata/{code}"
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        airports.append(response.json())
        time.sleep(1)  # controlled batching

    return airports


# =========================
# Fetch Flights Data (Arrivals + Departures)
# =========================

def fetch_flights():
    print("Fetching flight data (recent arrivals & departures)...")
    all_flights = []

    params = {
        "withDelays": "true",
        "limit": 100
    }

    for code in AIRPORT_IATA_CODES:
        for flight_type in ["departures", "arrivals"]:
            print(f"Fetching {flight_type} for {code}...")
            url = f"{BASE_URL}/flights/airports/iata/{code}/{flight_type}"
            response = requests.get(url, headers=HEADERS, params=params)
            response.raise_for_status()

            all_flights.append({
                "airport": code,
                "type": flight_type,
                "data": response.json()
            })

            time.sleep(1)

    return all_flights


# =========================
# Main Execution
# =========================

if __name__ == "__main__":
    print("==============================================")
    print(" AeroDataBox One-Time Data Fetch — STARTED ")
    print("==============================================")

    airports_data = fetch_airport_data()
    save_json(RAW_DATA_PATHS["airports"], airports_data)

    flights_data = fetch_flights()
    save_json(RAW_DATA_PATHS["flights"], flights_data)

    print("==============================================")
    print(" DATA DOWNLOAD COMPLETED SUCCESSFULLY ")
    print("==============================================")
