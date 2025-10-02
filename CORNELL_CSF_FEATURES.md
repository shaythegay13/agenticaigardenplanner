# Cornell Climate Smart Farming Integration Guide

This document explains the Cornell CSF tool methodologies integrated into the AI Garden Planner.

## Table of Contents
- [Water Deficit Calculator](#water-deficit-calculator)
- [Seasonal Planning Tools](#seasonal-planning-tools)
- [Usage Examples](#usage-examples)
- [Scientific Background](#scientific-background)
- [References](#references)

---

## Water Deficit Calculator

Based on the [Cornell CSF Water Deficit Calculator](https://climatesmartfarming.org/tools/csf-water-deficit-calculator/)

### Overview
The water deficit calculator estimates soil water content within a crop's effective root zone to inform irrigation decisions. It uses a water balance model that accounts for:

- **Precipitation**: Rainfall input to the soil
- **Evapotranspiration (ET)**: Water loss through evaporation and plant transpiration
- **Runoff**: Water lost when rain intensity exceeds soil infiltration
- **Drainage**: Water lost below the root zone when soil exceeds field capacity

### Key Concepts

#### 1. Soil Water Capacity
Different soil types hold different amounts of available water:

| Soil Type | Water Capacity (inches per foot) | Description |
|-----------|----------------------------------|-------------|
| **High** (Clay) | 2.5 | Fine-textured, holds water well but drains slowly |
| **Medium** (Loam) | 1.75 | Balanced texture, ideal for most crops |
| **Low** (Sand) | 0.75 | Coarse, drains quickly, needs frequent watering |

#### 2. Evapotranspiration (ET)
We calculate reference ET using the **Hargreaves-Samani equation**, a temperature-based method that works when only temperature data is available:

```
ET₀ = 0.0023 × Ra × (Tₐᵥᵍ + 17.8) × √(Tₘₐₓ - Tₘᵢₙ)
```

Where:
- **Ra** = Extraterrestrial radiation (varies by latitude and day of year)
- **Tₐᵥᵍ** = Average temperature
- **Tₘₐₓ, Tₘᵢₙ** = Daily maximum and minimum temperatures

#### 3. Crop Coefficients (Kc)
Different crops have different water needs. We apply crop-specific coefficients:

| Crop Category | Coefficient (Kc) | Examples |
|---------------|------------------|----------|
| Herbs | 0.6 | Basil, parsley, cilantro |
| Leafy Greens | 0.7 | Lettuce, spinach, kale |
| Root Crops | 0.8 | Carrots, beets, radishes |
| Vegetables | 0.85 | Various mixed vegetables |
| Beans & Peas | 0.95 | Bush beans, snap peas |
| Tomatoes & Peppers | 1.05 | High water users |

**Crop ET = Reference ET × Kc**

#### 4. Water Balance Model
Daily water balance calculation:

```
Water(day+1) = Water(day) + Precipitation + Irrigation - ET - Runoff - Drainage
```

**Constraints:**
- Water content cannot exceed field capacity (excess drains away)
- Water content cannot be negative (ET limited by available water)
- Heavy rainfall (>2 inches) loses ~25% to runoff

#### 5. Water Deficit & Stress Levels

**Water Deficit** = Field Capacity - Current Water Content

| Stress Level | Deficit (% of capacity) | Plant Response |
|-------------|------------------------|----------------|
| **Optimal** | 0-10% | No stress, ideal growth |
| **Slight** | 10-25% | Minimal impact, monitor closely |
| **Moderate** | 25-50% | Growth slowing, irrigation recommended |
| **Severe** | >50% | Significant stress, yield loss likely |

### Irrigation Recommendations

The system provides actionable recommendations:

- **Optimal**: No irrigation needed
- **Slight**: Consider light irrigation in 1-2 days if dry trend continues
- **Moderate**: Irrigate soon with calculated deficit amount
- **Severe**: URGENT - Irrigate immediately, split applications if >1 inch

---

## Seasonal Planning Tools

### Cover Crops

Based on [Cornell CSF Winter Cover Crop Planting Scheduler](https://climatesmartfarming.org/tools/csf-winter-cover-crop-planting-scheduler/)

#### Growing Degree Days (GDD)
Cover crop establishment timing is calculated using GDD:

```
GDD = max(0, (Tₘₐₓ + Tₘᵢₙ) / 2 - Tᵦₐₛₑ)
```

Each crop has a base temperature and target GDD for establishment:

| Cover Crop | Base Temp (°C) | Target GDD | Season | Purpose |
|-----------|----------------|------------|--------|---------|
| **Winter Rye** | 0 | 150 | Cool | Overwintering, erosion control |
| **Buckwheat** | 10 | 800 | Warm | Quick biomass, weed suppression |
| **Crimson Clover** | 5 | 400 | Cool | Nitrogen fixation, pollinator |
| **Hairy Vetch** | 5 | 350 | Cool | High nitrogen fixation |
| **Tillage Radish** | 5 | 400 | Cool | Deep root, breaks compaction |
| **Field Peas** | 4 | 600 | Cool | Nitrogen, good for summer |
| **Oats** | 4 | 500 | Cool | Quick establishment |

#### Planting Windows
The system calculates optimal planting dates by:
1. Estimating days needed to accumulate target GDD
2. Working backward from first frost date
3. Adding a 2-week safety buffer

**Example:**
- First frost: October 15
- Tillage Radish needs 400 GDD
- Average daily accumulation: 10 GDD/day
- Days needed: 40 days
- Latest planting: September 5 (Oct 15 - 40 days)
- Optimal window: August 22 - September 5

### Succession Planting

Continuous harvest strategy for fast-growing crops.

#### Recommended Succession Crops

| Crop | Days to Harvest | Interval | Season | Notes |
|------|----------------|----------|--------|-------|
| Radishes | 25 | 10 days | Cool | Fastest turnover |
| Arugula | 30 | 14 days | Cool | Spicy green |
| Spinach | 40 | 14 days | Cool | Bolt-resistant varieties |
| Cilantro | 40 | 14 days | Cool | Bolts in heat |
| Lettuce | 45 | 14 days | Cool | Cut-and-come-again |
| Beets | 55 | 21 days | Cool | Greens + roots |
| Bush Beans | 55 | 21 days | Warm | Continuous production |
| Carrots | 70 | 21 days | Cool | Stagger for size variety |

#### Strategy
1. **Calculate harvest window**: Last frost → First frost
2. **Schedule plantings**: Every N days (crop-specific interval)
3. **Account for changing season**: Cool crops twice (spring + fall)
4. **Track plantings**: Date labels and garden journal

**Example Lettuce Schedule:**
```
Planting #1: April 1 → Harvest: May 15
Planting #2: April 15 → Harvest: May 30
Planting #3: May 1 → Harvest: June 15
...continuous through June
```

---

## Usage Examples

### Example 1: Check Irrigation Needs

```python
from agi_agent.gardening.water_management import (
    simulate_water_deficit,
    generate_irrigation_recommendation,
    SoilType,
    CropWaterUse,
)
from datetime import date

# Your 7-day forecast
results = simulate_water_deficit(
    daily_highs_c=[28, 30, 29, 27, 26, 25, 28],
    daily_lows_c=[18, 20, 19, 17, 16, 15, 18],
    daily_precip_mm=[0, 0, 5, 15, 0, 0, 0],
    latitude=40.7128,
    start_date=date.today(),
    soil_type=SoilType.MEDIUM,
    crop_type=CropWaterUse.TOMATOES_PEPPERS,
)

recommendation = generate_irrigation_recommendation(results)
print(recommendation)
```

### Example 2: Plan Cover Crops

```python
from agi_agent.gardening.seasonal_planning import (
    estimate_cover_crop_window,
    CoverCropType,
)
from datetime import date

window = estimate_cover_crop_window(
    current_date=date.today(),
    first_frost_date=date(2024, 10, 15),
    cover_crop=CoverCropType.WINTER_RYE,
    avg_daily_gdd=10.0
)

print(f"Status: {window['status']}")
print(f"Message: {window['message']}")
print(f"Plant between {window['optimal_start']} and {window['latest_date']}")
```

### Example 3: Create Succession Schedule

```python
from agi_agent.gardening.seasonal_planning import (
    generate_succession_planting_schedule,
)
from datetime import date

schedule = generate_succession_planting_schedule(
    start_date=date(2024, 4, 1),
    end_date=date(2024, 6, 15),
    crop_name="Lettuce",
    days_to_harvest=45,
    planting_interval_days=14
)

for planting in schedule:
    print(f"Plant: {planting['planting_date']} → Harvest: {planting['expected_harvest']}")
```

---

## Scientific Background

### Why Temperature-Based ET?

The Hargreaves-Samani equation is ideal for home gardeners because:
1. **Only requires temperature data** (widely available in weather forecasts)
2. **More accurate than Thornthwaite** method for daily estimates
3. **Accounts for latitude** and seasonal radiation changes
4. **Well-validated** across diverse climates

More complex methods (Penman-Monteith) require:
- Wind speed
- Solar radiation
- Humidity
- Cloud cover

These are often unavailable in typical weather forecasts.

### Water Balance Simplifications

Our model makes reasonable assumptions for home gardens:
1. **Root depth = 1 foot**: Most vegetables have 6-18 inch effective root zones
2. **Field capacity = 100%**: Optimal soil moisture for most crops
3. **Runoff at 25%**: Heavy rain (>2 inches) events lose water to runoff
4. **No capillary rise**: Conservative approach (underestimates available water)

These simplifications err on the side of caution, preventing under-watering.

### Growing Degree Days

GDD accumulation predicts crop development better than calendar dates because:
- **Temperature drives growth**, not time
- **Regional adaptability**: Same crop, different climates
- **Phenological accuracy**: Predicts life stages (germination, flowering, maturity)

Base temperatures represent the minimum for metabolic activity in each species.

---

## References

### Cornell Climate Smart Farming Tools
1. **CSF Water Deficit Calculator**  
   https://climatesmartfarming.org/tools/csf-water-deficit-calculator/
   
2. **CSF Winter Cover Crop Planting Scheduler**  
   https://climatesmartfarming.org/tools/csf-winter-cover-crop-planting-scheduler/

3. **Cornell Climate Change Visualization**  
   https://climatesmartfarming.org/tools/csf-county-climate-change/

### Scientific Literature
- Hargreaves, G.H., & Samani, Z.A. (1985). Reference crop evapotranspiration from temperature. *Applied Engineering in Agriculture*, 1(2), 96-99.

- Allen, R.G., et al. (1998). *Crop evapotranspiration - Guidelines for computing crop water requirements*. FAO Irrigation and drainage paper 56.

- McMaster, G.S., & Wilhelm, W.W. (1997). Growing degree-days: one equation, two interpretations. *Agricultural and Forest Meteorology*, 87(4), 291-300.

### Data Sources
- **Open-Meteo**: Weather forecast API (https://open-meteo.com/)
- **ERA5**: Historical climate reanalysis for USDA zone estimation
- **NRCC**: Northeast Regional Climate Center moisture maps

---

## Limitations & Future Enhancements

### Current Limitations
1. **No soil moisture sensors**: Model-based only (no real-time feedback)
2. **Simplified runoff model**: Doesn't account for slope or soil infiltration rates
3. **No crop growth stages**: Uses constant Kc (should vary by development stage)
4. **No irrigation efficiency**: Assumes 100% efficient application

### Potential Enhancements
1. **Integrate soil moisture sensor data** for calibration
2. **Add crop-specific growth stage adjustments** for Kc
3. **Incorporate NEWA pest/disease models** for integrated management
4. **Add climate change scenarios** from CSF climate tool
5. **Support for perennial crops** (fruit trees, berries) with different root zones

---

## Support & Contribution

This implementation is open-source and based on publicly available Cornell CSF methodologies. Contributions welcome!

For questions about the scientific methods, refer to Cornell's documentation or contact your local extension office: http://cce.cornell.edu/localoffices

---

**Last Updated**: October 2024  
**Version**: 1.0  
**Based on**: Cornell Climate Smart Farming Program (climatesmartfarming.org)
