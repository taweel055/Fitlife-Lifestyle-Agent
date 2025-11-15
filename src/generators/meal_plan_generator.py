"""Meal Plan Generator for creating complete weekly plans"""

from typing import List, Optional
from datetime import datetime, timedelta
from ..models import (
    Client, Protocol, DayType, Meal, MealType,
    DayPlan, WeekPlan
)
from ..calculators import LBMCalculator, MacroCalculator
from ..database import FoodDatabase


class MealPlanGenerator:
    """Generate complete meal plans for clients"""

    def __init__(self):
        """Initialize generator with food database"""
        self.food_db = FoodDatabase()

    def determine_day_type(
        self,
        day_name: str,
        training_days: List[str],
        high_days: List[str]
    ) -> tuple[DayType, bool]:
        """
        Determine if a day is LOW, MEDIUM, or HIGH and if it's a training day

        Args:
            day_name: Name of the day (e.g., 'Monday')
            training_days: List of training day names
            high_days: List of HIGH day names

        Returns:
            Tuple of (DayType, is_training_day)
        """
        is_training = day_name in training_days
        is_high = day_name in high_days

        if is_high:
            return (DayType.HIGH, True)  # HIGH days are always training days
        elif is_training:
            return (DayType.MEDIUM, True)
        else:
            return (DayType.LOW, False)

    def generate_meal_times(
        self,
        day_type: DayType,
        is_training_day: bool,
        training_time: Optional[str] = "5:00 PM"
    ) -> dict:
        """
        Generate suggested meal times

        Args:
            day_type: LOW, MEDIUM, or HIGH
            is_training_day: Whether this is a training day
            training_time: Time of training session

        Returns:
            Dictionary mapping meal names to times
        """
        meal_times = {}

        if is_training_day:
            # Training day schedule
            meal_times = {
                'Meal 1': '6:00 AM',
                'Meal 2': '9:00 AM',
                'Meal 3': '12:00 PM',
                'Pre-Workout': '3:30 PM',  # 1.5 hours before training
                'Intra-Workout': training_time,
                'Post-Workout': '6:00 PM',  # Right after training
                'Meal 4': '8:30 PM',
            }
        else:
            # Non-training day schedule
            meal_times = {
                'Meal 1': '6:00 AM',
                'Meal 2': '9:00 AM',
                'Meal 3': '12:00 PM',
                'Meal 4': '3:00 PM',
                'Meal 5': '6:00 PM',
                'Meal 6': '9:00 PM',
            }

        return meal_times

    def suggest_food_sources(self, meal: Meal, day_type: DayType) -> Meal:
        """
        Add food suggestions to a meal based on its macros

        Args:
            meal: Meal object to add suggestions to
            day_type: Type of day (affects carb choices)

        Returns:
            Updated Meal object with food suggestions
        """
        macros = meal.macros
        allow_sugary = day_type == DayType.HIGH

        # Protein sources
        if macros.protein > 0:
            protein_foods = self.food_db.get_protein_sources(preferred_only=True)
            meal.protein_sources = [food.name for food in protein_foods[:3]]

        # Carb sources
        if macros.carbs > 0:
            carb_foods = self.food_db.get_carb_sources(
                preferred_only=True,
                allow_sugary=allow_sugary
            )
            meal.carb_sources = [food.name for food in carb_foods[:3]]

            if allow_sugary and macros.carbs > 50:
                # Add sugary options for HIGH days
                sugary_foods = self.food_db.get_foods_by_category(
                    self.food_db.FoodCategory.CARB_SUGARY
                )
                meal.carb_sources.extend([food.name for food in sugary_foods[:2]])
                meal.notes = "50% of carbs can come from sugary sources on HIGH days"

        # Fat sources
        if macros.fat > 0:
            fat_foods = self.food_db.get_fat_sources()
            meal.fat_sources = [food.name for food in fat_foods[:3]]

        # Vegetables (for meals with <25g carbs or as free addition)
        if macros.carbs < 25:
            veggies = self.food_db.get_vegetables()
            meal.vegetables = [food.name for food in veggies[:4]]
            if not meal.notes:
                meal.notes = "Add vegetables as 'free' carbs"

        return meal

    def generate_day_plan(
        self,
        client: Client,
        day_name: str,
        lbm: float,
        training_time: Optional[str] = "5:00 PM"
    ) -> DayPlan:
        """
        Generate a complete day meal plan

        Args:
            client: Client object
            day_name: Name of the day
            lbm: Lean body mass
            training_time: Time of training if applicable

        Returns:
            DayPlan object with all meals
        """
        # Determine day type
        day_type, is_training = self.determine_day_type(
            day_name,
            client.training_days,
            client.high_days
        )

        # Get meal structure for this day type
        meal_structure = MacroCalculator.get_meal_structure(
            client.protocol,
            day_type
        )

        # Generate meal times
        meal_times = self.generate_meal_times(day_type, is_training, training_time)

        # Create meals
        meals = []
        meal_counter = 1
        regular_meal_counter = 1

        for meal_def in meal_structure:
            count = meal_def['count']

            for i in range(count):
                # Determine meal name and time
                if meal_def['type'] == MealType.REGULAR:
                    meal_name = f"Meal {regular_meal_counter}"
                    meal_time = meal_times.get(meal_name, None)
                    regular_meal_counter += 1
                else:
                    meal_name = meal_def['name']
                    meal_time = meal_times.get(meal_name, None)

                # Create meal
                meal = Meal(
                    name=meal_name,
                    meal_type=meal_def['type'],
                    macros=meal_def['macros'],
                    time=meal_time
                )

                # Add food suggestions
                meal = self.suggest_food_sources(meal, day_type)

                meals.append(meal)

        # Create day plan
        day_plan = DayPlan(
            day_name=day_name,
            day_type=day_type,
            is_training_day=is_training,
            training_time=training_time if is_training else None,
            meals=meals
        )

        return day_plan

    def generate_week_plan(
        self,
        client: Client,
        week_number: int = 1,
        training_time: Optional[str] = "5:00 PM"
    ) -> WeekPlan:
        """
        Generate a complete week meal plan

        Args:
            client: Client object
            week_number: Week number (for tracking)
            training_time: Default training time

        Returns:
            WeekPlan object with 7 days
        """
        # Calculate LBM
        lbm = LBMCalculator.calculate_lbm(client)

        # Days of the week
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

        # Generate plan for each day
        day_plans = []
        for day_name in days:
            day_plan = self.generate_day_plan(client, day_name, lbm, training_time)
            day_plans.append(day_plan)

        # Create week plan
        week_plan = WeekPlan(
            client_name=client.name,
            week_number=week_number,
            lean_body_mass=lbm,
            protocol=client.protocol.value,
            days=day_plans
        )

        return week_plan

    def get_protocol_summary(self, client: Client) -> dict:
        """
        Get a summary of the protocol requirements

        Args:
            client: Client object

        Returns:
            Dictionary with protocol information
        """
        lbm = LBMCalculator.calculate_lbm(client)
        protein_per_meal = LBMCalculator.calculate_protein_per_meal(lbm)

        summary = {
            'client_name': client.name,
            'protocol': client.protocol.value,
            'body_weight': f"{client.weight} {client.weight_unit.value}",
            'body_fat_percentage': f"{client.body_fat_percentage}%",
            'lean_body_mass': f"{lbm} lbs",
            'protein_per_meal': f"{protein_per_meal}g",
            'training_days': client.training_days,
            'high_days': client.high_days,
            'cardio': MacroCalculator.get_cardio_recommendation(client.protocol),
        }

        # Add macro breakdowns for each day type
        for day_type in [DayType.LOW, DayType.MEDIUM, DayType.HIGH]:
            macros = MacroCalculator.calculate_day_macros(client.protocol, day_type)
            summary[f'{day_type.value.lower()}_day_macros'] = {
                'protein': f"{macros.protein}g",
                'carbs': f"{macros.carbs}g",
                'fat': f"{macros.fat}g",
                'calories': macros.calculate_calories()
            }

        return summary
