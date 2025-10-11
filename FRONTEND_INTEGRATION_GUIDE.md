# Frontend Integration Guide - 9-Question Garden Planner

## 📋 Overview

The backend is now fully configured to handle your 9-question frontend flow. All questions map directly to backend parameters for intelligent garden planning.

---

## 🎯 Question Flow & Backend Mapping

### **Question 1: Location** (Required)
**Purpose:** Geocoding, Google APIs (solar, air quality, pollen, elevation), climate data

**Frontend Input:**
- Address (text input) OR
- Coordinates (latitude/longitude)

**Backend Parameters:**
```json
{
  "address": "123 Main St, New York, NY",
  // OR
  "latitude": 40.7128,
  "longitude": -74.0060
}
```

**Backend Processing:**
- Geocodes address using Google Maps Geocoding API
- Fetches climate data, USDA zone, frost dates
- Can receive Google API data from frontend or fetch it server-side

---

### **Question 2: Gardening Method** (Required)
**Purpose:** Refines crop suggestions (e.g., no large trees for containers)

**Options:**
- Container Gardening
- Raised Beds
- In-ground Gardening
- Vertical Gardening
- Indoor Gardening
- Rooftop Gardening
- Hydroponic Gardening

**Backend Parameter:**
```json
{
  "method": "Container Gardening"
}
```

**Impact on Recommendations:**
- **Indoor/Container:** Suggests compact varieties, herbs, microgreens
- **Vertical:** Suggests vining crops (beans, cucumbers, tomatoes)
- **Hydroponic:** Suggests leafy greens, herbs
- **Large spaces:** Includes fruit trees, large squash

---

### **Question 3: Space Size** (Required)
**Purpose:** Determines how many plants to recommend

**Options:**
- Small (windowsill, few containers)
- Medium (balcony, small patio)
- Large (backyard, rooftop)
- Very Large (community garden plot)

**Backend Parameter:**
```json
{
  "size": "Medium (balcony, small patio)"
}
```

---

### **Question 4: Growing Location** (Required)
**Purpose:** Determines sunlight needs and soil considerations

**Sub-questions:**
- **Where:** Indoors / Outdoors / Both
- **Sunlight:** Full Sun / Partial Sun / Limited Sun / No Sun / Artificial Lights

**Backend Parameters:**
```json
{
  "growing_location": "Outdoors",
  "sunlight": "Full Sun (6+ hours direct sunlight)",
  "soil_type": "Medium (Loam, mixed)"  // Auto-detected or user-specified
}
```

**Sunlight Options:**
- `"Full Sun (6+ hours direct sunlight)"`
- `"Partial Sun (4-6 hours direct sunlight)"`
- `"Limited Sun (2-4 hours direct sunlight)"`
- `"No Sun (shade only)"`
- `"Artificial Lights (grow lights)"`

---

### **Question 5: Growing Seasons** (Required)
**Purpose:** Determines planting calendar and succession planting

**Options:** (Select all that apply)
- Spring
- Summer
- Fall
- Winter

**Backend Parameter:**
```json
{
  "seasons": ["Spring", "Summer", "Fall"]
}
```

**Impact:**
- Generates season-specific planting calendar
- Suggests succession planting for continuous harvest
- Recommends cover crops for off-seasons

---

### **Question 6: Time Commitment** (Required)
**Purpose:** Filters crops by maintenance needs

**Options:**
- Minimal (check weekly)
- Moderate (few times per week)
- Dedicated (daily care)

**Backend Parameter:**
```json
{
  "time_commitment": "Moderate (few times per week)"
}
```

**Impact:**
- **Minimal:** Prioritizes drought-tolerant, low-maintenance crops
- **Moderate:** Balanced selection
- **Dedicated:** Includes high-maintenance crops (tomatoes, peppers)

---

### **Question 7: Experience Level** (Required)
**Purpose:** Adjusts complexity of recommendations and care instructions

**Options:**
- Beginner (never grown anything before)
- Novice (grown a few plants)
- Intermediate (successful garden seasons)
- Advanced (experienced gardener)

**Backend Parameter:**
```json
{
  "experience": "Beginner (never grown anything before)"
}
```

**Impact:**
- **Beginner:** Suggests easy crops (lettuce, radishes, herbs)
- **Advanced:** Includes challenging crops (melons, artichokes)
- Adjusts detail level in care instructions

---

### **Question 8: Garden Goals** (Required)
**Purpose:** Determines which crops to recommend

**Sub-questions:**

#### **8a. What do you want to grow?** (Select all that apply)
- Leafy Greens (lettuce, spinach, kale)
- Tomatoes
- Root Vegetables (carrots, radishes, beets)
- Onions and Garlic
- Squash and Cucumbers
- Herbs (basil, parsley, cilantro, mint)
- Peppers
- Microgreens
- Beans and Peas
- **I don't know - suggest crops for me** ⭐ (Important for new growers!)

#### **8b. Preferences** (Select all that apply)
- Drought Resistant
- Native Plants
- Low Maintenance
- Pest Resistant
- Fast Growing

#### **8c. Additional Notes** (Optional text field)
User can type custom requirements

