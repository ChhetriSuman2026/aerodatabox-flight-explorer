import streamlit as st
import pandas as pd
import mysql.connector

from config.config import DB_CONFIG

# =========================
# Database Connection
# =========================

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


# =========================
# Page Setup
# =========================

st.set_page_config(page_title="AeroDataBox Flight Explorer", layout="wide")
st.title("✈️ AeroDataBox Flight Explorer")

st.markdown(
    "A simple application to explore airport, flight, and delay data "
    "extracted and processed from AeroDataBox."
)

# =========================
# Summary Metrics
# =========================

conn = get_connection()

airport_count = pd.read_sql("SELECT COUNT(*) AS cnt FROM airport", conn)["cnt"][0]
flight_count = pd.read_sql("SELECT COUNT(*) AS cnt FROM flights", conn)["cnt"][0]
avg_delay = pd.read_sql(
    "SELECT ROUND(AVG(avg_delay_min), 2) AS avg_delay FROM airport_delays", conn
)["avg_delay"][0]

col1, col2, col3 = st.columns(3)

col1.metric("Total Airports", airport_count)
col2.metric("Total Flights", flight_count)
col3.metric("Avg Delay (min)", avg_delay)

st.divider()

# =========================
# Filters
# =========================

airlines = pd.read_sql(
    "SELECT DISTINCT airline_code FROM flights ORDER BY airline_code", conn
)["airline_code"].tolist()

statuses = ["All", "On Time", "Delayed", "Cancelled"]

selected_airline = st.selectbox("Select Airline", ["All"] + airlines)
selected_status = st.selectbox("Select Flight Status", statuses)

# =========================
# Flights Table
# =========================

query = """
SELECT
    flight_number,
    airline_code,
    origin_iata,
    destination_iata,
    status,
    scheduled_departure
FROM flights
WHERE 1=1
"""

params = []

if selected_airline != "All":
    query += " AND airline_code = %s"
    params.append(selected_airline)

if selected_status != "All":
    query += " AND status = %s"
    params.append(selected_status)

query += " ORDER BY scheduled_departure DESC LIMIT 20"

flights_df = pd.read_sql(query, conn, params=params)

st.subheader("Recent Flights")
st.dataframe(flights_df, use_container_width=True)

st.divider()

# =========================
# Delay Analysis
# =========================

delay_df = pd.read_sql(
    """
    SELECT
        airport_iata,
        ROUND(
            SUM(delayed_flights) / SUM(total_flights) * 100, 2
        ) AS delay_percentage
    FROM airport_delays
    GROUP BY airport_iata
    ORDER BY delay_percentage DESC
    """,
    conn
)

st.subheader("Delay Percentage by Airport")
st.bar_chart(delay_df.set_index("airport_iata"))

conn.close()
