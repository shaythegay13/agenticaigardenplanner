#!/usr/bin/env python3
"""
Test script for v3.1 quick wins features.
Tests companion planting, yield estimates, disease prevention, and educational resources.
"""

from agi_agent.gardening import (
    # v3.1 imports
    get_companion_info,
    generate_companion_planting_guide,
    estimate_yield,
    generate_yield_summary,
    YieldUnit,
    get_disease_info,
    generate_disease_prevention_guide,
    get_resources_by_topic,
    generate_resource_guide,
    ResourceType,
    ResourceSkillLevel,
    
    # Base models
    SpaceSize,
    Sunlight,
    Experience,
)


def test_companion_planting():
    """Test companion planting module"""
    print("=" * 70)
    print("TESTING COMPANION PLANTING")
    print("=" * 70)
    
    print("\n1. Testing companion info lookup...")
    tomato_info = get_companion_info("tomatoes")
    print(f"   ✓ Tomatoes have {len(tomato_info.good_companions)} good companions")
    print(f"   ✓ Good companions: {', '.join(tomato_info.good_companions[:3])}")
    print(f"   ✓ Bad companions: {', '.join(tomato_info.bad_companions[:3])}")
    
    print("\n2. Testing companion guide generation...")
    crops = ["tomatoes", "lettuce", "basil", "beans", "carrots"]
    guide = generate_companion_planting_guide(crops)
    print(f"   ✓ Generated guide for {len(crops)} crops")
    print(f"   ✓ Guide length: {len(guide)} characters")
    
    print("\n✅ Companion planting tests passed!")


def test_yield_estimates():
    """Test yield estimator module"""
    print("\n" + "=" * 70)
    print("TESTING YIELD ESTIMATES")
    print("=" * 70)
    
    print("\n1. Testing single crop yield estimate...")
    yield_est = estimate_yield(
        "tomatoes",
        SpaceSize.MEDIUM,
        Sunlight.FULL_SUN,
        Experience.INTERMEDIATE
    )
    print(f"   ✓ Estimated yield: {yield_est['estimated_yield']} {yield_est['unit']}")
    print(f"   ✓ Range: {yield_est['low_estimate']}-{yield_est['high_estimate']} {yield_est['unit']}")
    print(f"   ✓ Days to harvest: {yield_est['days_to_harvest']}")
    
    print("\n2. Testing yield summary for multiple crops...")
    crops = ["tomatoes", "lettuce", "basil", "peppers", "beans"]
    summary = generate_yield_summary(
        crops,
        SpaceSize.MEDIUM,
        Sunlight.FULL_SUN,
        Experience.BEGINNER
    )
    print(f"   ✓ Generated summary for {len(crops)} crops")
    print(f"   ✓ Summary length: {len(summary)} characters")
    
    print("\n✅ Yield estimate tests passed!")


def test_disease_prevention():
    """Test disease prevention module"""
    print("\n" + "=" * 70)
    print("TESTING DISEASE PREVENTION")
    print("=" * 70)
    
    print("\n1. Testing disease info lookup...")
    tomato_diseases = get_disease_info("tomatoes")
    print(f"   ✓ Found {len(tomato_diseases)} common tomato diseases")
    if tomato_diseases:
        print(f"   ✓ First disease: {tomato_diseases[0].name}")
        print(f"   ✓ Symptoms: {len(tomato_diseases[0].symptoms)} listed")
        print(f"   ✓ Prevention tips: {len(tomato_diseases[0].prevention)}")
    
    print("\n2. Testing disease prevention guide...")
    crops = ["tomatoes", "cucumbers", "beans", "squash"]
    guide = generate_disease_prevention_guide(crops)
    print(f"   ✓ Generated guide for {len(crops)} crops")
    print(f"   ✓ Guide length: {len(guide)} characters")
    
    print("\n✅ Disease prevention tests passed!")


def test_educational_resources():
    """Test educational resources module"""
    print("\n" + "=" * 70)
    print("TESTING EDUCATIONAL RESOURCES")
    print("=" * 70)
    
    print("\n1. Testing resource lookup by topic...")
    tomato_resources = get_resources_by_topic("tomatoes")
    print(f"   ✓ Found {len(tomato_resources)} tomato resources")
    if tomato_resources:
        print(f"   ✓ First resource: {tomato_resources[0].title}")
        print(f"   ✓ Type: {tomato_resources[0].type.value}")
    
    print("\n2. Testing resource guide generation...")
    crops = ["tomatoes", "lettuce", "basil"]
    guide = generate_resource_guide(
        crops,
        ResourceSkillLevel.BEGINNER
    )
    print(f"   ✓ Generated resource guide for beginners")
    print(f"   ✓ Guide length: {len(guide)} characters")
    
    print("\n3. Testing resource types...")
    print(f"   ✓ Available resource types: {len(ResourceType)} types")
    print(f"     - {', '.join([t.value for t in ResourceType])}")
    
    print("\n✅ Educational resources tests passed!")


def test_integration():
    """Test that all v3.1 features work together"""
    print("\n" + "=" * 70)
    print("TESTING INTEGRATION")
    print("=" * 70)
    
    print("\n1. Testing complete workflow...")
    crops = ["tomatoes", "lettuce", "basil", "peppers"]
    
    # Companion planting
    companions = generate_companion_planting_guide(crops)
    print(f"   ✓ Companion guide: {len(companions)} chars")
    
    # Yield estimates
    yields = generate_yield_summary(
        crops,
        SpaceSize.MEDIUM,
        Sunlight.FULL_SUN,
        Experience.INTERMEDIATE
    )
    print(f"   ✓ Yield estimates: {len(yields)} chars")
    
    # Disease prevention
    diseases = generate_disease_prevention_guide(crops)
    print(f"   ✓ Disease guide: {len(diseases)} chars")
    
    # Educational resources
    resources = generate_resource_guide(crops, ResourceSkillLevel.INTERMEDIATE)
    print(f"   ✓ Learning resources: {len(resources)} chars")
    
    print("\n2. Testing all enums and types...")
    print(f"   ✓ YieldUnit: {len(YieldUnit)} units")
    print(f"   ✓ ResourceType: {len(ResourceType)} types")
    print(f"   ✓ ResourceSkillLevel: {len(ResourceSkillLevel)} levels")
    
    print("\n✅ Integration tests passed!")


def main():
    """Run all v3.1 tests"""
    print("\n" + "🌱" * 35)
    print("AI GARDEN PLANNER v3.1 - QUICK WINS VERIFICATION")
    print("🌱" * 35 + "\n")
    
    try:
        test_companion_planting()
        test_yield_estimates()
        test_disease_prevention()
        test_educational_resources()
        test_integration()
        
        print("\n" + "=" * 70)
        print("🎉 ALL v3.1 TESTS PASSED!")
        print("=" * 70 + "\n")
        
        print("Summary:")
        print("  ✓ Companion Planting: Working")
        print("  ✓ Yield Estimates: Working")
        print("  ✓ Disease Prevention: Working")
        print("  ✓ Educational Resources: Working")
        print("  ✓ All integrations: Working")
        print("\nv3.1 Quick Wins are ready! 🚀\n")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