**Backend Parameters:**
```json
{
  "crop_interests": ["Herbs", "Leafy Greens"],
  // OR for new growers:
  "crop_interests": ["I don't know - suggest crops for me"],
  
  "preferences": ["Low Maintenance", "Fast Growing"],
  "additional_notes": "I have a cat, need pet-safe plants"
}
```

**Impact:**
- **"I don't know":** Backend suggests beginner-friendly variety based on all other factors
- **Specific interests:** Filters to requested crop families
- **Preferences:** Prioritizes matching characteristics

---

### **Question 9: Garden Space Image** (Optional)
**Purpose:** Visual layout planning and companion planting

**Frontend Input:**
- Image upload (photo of garden space)

**Backend Parameters:**
```json
{
  "garden_image_url": "https://...",
  // OR
  "garden_image_base64": "data:image/jpeg;base64,..."
}
```

**Backend Processing:**
- Analyzes image for:
  - Available space dimensions
  - Sunlight patterns (if visible)
  - Existing structures
- Generates spatial layout recommendations
- Suggests companion planting arrangements
- Provides "plant X here, plant Y there" guidance

---

## 🔌 API Endpoints

### **GET `/api/enums`**
Returns all dropdown options for the frontend

**Response:**
```json
{
  "methods": ["Container Gardening", "Raised Beds", ...],
  "sizes": ["Small (windowsill, few containers)", ...],
  "growing_locations": ["Indoors", "Outdoors", "Both"],
  "sunlight": ["Full Sun (6+ hours direct sunlight)", ...],
  "seasons": ["Spring", "Summer", "Fall", "Winter"],
  "time_commitments": ["Minimal (check weekly)", ...],
  "experience": ["Beginner (never grown anything before)", ...],
  "crop_interests": ["Leafy Greens (lettuce, spinach, kale)", ...],
  "preferences": ["Drought Resistant", "Low Maintenance", ...]
}
```

### **POST `/api/v1/garden-plan/generate`**
Generates personalized garden plan

**Full Request Example:**
```json
{
  "address": "New York, NY",
  "method": "Raised Beds",
  "size": "Medium (balcony, small patio)",
  "growing_location": "Outdoors",
  "sunlight": "Full Sun (6+ hours direct sunlight)",
  "seasons": ["Spring", "Summer", "Fall"],
  "time_commitment": "Moderate (few times per week)",
  "experience": "Beginner (never grown anything before)",
  "crop_interests": ["I don't know - suggest crops for me"],
  "preferences": ["Low Maintenance", "Fast Growing"],
  "additional_notes": "First time gardener, want easy success!",
  "garden_image_url": "https://example.com/my-garden.jpg"
}
```

**Response:**
- 10-15+ crop recommendations from 270+ database
- Detailed variety information
- Planting calendar with frost dates
- Disease prevention guide
- Companion planting suggestions
- Watering schedule
- Care instructions
- Layout recommendations (if image provided)

---

## 🎨 Frontend Best Practices

### **Question 1 - Location**
- Provide autocomplete for address input
- Allow manual coordinate entry for precision
- Show map preview of location

### **Question 2 - Method**
- Show icons for each method
- Provide brief descriptions on hover

### **Question 3 - Size**
- Visual size comparison (icons/images)

### **Question 4 - Location & Sunlight**
- Conditional logic: If "Indoors" → show "Artificial Lights" option
- If "Outdoors" → show sun exposure options

### **Question 5 - Seasons**
- Checkboxes for multi-select
- Default to current + next season

### **Question 6 - Time**
- Radio buttons
- Show time estimates (e.g., "~30 min/week")

### **Question 7 - Experience**
- Radio buttons
- Friendly descriptions

### **Question 8 - Goals**
- **8a:** Checkboxes with "I don't know" as prominent option
- **8b:** Checkboxes for preferences
- **8c:** Text area for notes

### **Question 9 - Image**
- Drag-and-drop upload
- Camera capture on mobile
- Preview before submit
- Mark as optional but encourage use

---

## 🧠 Backend Intelligence

The backend uses all this data to:

1. **Filter crops** by method, size, sunlight, experience
2. **Prioritize crops** by preferences (low maintenance, fast growing, etc.)
3. **Generate calendar** based on location climate and selected seasons
4. **Recommend varieties** from 270+ crop database
5. **Provide layout** if image uploaded
6. **Suggest companions** for pest control and yield
7. **Calculate watering** based on climate and soil
8. **Warn about diseases** specific to location and crops
9. **Adapt to time commitment** with appropriate care schedules

---

## 🚀 Ready to Use

The backend is **fully configured** to handle all 9 questions. Simply:

1. Call `GET /api/enums` to populate dropdowns
2. Collect user answers through your 9-question flow
3. POST to `/api/v1/garden-plan/generate` with all parameters
4. Display the comprehensive garden plan!

**Base URL:** `https://agenticaigardenplanner.onrender.com`

---

## 📝 Notes

- All parameters have sensible defaults
- Only `address/coordinates`, `method`, `size`, and `experience` are truly required
- Backend handles "I don't know - suggest crops for me" intelligently
- Image upload is optional but enhances recommendations
- Google API data can be fetched by frontend or backend
