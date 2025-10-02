# Quick Start Guide - New Features

## What's New?

Your AI Garden Planner now includes **Cornell Climate Smart Farming** methodologies:

### 🌊 Water Management
- Real-time water deficit calculations
- Soil-type specific irrigation recommendations
- 7-day forecast analysis
- Stress level warnings

### 🌱 Seasonal Planning
- Cover crop planting windows
- Succession planting schedules
- Growing degree day calculations
- Continuous harvest strategies

---

## Quick Test (No Dependencies Required)

### 1. Verify Installation

```bash
# Check all modules compile
python3 -m py_compile agi_agent/gardening/water_management.py
python3 -m py_compile agi_agent/gardening/seasonal_planning.py
python3 -m py_compile agi_agent/gardening/planner.py

# Should return with no errors (exit code 0)
```

### 2. Run Demo Script

```bash
# After installing dependencies (see below)
python3 demo_water_management.py
```

This will show:
- ET calculations for different temperatures
- Water balance simulation for 3 soil types
- Cover crop planting windows
- Succession planting schedules

---

## Installation (For Running the Full System)

### Option 1: Virtual Environment (Recommended)

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the planner
python -m agi_agent.cli
```

### Option 2: Using pipx (For CLI use)

```bash
# Install pipx if not available
sudo apt install pipx

# Install in isolated environment
pipx install -e .

# Run from anywhere
agi-garden-planner
```

---

## Using the New Features

### In the CLI

When you run `python -m agi_agent.cli`, you'll now see:

**New Question:**
```
Choose soil type (for water management analysis):
  1. High (Clay, fine textured)
  2. Medium (Loam, mixed)
  3. Low (Sand, coarse)
  4. Unknown - use medium as default
Your choice #: _
```

**New Output Sections:**
1. **Current Water Status** - Irrigation needs based on forecast
2. **Succession Planting Guide** - Season-specific crop schedules
3. **Cover Crop Recommendations** - Timing for soil health crops

### Programmatically

```python
from agi_agent.gardening import (
    UserInput, LocationInput, SoilType, 
    generate_plan, fetch_simple_forecast
)

# Key change: Add soil_type parameter
user = UserInput(
    location=LocationInput(address="Brooklyn, NY"),
    soil_type=SoilType.MEDIUM,  # ← NEW!
    # ... other parameters
)

lat, lon = (40.7128, -74.0060)
climate = fetch_simple_forecast(lat, lon)
plan = generate_plan(user, climate)
```

---

## Example Output

### Water Deficit Analysis

```
Current Water Status:
- Water Deficit: 0.85 inches
- Stress Level: Moderate
- 7-day Average Deficit: 0.62 inches

⚠ Irrigation needed soon to prevent yield impacts.
Apply 0.85 inches to restore optimal moisture.
Water deeply to encourage root development.
```

### Cover Crop Recommendations

```
Fall Cover Crop Planting:
- Winter Rye: Plant soon! 18 days until latest safe date.
  Hardy; establishes quickly; excellent for overwintering
  
- Crimson Clover: Optimal planting window opens in 5 days.
  Nitrogen fixer; beautiful flowers in spring
```

### Succession Planting

```
Spring Succession Crops (plant now through early summer):
- Lettuce (45 days): Plant every 2 weeks spring and fall
- Radishes (25 days): Fast-growing; sow every 10 days
- Spinach (40 days): Plant every 2 weeks; bolt-resistant varieties
```

---

## File Structure

New files added:
```
agi_agent/gardening/
├── water_management.py       # Water deficit calculations
├── seasonal_planning.py      # Cover crops & succession
└── models.py                 # Added SoilType enum

demo_water_management.py      # Standalone demo
CORNELL_CSF_FEATURES.md       # Full technical documentation
QUICK_START.md                # This file
```

Modified files:
```
agi_agent/gardening/
├── planner.py                # Integrated new modules
├── __init__.py               # Exported new functions
└── models.py                 # Added SoilType

agi_agent/cli.py              # Added soil type prompt
README.md                     # Updated documentation
```

---

## Testing Checklist

- [x] **Syntax**: All Python files compile without errors
- [ ] **Dependencies**: Install requirements in virtual environment
- [ ] **Demo**: Run `demo_water_management.py` successfully
- [ ] **CLI**: Run `python -m agi_agent.cli` and see new prompts
- [ ] **Output**: Verify water analysis appears in generated plan
- [ ] **Cover Crops**: Check cover crop recommendations show current season
- [ ] **Succession**: Verify succession planting guide is included

---

## Troubleshooting

### "Module not found" errors
→ Install dependencies: `pip install -r requirements.txt`

### "externally-managed-environment" error
→ Use virtual environment: `python3 -m venv venv && source venv/bin/activate`

### Water analysis shows "unavailable"
→ Check that you selected a soil type (not "Unknown")

### No cover crop recommendations
→ This is season-dependent; fall shows most recommendations

---

## What the Tools Calculate

### Water Deficit Calculator
- **Input**: Temperature forecast + precipitation + soil type + crop type
- **Process**: Daily water balance (precip - ET - runoff - drainage)
- **Output**: Irrigation amount needed + stress level + timing

### Cover Crop Planner
- **Input**: Current date + first frost date + crop type
- **Process**: Growing degree day accumulation estimate
- **Output**: Optimal planting window + latest safe date

### Succession Planner
- **Input**: Frost dates + current season
- **Process**: Match season to crop + calculate intervals
- **Output**: Planting schedule for continuous harvest

---

## Cornell CSF Resources

These tools are based on:
- [CSF Water Deficit Calculator](https://climatesmartfarming.org/tools/csf-water-deficit-calculator/)
- [CSF Cover Crop Scheduler](https://climatesmartfarming.org/tools/csf-winter-cover-crop-planting-scheduler/)

For more details, see `CORNELL_CSF_FEATURES.md` in this directory.

---

## Next Steps

1. **Test the demo**: `python3 demo_water_management.py`
2. **Try the CLI**: `python -m agi_agent.cli`
3. **Read the docs**: Check `CORNELL_CSF_FEATURES.md` for scientific details
4. **Integrate**: Use programmatically in your own code

Happy gardening! 🌱
