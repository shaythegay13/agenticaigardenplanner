# AI Garden Planner API Documentation

REST API for the AI Garden Planner - designed for Lovable frontend integration.

## Base URL
http://localhost:8000

## Endpoints

### 1. Health Check

GET /GET/health

Check if API is online.

**Response:**
```json
{
  "status": "online",
  "service": "AI Garden Planner API",
  "version": "4.0.2"
}

### 2. Get Dropdown Options

GET /api/enums

### 3. Get All Crops

GET /api/crops

### 4. Generate Garden Plan

POST /api/plan

### GET /api/enums

Get dropdown options for frontend forms.

{
  "methods": ["Raised Beds", "Container Gardening", ...],
  "sizes": ["Small", "Medium", "Large"],
  "sunlight": ["Full Sun (6+ hours)", ...],
  "experience": ["Beginner", "Novice", ...],
  "crop_interests": ["Tomatoes", "Herbs", ...],
  "preferences": ["Fast Growing", "Low Maintenance", ...]
}

### GET /api/crops

Get all 100 crops.

{
  "total_crops": 100,
  "crops": [
    {
      "name": "Tomatoes",
      "key": "tomatoes",
      "variety_count": 3
    },
    ...
  ]
}

### POST /api/plan

Generate personalized garden plan.

**Request Body:**
```json
{
  "address": "123 Main St, Anytown, USA",
  "method": "Raised Beds",
  "size": "Small",
  "sunlight": "Full Sun (6+ hours)",
  "experience": "Beginner",
  "crop_interests": ["Tomatoes", "Herbs"],
  "preferences": ["Fast Growing", "Low Maintenance"]
}
```

**Response:**
```json
{
  "success": true,
  "plan": "Your personalized garden plan...",
  "location": {
    "city": "Anytown",
    "state": "AnyState",
    "usda_zone": "12"
  }
}
```