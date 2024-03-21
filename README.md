# Gemini Flights Manager

## Overview
Gemini Flights Manager is a backend system built using FastAPI, aimed at managing and simulating flight-related operations. This system offers a robust platform for handling various aspects of flight management, including flight generation, search, and booking functionalities.

The project utilizes FastAPI's efficient framework to create a high-performance, scalable solution suitable for flight data management. It comes with an SQLite database (flights.db) pre-populated with initial data, facilitating quick deployment and testing.

## Key Features:
- Advanced search capabilities for querying flights based on criteria like origin, destination, and dates.
- Booking system handling seat availability across different classes and calculating costs accordingly.


## Project Purpose and Methodology:
The goal of this project is to provide a seamless and intuitive flight management system that simplifies the traditionally complex flight booking process. By leveraging advanced AI technology, Gemini Flights Manager enables users to search and book flights effortlessly through a conversational interface. The system integrates with Google's Gemini model to offer personalized recommendations and real-time flight management capabilities.

## Methodology Highlights:
- Utilization of FastAPI for building a robust backend system.
- Integration with Google's Gemini model for advanced AI capabilities.
- Pre-populated SQLite database for quick deployment and testing.

**Note:** For Gemini Function Calling, only the search_flights and book_flight functions are required.


## Installation
### Prerequisites
Before starting, ensure you have the following installed on your system:

- Python 3.6 or higher
- FastAPI
- Uvicorn (ASGI server for FastAPI)

## Step-by-Step Installation Guide
1. Clone the Repository

``` bash
git clone https://github.com/your-username/your-repository.git
cd your-repository
```

2. Set Up a Virtual Environment (Optional but recommended)

```bash
virtualenv venv
source venv/bin/activate
```

3. Install Dependencies

``` bash
pip install -r requirements.txt
```

4. Starting the FastAPI Server

```bash
uvicorn main:app
```

## Accessing the API
Once the server is running, access the API at http://127.0.0.1:8000.

For interactive API documentation, visit http://127.0.0.1:8000/docs, where you can test the API endpoints directly from your browser.
