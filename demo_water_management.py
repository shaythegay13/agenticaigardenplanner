#!/usr/bin/env python3
"""
Demo script showing the new water management and seasonal planning features.
This can be run standalone to test the new Cornell CSF-based functionality.
"""

from datetime import date, timedelta
from agi_agent.gardening.water_management import (
    SoilType,
    CropWaterUse,
    simulate_water_deficit,
    generate_irrigation_recommendation,
    estimate_reference_et_hargreaves,
)
from agi_agent.gardening.seasonal_planning import (
    CoverCropType,
    estimate_cover_crop_window,
    generate_cover_crop_recommendations,
    generate_succession_planting_schedule,
    recommend_succession_crops,
)


def demo_water_management():
    """Demonstrate water deficit calculations"""
    print("=" * 70)
    print("WATER DEFICIT ANALYSIS DEMO")
    print("=" * 70)
    
    # Simulated 7-day forecast for NYC in summer
    daily_highs_c = [28.0, 30.0, 29.0, 27.0, 26.0, 25.0, 28.0]
    daily_lows_c = [18.0, 20.0, 19.0, 17.0, 16.0, 15.0, 18.0]
    daily_precip_mm = [0.0, 0.0, 5.0, 15.0, 0.0, 0.0, 0.0]  # Rain on days 3 and 4
    latitude = 40.7128  # NYC
    
    print("\n📊 Forecast Data (7 days):")
    print(f"Location: New York City (lat: {latitude})")
    print(f"High Temps (°C): {daily_highs_c}")
    print(f"Low Temps (°C): {daily_lows_c}")
    print(f"Precipitation (mm): {daily_precip_mm}")
    
    # Test with different soil types
    for soil_type in [SoilType.HIGH, SoilType.MEDIUM, SoilType.LOW]:
        print(f"\n{'─' * 70}")
        print(f"Soil Type: {soil_type.value}")
        print(f"{'─' * 70}")
        
        results = simulate_water_deficit(
            daily_highs_c=daily_highs_c,
            daily_lows_c=daily_lows_c,
            daily_precip_mm=daily_precip_mm,
            latitude=latitude,
            start_date=date.today(),
            soil_type=soil_type,
            crop_type=CropWaterUse.TOMATOES_PEPPERS,
        )
        
        print("\n📅 Daily Water Balance:")
        print(f"{'Day':<5} {'Water':<8} {'Deficit':<8} {'Precip':<8} {'ET':<8} {'Stress':<10}")
        print(f"{'':5} {'(in)':<8} {'(in)':<8} {'(in)':<8} {'(in)':<8} {'Level':<10}")
        print("─" * 70)
        
        for i, day in enumerate(results, 1):
            print(f"{i:<5} {day['water_content_inches']:<8.3f} {day['water_deficit_inches']:<8.3f} "
                  f"{day['precipitation_inches']:<8.3f} {day['et_inches']:<8.3f} {day['stress_level']:<10}")
        
        print(f"\n💧 Irrigation Recommendation:")
        print("─" * 70)
        recommendation = generate_irrigation_recommendation(results)
        print(recommendation)
        print()


def demo_et_calculation():
    """Demonstrate ET calculation"""
    print("\n" + "=" * 70)
    print("EVAPOTRANSPIRATION CALCULATION DEMO")
    print("=" * 70)
    
    latitude = 40.7128  # NYC
    day_of_year = date.today().timetuple().tm_yday
    
    print(f"\nLocation: NYC (lat: {latitude})")
    print(f"Day of Year: {day_of_year}")
    print("\nET Calculation for Different Temperature Ranges:")
    print(f"{'High (°C)':<12} {'Low (°C)':<12} {'ET (inches/day)':<18}")
    print("─" * 70)
    
    temp_scenarios = [
        (25, 15),  # Mild
        (30, 20),  # Warm
        (35, 25),  # Hot
        (20, 10),  # Cool
    ]
    
    for high, low in temp_scenarios:
        et = estimate_reference_et_hargreaves(high, low, latitude, day_of_year)
        print(f"{high:<12} {low:<12} {et:<18.3f}")


def demo_seasonal_planning():
    """Demonstrate seasonal planning features"""
    print("\n" + "=" * 70)
    print("SEASONAL PLANNING DEMO")
    print("=" * 70)
    
    current_date = date.today()
    # Assume first frost in mid-October
    first_frost = date(current_date.year, 10, 15)
    
    print(f"\nCurrent Date: {current_date.strftime('%B %d, %Y')}")
    print(f"Expected First Frost: {first_frost.strftime('%B %d, %Y')}")
    
    print("\n🌱 Cover Crop Planting Windows:")
    print("─" * 70)
    
    for cover_crop in [CoverCropType.WINTER_RYE, CoverCropType.BUCKWHEAT, 
                       CoverCropType.CRIMSON_CLOVER, CoverCropType.RADISH]:
        window = estimate_cover_crop_window(
            current_date=current_date,
            first_frost_date=first_frost,
            cover_crop=cover_crop,
            avg_daily_gdd=10.0
        )
        print(f"\n{cover_crop.value}:")
        print(f"  Status: {window['status']}")
        print(f"  Optimal Start: {window['optimal_start']}")
        print(f"  Latest Date: {window['latest_date']}")
        print(f"  Message: {window['message']}")
    
    print("\n\n🔄 Succession Planting Recommendations:")
    print("─" * 70)
    
    succession_crops = recommend_succession_crops()
    for crop in succession_crops[:5]:  # Show first 5
        print(f"\n{crop['name']} ({crop['season']} season):")
        print(f"  Days to Harvest: {crop['days_to_harvest']}")
        print(f"  Planting Interval: every {crop['interval_days']} days")
        print(f"  Notes: {crop['notes']}")


def demo_succession_schedule():
    """Generate a sample succession planting schedule"""
    print("\n" + "=" * 70)
    print("SUCCESSION SCHEDULE EXAMPLE")
    print("=" * 70)
    
    # Example: Lettuce succession planting for spring
    start_date = date(2024, 4, 1)  # April 1
    end_date = date(2024, 6, 15)   # June 15
    
    schedule = generate_succession_planting_schedule(
        start_date=start_date,
        end_date=end_date,
        crop_name="Lettuce",
        days_to_harvest=45,
        planting_interval_days=14
    )
    
    print("\nLettuce Succession Schedule (Spring):")
    print(f"{'Planting #':<12} {'Plant Date':<15} {'Harvest Date':<15}")
    print("─" * 70)
    
    for i, planting in enumerate(schedule, 1):
        print(f"{i:<12} {planting['planting_date']:<15} {planting['expected_harvest']:<15}")
    
    print(f"\nTotal Plantings: {len(schedule)}")
    print("Result: Continuous lettuce harvest for 2.5 months!")


def main():
    """Run all demos"""
    print("\n" + "█" * 70)
    print("  CORNELL CSF-BASED GARDEN PLANNING FEATURES DEMO")
    print("█" * 70)
    
    try:
        demo_et_calculation()
        demo_water_management()
        demo_seasonal_planning()
        demo_succession_schedule()
        
        print("\n" + "=" * 70)
        print("✅ All demos completed successfully!")
        print("=" * 70)
        print("\nThese features are now integrated into the main garden planner.")
        print("Run: python3 -m agi_agent.cli")
        print("=" * 70 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error during demo: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
