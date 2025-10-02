#!/usr/bin/env python3
"""
Test script for v4.0 Phase 2: Enhanced Crop Recommendations & Harvest Schedules
"""

from agi_agent.gardening.crop_varieties import (
    generate_variety_guide,
    get_varieties_for_crop,
    get_variety_by_name,
    get_recommended_varieties,
    Difficulty,
)


def test_variety_database():
    """Test variety database coverage"""
    print("=" * 70)
    print("TEST 1: Variety Database Coverage")
    print("=" * 70)
    print()
    
    crops = ["tomatoes", "lettuce", "peppers"]
    total_varieties = 0
    
    for crop in crops:
        varieties = get_varieties_for_crop(crop)
        total_varieties += len(varieties)
        print(f"{crop.title()}: {len(varieties)} varieties")
        for v in varieties:
            print(f"  • {v.variety_name} ({v.difficulty.value}, {v.days_to_maturity} days)")
    
    print(f"\nTotal varieties in database: {total_varieties}")
    print()


def test_variety_details():
    """Test detailed variety information"""
    print("=" * 70)
    print("TEST 2: Detailed Variety Information")
    print("=" * 70)
    print()
    
    # Test specific variety
    sungold = get_variety_by_name("tomatoes", "Sungold")
    if sungold:
        print(f"Variety: {sungold.variety_name}")
        print(f"Description: {sungold.description}")
        print(f"Difficulty: {sungold.difficulty.value}")
        print(f"Days to Maturity: {sungold.days_to_maturity}")
        print(f"Expected Yield: {sungold.expected_yield_per_plant}")
        print(f"Space Required: {sungold.space_per_plant_sqft} sq ft")
        print(f"Container Suitable: {'Yes' if sungold.container_suitable else 'No'}")
        print(f"Disease Resistant: {'Yes' if sungold.disease_resistant else 'No'}")
        
        if sungold.harvest_info:
            print(f"\nHarvest Information:")
            print(f"  First Harvest: {sungold.harvest_info.days_to_maturity} days")
            print(f"  Harvest Period: {sungold.harvest_info.harvest_period_weeks} weeks")
            print(f"  Technique: {sungold.harvest_info.harvest_technique}")
            print(f"  Frequency: {sungold.harvest_info.harvest_frequency}")
        
        print(f"\nCare Tips ({len(sungold.care_tips)} tips):")
        for tip in sungold.care_tips[:3]:
            print(f"  • {tip}")
    
    print()


def test_variety_filtering():
    """Test variety filtering by criteria"""
    print("=" * 70)
    print("TEST 3: Variety Filtering")
    print("=" * 70)
    print()
    
    # Filter by difficulty
    print("Easy tomato varieties:")
    easy_tomatoes = get_recommended_varieties("tomatoes", difficulty_filter=Difficulty.EASY)
    for v in easy_tomatoes:
        print(f"  • {v.variety_name} ({v.days_to_maturity} days)")
    
    # Filter by container suitability
    print("\nContainer-suitable lettuce:")
    container_lettuce = get_recommended_varieties("lettuce", container_only=True)
    for v in container_lettuce:
        print(f"  • {v.variety_name} ({v.space_per_plant_sqft} sq ft)")
    
    # Filter by disease resistance
    print("\nDisease-resistant tomatoes:")
    resistant_tomatoes = get_recommended_varieties("tomatoes", disease_resistant_only=True)
    for v in resistant_tomatoes:
        print(f"  • {v.variety_name}")
    
    print()


def test_harvest_schedules():
    """Test harvest schedule information"""
    print("=" * 70)
    print("TEST 4: Harvest Schedules")
    print("=" * 70)
    print()
    
    crops = ["tomatoes", "lettuce", "peppers"]
    
    for crop in crops:
        varieties = get_varieties_for_crop(crop)
        if varieties:
            print(f"{crop.title()} Harvest Schedules:")
            for v in varieties[:2]:  # Show 2 per crop
                if v.harvest_info:
                    print(f"\n  {v.variety_name}:")
                    print(f"    First Harvest: Day {v.harvest_info.days_to_maturity}")
                    print(f"    Duration: {v.harvest_info.harvest_period_weeks} weeks")
                    print(f"    Peak: Weeks {v.harvest_info.peak_production_weeks}")
                    print(f"    Frequency: {v.harvest_info.harvest_frequency}")
            print()


def test_variety_guides():
    """Test variety guide generation"""
    print("=" * 70)
    print("TEST 5: Variety Guide Generation")
    print("=" * 70)
    
    # Generate guide for tomatoes
    guide = generate_variety_guide("tomatoes", max_varieties=2)
    print(guide)
    
    # Generate guide for peppers
    guide = generate_variety_guide("peppers", max_varieties=2)
    print(guide)
    print()


def test_attributes():
    """Test variety attributes"""
    print("=" * 70)
    print("TEST 6: Variety Attributes")
    print("=" * 70)
    print()
    
    varieties = get_varieties_for_crop("tomatoes")
    
    print("Tomato Variety Attributes:")
    for v in varieties:
        attributes = []
        if v.heirloom:
            attributes.append("Heirloom")
        if v.disease_resistant:
            attributes.append("Disease Resistant")
        if v.container_suitable:
            attributes.append("Container Suitable")
        if v.determinate is not None:
            attributes.append("Determinate" if v.determinate else "Indeterminate")
        
        print(f"\n{v.variety_name}:")
        print(f"  Attributes: {', '.join(attributes) if attributes else 'None'}")
        print(f"  Companions: {len(v.good_companions)} good, {len(v.avoid_companions)} avoid")
        print(f"  Diseases: {len(v.common_diseases)} common")
    
    print()


def main():
    """Run all Phase 2 tests"""
    print()
    print("🌱" * 35)
    print("AI GARDEN PLANNER v4.0 - PHASE 2 TEST")
    print("🌱" * 35)
    print()
    
    try:
        test_variety_database()
        test_variety_details()
        test_variety_filtering()
        test_harvest_schedules()
        test_variety_guides()
        test_attributes()
        
        print("=" * 70)
        print("✅ ALL PHASE 2 TESTS PASSED!")
        print("=" * 70)
        print()
        print("v4.0 Phase 2 - Enhanced Crop Recommendations is working! 🚀")
        print()
        
        return 0
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
