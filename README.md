# IndexFlora API

A high-performance search engine API built with FastAPI, Redis Stack (RediSearch), and MySQL. IndexFlora provides full-text search capabilities with schema-based document indexing and real-time search functionality.

## Features

- **Schema-based Search**: Define custom search schemas with different field types (text, numeric, tag)
- **High-Performance Indexing**: Bulk document indexing with Redis Stack
- **Real-time Search**: Fast full-text search with scoring and pagination
- **Search Analytics**: Built-in search logging and performance monitoring
- **RESTful API**: Clean, well-documented REST endpoints
- **Docker Support**: Easy deployment with Docker Compose
- **Comprehensive Testing**: Integration tests with performance benchmarks

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   FastAPI App   │────│   MySQL DB      │    │   Redis Stack   │
│                 │    │                 │    │                 │
│ • Schema Mgmt   │    │ • Schema Defs   │    │ • Search Index  │
│ • Document API  │    │ • Search Logs   │    │ • Document Store│
│ • Search API    │    │                 │    │ • Full-text     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Prerequisites

- Docker and Docker Compose
- Python 3.11+ (for local development)
- MySQL 8.0+ (if running locally)
- Redis Stack (if running locally)

## Quick Start

### Using Docker (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd indexflora-api
   ```

2. **Start the services**
   ```bash
   docker-compose up -d
   ```

3. **Initialize the database**
   ```bash
   # Connect to MySQL and run the initialization script
   mysql -h localhost -P 3306 -u root -p < sql/001_init_search_engine.sql
   ```

4. **Access the API**
   - API: http://localhost:8400
   - API Documentation: http://localhost:8400/docs
   - Redis Stack UI: http://localhost:8001 (if enabled)

### Local Development

1. **Install dependencies**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your database and Redis settings
   ```

3. **Start the application**
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

## API Documentation

### Base URL
```
http://localhost:8400
```

### Authentication
Currently, the API is open (no authentication required). Add authentication middleware as needed.

### Endpoints

#### Schema Management

**Create Schema**
```http
POST /schemas/
Content-Type: application/json

{
  "name": "products",
  "fields": [
    {
      "name": "title",
      "type": "text",
      "sortable": true,
      "weight": 2.0
    },
    {
      "name": "price",
      "type": "numeric",
      "sortable": true
    },
    {
      "name": "category",
      "type": "tag",
      "sortable": true
    }
  ]
}
```

#### Document Management

**Index Document**
```http
POST /documents/
Content-Type: application/json

{
  "schema_name": "products",
  "document_id": "product_123",
  "fields": {
    "title": "Laptop Pro 15",
    "price": 1299.99,
    "category": "electronics"
  }
}
```

**Search Documents**
```http
GET /documents/search/?schema_name=products&term=laptop&limit=10&offset=0
```

Response:
```json
{
  "success": true,
  "message": "Search completed successfully",
  "data": {
    "total": 25,
    "documents": [
      {
        "id": "products:product_123",
        "fields": {
          "title": "Laptop Pro 15",
          "price": 1299.99,
          "category": "electronics"
        },
        "score": 1.5
      }
    ]
  }
}
```

## Testing

### Run Tests

```bash
# Run all tests
pytest tests/ -v

# Run with output (to see print statements)
pytest tests/ -v -s

# Run specific test
pytest tests/test_integration.py -v -s
```

### Test Coverage

The project includes comprehensive integration tests that:

- Test schema creation and validation
- Test bulk document indexing (1000 documents)
- Test concurrent search operations (50 searches)
- Measure and report performance metrics
- Validate search results and scoring

### Performance Benchmarks

The integration test provides performance metrics:
- **Indexing Rate**: Documents per second
- **Search Rate**: Searches per second
- **Response Time**: Average search duration
- **Success Rate**: Percentage of successful operations

## Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
# Database Configuration
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=root
MYSQL_DB=search_engine

# Redis Configuration
REDIS_HOST=redis
REDIS_PORT=6379
```

### Field Types

| Type        | Description             | Use Case                    |
|-------------|-------------------------|-----------------------------|
| `text`      | Full-text searchable    | Product names, descriptions |
| `numeric`   | Numeric values          | Prices, quantities, scores  |
| `tag`       | Exact match tags        | Categories, status, labels  |

### Field Options

- `sortable`: Enable sorting by this field
- `weight`: Boost factor for text fields (default: 1.0)

## Monitoring and Logging

### Search Analytics

The API automatically logs search operations with:
- Search terms and parameters
- Response times
- Schema usage
- Performance metrics

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## Documentation

- **[API Reference](docs/API.md)** - Complete API documentation

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**IndexFlora API** - Fast, scalable search made simple.
