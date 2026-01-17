import json
import random
from datetime import datetime, timedelta
from pathlib import Path

# =========================
# Paths
# =========================

RAW_DIR = Path("data/raw")

AIRPORTS_FILE = RAW_DIR / "airports.json"
FLIGHTS_FILE = RAW_DIR / "flights.json"
AIRCRAFT_FILE = RAW_DIR / "aircraft.json"
DELAYS_FILE = RAW_DIR / "airport_delays.json"

PAST_DAYS = 5
TOTAL_FLIGHTS = 400
TOTAL_AIRCRAFT = 25

# =========================
# Helpers
# =========================

def load_airports():
    with open(AIRPORTS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    iata_codes = []

    for a in data:
        # Case 1: direct "iata"
        if isinstance(a, dict):
            if "iata" in a and a["iata"]:
                iata_codes.append(a["iata"])

            # Case 2: nested codes -> iata
            elif "codes" in a and isinstance(a["codes"], dict):
                if a["codes"].get("iata"):
                    iata_codes.append(a["codes"]["iata"])

    # Deduplicate
    iata_codes = list(set(iata_codes))

    if len(iata_codes) < 2:
        raise ValueError("Not enough airport IATA codes found in airports.json")

    return iata_codes


def random_datetime_within_days(days):
    end = datetime.utcnow()
    start = end - timedelta(days=days)
    delta = end - start
    return start + timedelta(seconds=random.randint(0, int(delta.total_seconds())))

# =========================
# Aircraft Generation
# =========================

def generate_aircraft():
    manufacturers = ["Airbus", "Boeing"]
    models = {
        "Airbus": ["A320", "A321", "A330"],
        "Boeing": ["737-800", "737 MAX", "787"]
    }

    aircraft = []

    for i in range(TOTAL_AIRCRAFT):
        manufacturer = random.choice(manufacturers)
        model = random.choice(models[manufacturer])

        aircraft.append({
            "registration": f"VT-{random.randint(1000, 9999)}",
            "model": model,
            "manufacturer": manufacturer,
            "icao_type_code": model.replace("-", ""),
            "owner": random.choice(["IndiGo", "Air India", "Emirates", "Lufthansa"])
        })

    return aircraft

# =========================
# Flights Generation
# =========================

def generate_flights(airports, aircraft):
    statuses = ["On Time", "Delayed", "Cancelled"]
    airlines = ["AI", "6E", "EK", "LH", "AF"]

    flights = []

    for i in range(TOTAL_FLIGHTS):
        origin, destination = random.sample(airports, 2)
        aircraft_used = random.choice(aircraft)
        scheduled_dep = random_datetime_within_days(PAST_DAYS)
        scheduled_arr = scheduled_dep + timedelta(hours=random.randint(1, 10))

        status = random.choices(
            statuses,
            weights=[0.65, 0.25, 0.10],
            k=1
        )[0]

        actual_dep = scheduled_dep + timedelta(minutes=random.randint(5, 90)) if status == "Delayed" else scheduled_dep
        actual_arr = scheduled_arr + timedelta(minutes=random.randint(5, 90)) if status == "Delayed" else scheduled_arr

        if status == "Cancelled":
            actual_dep = None
            actual_arr = None

        flights.append({
            "flight_id": f"FL{i+1:05d}",
            "flight_number": f"{random.choice(airlines)}{random.randint(100, 9999)}",
            "aircraft_registration": aircraft_used["registration"],
            "origin_iata": origin,
            "destination_iata": destination,
            "scheduled_departure": scheduled_dep.isoformat(),
            "actual_departure": actual_dep.isoformat() if actual_dep else None,
            "scheduled_arrival": scheduled_arr.isoformat(),
            "actual_arrival": actual_arr.isoformat() if actual_arr else None,
            "status": status,
            "airline_code": random.choice(airlines)
        })

    return flights

# =========================
# Airport Delays Generation
# =========================

def generate_delays(airports):
    delays = []
    today = datetime.utcnow().date()

    for airport in airports:
        for d in range(PAST_DAYS):
            date = today - timedelta(days=d)
            total = random.randint(40, 120)
            delayed = random.randint(5, total // 2)

            delays.append({
                "airport_iata": airport,
                "delay_date": date.isoformat(),
                "total_flights": total,
                "delayed_flights": delayed,
                "avg_delay_min": random.randint(10, 60),
                "median_delay_min": random.randint(5, 45),
                "canceled_flights": random.randint(0, 10)
            })

    return delays

# =========================
# Main
# =========================

if __name__ == "__main__":
    print("==============================================")
    print(" Generating Dummy Aviation Data — STARTED ")
    print("==============================================")

    airports = load_airports()
    print(f"Loaded {len(airports)} airports")

    aircraft = generate_aircraft()
    flights = generate_flights(airports, aircraft)
    delays = generate_delays(airports)

    with open(AIRCRAFT_FILE, "w", encoding="utf-8") as f:
        json.dump(aircraft, f, indent=2)

    with open(FLIGHTS_FILE, "w", encoding="utf-8") as f:
        json.dump(flights, f, indent=2)

    with open(DELAYS_FILE, "w", encoding="utf-8") as f:
        json.dump(delays, f, indent=2)

    print("==============================================")
    print(" Dummy Data Generated Successfully ")
    print("==============================================")
    print(f"Aircraft: {len(aircraft)}")
    print(f"Flights: {len(flights)}")
    print(f"Airport Delay Records: {len(delays)}")
