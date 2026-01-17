-- =========================
-- AeroDataBox Flight Explorer
-- Database Schema
-- =========================

-- Airport table
CREATE TABLE IF NOT EXISTS airport (
    airport_id INT AUTO_INCREMENT PRIMARY KEY,
    icao_code VARCHAR(10) UNIQUE,
    iata_code VARCHAR(10) UNIQUE,
    name VARCHAR(255),
    city VARCHAR(100),
    country VARCHAR(100),
    continent VARCHAR(50),
    latitude DECIMAL(9,6),
    longitude DECIMAL(9,6),
    timezone VARCHAR(50)
);

-- Aircraft table
CREATE TABLE IF NOT EXISTS aircraft (
    aircraft_id INT AUTO_INCREMENT PRIMARY KEY,
    registration VARCHAR(20) UNIQUE,
    model VARCHAR(100),
    manufacturer VARCHAR(100),
    icao_type_code VARCHAR(20),
    owner VARCHAR(100)
);

-- Flights table
CREATE TABLE IF NOT EXISTS flights (
    flight_id VARCHAR(50) PRIMARY KEY,
    flight_number VARCHAR(20),
    aircraft_registration VARCHAR(20),
    origin_iata VARCHAR(10),
    destination_iata VARCHAR(10),
    scheduled_departure DATETIME,
    actual_departure DATETIME,
    scheduled_arrival DATETIME,
    actual_arrival DATETIME,
    status VARCHAR(50),
    airline_code VARCHAR(10)
);

-- Airport delays table
CREATE TABLE IF NOT EXISTS airport_delays (
    delay_id INT AUTO_INCREMENT PRIMARY KEY,
    airport_iata VARCHAR(10),
    delay_date DATE,
    total_flights INT,
    delayed_flights INT,
    avg_delay_min INT,
    median_delay_min INT,
    canceled_flights INT
);

-- =========================
-- Indexes for Performance
-- =========================

CREATE INDEX idx_flights_origin ON flights(origin_iata);
CREATE INDEX idx_flights_destination ON flights(destination_iata);
CREATE INDEX idx_flights_status ON flights(status);
CREATE INDEX idx_flights_airline ON flights(airline_code);

CREATE INDEX idx_airport_iata ON airport(iata_code);
CREATE INDEX idx_aircraft_registration ON aircraft(registration);
CREATE INDEX idx_delay_airport_date ON airport_delays(airport_iata, delay_date);
