import json
from datetime import datetime
from pathlib import Path

from database.db_connection import get_db_connection

RAW_DIR = Path("data/raw")

AIRPORTS_FILE = RAW_DIR / "airports.json"
AIRCRAFT_FILE = RAW_DIR / "aircraft.json"
FLIGHTS_FILE = RAW_DIR / "flights.json"
DELAYS_FILE = RAW_DIR / "airport_delays.json"


# =========================
# Helpers
# =========================

def parse_datetime(value):
    if value is None:
        return None
    return datetime.fromisoformat(value)


def clear_tables(cursor):
    cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
    cursor.execute("TRUNCATE TABLE flights")
    cursor.execute("TRUNCATE TABLE aircraft")
    cursor.execute("TRUNCATE TABLE airport_delays")
    cursor.execute("TRUNCATE TABLE airport")
    cursor.execute("SET FOREIGN_KEY_CHECKS = 1")


# =========================
# Loaders
# =========================

def load_airports(cursor):
    with open(AIRPORTS_FILE, "r", encoding="utf-8") as f:
        airports = json.load(f)

    sql = """
        INSERT INTO airport (
            icao_code, iata_code, name, city, country,
            continent, latitude, longitude, timezone
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    for a in airports:
        # Extract nested values safely
        city = a.get("city", {})
        country = a.get("country", {})
        continent = a.get("continent", {})
        timezone = a.get("timezone", {})

        cursor.execute(sql, (
            a.get("icao"),
            a.get("iata") or a.get("iataCode") or a.get("codes", {}).get("iata"),
            a.get("name"),
            city.get("name") if isinstance(city, dict) else city,
            country.get("name") if isinstance(country, dict) else country,
            continent.get("name") if isinstance(continent, dict) else continent,
            a.get("location", {}).get("lat"),
            a.get("location", {}).get("lon"),
            timezone.get("name") if isinstance(timezone, dict) else timezone
        ))



def load_aircraft(cursor):
    with open(AIRCRAFT_FILE, "r", encoding="utf-8") as f:
        aircraft = json.load(f)

    sql = """
        INSERT INTO aircraft (
            registration, model, manufacturer, icao_type_code, owner
        )
        VALUES (%s, %s, %s, %s, %s)
    """

    for a in aircraft:
        cursor.execute(sql, (
            a["registration"],
            a["model"],
            a["manufacturer"],
            a["icao_type_code"],
            a["owner"]
        ))


def load_flights(cursor):
    with open(FLIGHTS_FILE, "r", encoding="utf-8") as f:
        flights = json.load(f)

    sql = """
        INSERT INTO flights (
            flight_id, flight_number, aircraft_registration,
            origin_iata, destination_iata,
            scheduled_departure, actual_departure,
            scheduled_arrival, actual_arrival,
            status, airline_code
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    for f in flights:
        cursor.execute(sql, (
            f["flight_id"],
            f["flight_number"],
            f["aircraft_registration"],
            f["origin_iata"],
            f["destination_iata"],
            parse_datetime(f["scheduled_departure"]),
            parse_datetime(f["actual_departure"]),
            parse_datetime(f["scheduled_arrival"]),
            parse_datetime(f["actual_arrival"]),
            f["status"],
            f["airline_code"]
        ))


def load_delays(cursor):
    with open(DELAYS_FILE, "r", encoding="utf-8") as f:
        delays = json.load(f)

    sql = """
        INSERT INTO airport_delays (
            airport_iata, delay_date, total_flights,
            delayed_flights, avg_delay_min,
            median_delay_min, canceled_flights
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    for d in delays:
        cursor.execute(sql, (
            d["airport_iata"],
            d["delay_date"],
            d["total_flights"],
            d["delayed_flights"],
            d["avg_delay_min"],
            d["median_delay_min"],
            d["canceled_flights"]
        ))


# =========================
# Main
# =========================

if __name__ == "__main__":
    print("==============================================")
    print(" ETL: CLEAR + LOAD — STARTED ")
    print("==============================================")

    conn = get_db_connection()
    cursor = conn.cursor()

    clear_tables(cursor)
    print("Tables cleared")

    load_airports(cursor)
    print("Airports loaded")

    load_aircraft(cursor)
    print("Aircraft loaded")

    load_flights(cursor)
    print("Flights loaded")

    load_delays(cursor)
    print("Airport delays loaded")

    conn.commit()
    cursor.close()
    conn.close()

    print("==============================================")
    print(" ETL COMPLETED SUCCESSFULLY ")
    print("==============================================")
