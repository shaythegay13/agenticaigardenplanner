# AI Garden Planner v4.0 - Complete Garden Management

A comprehensive, climate-aware garden planning system with visual layout generation, 200+ companion relationships, 140+ educational resources, 50 diseases with seasonal tracking, and regional disease risk assessment.

## Features

### 🌱 **Core Planning** (v1.0)
- **Personalized Plans**: Location, method, space, sunlight, soil, experience, and goals
- **Knowledge-Based Recommendations**: Curated plant database with smart filtering
- **Interactive CLI**: Step-by-step questionnaire with immediate results

### 💧 **Water & Season Management** (v2.0)
- **Water Deficit Analysis**: Cornell CSF-based irrigation recommendations
- **Evapotranspiration**: Temperature-based ET calculations
- **Cover Crops**: Planting windows with growing degree days
- **Succession Planting**: Continuous harvest scheduling

### 🌍 **Climate Adaptation & Resilience** (v3.0)
- **Drought Monitoring**: Current drought status and adapted strategies
- **Climate Hubs**: USDA regional resources and guidance
- **Future Projections**: 2030s, 2050s, 2080s climate outlook
- **Climate-Adapted Crops**: 60+ varieties for changing conditions
- **State Assessments**: Detailed climate impact reports (NY, CA)
- **Regional Tools**: Specialized resources by region
- **Coastal Risk**: Flooding and sea level rise assessment

### 🎯 **Essential Gardening Features** (v3.1)
- **Companion Planting**: Strategic crop pairing for better yields
- **Yield Estimates**: Realistic harvest predictions based on your conditions
- **Disease Prevention**: Common diseases, symptoms, and organic treatments
- **Educational Resources**: Curated videos, articles, and guides
- **Skill-Matched Learning**: Resources tailored to your experience level

### 📊 **Database Expansions & Regional Intelligence** (v3.2)
- **Expanded Companions**: 30+ crops with 200+ relationships (173% increase)
- **Three Sisters System**: Full corn-beans-squash companion data
- **Expanded Resources**: 140+ curated videos, articles, guides, and books (250% increase)
- **Regional Disease Risk**: Location-aware disease prevention across 4 US regions
- **Risk Level Indicators**: 🔴 Very High, 🟠 High, 🟡 Moderate, 🟢 Low
- **Container & Raised Bed Guides**: Space-efficient growing methods

### 🏥 **Disease Intelligence** (v3.3)
- **50 Diseases**: Comprehensive coverage across 17 crops (525% increase from v3.2)
- **Seasonal Tracking**: Peak disease seasons for all diseases (Spring, Summer, Fall, Winter, Year-Round)
- **11 New Crops**: Peppers, lettuce, spinach, onions, carrots, potatoes, melons, peas, corn, eggplant, kale
- **Enhanced Coverage**: 7 tomato diseases, 3 pepper diseases, 3 melon diseases, 3 pea diseases
- **31 Unique Diseases**: Bacterial, fungal, viral, and physiological disorders documented

### 🎨 **Visual Garden Layout** (v4.0 Phase 1 - NEW!)
- **ASCII Visualization**: Auto-generated 2D garden bed layouts
- **Companion Integration**: Layouts respect companion planting relationships
- **Smart Placement**: Large crops placed to avoid shading smaller ones
- **Space Optimization**: Square Foot Gardening principles integrated
- **Multiple Spacing Methods**: Square Foot, Intensive, Traditional, Wide
- **Crop Size Intelligence**: Automatic spacing based on plant size

### 📊 **Data Sources**
- Open-Meteo (weather forecasts)
- USDA (hardiness zones, climate hubs)
- US Drought Monitor (drought status)
- NOAA (climate projections)
- State Climate Offices (regional assessments)
- Cornell CSF (agricultural tools)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/agentic-agi.git
   cd agentic-agi
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Start the interactive CLI from the project root:
```bash
python -m agi_agent.cli
```

The CLI will prompt for the following inputs:

- Location: Address or coordinates (lat/lon). Address is geocoded via Google Maps Geocoding API (with OpenStreetMap fallback).
- Gardening Method: `Raised Beds`, `Container Gardening`, `In-ground Gardening`, `Vertical Gardening`, `Indoor Gardening`, `Rooftop Gardening`.
- Space Size: `Small`, `Medium`, `Large`, or `Very Large`.
- Sunlight: `Full Sun`, `Partial Sun`, `Partial Shade`, `Shade`, or `Artificial Light Only`.
- Experience: `Beginner`, `Novice`, `Intermediate`, `Advanced`.
- Soil Type: `High (Clay)`, `Medium (Loam)`, `Low (Sand)`, or `Unknown` - used for water deficit calculations.
- Goals: Crop interests, preferences (fast growing, low maintenance, year-round, etc.), and optional notes.
- Image Path: Optional path to an image of your space to note microclimate/obstruction considerations.

Output includes:

### Current Conditions
- Resolved coordinates and climate summary
- Enhanced USDA hardiness zone information
- Current drought status and adapted recommendations (v3.0)
- Regional climate hub resources (v3.0)

