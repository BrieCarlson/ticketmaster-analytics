# Ticketmaster Event Analytics

An automated data analytics pipeline that collects Ticketmaster event data across six states, transforms and loads the data into PostgreSQL, maintains historical event snapshots, and exports analysis data for visualization in Tableau Public.

## Interactive Dashboard

[![Ticketmaster Event Analytics Dashboard](docs/dashboard-preview.png)](https://public.tableau.com/views/TicketmasterEventAnalytics/Dashboard1?:showVizHome=no)

**[View the Interactive Dashboard on Tableau Public](https://public.tableau.com/views/TicketmasterEventAnalytics/Dashboard1?:showVizHome=no)**

## Project Overview

This project uses the Ticketmaster Discovery API to collect event data across Ohio, Michigan, Indiana, Kentucky, Pennsylvania, and West Virginia. The data is processed through a Python ETL pipeline, stored in a PostgreSQL database, and maintained through historical daily snapshots to track changes in event availability and details over time.

The project includes SQL analysis and an interactive Tableau Public dashboard that explores event trends by state, segment, month, city, and venue. The pipeline is also configured to run automatically on a daily schedule using Windows Task Scheduler.

## Technologies & Tools

- Python
- PostgreSQL
- SQL
- Pandas
- Requests
- Ticketmaster Discovery API
- Tableau Public
- Git & GitHub
- Windows Task Scheduler

## Data Pipeline

1. **Extract** - Collect event data from the Ticketmaster Discovery API across six states.
2. **Transform** - Clean and structure the raw JSON data using Python and Pandas.
3. **Load** - Store current event data and historical daily snapshots in PostgreSQL.
4. **Analyze** - Use SQL to analyze event trends, locations, venues, categories, and pricing.
5. **Export** - Generate a CSV dataset for Tableau visualization.
6. **Visualize** - Present the analysis through an interactive Tableau Public dashboard.
7. **Automate** - Run the complete pipeline on a daily schedule using Windows Task Scheduler.

## Key Features

- Automated API data collection
- Python-based ETL pipeline
- PostgreSQL relational database
- Historical daily event snapshots
- SQL-based data analysis
- Data cleaning and duplicate handling
- Interactive Tableau Public dashboard
- Automated daily pipeline execution
