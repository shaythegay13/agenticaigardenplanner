#!/usr/bin/env python3
"""
Test script for v4.0 Phase 1: Visual Layout Generator
"""

from agi_agent.gardening.layout_generator import (
    generate_layout_guide,
    generate_layout,
    SpacingMethod,
    get_crop_size,
    PlantSize,
)


def test_layout_basic():
    """Test basic layout generation"""
    print("=" * 70)
    print("TEST 1: Basic 4x8 Bed Layout")
    print("=" * 70)
    print()
    
    crops = ["tomatoes", "basil", "lettuce", "carrots"]
    layout_guide = generate_layout_guide(crops, "4x8 bed")
    print(layout_guide)
    print()


def test_layout_companions():
    """Test layout with companion planting"""
    print("=" * 70)
    print("TEST 2: Layout with Companion Planting")
    print("=" * 70)
    print()
    
    # Crops known to be good companions
    crops = ["tomatoes", "basil", "marigolds", "lettuce", "carrots", "onions"]
    layout_guide = generate_layout_guide(crops, "4x8 bed")
    print(layout_guide)
    print()


def test_layout_intensive():
    """Test intensive spacing method"""
    print("=" * 70)
    print("TEST 3: Intensive Spacing Method")
    print("=" * 70)
    print()
    
    crops = ["lettuce", "radishes", "spinach", "green onions"]
    layout = generate_layout(crops, 4, 4, SpacingMethod.INTENSIVE)
    
    from agi_agent.gardening.layout_generator import generate_ascii_layout
    print(generate_ascii_layout(layout))
    print()


def test_large_garden():
    """Test larger garden bed"""
    print("=" * 70)
    print("TEST 4: Large Garden Bed (8x12)")
    print("=" * 70)
    print()
    
    crops = [
        "tomatoes", "peppers", "eggplant",
        "cucumbers", "squash",
        "beans", "peas",
        "lettuce", "spinach", "basil", "marigolds"
    ]
    layout_guide = generate_layout_guide(crops, "8x12 bed")
    print(layout_guide)
    print()


def test_crop_sizes():
    """Test crop size classification"""
    print("=" * 70)
    print("TEST 5: Crop Size Classification")
    print("=" * 70)
    print()
    
    test_crops = [
        "tomatoes", "lettuce", "peppers", "cucumbers",
        "radishes", "corn", "basil", "squash", "carrots"
    ]
    
    for crop in test_crops:
        size = get_crop_size(crop)
        print(f"  {crop.title():15} -> {size.value}")
    print()


def test_three_sisters():
    """Test Three Sisters planting layout"""
    print("=" * 70)
    print("TEST 6: Three Sisters Planting")
    print("=" * 70)
    print()
    
    crops = ["corn", "beans", "squash"]
    layout_guide = generate_layout_guide(crops, "10x10 bed")
    print(layout_guide)
    print()


def main():
    """Run all layout generator tests"""
    print()
    print("🌱" * 35)
    print("AI GARDEN PLANNER v4.0 - PHASE 1 LAYOUT GENERATOR TEST")
    print("🌱" * 35)
    print()
    
    try:
        test_layout_basic()
        test_layout_companions()
        test_layout_intensive()
        test_large_garden()
        test_crop_sizes()
        test_three_sisters()
        
        print("=" * 70)
        print("✅ ALL LAYOUT TESTS COMPLETED!")
        print("=" * 70)
        print()
        print("v4.0 Phase 1 - Visual Layout Generator is working! 🚀")
        print()
        
        return 0
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
