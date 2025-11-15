#!/usr/bin/env python3
"""
Example usage of the Fitlife Meal Plan Generator
Demonstrates programmatic usage of all components
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.models import Client, Protocol, WeightUnit, Language
from src.generators import MealPlanGenerator
from src.database import SupplementDatabase, FoodDatabase
from src.exporters import MarkdownExporter
from src.calculators import LBMCalculator, MacroCalculator


def example_1_basic_usage():
    """Example 1: Basic meal plan generation"""
    print("\n" + "="*60)
    print("EXAMPLE 1: Basic Meal Plan Generation")
    print("="*60 + "\n")

    # Create a client
    client = Client(
        name="John Doe",
        weight=200,
        weight_unit=WeightUnit.LBS,
        body_fat_percentage=18.0,
        protocol=Protocol.SHREDDED,
        training_days=["Monday", "Wednesday", "Friday"],
        high_days=["Saturday"],
        language=Language.ENGLISH
    )

    # Generate meal plan
    generator = MealPlanGenerator()
    week_plan = generator.generate_week_plan(client)

    # Display summary
    print(f"Client: {week_plan.client_name}")
    print(f"LBM: {week_plan.lean_body_mass} lbs")
    print(f"Protocol: {week_plan.protocol}")
    print(f"Total days planned: {len(week_plan.days)}")

    # Show Monday's plan
    monday = week_plan.days[0]
    print(f"\n{monday.day_name} ({monday.day_type.value}):")
    print(f"  Total meals: {len(monday.meals)}")
    print(f"  Total macros: {monday.get_total_macros()}")
    print(f"  Total calories: {monday.get_total_calories()}")


def example_2_massive_protocol():
    """Example 2: MASSIVE protocol with custom settings"""
    print("\n" + "="*60)
    print("EXAMPLE 2: MASSIVE Protocol")
    print("="*60 + "\n")

    # Create a bulking client
    client = Client(
        name="Mike Johnson",
        weight=75,  # kg
        weight_unit=WeightUnit.KG,
        body_fat_percentage=12.0,
        height=72,  # inches
        protocol=Protocol.MASSIVE,
        training_days=["Monday", "Tuesday", "Thursday", "Friday"],
        high_days=["Tuesday", "Friday"],  # 2 HIGH days for MASSIVE
        language=Language.ENGLISH
    )

    print(f"Client weight: {client.get_weight_in_lbs():.1f} lbs ({client.weight} kg)")

    # Calculate LBM
    lbm = LBMCalculator.calculate_lbm(client)
    protein_per_meal = LBMCalculator.calculate_protein_per_meal(lbm)

    print(f"Lean Body Mass: {lbm} lbs")
    print(f"Protein per meal: {protein_per_meal}g")

    # Generate plan
    generator = MealPlanGenerator()
    week_plan = generator.generate_week_plan(client, week_number=1)

    # Display day type distribution
    day_types = {}
    for day in week_plan.days:
        day_type = day.day_type.value
        day_types[day_type] = day_types.get(day_type, 0) + 1

    print(f"\nDay distribution:")
    for day_type, count in day_types.items():
        print(f"  {day_type}: {count} days")


def example_3_supplement_recommendations():
    """Example 3: Supplement recommendations"""
    print("\n" + "="*60)
    print("EXAMPLE 3: Supplement Recommendations")
    print("="*60 + "\n")

    supp_db = SupplementDatabase()

    # Get CUTTING stack
    cutting_stack = supp_db.get_cutting_stack()
    print(f"{cutting_stack.stack_name}")
    print(f"Goal: {cutting_stack.goal}")

    required = cutting_stack.get_required_supplements()
    optional = cutting_stack.get_optional_supplements()

    print(f"\nRequired supplements: {len(required)}")
    for supp in required:
        print(f"  - {supp.name}: {supp.dose} ({supp.timing.value})")

    print(f"\nOptional supplements: {len(optional)}")
    for supp in optional:
        print(f"  - {supp.name}: {supp.dose}")

    min_cost, max_cost = cutting_stack.calculate_total_cost()
    print(f"\nEstimated cost: ${min_cost:.0f} - ${max_cost:.0f}/month")

    # Get BULKING stack
    print("\n" + "-"*60 + "\n")

    bulking_stack = supp_db.get_bulking_stack()
    print(f"{bulking_stack.stack_name}")
    print(f"Goal: {bulking_stack.goal}")

    required = bulking_stack.get_required_supplements()
    print(f"\nRequired supplements: {len(required)}")
    for supp in required:
        print(f"  - {supp.name}: {supp.dose} ({supp.timing.value})")

    min_cost, max_cost = bulking_stack.calculate_total_cost()
    print(f"\nEstimated cost: ${min_cost:.0f} - ${max_cost:.0f}/month")


def example_4_food_database():
    """Example 4: Working with the food database"""
    print("\n" + "="*60)
    print("EXAMPLE 4: Food Database")
    print("="*60 + "\n")

    food_db = FoodDatabase()

    # Get protein sources
    proteins = food_db.get_protein_sources(preferred_only=True)
    print(f"Preferred protein sources: {len(proteins)}")
    for food in proteins[:5]:
        print(f"  - {food.name}: {food.protein_per_serving}p/{food.carbs_per_serving}c/{food.fat_per_serving}f per {food.serving_size}")

    # Get carb sources
    print("\n")
    carbs = food_db.get_carb_sources(preferred_only=True)
    print(f"Preferred carb sources: {len(carbs)}")
    for food in carbs[:5]:
        print(f"  - {food.name}: {food.protein_per_serving}p/{food.carbs_per_serving}c/{food.fat_per_serving}f per {food.serving_size}")

    # Get vegetables
    print("\n")
    veggies = food_db.get_vegetables()
    print(f"Vegetable options: {len(veggies)}")
    for food in veggies:
        print(f"  - {food.name}: {food.carbs_per_serving}c per {food.serving_size}")

    # Calculate servings for target protein
    print("\n" + "-"*60)
    chicken = food_db.get_food_by_name("Chicken Breast")
    target_protein = 50
    servings, macros = chicken.calculate_serving_for_protein(target_protein)
    print(f"\nTo get {target_protein}g protein from {chicken.name}:")
    print(f"  Need {servings} servings ({servings * 4:.1f} oz)")
    print(f"  Total macros: {macros}")


def example_5_export_to_markdown():
    """Example 5: Export meal plans to markdown"""
    print("\n" + "="*60)
    print("EXAMPLE 5: Export to Markdown")
    print("="*60 + "\n")

    # Create client and generate plan
    client = Client(
        name="Sarah Williams",
        weight=140,
        weight_unit=WeightUnit.LBS,
        body_fat_percentage=22.0,
        protocol=Protocol.SHREDDED,
        training_days=["Monday", "Wednesday", "Friday"],
        high_days=["Saturday"],
        language=Language.ENGLISH
    )

    generator = MealPlanGenerator()
    week_plan = generator.generate_week_plan(client)

    # Export week plan
    week_md = MarkdownExporter.export_week_plan(week_plan, include_food_suggestions=True)
    week_path = MarkdownExporter.save_to_file(week_md, "example_week_plan.md")
    print(f"✅ Week plan saved to: {week_path}")

    # Export supplement stack
    supp_db = SupplementDatabase()
    stack = supp_db.get_recommended_stack(client.protocol)
    supp_md = MarkdownExporter.export_supplement_stack(stack)
    supp_path = MarkdownExporter.save_to_file(supp_md, "example_supplements.md")
    print(f"✅ Supplements saved to: {supp_path}")

    # Export protocol summary
    summary = generator.get_protocol_summary(client)
    summary_md = MarkdownExporter.export_protocol_summary(summary)
    summary_path = MarkdownExporter.save_to_file(summary_md, "example_summary.md")
    print(f"✅ Summary saved to: {summary_path}")

    print("\nAll files saved successfully!")


def example_6_macro_calculations():
    """Example 6: Understanding macro calculations"""
    print("\n" + "="*60)
    print("EXAMPLE 6: Macro Calculations")
    print("="*60 + "\n")

    from src.models import DayType

    # SHREDDED protocol macros
    print("SHREDDED Protocol Daily Macros:")
    for day_type in [DayType.LOW, DayType.MEDIUM, DayType.HIGH]:
        macros = MacroCalculator.calculate_day_macros(Protocol.SHREDDED, day_type)
        print(f"  {day_type.value}: {macros} = {macros.calculate_calories()} cal")

    print("\n")

    # MASSIVE protocol macros
    print("MASSIVE Protocol Daily Macros:")
    for day_type in [DayType.LOW, DayType.MEDIUM, DayType.HIGH]:
        macros = MacroCalculator.calculate_day_macros(Protocol.MASSIVE, day_type)
        print(f"  {day_type.value}: {macros} = {macros.calculate_calories()} cal")

    # Cardio recommendations
    print("\n")
    print(f"SHREDDED Cardio: {MacroCalculator.get_cardio_recommendation(Protocol.SHREDDED)}")
    print(f"MASSIVE Cardio: {MacroCalculator.get_cardio_recommendation(Protocol.MASSIVE)}")


def main():
    """Run all examples"""
    print("\n" + "="*70)
    print(" "*15 + "FITLIFE MEAL PLAN GENERATOR")
    print(" "*20 + "Example Usage")
    print("="*70)

    examples = [
        ("Basic Meal Plan Generation", example_1_basic_usage),
        ("MASSIVE Protocol", example_2_massive_protocol),
        ("Supplement Recommendations", example_3_supplement_recommendations),
        ("Food Database", example_4_food_database),
        ("Export to Markdown", example_5_export_to_markdown),
        ("Macro Calculations", example_6_macro_calculations),
    ]

    for i, (title, func) in enumerate(examples, 1):
        try:
            func()
            if i < len(examples):
                input("\nPress Enter to continue to next example...")
        except Exception as e:
            print(f"\n❌ Error in {title}: {str(e)}")
            import traceback
            traceback.print_exc()

    print("\n" + "="*70)
    print("All examples completed!")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
