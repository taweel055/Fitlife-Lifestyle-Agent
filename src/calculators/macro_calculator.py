"""Macro Calculator for both SHREDDED and MASSIVE protocols"""

from typing import Dict, List
from ..models import Client, Protocol, DayType, Macros, MealType


class MacroCalculator:
    """Calculate macronutrients for different protocols and day types"""

    # SHREDDED Protocol Specifications
    SHREDDED_SPECS = {
        DayType.LOW: {
            'total_protein': 300,
            'total_carbs': 120,
            'meal_count': 6,
            'meal_type': MealType.REGULAR,
            'meals': [
                {'name': 'Meal 1-3', 'count': 3, 'protein': 50, 'carbs': 25, 'fat': 4},
                {'name': 'Meal 4-6', 'count': 3, 'protein': 50, 'carbs': 15, 'fat': 8},
            ]
        },
        DayType.MEDIUM: {
            'total_protein': 250,
            'total_carbs': 220,
            'has_training_meals': True,
            'training_meals': [
                {'name': 'Pre-Workout', 'type': MealType.PRE_WORKOUT, 'protein': 40, 'carbs': 60, 'fat': 0},
                {'name': 'Intra-Workout', 'type': MealType.INTRA_WORKOUT, 'protein': 10, 'carbs': 20, 'fat': 0},
                {'name': 'Post-Workout', 'type': MealType.POST_WORKOUT, 'protein': 40, 'carbs': 60, 'fat': 0},
            ],
            'regular_meals': [
                {'name': 'Regular Meals 1-4', 'count': 4, 'protein': 40, 'carbs': 20, 'fat': 6},
            ]
        },
        DayType.HIGH: {
            'total_protein': 190,
            'total_carbs': 730,
            'has_training_meals': True,
            'training_meals': [
                {'name': 'Pre-Workout', 'type': MealType.PRE_WORKOUT, 'protein': 30, 'carbs': 115, 'fat': 0},
                {'name': 'Intra-Workout', 'type': MealType.INTRA_WORKOUT, 'protein': 10, 'carbs': 40, 'fat': 0},
                {'name': 'Post-Workout', 'type': MealType.POST_WORKOUT, 'protein': 30, 'carbs': 115, 'fat': 0},
            ],
            'regular_meals': [
                {'name': 'Regular Meals 1-4', 'count': 4, 'protein': 30, 'carbs': 115, 'fat': 0},
            ]
        }
    }

    # MASSIVE Protocol Specifications
    MASSIVE_SPECS = {
        DayType.LOW: {
            'total_protein': 300,
            'total_carbs': 240,
            'meal_count': 6,
            'meal_type': MealType.REGULAR,
            'meals': [
                {'name': 'Meal 1-3', 'count': 3, 'protein': 50, 'carbs': 45, 'fat': 8},
                {'name': 'Meal 4-6', 'count': 3, 'protein': 50, 'carbs': 35, 'fat': 13},
            ]
        },
        DayType.MEDIUM: {
            'total_protein': 310,
            'total_carbs': 450,
            'has_training_meals': True,
            'training_meals': [
                {'name': 'Pre-Workout', 'type': MealType.PRE_WORKOUT, 'protein': 50, 'carbs': 95, 'fat': 0},
                {'name': 'Intra-Workout', 'type': MealType.INTRA_WORKOUT, 'protein': 10, 'carbs': 20, 'fat': 0},
                {'name': 'Post-Workout', 'type': MealType.POST_WORKOUT, 'protein': 50, 'carbs': 95, 'fat': 0},
            ],
            'regular_meals': [
                {'name': 'Regular Meals 1-2', 'count': 2, 'protein': 50, 'carbs': 70, 'fat': 8},
                {'name': 'Regular Meals 3-4', 'count': 2, 'protein': 50, 'carbs': 50, 'fat': 12},
            ]
        },
        DayType.HIGH: {
            'total_protein': 220,
            'total_carbs': 730,
            'has_training_meals': True,
            'training_meals': [
                {'name': 'Pre-Workout', 'type': MealType.PRE_WORKOUT, 'protein': 35, 'carbs': 115, 'fat': 0},
                {'name': 'Intra-Workout', 'type': MealType.INTRA_WORKOUT, 'protein': 10, 'carbs': 40, 'fat': 0},
                {'name': 'Post-Workout', 'type': MealType.POST_WORKOUT, 'protein': 35, 'carbs': 115, 'fat': 0},
            ],
            'regular_meals': [
                {'name': 'Regular Meals 1-4', 'count': 4, 'protein': 35, 'carbs': 115, 'fat': 0},
            ]
        }
    }

    @classmethod
    def get_protocol_specs(cls, protocol: Protocol) -> Dict:
        """Get protocol specifications"""
        if protocol == Protocol.SHREDDED:
            return cls.SHREDDED_SPECS
        else:  # Protocol.MASSIVE
            return cls.MASSIVE_SPECS

    @classmethod
    def calculate_day_macros(cls, protocol: Protocol, day_type: DayType) -> Macros:
        """
        Calculate total macros for a specific day type

        Args:
            protocol: SHREDDED or MASSIVE
            day_type: LOW, MEDIUM, or HIGH

        Returns:
            Total Macros for the day
        """
        specs = cls.get_protocol_specs(protocol)
        day_spec = specs[day_type]

        total_protein = day_spec['total_protein']
        total_carbs = day_spec['total_carbs']

        # Calculate total fat from meal specs
        total_fat = 0
        if 'meals' in day_spec:
            for meal_group in day_spec['meals']:
                total_fat += meal_group['fat'] * meal_group['count']
        if 'training_meals' in day_spec:
            for meal in day_spec['training_meals']:
                total_fat += meal['fat']
        if 'regular_meals' in day_spec:
            for meal_group in day_spec['regular_meals']:
                total_fat += meal_group['fat'] * meal_group['count']

        return Macros(protein=total_protein, carbs=total_carbs, fat=total_fat)

    @classmethod
    def get_meal_structure(cls, protocol: Protocol, day_type: DayType) -> List[Dict]:
        """
        Get meal structure for a specific protocol and day type

        Args:
            protocol: SHREDDED or MASSIVE
            day_type: LOW, MEDIUM, or HIGH

        Returns:
            List of meal definitions
        """
        specs = cls.get_protocol_specs(protocol)
        day_spec = specs[day_type]

        meal_structure = []

        if day_spec.get('has_training_meals', False):
            # Training day - add training meals first
            for meal_def in day_spec['training_meals']:
                meal_structure.append({
                    'name': meal_def['name'],
                    'type': meal_def['type'],
                    'macros': Macros(
                        protein=meal_def['protein'],
                        carbs=meal_def['carbs'],
                        fat=meal_def['fat']
                    ),
                    'count': 1
                })

            # Add regular meals
            for meal_group in day_spec['regular_meals']:
                meal_structure.append({
                    'name': meal_group['name'],
                    'type': MealType.REGULAR,
                    'macros': Macros(
                        protein=meal_group['protein'],
                        carbs=meal_group['carbs'],
                        fat=meal_group['fat']
                    ),
                    'count': meal_group['count']
                })
        else:
            # Non-training day - all regular meals
            for meal_group in day_spec['meals']:
                meal_structure.append({
                    'name': meal_group['name'],
                    'type': MealType.REGULAR,
                    'macros': Macros(
                        protein=meal_group['protein'],
                        carbs=meal_group['carbs'],
                        fat=meal_group['fat']
                    ),
                    'count': meal_group['count']
                })

        return meal_structure

    @classmethod
    def get_cardio_recommendation(cls, protocol: Protocol) -> str:
        """Get cardio recommendation for the protocol"""
        if protocol == Protocol.SHREDDED:
            return "30 min HIIT 5x/week OR 15,000 steps/day"
        else:  # Protocol.MASSIVE
            return "12 min HIIT 3x/week OR 12,000 steps/day"