### Planning Recommendations
- Layout and setup tips tailored to your method, size, and light
- Top 10 recommended crops with detailed notes
- Frost-aware planting calendar
- Water deficit analysis with irrigation timing (v2.0)
- Succession planting guide for continuous harvests (v2.0)
- Cover crop recommendations with planting windows (v2.0)
- Care schedule (watering, feeding, mulch, pests)
- Multi-year crop rotation strategies

### Climate Resilience (v3.0 NEW!)
- Future climate outlook (2030s, 2050s, 2080s projections)
- Climate-adapted crop varieties by trend type
- State climate assessment highlights (NY, CA)
- Regional tool ecosystem links
- Coastal flooding risk assessment (if applicable)

## Project Structure

```
ai-garden-planner/
├── agi_agent/
│   ├── __init__.py
│   ├── cli.py
│   ├── core/
│   │   └── agent.py
│   └── gardening/
│       ├── __init__.py
│       ├── climate.py              # Weather & frost data
│       ├── knowledge.py            # Plant database
│       ├── models.py               # Data models
│       ├── planner.py              # Main planning engine
│       ├── vision.py               # Image analysis
│       ├── water_management.py     # v2.0: Water deficit calculator
│       ├── seasonal_planning.py    # v2.0: Cover crops & succession
│       ├── climate_adaptation.py   # v3.0: Drought & climate hubs
│       ├── future_climate.py       # v3.0: Climate projections
│       └── regional_resources.py   # v3.0: State assessments & tools
├── requirements.txt
├── README.md
├── CHANGELOG_v3.md                 # v3.0 release notes
└── RESOURCE_ANALYSIS.md            # Climate resource evaluation
```

## Minimal Example (Programmatic)

```python
from agi_agent.gardening import (
    LocationInput, GardeningMethod, SpaceSize, Sunlight, Experience, SoilType,
    UserGoals, UserInput, CropInterest, Preference,
    geocode_location, fetch_simple_forecast, generate_plan
)

loc = LocationInput(address="New York, NY")
lat, lon = geocode_location(loc)
climate = fetch_simple_forecast(lat, lon)

user = UserInput(
    location=LocationInput(latitude=lat, longitude=lon, address=loc.address),
    method=GardeningMethod.CONTAINERS,
    size=SpaceSize.MEDIUM,
    sunlight=Sunlight.PARTIAL_SUN,
    experience=Experience.BEGINNER,
    soil_type=SoilType.MEDIUM,  # For water deficit analysis
    goals=UserGoals(
        crops=[CropInterest.HERBS, CropInterest.LEAFY_GREENS],
        preferences=[Preference.LOW_MAINTENANCE, Preference.FAST_GROWING],
        notes="Kitchen herbs and salads"
    )
)

plan = generate_plan(user, climate)
print(plan)
```

## What's New in v3.0

### 🌍 Phase 1: Climate Adaptation (High Priority)
**Official USDA Hardiness Zones**
- Enhanced zone information with temperature details
- Perennial plant guidance
- Future zone shift predictions

**US Drought Monitor Integration**
- Current drought status (D0-D4 classifications)
- Severity-based gardening recommendations
- Water restriction guidance
- 6 drought adaptation strategies

**USDA Climate Hub Resources**
- 10 regional climate hubs mapped nationwide
- Direct links to hub-specific resources
- Regional climate adaptation strategies
- Extreme weather preparation guides

### 🔮 Phase 2: Future Climate Projections (Medium Priority)
**Mid-Century Outlook (2050s)**
- Temperature projections by region (+1.5°C to +4.5°C)
- Precipitation changes (±5% to ±20%)
- Growing season extensions (+10 to +40 days)
- Extreme heat day increases

**Climate-Resilient Crops**
- 60+ adapted crop varieties
- Strategies for 6 trend types (warming, drying, wetting, extreme heat, etc.)
- 40+ adaptation actions across scenarios
- Zone shift predictions for long-term planning

### 📍 Phase 3: Regional Resources (Specialized)
**State Climate Assessments**
- New York 2024 assessment integrated
- California 2018 assessment
- Key findings for agriculture
- State-specific recommendations

**Regional Tool Ecosystem**
- Northeast: NRCC, Cornell CSF
- West: WSU Ag Tools, Climate Toolbox
- Midwest: U2U Climate Tools
- Southeast: SERCC

**Coastal & Flood Risk**
- Coastal flooding assessment
- FEMA flood zone information
- Sea level rise considerations
- Risk-appropriate gardening strategies

---

## Features From Previous Versions

### v2.0 - Water & Season Management
- Cornell CSF water deficit calculator
- Hargreaves-Samani evapotranspiration
- Cover crop planting windows with GDD
- Succession planting schedules
- 8-year frost date calculations

### v1.0 - Core Planning
- Plant recommendation engine
- Regional plant database
- Method/space/sunlight filtering
- Interactive CLI questionnaire

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

MIT
