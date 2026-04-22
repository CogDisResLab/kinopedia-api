# Kinopedia API

Backend API for kinase database built with FastAPI.

## Features

-  RESTful API for kinase data
-  8 kinases with ~15,000 substrates from KEA3
-  Automatic API documentation (Swagger UI)
-  Business logic enforcement (STK33 pseudokinase, CASK disputed status)
-  Docker deployment ready
-  70%+ test coverage

## Quick Start

### Local Development

```cmd
# Clone repository
git clone https://github.com/CogDisResLab/kinopedia-api
cd kinopedia-api

# Create virtual environment
py -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run server
uvicorn app.main:app --reload
```

Visit http://localhost:8000/docs for interactive API documentation.

### Docker

```cmd
# Build image
docker build -t kinopedia-api .

# Run container
docker run -p 8000:8000 kinopedia-api
```

\### Using Docker Compose

```cmd

docker-compose up

```


Visit: http://localhost:8000/docs



\*\*Note:\*\* Docker files are included and tested. Windows users may need to run Docker Desktop as Administrator.



\### Without Docker



If Docker is not available, you can run directly:



```cmd

py -m venv venv

venv\\Scripts\\activate

pip install -r requirements.txt

uvicorn app.main:app --reload

```


## API Endpoints

### Kinases
- `GET /kinases/` - List all kinases (with optional filtering)
- `GET /kinases/{id}` - Get kinase details with substrate counts
- `GET /kinases/{id}/substrates` - Get all substrates for a kinase
- `GET /kinases/{id}/conflicts` - Get documented data conflicts

### Substrates
- `POST /substrates/` - Add new substrate annotation (with validation)

### Structures
- `GET /structures/pdb/{pdb_id}` - Get PDB experimental structure
- `GET /structures/alphafold/{protein_id}` - Get AlphaFold predicted model

## Business Logic

### STK33 Pseudokinase Enforcement
STK33 is a confirmed catalytically inactive pseudokinase. Attempts to add 
substrates via POST will return `403 Forbidden` with message:
"Catalytically inactive pseudokinase cannot have functional substrates."

### CASK Disputed Activity
CASK kinase activity status is disputed in the literature. GET requests 
include special metadata fields:
- `status`: "disputed_activity"
- `note`: "Literature contains conflicting reports on catalytic activity."

## Testing

```cmd
# Run all tests
pytest tests\ -v

# Run with coverage
pytest tests\ --cov=app --cov-report=term-missing
```

Current coverage: 88%

## Database

Currently uses SQLite (`kinopedia.db`) for simplicity and portability.

For PostgreSQL setup in production, see [POSTGRESQL_SETUP.md](POSTGRESQL_SETUP.md).

##  Project Structure

kinopedia-api/
├── app/
│   ├── main.py              # FastAPI application
│   ├── database.py          # Database connection (async)
│   ├── models.py            # SQLAlchemy ORM models
│   ├── schemas.py           # Pydantic validation schemas
│   └── routers/
│       ├── kinases.py       # Kinase endpoints
│       ├── substrates.py    # Substrate endpoints
│       └── structures.py    # Structure endpoints
├── tests/                   # Unit tests (pytest)
├── kinopedia.db             # SQLite database
├── Dockerfile               # Docker configuration
├── docker-compose.yml       # Docker Compose setup
├── requirements.txt         # Python dependencies
└── README.md                # This file

## Technology Stack

- **Framework:** FastAPI 0.110+
- **ORM:** SQLAlchemy 2.0 (async)
- **Database:** SQLite (aiosqlite driver)
- **Validation:** Pydantic v2
- **Testing:** pytest + pytest-asyncio
- **Python:** 3.12+

## Development

**Created by:** Sakshi Dhumma  
**Date:** April 2026  
**Version:** 1.0.0

Based on trial assignment database with 8 curated kinases:
AKT1, CDK1, MAPK1, EGFR, SRC, CAMK2A, CASK, STK33

## License

This project is for academic/research purposes.
