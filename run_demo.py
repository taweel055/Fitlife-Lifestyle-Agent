#!/usr/bin/env python3
"""Quick demo script to run the application"""

import sys
import os
from datetime import datetime

# Add src to path (same as main.py)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.models import Client, Protocol, WeightUnit
from src.generators import MealPlanGenerator
from src.database import SupplementDatabase
from src.exporters import MarkdownExporter

print('\n' + '='*60)
print('FITLIFE LIFESTYLE AGENT - DEMO MODE')
print('='*60 + '\n')

# Create sample client
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

print("Client Profile:")
print(f"  Name: {client.name}")
print(f"  Weight: {client.weight} {client.weight_unit.value}")
print(f"  Body Fat: {client.body_fat_percentage}%")
print(f"  Protocol: {client.protocol.value}")
print(f"  Training Days: {', '.join(client.training_days)}")
print(f"  HIGH Days: {', '.join(client.high_days)}")

print("\n⏳ Generating meal plan...")
generator = MealPlanGenerator()
week_plan = generator.generate_week_plan(client, week_number=1)

print("✅ Meal plan generated!")
print(f"  Lean Body Mass: {week_plan.lean_body_mass} lbs")
print(f"  Total days: {len(week_plan.days)}")

# Show Monday's plan
monday = week_plan.days[0]
print(f"\n📅 {monday.day_name} ({monday.day_type.value} DAY):")
print(f"  Total meals: {len(monday.meals)}")
total_macros = monday.get_total_macros()
total_calories = monday.get_total_calories()
print(f"  Daily macros: {total_macros.protein}p / {total_macros.carbs}c / {total_macros.fat}f")
print(f"  Total calories: {total_calories} cal")

print("\n⏳ Getting supplement recommendations...")
supp_db = SupplementDatabase()
supplement_stack = supp_db.get_recommended_stack(client.protocol)
print("✅ Supplements ready!")
required = supplement_stack.get_required_supplements()
min_cost, max_cost = supplement_stack.calculate_total_cost()
print(f"  Required supplements: {len(required)}")
print(f"  Estimated cost: ${min_cost:.0f} - ${max_cost:.0f}/month")

print("\n⏳ Exporting to Markdown...")
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

week_md = MarkdownExporter.export_week_plan(week_plan, include_food_suggestions=True)
week_filename = f"{client.name.replace(' ', '_')}_{client.protocol.value}_Week1_{timestamp}.md"
week_path = MarkdownExporter.save_to_file(week_md, week_filename)

supp_md = MarkdownExporter.export_supplement_stack(supplement_stack)
supp_filename = f"{client.name.replace(' ', '_')}_{client.protocol.value}_Supplements_{timestamp}.md"
supp_path = MarkdownExporter.save_to_file(supp_md, supp_filename)

summary = generator.get_protocol_summary(client)
summary_md = MarkdownExporter.export_protocol_summary(summary)
summary_filename = f"{client.name.replace(' ', '_')}_{client.protocol.value}_Summary_{timestamp}.md"
summary_path = MarkdownExporter.save_to_file(summary_md, summary_filename)

print("\n✅ Files saved:")
print(f"  📄 Week Plan: {week_path}")
print(f"  💊 Supplements: {supp_path}")
print(f"  📊 Summary: {summary_path}")

print("\n" + "="*60)
print("✅ DEMO COMPLETE!")
print("="*60 + "\n")

