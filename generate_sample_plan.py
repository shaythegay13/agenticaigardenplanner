#!/usr/bin/env python3
"""
Generate a sample garden plan to show the user
"""

from agi_agent.gardening.models import (
    UserInput,
    LocationInput,
    GardeningMethod,
    SpaceSize,
    Sunlight,
    Experience,
    UserGoals,
    CropInterest,
    Preference,
    SoilType,
)
from agi_agent.gardening.climate import geocode_location, fetch_simple_forecast
from agi_agent.gardening.planner import generate_plan

# Create sample user profile - NYC beginner gardener
print("Generating sample garden plan...")
print("Location: New York City")
print("Profile: Beginner, Raised Beds, Medium Space, Full Sun")
print()

user = UserInput(
    method=GardeningMethod.RAISED_BEDS,
    size=SpaceSize.MEDIUM,
    sunlight=Sunlight.FULL_SUN,
    soil_type=SoilType.MEDIUM,
    experience=Experience.BEGINNER,
    goals=UserGoals(
        crops=[CropInterest.TOMATOES, CropInterest.HERBS, CropInterest.LEAFY_GREENS],
        preferences=[Preference.FAST_GROWING, Preference.LOW_MAINTENANCE]
    ),
    location=LocationInput(
        latitude=40.8255,
        longitude=-73.9493,
        address='New York, NY'
    )
)

# Get climate data
try:
    climate = fetch_simple_forecast(user.location.latitude, user.location.longitude)
    
    # Generate plan
    plan = generate_plan(user, climate)
    
    # Print the plan
    print(plan)
    
except Exception as e:
    print(f"Error generating plan: {e}")
    import traceback
    traceback.print_exc()
