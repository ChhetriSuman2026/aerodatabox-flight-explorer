# AeroDataBox Flight Explorer

## Project Overview
AeroDataBox Flight Explorer is an end-to-end aviation data analytics application built using Python, MySQL, and Streamlit.  
The project demonstrates how raw aviation data can be transformed into structured relational tables, analyzed using SQL, and visualized through an interactive web application.

This project focuses on **data engineering fundamentals** such as ETL pipelines, database design, and SQL analytics rather than UI complexity.

---

## Objectives
- Extract and structure aviation-related data
- Design a normalized relational database schema
- Implement a complete ETL (Extract–Transform–Load) pipeline
- Perform analytical SQL queries on flight operations
- Visualize insights using a Streamlit dashboard

---

## Tech Stack
- **Language:** Python  
- **Database:** MySQL  
- **ETL & Analysis:** Python, Pandas  
- **Visualization:** Streamlit  
- **API Source:** AeroDataBox (airport metadata)

---

## Project Structure
```
aerodatabox-flight-explorer/
├── app.py
├── config/
├── database/
├── etl/
├── scripts/
├── data/
│   └── raw/
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Database Design
The database consists of four normalized tables:
- airport
- aircraft
- flights
- airport_delays

This structure avoids redundancy and supports efficient analytical queries.

---

## Data Strategy
Due to API access limitations, airport metadata was fetched from the AeroDataBox API, while flight, aircraft and delay data were generated synthetically to simulate realistic aviation operations over the last 5 days.

All datasets are stored locally in `data/raw/` for offline and reproducible execution.

---

## ETL Pipeline
- **Extract:** Load raw JSON files from `data/raw/`
- **Transform:** Flatten nested fields and convert timestamps
- **Load:** Clear-and-load strategy for idempotent execution

---

## SQL Analysis
The project includes analytical queries such as:
- Flight counts by aircraft model
- Busiest origin and destination airports
- Domestic vs international flight classification
- Delay percentage analysis by airport

---

## Streamlit Application
The Streamlit app provides:
- Summary metrics
- Flight filtering
- Delay analysis visualizations
- SQL-backed tables and charts

---

## How to Run

```Python
pip install -r requirements.txt
python -m etl.load
streamlit run app.py
```

---

## Challenges Faced
- API access limitations
- JSON to SQL data type issues
- SQL keyword conflicts
- Git repository structure corrections

---

## Key Learnings
- Importance of schema design
- ETL pipeline reliability
- SQL analytical thinking
- Clean project structuring

---

## Conclusion
This project demonstrates a complete data workflow from raw aviation data to structured insights, focusing on correctness, modularity and reproducibility.