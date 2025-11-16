#!/usr/bin/env python3
"""
Auto-run demo - automatically generates a demo meal plan
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.models import Client, Protocol, WeightUnit
from src.generators import MealPlanGenerator
from src.database import SupplementDatabase
from src.exporters import MarkdownExporter
from datetime import datetime


def main():
    """Run automated demo"""
    print("\n" + "="*70)
    print(" "*15 + "FITLIFE LIFESTYLE AGENT")
    print(" "*17 + "Meal Plan Generator")
    print(" "*20 + "AUTO-DEMO MODE")
    print("="*70 + "\n")

    # Create sample client
    print("📋 Creating sample client profile...")
    client = Client(
        name="Ahmed Hassan",
        weight=180,
        weight_unit=WeightUnit.LBS,
        body_fat_percentage=15.0,
        height=72,
        protocol=Protocol.SHREDDED,
        training_days=["Monday", "Wednesday", "Friday"],
        high_days=["Saturday"],
        language="en"
    )

    print(f"✅ Client: {client.name}")
    print(f"   Weight: {client.weight} {client.weight_unit.value}")
    print(f"   Body Fat: {client.body_fat_percentage}%")
    print(f"   Protocol: {client.protocol.value}")
    print(f"   Training Days: {', '.join(client.training_days)}")
    print(f"   HIGH Days: {', '.join(client.high_days)}")

    # Generate meal plan
    print("\n⏳ Generating meal plan...")
    generator = MealPlanGenerator()
    week_plan = generator.generate_week_plan(client, week_number=1)

    print(f"✅ 7-day meal plan generated")
    print(f"   LBM: {week_plan.lean_body_mass} lbs")
    print(f"   Protocol: {week_plan.protocol}")

    # Get supplement recommendations
    print("\n⏳ Getting supplement recommendations...")
    supp_db = SupplementDatabase()
    supplement_stack = supp_db.get_recommended_stack(client.protocol)

    min_cost, max_cost = supplement_stack.calculate_total_cost()
    print(f"✅ {supplement_stack.stack_name}")
    print(f"   Supplements: {len(supplement_stack.supplements)}")
    print(f"   Cost: ${min_cost:.0f} - ${max_cost:.0f}/month")

    # Get summary
    summary = generator.get_protocol_summary(client)

    # Export
    print("\n⏳ Exporting to markdown files...")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    week_md = MarkdownExporter.export_week_plan(week_plan, include_food_suggestions=True)
    week_path = MarkdownExporter.save_to_file(week_md, f"DEMO_Week_Plan_{timestamp}.md")

    supp_md = MarkdownExporter.export_supplement_stack(supplement_stack)
    supp_path = MarkdownExporter.save_to_file(supp_md, f"DEMO_Supplements_{timestamp}.md")

    summary_md = MarkdownExporter.export_protocol_summary(summary)
    summary_path = MarkdownExporter.save_to_file(summary_md, f"DEMO_Summary_{timestamp}.md")

    print("\n" + "="*70)
    print("✅ DEMO COMPLETE!")
    print("="*70)

    print("\n📁 Files Generated:")
    print(f"   📄 Week Plan: {os.path.basename(week_path)}")
    print(f"   💊 Supplements: {os.path.basename(supp_path)}")
    print(f"   📊 Summary: {os.path.basename(summary_path)}")

    print(f"\n📍 Location: {os.path.dirname(week_path)}/")

    # Display quick preview
    print("\n" + "="*70)
    print("📊 QUICK PREVIEW")
    print("="*70)

    print(f"\n🎯 Client Stats:")
    print(f"   Name: {client.name}")
    print(f"   LBM: {week_plan.lean_body_mass} lbs")
    print(f"   Protocol: {client.protocol.value}")

    print(f"\n📅 Weekly Schedule:")
    for day in week_plan.days:
        total_macros = day.get_total_macros()
        total_cals = day.get_total_calories()
        print(f"   {day.day_name:9s} ({day.day_type.value:6s}): "
              f"{total_macros.protein}p/{total_macros.carbs}c/{total_macros.fat}f "
              f"= {total_cals:,} cal | {len(day.meals)} meals")

    print(f"\n💊 Supplement Stack:")
    required = supplement_stack.get_required_supplements()
    for supp in required[:5]:
        print(f"   • {supp.name}: {supp.dose} ({supp.timing.value})")
    if len(required) > 5:
        print(f"   ... and {len(required) - 5} more")

    print(f"\n🏃 Cardio Requirement:")
    print(f"   {summary['cardio']}")

    print("\n" + "="*70)
    print("🎉 Demo completed successfully!")
    print("="*70 + "\n")

    print("💡 To see the full meal plan, open the generated files in the output/ directory")
    print("💡 To create a custom meal plan, run: python main.py")
    print()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
