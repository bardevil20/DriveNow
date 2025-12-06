# DriveNow API

Car rental management REST API built with Flask using a layered architecture.

## Architecture

```
├── app.py                  # Application entry point & database initialization
├── config.py               # Configuration (MySQL, environment variables)
├── core/                   # Core utilities
│   ├── __init__.py         # Logging setup
│   └── exceptions.py       # Custom exceptions (NotFoundError, ValidationError, etc.)
├── models/                 # SQLAlchemy database models
│   ├── cars.py             # Car model with status enum
│   └── rentals.py          # Rental model with car relationship
├── repositories/           # Data access layer (database queries only)
│   ├── car_repository.py   # Car CRUD operations
│   └── rental_repository.py # Rental CRUD operations
├── services/               # Business logic layer
│   ├── car_service.py      # Car business logic & validation
│   └── rental_service.py   # Rental business logic & validation
└── routes/                 # API endpoints (request/response handling)
    ├── car_routes.py       # Car API endpoints
    └── rentals_routes.py   # Rental API endpoints
```

## Tech Stack

- **Flask** - Web framework
- **Flask-SQLAlchemy** - ORM for database operations
- **MySQL** - Database
- **python-dotenv** - Environment variable management

## Setup

```bash
# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Configure environment (copy and edit .env.example)
copy .env.example .env  # Windows
cp .env.example .env    # Linux/Mac

# Run application (auto-creates database and tables)
python app.py
```

The application automatically creates the database and tables on startup if they don't exist.

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `MYSQL_HOST` | localhost | MySQL host |
| `MYSQL_PORT` | 3306 | MySQL port |
| `MYSQL_USER` | root | MySQL username |
| `MYSQL_PASSWORD` | - | MySQL password |
| `MYSQL_DATABASE` | drivenow | Database name |
| `LOG_LEVEL` | INFO | Logging level |

## API Endpoints

### Cars

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/cars` | Create a new car |
| GET | `/api/cars/get_cars` | List all cars |
| GET | `/api/cars/<id>` | Get car by ID |
| PUT | `/api/cars/<id>/status` | Update car status |
| DELETE | `/api/cars/<id>` | Delete car (completes active rental) |

### Rentals

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/rentals/register` | Register a new rental |
| GET | `/api/rentals/get_rentals` | List all rentals |
| GET | `/api/rentals/<id>` | Get rental by ID |
| PUT | `/api/rentals/<id>/end` | End/complete a rental |
| DELETE | `/api/rentals/<id>` | Delete rental |

### Car Statuses

- `AVAILABLE` - Car is available for rental
- `IN_USE` - Car is currently rented
- `UNDER_MAINTENANCE` - Car is under maintenance

## API Examples

```bash
# Create a car
curl -X POST http://localhost:5000/api/cars \
  -H "Content-Type: application/json" \
  -d '{"model": "Toyota Camry", "year": "2023"}'

# Get all cars
curl http://localhost:5000/api/cars/get_cars

# Update car status
curl -X PUT http://localhost:5000/api/cars/1/status \
  -H "Content-Type: application/json" \
  -d '{"status": "AVAILABLE"}'

# Register a rental
curl -X POST http://localhost:5000/api/rentals/register \
  -H "Content-Type: application/json" \
  -d '{"car_id": "1", "customer_name": "John Doe", "start_date": "20241206", "end_date": "20241210"}'

# End a rental
curl -X PUT http://localhost:5000/api/rentals/1/end

# Get all rentals
curl http://localhost:5000/api/rentals/get_rentals
```

## HTTP Status Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 201 | Created |
| 400 | Bad request / Validation error |
| 404 | Resource not found |

## Error Response Format

```json
{
  "error": "Error message description"
}
```
