#!/usr/bin/env python3
"""
Comprehensive test suite to verify all features are functional
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Test 1: Verify all imports work"""
    print("\n" + "="*60)
    print("TEST 1: Verifying Imports")
    print("="*60)

    try:
        from src.models import Client, Protocol, WeightUnit, Language, Meal, MealType, DayType
        from src.models import Food, FoodCategory, Supplement, SupplementStack, Macros
        print("✅ Models imported successfully")

        from src.calculators import LBMCalculator, MacroCalculator
        print("✅ Calculators imported successfully")

        from src.database import FoodDatabase, SupplementDatabase
        print("✅ Databases imported successfully")

        from src.generators import MealPlanGenerator
        print("✅ Generators imported successfully")

        from src.exporters import MarkdownExporter
        print("✅ Exporters imported successfully")

        from src.utils import InputCollector
        print("✅ Utils imported successfully")

        return True
    except Exception as e:
        print(f"❌ Import failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_data_models():
    """Test 2: Verify data models and validation"""
    print("\n" + "="*60)
    print("TEST 2: Testing Data Models")
    print("="*60)

    try:
        from src.models import Client, Protocol, WeightUnit, Macros

        # Create a valid client
        client = Client(
            name="Test Client",
            weight=180,
            weight_unit=WeightUnit.LBS,
            body_fat_percentage=15.0,
            protocol=Protocol.SHREDDED,
            training_days=["Monday", "Wednesday", "Friday"],
            high_days=["Saturday"],
            language="en"
        )
        print(f"✅ Client model created: {client.name}")

        # Test weight conversion
        weight_lbs = client.get_weight_in_lbs()
        weight_kg = client.get_weight_in_kg()
        print(f"✅ Weight conversion: {weight_lbs:.1f} lbs = {weight_kg:.1f} kg")

        # Test macros
        macros = Macros(protein=50, carbs=25, fat=4)
        calories = macros.calculate_calories()
        print(f"✅ Macros calculation: {macros} = {calories} cal")

        # Test validation (should fail)
        try:
            invalid_client = Client(
                name="",  # Invalid: empty name
                weight=180,
                weight_unit=WeightUnit.LBS,
                body_fat_percentage=15.0,
                protocol=Protocol.SHREDDED,
                training_days=["Monday"],
                high_days=["Saturday"],
                language="en"
            )
            print("❌ Validation should have failed for empty name")
            return False
        except:
            print("✅ Validation correctly rejected invalid data")

        return True
    except Exception as e:
        print(f"❌ Data model test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_calculators():
    """Test 3: Test calculation engines"""
    print("\n" + "="*60)
    print("TEST 3: Testing Calculators")
    print("="*60)

    try:
        from src.models import Client, Protocol, WeightUnit, DayType
        from src.calculators import LBMCalculator, MacroCalculator

        # Create test client
        client = Client(
            name="Test Client",
            weight=180,
            weight_unit=WeightUnit.LBS,
            body_fat_percentage=15.0,
            protocol=Protocol.SHREDDED,
            training_days=["Monday"],
            high_days=["Saturday"],
            language="en"
        )

        # Test LBM calculation
        lbm = LBMCalculator.calculate_lbm(client)
        expected_lbm = 180 * (1 - 0.15)  # 153
        print(f"✅ LBM calculated: {lbm} lbs (expected: {expected_lbm})")

        if abs(lbm - expected_lbm) > 0.1:
            print(f"❌ LBM calculation error: {lbm} != {expected_lbm}")
            return False

        # Test protein per meal
        protein = LBMCalculator.calculate_protein_per_meal(lbm)
        print(f"✅ Protein per meal: {protein}g")

        # Test macro calculations for different day types
        for day_type in [DayType.LOW, DayType.MEDIUM, DayType.HIGH]:
            macros = MacroCalculator.calculate_day_macros(Protocol.SHREDDED, day_type)
            print(f"✅ SHREDDED {day_type.value}: {macros}")

        # Test meal structure
        structure = MacroCalculator.get_meal_structure(Protocol.SHREDDED, DayType.LOW)
        print(f"✅ Meal structure retrieved: {len(structure)} meal groups")

        # Test cardio recommendation
        cardio = MacroCalculator.get_cardio_recommendation(Protocol.SHREDDED)
        print(f"✅ Cardio recommendation: {cardio}")

        return True
    except Exception as e:
        print(f"❌ Calculator test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_databases():
    """Test 4: Test food and supplement databases"""
    print("\n" + "="*60)
    print("TEST 4: Testing Databases")
    print("="*60)

    try:
        from src.database import FoodDatabase, SupplementDatabase
        from src.models import Protocol, FoodCategory

        # Test food database
        food_db = FoodDatabase()

        all_foods = food_db.get_all_foods()
        print(f"✅ Food database loaded: {len(all_foods)} items")

        proteins = food_db.get_protein_sources(preferred_only=True)
        print(f"✅ Preferred proteins: {len(proteins)} items")

        carbs = food_db.get_carb_sources(preferred_only=False, allow_sugary=True)
        print(f"✅ Carb sources (all): {len(carbs)} items")

        fats = food_db.get_fat_sources()
        print(f"✅ Fat sources: {len(fats)} items")

        veggies = food_db.get_vegetables()
        print(f"✅ Vegetables: {len(veggies)} items")

        # Test specific food
        chicken = food_db.get_food_by_name("Chicken Breast")
        if chicken:
            print(f"✅ Food lookup: {chicken.name} - {chicken.protein_per_serving}p per {chicken.serving_size}")

            # Test serving calculation
            servings, macros = chicken.calculate_serving_for_protein(50)
            print(f"✅ Serving calculation: {servings} servings for 50g protein = {macros}")
        else:
            print("❌ Chicken Breast not found in database")
            return False

        # Test supplement database
        supp_db = SupplementDatabase()

        cutting_stack = supp_db.get_cutting_stack()
        print(f"✅ Cutting stack: {len(cutting_stack.supplements)} supplements")

        bulking_stack = supp_db.get_bulking_stack()
        print(f"✅ Bulking stack: {len(bulking_stack.supplements)} supplements")

        # Test stack for protocol
        shredded_stack = supp_db.get_recommended_stack(Protocol.SHREDDED)
        massive_stack = supp_db.get_recommended_stack(Protocol.MASSIVE)
        print(f"✅ Protocol stacks retrieved")

        min_cost, max_cost = shredded_stack.calculate_total_cost()
        print(f"✅ Cost calculation: ${min_cost:.0f} - ${max_cost:.0f}/month")

        return True
    except Exception as e:
        print(f"❌ Database test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_meal_plan_generator():
    """Test 5: Test meal plan generation"""
    print("\n" + "="*60)
    print("TEST 5: Testing Meal Plan Generator")
    print("="*60)

    try:
        from src.models import Client, Protocol, WeightUnit
        from src.generators import MealPlanGenerator

        # Create test client
        client = Client(
            name="Test Client",
            weight=180,
            weight_unit=WeightUnit.LBS,
            body_fat_percentage=15.0,
            protocol=Protocol.SHREDDED,
            training_days=["Monday", "Wednesday", "Friday"],
            high_days=["Saturday"],
            language="en"
        )

        generator = MealPlanGenerator()

        # Test day type determination
        day_type, is_training = generator.determine_day_type("Monday", client.training_days, client.high_days)
        print(f"✅ Day type determination: Monday = {day_type.value}, Training: {is_training}")

        # Test meal times generation
        meal_times = generator.generate_meal_times(day_type, is_training)
        print(f"✅ Meal times generated: {len(meal_times)} time slots")

        # Test single day plan
        day_plan = generator.generate_day_plan(client, "Monday", 153.0)
        print(f"✅ Day plan generated: {day_plan.day_name} - {len(day_plan.meals)} meals")

        total_macros = day_plan.get_total_macros()
        total_calories = day_plan.get_total_calories()
        print(f"✅ Day totals: {total_macros} = {total_calories} cal")

        # Test week plan
        week_plan = generator.generate_week_plan(client, week_number=1)
        print(f"✅ Week plan generated: {len(week_plan.days)} days")
        print(f"   Client: {week_plan.client_name}")
        print(f"   LBM: {week_plan.lean_body_mass} lbs")
        print(f"   Protocol: {week_plan.protocol}")

        # Verify all days have meals
        for day in week_plan.days:
            if len(day.meals) == 0:
                print(f"❌ {day.day_name} has no meals!")
                return False

        print(f"✅ All days have meals")

        # Test protocol summary
        summary = generator.get_protocol_summary(client)
        print(f"✅ Protocol summary generated with {len(summary)} fields")

        return True
    except Exception as e:
        print(f"❌ Meal plan generator test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_markdown_export():
    """Test 6: Test markdown export"""
    print("\n" + "="*60)
    print("TEST 6: Testing Markdown Export")
    print("="*60)

    try:
        from src.models import Client, Protocol, WeightUnit
        from src.generators import MealPlanGenerator
        from src.database import SupplementDatabase
        from src.exporters import MarkdownExporter

        # Create test client and plan
        client = Client(
            name="Test Client",
            weight=180,
            weight_unit=WeightUnit.LBS,
            body_fat_percentage=15.0,
            protocol=Protocol.SHREDDED,
            training_days=["Monday", "Wednesday", "Friday"],
            high_days=["Saturday"],
            language="en"
        )

        generator = MealPlanGenerator()
        week_plan = generator.generate_week_plan(client)

        # Test week plan export
        week_md = MarkdownExporter.export_week_plan(week_plan, include_food_suggestions=True)
        print(f"✅ Week plan markdown generated: {len(week_md)} characters")

        if "SHREDDED Protocol" not in week_md:
            print("❌ Week plan missing protocol header")
            return False

        # Test day plan export
        day_md = MarkdownExporter.export_day_plan(week_plan.days[0], include_food_suggestions=True)
        print(f"✅ Day plan markdown generated: {len(day_md)} characters")

        # Test supplement stack export
        supp_db = SupplementDatabase()
        stack = supp_db.get_recommended_stack(client.protocol)
        supp_md = MarkdownExporter.export_supplement_stack(stack)
        print(f"✅ Supplement stack markdown generated: {len(supp_md)} characters")

        # Test protocol summary export
        summary = generator.get_protocol_summary(client)
        summary_md = MarkdownExporter.export_protocol_summary(summary)
        print(f"✅ Protocol summary markdown generated: {len(summary_md)} characters")

        # Test file saving
        test_content = "# Test File\n\nThis is a test."
        test_path = MarkdownExporter.save_to_file(test_content, "test_export.md")
        print(f"✅ File saved to: {test_path}")

        # Verify file exists
        if not os.path.exists(test_path):
            print(f"❌ File not found at {test_path}")
            return False

        # Clean up test file
        os.remove(test_path)
        print(f"✅ Test file cleaned up")

        return True
    except Exception as e:
        print(f"❌ Markdown export test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_integration():
    """Test 7: Full integration test"""
    print("\n" + "="*60)
    print("TEST 7: Integration Test (Full Workflow)")
    print("="*60)

    try:
        from src.models import Client, Protocol, WeightUnit
        from src.generators import MealPlanGenerator
        from src.database import SupplementDatabase
        from src.exporters import MarkdownExporter
        from datetime import datetime

        # Simulate full workflow
        print("\n1. Creating client...")
        client = Client(
            name="Integration Test Client",
            weight=200,
            weight_unit=WeightUnit.LBS,
            body_fat_percentage=20.0,
            height=72,
            protocol=Protocol.MASSIVE,
            training_days=["Monday", "Tuesday", "Thursday", "Friday"],
            high_days=["Tuesday", "Friday"],
            language="en"
        )
        print(f"   ✅ Client created: {client.name}")

        print("\n2. Generating meal plan...")
        generator = MealPlanGenerator()
        week_plan = generator.generate_week_plan(client, week_number=1)
        print(f"   ✅ Week plan generated")
        print(f"      LBM: {week_plan.lean_body_mass} lbs")
        print(f"      Days: {len(week_plan.days)}")

        print("\n3. Getting supplement recommendations...")
        supp_db = SupplementDatabase()
        supplement_stack = supp_db.get_recommended_stack(client.protocol)
        print(f"   ✅ Supplement stack: {supplement_stack.stack_name}")
        print(f"      Supplements: {len(supplement_stack.supplements)}")

        print("\n4. Getting protocol summary...")
        summary = generator.get_protocol_summary(client)
        print(f"   ✅ Summary generated with {len(summary)} fields")

        print("\n5. Exporting to markdown...")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Export week plan
        week_md = MarkdownExporter.export_week_plan(week_plan, include_food_suggestions=True)
        week_path = MarkdownExporter.save_to_file(week_md, f"TEST_Week_{timestamp}.md")
        print(f"   ✅ Week plan saved: {os.path.basename(week_path)}")

        # Export supplements
        supp_md = MarkdownExporter.export_supplement_stack(supplement_stack)
        supp_path = MarkdownExporter.save_to_file(supp_md, f"TEST_Supplements_{timestamp}.md")
        print(f"   ✅ Supplements saved: {os.path.basename(supp_path)}")

        # Export summary
        summary_md = MarkdownExporter.export_protocol_summary(summary)
        summary_path = MarkdownExporter.save_to_file(summary_md, f"TEST_Summary_{timestamp}.md")
        print(f"   ✅ Summary saved: {os.path.basename(summary_path)}")

        print("\n6. Verifying output files...")
        for path in [week_path, supp_path, summary_path]:
            if not os.path.exists(path):
                print(f"   ❌ File not found: {path}")
                return False
            size = os.path.getsize(path)
            print(f"   ✅ {os.path.basename(path)}: {size} bytes")

        print("\n7. Validating content...")
        with open(week_path, 'r') as f:
            content = f.read()
            if "MASSIVE Protocol" not in content:
                print("   ❌ Week plan missing protocol header")
                return False
            if "Monday" not in content:
                print("   ❌ Week plan missing days")
                return False
            print("   ✅ Week plan content validated")

        print("\n8. Cleaning up test files...")
        for path in [week_path, supp_path, summary_path]:
            os.remove(path)
        print("   ✅ Test files cleaned up")

        return True
    except Exception as e:
        print(f"❌ Integration test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("\n" + "="*70)
    print(" "*15 + "FITLIFE MEAL PLAN GENERATOR")
    print(" "*20 + "Functional Test Suite")
    print("="*70)

    tests = [
        ("Import Verification", test_imports),
        ("Data Models", test_data_models),
        ("Calculators", test_calculators),
        ("Databases", test_databases),
        ("Meal Plan Generator", test_meal_plan_generator),
        ("Markdown Export", test_markdown_export),
        ("Full Integration", test_integration),
    ]

    results = []

    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n❌ Test '{test_name}' crashed: {str(e)}")
            import traceback
            traceback.print_exc()
            results.append((test_name, False))

    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status}: {test_name}")

    print("="*70)
    print(f"\nResults: {passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 ALL TESTS PASSED! Application is fully functional.")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please review errors above.")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
