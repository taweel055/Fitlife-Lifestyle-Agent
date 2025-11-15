#!/usr/bin/env python3
"""
Fitlife Lifestyle Agent - Meal Plan Generator
Main application entry point
"""

import sys
import os
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.models import Client, Protocol
from src.utils import InputCollector
from src.generators import MealPlanGenerator
from src.database import SupplementDatabase
from src.exporters import MarkdownExporter


def print_banner():
    """Print application banner"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║            FITLIFE LIFESTYLE AGENT                           ║
    ║            Meal Plan Generation System                       ║
    ║                                                              ║
    ║         Supporting SHREDDED & MASSIVE Protocols              ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)


def print_menu():
    """Print main menu"""
    print("\n" + "="*60)
    print("MAIN MENU")
    print("="*60)
    print("1. Generate New Meal Plan")
    print("2. Quick Demo (Sample Client)")
    print("3. Exit")
    print("="*60)


def generate_meal_plan_interactive():
    """Generate meal plan with interactive input"""
    # Collect client information
    client = InputCollector.collect_client_info()

    if not InputCollector.confirm_action("Generate meal plan for this client?"):
        print("❌ Cancelled")
        return

    # Generate meal plan
    print("\n⏳ Generating meal plan...")
    generator = MealPlanGenerator()
    week_plan = generator.generate_week_plan(client, week_number=1)

    print("✅ Meal plan generated successfully!")

    # Get protocol summary
    summary = generator.get_protocol_summary(client)

    # Get supplement recommendations
    print("\n⏳ Getting supplement recommendations...")
    supp_db = SupplementDatabase()
    supplement_stack = supp_db.get_recommended_stack(client.protocol)

    print("✅ Supplement recommendations ready!")

    # Export to markdown
    print("\n⏳ Exporting to Markdown...")

    # Export week plan
    week_md = MarkdownExporter.export_week_plan(week_plan, include_food_suggestions=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    week_filename = f"{client.name.replace(' ', '_')}_{client.protocol.value}_Week1_{timestamp}.md"
    week_path = MarkdownExporter.save_to_file(week_md, week_filename)

    # Export supplement stack
    supp_md = MarkdownExporter.export_supplement_stack(supplement_stack)
    supp_filename = f"{client.name.replace(' ', '_')}_{client.protocol.value}_Supplements_{timestamp}.md"
    supp_path = MarkdownExporter.save_to_file(supp_md, supp_filename)

    # Export protocol summary
    summary_md = MarkdownExporter.export_protocol_summary(summary)
    summary_filename = f"{client.name.replace(' ', '_')}_{client.protocol.value}_Summary_{timestamp}.md"
    summary_path = MarkdownExporter.save_to_file(summary_md, summary_filename)

    print("\n" + "="*60)
    print("✅ GENERATION COMPLETE!")
    print("="*60)
    print("\nFiles saved:")
    print(f"📄 Week Plan: {week_path}")
    print(f"💊 Supplements: {supp_path}")
    print(f"📊 Summary: {summary_path}")
    print("="*60 + "\n")

    # Display quick summary
    print("\n📊 QUICK SUMMARY:")
    print(f"Lean Body Mass: {week_plan.lean_body_mass} lbs")
    print(f"Protocol: {week_plan.protocol}")
    print(f"Training Days: {', '.join(client.training_days)}")
    print(f"HIGH Days: {', '.join(client.high_days)}")
    print(f"\nCardio: {summary['cardio']}")

    print("\n💊 SUPPLEMENT STACK:")
    required = supplement_stack.get_required_supplements()
    print(f"Required supplements: {len(required)}")
    min_cost, max_cost = supplement_stack.calculate_total_cost()
    print(f"Estimated cost: ${min_cost:.0f} - ${max_cost:.0f}/month")


def run_demo():
    """Run demo with sample client"""
    print("\n" + "="*60)
    print("DEMO MODE - Sample Client")
    print("="*60 + "\n")

    # Create sample client
    client = Client(
        name="Ahmed Hassan",
        weight=180,
        weight_unit="lbs",
        body_fat_percentage=15.0,
        height=72,
        protocol=Protocol.SHREDDED,
        training_days=["Monday", "Wednesday", "Friday"],
        high_days=["Saturday"],
        language="en"
    )

    print("Using sample client:")
    print(f"  Name: {client.name}")
    print(f"  Weight: {client.weight} {client.weight_unit.value}")
    print(f"  Body Fat: {client.body_fat_percentage}%")
    print(f"  Protocol: {client.protocol.value}")
    print(f"  Training Days: {', '.join(client.training_days)}")
    print(f"  HIGH Days: {', '.join(client.high_days)}")

    if not InputCollector.confirm_action("\nGenerate demo meal plan?"):
        print("❌ Cancelled")
        return

    # Generate meal plan
    print("\n⏳ Generating meal plan...")
    generator = MealPlanGenerator()
    week_plan = generator.generate_week_plan(client, week_number=1)

    # Get supplement recommendations
    supp_db = SupplementDatabase()
    supplement_stack = supp_db.get_recommended_stack(client.protocol)

    # Get summary
    summary = generator.get_protocol_summary(client)

    # Export
    print("\n⏳ Exporting to Markdown...")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    week_md = MarkdownExporter.export_week_plan(week_plan, include_food_suggestions=True)
    week_path = MarkdownExporter.save_to_file(week_md, f"DEMO_Week_Plan_{timestamp}.md")

    supp_md = MarkdownExporter.export_supplement_stack(supplement_stack)
    supp_path = MarkdownExporter.save_to_file(supp_md, f"DEMO_Supplements_{timestamp}.md")

    summary_md = MarkdownExporter.export_protocol_summary(summary)
    summary_path = MarkdownExporter.save_to_file(summary_md, f"DEMO_Summary_{timestamp}.md")

    print("\n" + "="*60)
    print("✅ DEMO COMPLETE!")
    print("="*60)
    print("\nFiles saved:")
    print(f"📄 Week Plan: {week_path}")
    print(f"💊 Supplements: {supp_path}")
    print(f"📊 Summary: {summary_path}")
    print("="*60 + "\n")


def main():
    """Main application loop"""
    print_banner()

    while True:
        print_menu()

        choice = input("\nSelect option (1-3): ").strip()

        if choice == '1':
            try:
                generate_meal_plan_interactive()
            except KeyboardInterrupt:
                print("\n\n❌ Operation cancelled by user")
            except Exception as e:
                print(f"\n❌ Error: {str(e)}")
                import traceback
                traceback.print_exc()

        elif choice == '2':
            try:
                run_demo()
            except KeyboardInterrupt:
                print("\n\n❌ Operation cancelled by user")
            except Exception as e:
                print(f"\n❌ Error: {str(e)}")
                import traceback
                traceback.print_exc()

        elif choice == '3':
            print("\n👋 Thank you for using Fitlife Lifestyle Agent!")
            print("Goodbye!\n")
            break

        else:
            print("\n❌ Invalid choice. Please select 1-3.")

        # Pause before showing menu again
        if choice in ['1', '2']:
            input("\nPress Enter to continue...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Application terminated by user. Goodbye!\n")
        sys.exit(0)
