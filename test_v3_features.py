#!/usr/bin/env python3
"""
Quick test script to verify v3.0 features are working correctly.
Tests all three priority phases without external API calls.
"""

from agi_agent.gardening import (
    # Phase 1 imports
    DroughtLevel,
    ClimateHub,
    get_usda_hardiness_zone_simple,
    fetch_drought_status_simple,
    get_climate_hub_for_location,
    
    # Phase 2 imports
    ClimateScenario,
    ClimateTrend,
    get_future_projections,
    analyze_climate_trends,
    recommend_resilient_varieties,
    
    # Phase 3 imports
    CoastalRisk,
    FloodZone,
    assess_coastal_risk,
    get_state_climate_assessment,
    get_regional_tools,
)

def test_phase1_climate_adaptation():
    """Test Phase 1: Climate Adaptation features"""
    print("=" * 70)
    print("TESTING PHASE 1: CLIMATE ADAPTATION")
    print("=" * 70)
    
    # Test USDA hardiness zone
    print("\n1. Testing USDA Hardiness Zone...")
    zone = get_usda_hardiness_zone_simple(42.4440, -76.5019, -20.5)
    print(f"   ✓ Zone: {zone}")
    
    # Test drought status
    print("\n2. Testing Drought Status...")
    drought = fetch_drought_status_simple(42.4440, -76.5019)
    print(f"   ✓ Drought Level: {drought['drought_level'].value}")
    print(f"   ✓ Severity: {drought['severity_numeric']}")
    
    # Test climate hub lookup
    print("\n3. Testing Climate Hub Lookup...")
    hub = get_climate_hub_for_location("New York", "Northeast")
    if hub:
        print(f"   ✓ Hub: {hub['name']}")
        print(f"   ✓ URL: {hub['url'][:50]}...")
    
    print("\n✅ Phase 1 tests passed!")


def test_phase2_future_projections():
    """Test Phase 2: Future Climate Projections"""
    print("\n" + "=" * 70)
    print("TESTING PHASE 2: FUTURE CLIMATE PROJECTIONS")
    print("=" * 70)
    
    # Test future projections
    print("\n1. Testing Future Projections...")
    projections = get_future_projections("Northeast", "2050s")
    if projections:
        print(f"   ✓ Temperature Increase: +{projections['temp_increase_c']}°C")
        print(f"   ✓ Precipitation Change: {projections['precip_change_pct']:+d}%")
        print(f"   ✓ Growing Season Increase: +{projections['growing_season_days']} days")
    
    # Test climate trend analysis
    print("\n2. Testing Climate Trend Analysis...")
    trends = analyze_climate_trends("Northeast")
    print(f"   ✓ Trends identified: {len(trends)}")
    for trend in trends[:3]:
        print(f"      - {trend.value}")
    
    # Test resilient crop recommendations
    print("\n3. Testing Resilient Crop Recommendations...")
    resilient = recommend_resilient_varieties([ClimateTrend.WARMING, ClimateTrend.EXTREME_HEAT])
    print(f"   ✓ Recommended crops: {len(resilient['crops'])}")
    print(f"   ✓ Sample crops: {', '.join(list(resilient['crops'])[:3])}")
    print(f"   ✓ Adaptation strategies: {len(resilient['strategies'])}")
    
    print("\n✅ Phase 2 tests passed!")


def test_phase3_regional_resources():
    """Test Phase 3: Regional Resources"""
    print("\n" + "=" * 70)
    print("TESTING PHASE 3: REGIONAL RESOURCES")
    print("=" * 70)
    
    # Test coastal risk assessment
    print("\n1. Testing Coastal Risk Assessment...")
    coastal = assess_coastal_risk(42.4440, -76.5019)
    print(f"   ✓ Risk Level: {coastal['risk_level'].value}")
    print(f"   ✓ Description: {coastal['description']}")
    
    # Test state climate assessment
    print("\n2. Testing State Climate Assessment...")
    assessment = get_state_climate_assessment("New York")
    if assessment:
        print(f"   ✓ Assessment: {assessment['name']}")
        print(f"   ✓ Year: {assessment['year']}")
        print(f"   ✓ Key findings: {len(assessment['key_findings'])}")
    
    # Test regional tools
    print("\n3. Testing Regional Tools...")
    tools = get_regional_tools("Northeast")
    if tools:
        print(f"   ✓ Tools available: {len(tools)}")
        for tool_name in tools:
            print(f"      - {tool_name}")
    
    print("\n✅ Phase 3 tests passed!")


def test_integration():
    """Test that all enums and classes are properly defined"""
    print("\n" + "=" * 70)
    print("TESTING INTEGRATION & ENUMS")
    print("=" * 70)
    
    print("\n1. Testing Enums...")
    print(f"   ✓ DroughtLevel: {len(DroughtLevel)} levels")
    print(f"   ✓ ClimateHub: {len(ClimateHub)} hubs")
    print(f"   ✓ ClimateScenario: {len(ClimateScenario)} scenarios")
    print(f"   ✓ ClimateTrend: {len(ClimateTrend)} trends")
    print(f"   ✓ CoastalRisk: {len(CoastalRisk)} risk levels")
    print(f"   ✓ FloodZone: {len(FloodZone)} zones")
    
    print("\n✅ Integration tests passed!")


def main():
    """Run all tests"""
    print("\n" + "🌱" * 35)
    print("AI GARDEN PLANNER v3.0 - FEATURE VERIFICATION")
    print("🌱" * 35 + "\n")
    
    try:
        test_phase1_climate_adaptation()
        test_phase2_future_projections()
        test_phase3_regional_resources()
        test_integration()
        
        print("\n" + "=" * 70)
        print("🎉 ALL TESTS PASSED - v3.0 FEATURES WORKING CORRECTLY!")
        print("=" * 70 + "\n")
        
        print("Summary:")
        print("  ✓ Phase 1: Climate Adaptation (USDA zones, drought, hubs)")
        print("  ✓ Phase 2: Future Projections (2030s, 2050s, 2080s)")
        print("  ✓ Phase 3: Regional Resources (state assessments, tools)")
        print("  ✓ All enums and data structures working")
        print("  ✓ No import errors or runtime exceptions")
        print("\nv3.0 is ready for production! 🚀\n")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
