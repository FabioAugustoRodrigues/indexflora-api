# IndexFlora API Reference

## Overview

The IndexFlora API provides a RESTful interface for managing search schemas and performing full-text search operations using Redis Stack (RediSearch).

## Base URL
```
http://localhost:8400
```

## Authentication
Currently, no authentication is required. All endpoints are publicly accessible.

## Response Format

All API responses follow this standard format:

### Success Response
```json
{
  "success": true,
  "message": "Operation completed successfully",
  "data": {
    // Response data here
  }
}
```

### Error Response
```json
{
  "success": false,
  "message": "Error description",
  "errors": ["Detailed error information"]
}
```

## Endpoints

### Schema Management

#### Create Schema
```http
POST /schemas/
```

**Request Body:**
```json
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

**Response:**
```json
{
  "success": true,
  "message": "Schema created successfully and index created in Redisearch",
  "data": {
    "index_name": "idx:products"
  }
}
```

**Field Types:**
- `text`: Full-text searchable fields
- `numeric`: Numeric values for sorting and filtering
- `tag`: Exact match tags for categorization

**Field Options:**
- `sortable` (boolean): Enable sorting by this field
- `weight` (float): Boost factor for text fields (default: 1.0)

### Document Management

#### Index Document
```http
POST /documents/
```

**Request Body:**
```json
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

**Response:**
```json
{
  "success": true,
  "message": "Document indexed successfully",
  "data": {
    "index_name": "products:product_123"
  }
}
```

#### Search Documents
```http
GET /documents/search/
```

**Query Parameters:**
- `schema_name` (string, required): Name of the schema to search
- `term` (string, required): Search term
- `limit` (integer, optional): Maximum number of results (default: 10)
- `offset` (integer, optional): Number of results to skip (default: 0)

**Example Request:**
```http
GET /documents/search/?schema_name=products&term=laptop&limit=10&offset=0
```

**Response:**
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
      },
      {
        "id": "products:product_456",
        "fields": {
          "title": "Gaming Laptop",
          "price": 1999.99,
          "category": "electronics"
        },
        "score": 1.2
      }
    ]
  }
}
```

## Error Codes

| Status Code | Description                              |
|-------------|------------------------------------------|
| 200         | Success                                  |
| 400         | Bad Request - Invalid input data         |
| 404         | Not Found - Schema or document not found |
| 409         | Conflict - Schema already exists         |
| 500         | Internal Server Error                    |

## Search Features

### Text Search
- **Full-text search**: Search across all text fields
- **Fuzzy matching**: Find similar terms
- **Phrase search**: Search for exact phrases
- **Wildcard support**: Use `*` for partial matches

### Numeric Search
- **Range queries**: Find documents within price ranges
- **Sorting**: Sort results by numeric fields
- **Filtering**: Filter by exact numeric values

### Tag Search
- **Exact matching**: Find documents with specific tags
- **Multiple tags**: Search for documents with any/all tags
- **Tag filtering**: Filter results by category

### Search Performance
- **Limit results**: Use appropriate limit values
- **Pagination**: Use offset for large result sets
- **Field selection**: Only search relevant fields

## Examples

### E-commerce Product Search
```json
{
  "name": "products",
  "fields": [
    {"name": "title", "type": "text", "sortable": true, "weight": 3.0},
    {"name": "description", "type": "text", "sortable": false, "weight": 1.0},
    {"name": "price", "type": "numeric", "sortable": true},
    {"name": "category", "type": "tag", "sortable": true},
    {"name": "brand", "type": "tag", "sortable": true},
    {"name": "in_stock", "type": "tag", "sortable": true}
  ]
}
```

### Content Management System
```json
{
  "name": "articles",
  "fields": [
    {"name": "title", "type": "text", "sortable": true, "weight": 2.0},
    {"name": "content", "type": "text", "sortable": false, "weight": 1.0},
    {"name": "author", "type": "tag", "sortable": true},
    {"name": "published_date", "type": "numeric", "sortable": true},
    {"name": "tags", "type": "tag", "sortable": true}
  ]
}
```

## Rate Limiting

Currently, no rate limiting is implemented. Consider implementing rate limiting for production use.

## CORS

CORS is not configured by default. Add CORS middleware for web applications:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

