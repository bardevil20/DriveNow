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

### Request Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              CLIENT REQUEST                                  │
│                          (HTTP: GET, POST, PUT, DELETE)                     │
└─────────────────────────────────┬───────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              ROUTES (API)                                    │
│  ┌─────────────────────────┐    ┌─────────────────────────────┐             │
│  │     car_routes.py       │    │    rentals_routes.py        │             │
│  ├─────────────────────────┤    ├─────────────────────────────┤             │
│  │ • Parse request JSON    │    │ • Parse request JSON        │             │
│  │ • Validate required     │    │ • Validate required         │             │
│  │   fields exist          │    │   fields exist              │             │
│  │ • Return HTTP response  │    │ • Return HTTP response      │             │
│  │ • Handle exceptions     │    │ • Handle exceptions         │             │
│  └─────────────────────────┘    └─────────────────────────────┘             │
└─────────────────────────────────┬───────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              SERVICES                                        │
│  ┌─────────────────────────┐    ┌─────────────────────────────┐             │
│  │    car_service.py       │◄──►│    rental_service.py        │             │
│  ├─────────────────────────┤    ├─────────────────────────────┤             │
│  │ • Business logic        │    │ • Business logic            │             │
│  │ • Data validation       │    │ • Data validation           │             │
│  │ • Status management     │    │ • Date validation           │             │
│  │ • Cross-service calls   │    │ • Car availability check    │             │
│  │ • Raise custom errors   │    │ • Raise custom errors       │             │
│  └─────────────────────────┘    └─────────────────────────────┘             │
└─────────────────────────────────┬───────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                            REPOSITORIES                                      │
│  ┌─────────────────────────┐    ┌─────────────────────────────┐             │
│  │  car_repository.py      │    │  rental_repository.py       │             │
│  ├─────────────────────────┤    ├─────────────────────────────┤             │
│  │ • CRUD operations       │    │ • CRUD operations           │             │
│  │ • Database queries      │    │ • Database queries          │             │
│  │ • No business logic     │    │ • No business logic         │             │
│  └─────────────────────────┘    └─────────────────────────────┘             │
└─────────────────────────────────┬───────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              MODELS                                          │
│  ┌─────────────────────────┐    ┌─────────────────────────────┐             │
│  │      cars.py            │    │      rentals.py             │             │
│  ├─────────────────────────┤    ├─────────────────────────────┤             │
│  │ • SQLAlchemy model      │    │ • SQLAlchemy model          │             │
│  │ • CarStatus enum        │◄───│ • Foreign key to Car        │             │
│  │ • to_dict() method      │    │ • to_dict() method          │             │
│  └─────────────────────────┘    └─────────────────────────────┘             │
└─────────────────────────────────┬───────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                          MySQL DATABASE                                      │
│  ┌─────────────────────────┐    ┌─────────────────────────────┐             │
│  │      cars table         │    │      rentals table          │             │
│  ├─────────────────────────┤    ├─────────────────────────────┤             │
│  │ id (PK)                 │◄───│ car_id (FK)                 │             │
│  │ model                   │    │ rental_id (PK)              │             │
│  │ year                    │    │ customer_name               │             │
│  │ status                  │    │ start_date / end_date       │             │
│  │ created_at              │    │ completed                   │             │
│  └─────────────────────────┘    └─────────────────────────────┘             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Layer Responsibilities

| Layer | Responsibility |
|-------|----------------|
| **Routes** | HTTP handling, request parsing, response formatting |
| **Services** | Business logic, validation, cross-entity operations |
| **Repositories** | Database CRUD operations only |
| **Models** | Data structure definitions, ORM mapping |

## Tech Stack

- **Flask** - Web framework
- **Flask-SQLAlchemy** - ORM for database operations
- **MySQL** - Database
- **Docker** - Containerization (optional)
- **python-dotenv** - Environment variable management
- **pytest** - Testing framework

* MySQL databes was selected because due to the relationships between rentals and cars (and assuming scaling and extending db with more tables like customers and etc. with other relationships between tables), and the constant scheme of tables - relational DB is best for this case

## Setup

### Option 1: Docker (Recommended)

Run the entire application with one command - no need to install Python or MySQL locally.

```bash
# Configure environment (set your password)
copy .env.example .env  # Windows
cp .env.example .env    # Linux/Mac
# Edit .env and set MYSQL_PASSWORD

# Start application + database
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down

# Stop and remove data
docker-compose down -v
```

The app will be available at `http://localhost:5000`

### Option 2: Manual Setup

Requires Python and MySQL installed locally.

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
| `MYSQL_HOST` | localhost | MySQL host (use `db` for Docker) |
| `MYSQL_PORT` | 3306 | MySQL port |
| `MYSQL_USER` | root / drivenow | MySQL username |
| `MYSQL_PASSWORD` | **required** | MySQL password |
| `MYSQL_DATABASE` | drivenow | Database name |
| `MYSQL_ROOT_PASSWORD` | root123 | MySQL root password (Docker only) |
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

## Testing

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_car_service.py

# Run specific test class
pytest tests/test_car_service.py::TestCarServiceCreateCar

# Run with coverage (requires pytest-cov)
pytest --cov=.
```

### Test Structure

```
tests/
├── conftest.py              # Shared fixtures
├── test_car_service.py      # CarService unit tests
├── test_rental_service.py   # RentalService unit tests
├── test_car_routes.py       # Car API endpoint tests
└── test_rental_routes.py    # Rental API endpoint tests
```

- **Service tests**: Mock repositories, test business logic
- **Route tests**: Mock services, test HTTP status codes

## Error Response Format

```json
{
  "error": "Error message description"
}
```
