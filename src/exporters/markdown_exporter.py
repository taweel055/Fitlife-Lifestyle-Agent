"""Markdown Exporter for meal plans and supplements"""

from typing import Optional
from ..models import WeekPlan, DayPlan, Meal, SupplementStack, Protocol
from ..calculators import MacroCalculator


class MarkdownExporter:
    """Export meal plans and supplements to Markdown format"""

    @staticmethod
    def export_week_plan(week_plan: WeekPlan, include_food_suggestions: bool = True) -> str:
        """
        Export a complete week plan to Markdown

        Args:
            week_plan: WeekPlan object
            include_food_suggestions: Whether to include food suggestions

        Returns:
            Markdown formatted string
        """
        lines = []

        # Header
        lines.append(f"# {week_plan.protocol} Protocol - Week {week_plan.week_number}")
        lines.append("")
        lines.append(f"**Client:** {week_plan.client_name}")
        lines.append(f"**Lean Body Mass:** {week_plan.lean_body_mass} lbs")
        lines.append(f"**Protocol:** {week_plan.protocol}")
        lines.append("")
        lines.append("---")
        lines.append("")

        # Cardio recommendation
        protocol_enum = Protocol.SHREDDED if week_plan.protocol == "SHREDDED" else Protocol.MASSIVE
        cardio = MacroCalculator.get_cardio_recommendation(protocol_enum)
        lines.append(f"**Cardio Requirement:** {cardio}")
        lines.append("")
        lines.append("---")
        lines.append("")

        # Export each day
        for day_plan in week_plan.days:
            day_md = MarkdownExporter.export_day_plan(
                day_plan,
                include_food_suggestions=include_food_suggestions
            )
            lines.append(day_md)
            lines.append("")

        return "\n".join(lines)

    @staticmethod
    def export_day_plan(day_plan: DayPlan, include_food_suggestions: bool = True) -> str:
        """
        Export a single day plan to Markdown

        Args:
            day_plan: DayPlan object
            include_food_suggestions: Whether to include food suggestions

        Returns:
            Markdown formatted string
        """
        lines = []

        # Day header
        day_title = f"## {day_plan.day_name} ({day_plan.day_type.value} DAY"
        if day_plan.is_training_day:
            day_title += f" - Training at {day_plan.training_time}"
        day_title += ")"
        lines.append(day_title)
        lines.append("")

        # Meal table
        lines.append("| Time | Meal | Protein | Carbs | Fat | Calories |")
        lines.append("|------|------|---------|-------|-----|----------|")

        for meal in day_plan.meals:
            time = meal.time or "TBD"
            name = meal.name
            if meal.meal_type.value != "REGULAR":
                name = f"{meal.name}"

            calories = meal.macros.calculate_calories()

            lines.append(
                f"| {time} | {name} | {meal.macros.protein}g | "
                f"{meal.macros.carbs}g | {meal.macros.fat}g | {calories} cal |"
            )

        lines.append("")

        # Daily totals
        total_macros = day_plan.get_total_macros()
        total_calories = day_plan.get_total_calories()

        lines.append(
            f"**Daily Total:** {total_macros.protein}g protein | "
            f"{total_macros.carbs}g carbs | {total_macros.fat}g fat | "
            f"~{total_calories:,} calories"
        )
        lines.append("")

        # Food suggestions (if requested)
        if include_food_suggestions:
            lines.append("### Food Suggestions")
            lines.append("")

            for meal in day_plan.meals:
                if (meal.protein_sources or meal.carb_sources or
                    meal.fat_sources or meal.vegetables):
                    lines.append(f"**{meal.name}:**")

                    if meal.protein_sources:
                        lines.append(f"- Protein: {', '.join(meal.protein_sources)}")
                    if meal.carb_sources:
                        lines.append(f"- Carbs: {', '.join(meal.carb_sources)}")
                    if meal.fat_sources:
                        lines.append(f"- Fats: {', '.join(meal.fat_sources)}")
                    if meal.vegetables:
                        lines.append(f"- Vegetables: {', '.join(meal.vegetables)}")
                    if meal.notes:
                        lines.append(f"- *Note: {meal.notes}*")

                    lines.append("")

        lines.append("---")
        lines.append("")

        return "\n".join(lines)

    @staticmethod
    def export_supplement_stack(stack: SupplementStack) -> str:
        """
        Export supplement stack to Markdown

        Args:
            stack: SupplementStack object

        Returns:
            Markdown formatted string
        """
        lines = []

        # Header
        lines.append(f"# {stack.stack_name}")
        lines.append("")
        lines.append(f"**Goal:** {stack.goal}")
        lines.append("")

        # Required supplements
        required = stack.get_required_supplements()
        if required:
            lines.append("## Required Supplements")
            lines.append("")
            lines.append("| Supplement | Dose | Timing | Purpose | Cost/Month |")
            lines.append("|------------|------|--------|---------|------------|")

            for supp in required:
                cost = f"${supp.estimated_cost_per_month:.0f}" if supp.estimated_cost_per_month else "N/A"
                lines.append(
                    f"| {supp.name} | {supp.dose} | {supp.timing.value} | "
                    f"{supp.purpose.value} | {cost} |"
                )

            lines.append("")

        # Optional supplements
        optional = stack.get_optional_supplements()
        if optional:
            lines.append("## Optional Supplements")
            lines.append("")
            lines.append("| Supplement | Dose | Timing | Purpose | Cost/Month |")
            lines.append("|------------|------|--------|---------|------------|")

            for supp in optional:
                cost = f"${supp.estimated_cost_per_month:.0f}" if supp.estimated_cost_per_month else "N/A"
                lines.append(
                    f"| {supp.name} | {supp.dose} | {supp.timing.value} | "
                    f"{supp.purpose.value} | {cost} |"
                )

            lines.append("")

        # Cost summary
        min_cost, max_cost = stack.calculate_total_cost()
        lines.append(f"**Estimated Monthly Cost:** ${min_cost:.0f} - ${max_cost:.0f}")
        lines.append("")

        # Notes section
        lines.append("## Important Notes")
        lines.append("")
        for supp in stack.supplements:
            if supp.notes:
                lines.append(f"- **{supp.name}:** {supp.notes}")
        lines.append("")

        return "\n".join(lines)

    @staticmethod
    def export_protocol_summary(summary: dict) -> str:
        """
        Export protocol summary to Markdown

        Args:
            summary: Dictionary with protocol information

        Returns:
            Markdown formatted string
        """
        lines = []

        # Header
        lines.append(f"# Protocol Summary: {summary['protocol']}")
        lines.append("")

        # Client info
        lines.append("## Client Information")
        lines.append("")
        lines.append(f"- **Name:** {summary['client_name']}")
        lines.append(f"- **Body Weight:** {summary['body_weight']}")
        lines.append(f"- **Body Fat:** {summary['body_fat_percentage']}")
        lines.append(f"- **Lean Body Mass:** {summary['lean_body_mass']}")
        lines.append(f"- **Protein Per Meal:** {summary['protein_per_meal']}")
        lines.append("")

        # Training schedule
        lines.append("## Training Schedule")
        lines.append("")
        lines.append(f"- **Training Days:** {', '.join(summary['training_days'])}")
        lines.append(f"- **HIGH Days:** {', '.join(summary['high_days'])}")
        lines.append(f"- **Cardio:** {summary['cardio']}")
        lines.append("")

        # Macro breakdowns
        lines.append("## Daily Macro Targets")
        lines.append("")

        for day_type in ['low', 'medium', 'high']:
            key = f'{day_type}_day_macros'
            if key in summary:
                macros = summary[key]
                lines.append(f"### {day_type.upper()} Day")
                lines.append(f"- Protein: {macros['protein']}")
                lines.append(f"- Carbs: {macros['carbs']}")
                lines.append(f"- Fat: {macros['fat']}")
                lines.append(f"- Calories: ~{macros['calories']:,}")
                lines.append("")

        return "\n".join(lines)

    @staticmethod
    def save_to_file(content: str, filename: str) -> str:
        """
        Save markdown content to a file

        Args:
            content: Markdown content
            filename: Output filename

        Returns:
            Absolute path to saved file
        """
        import os

        # Ensure .md extension
        if not filename.endswith('.md'):
            filename += '.md'

        # Create output directory if needed
        output_dir = os.path.join(os.getcwd(), 'output')
        os.makedirs(output_dir, exist_ok=True)

        # Save file
        filepath = os.path.join(output_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        return os.path.abspath(filepath)
