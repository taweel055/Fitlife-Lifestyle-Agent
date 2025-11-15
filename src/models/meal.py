"""Meal data models"""

from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field
from .macros import Macros


class DayType(str, Enum):
    """Day type based on calorie/macro level"""
    LOW = "LOW"          # Non-training days
    MEDIUM = "MEDIUM"    # Regular training days
    HIGH = "HIGH"        # High calorie days


class MealType(str, Enum):
    """Type of meal in the plan"""
    REGULAR = "REGULAR"          # Standard meal
    PRE_WORKOUT = "PRE_WORKOUT"  # Before training
    INTRA_WORKOUT = "INTRA_WORKOUT"  # During training
    POST_WORKOUT = "POST_WORKOUT"    # After training


class Meal(BaseModel):
    """Individual meal in a meal plan"""

    name: str = Field(..., description="Meal name/number")
    meal_type: MealType = Field(default=MealType.REGULAR, description="Type of meal")
    macros: Macros = Field(..., description="Macronutrient targets")

    time: Optional[str] = Field(None, description="Suggested meal time (e.g., '6:00 AM')")

    protein_sources: List[str] = Field(
        default_factory=list,
        description="Suggested protein foods"
    )
    carb_sources: List[str] = Field(
        default_factory=list,
        description="Suggested carbohydrate foods"
    )
    fat_sources: List[str] = Field(
        default_factory=list,
        description="Suggested fat foods"
    )
    vegetables: List[str] = Field(
        default_factory=list,
        description="Suggested vegetables (free carbs)"
    )

    notes: Optional[str] = Field(None, description="Special notes or instructions")

    def __str__(self) -> str:
        """String representation"""
        return f"{self.name} ({self.meal_type.value}): {self.macros}"

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Meal 1",
                "meal_type": "REGULAR",
                "macros": {"protein": 50, "carbs": 25, "fat": 4},
                "time": "6:00 AM",
                "protein_sources": ["Chicken breast", "Egg whites"],
                "carb_sources": ["White rice", "Oats"],
                "fat_sources": ["Almonds"],
                "vegetables": ["Broccoli", "Spinach"]
            }
        }


class DayPlan(BaseModel):
    """Meal plan for a single day"""

    day_name: str = Field(..., description="Day of the week")
    day_type: DayType = Field(..., description="LOW/MEDIUM/HIGH day")
    is_training_day: bool = Field(default=False, description="Is this a training day?")
    training_time: Optional[str] = Field(None, description="Training time if applicable")

    meals: List[Meal] = Field(default_factory=list, description="List of meals for the day")

    def get_total_macros(self) -> Macros:
        """Calculate total macros for the day"""
        total_protein = sum(meal.macros.protein for meal in self.meals)
        total_carbs = sum(meal.macros.carbs for meal in self.meals)
        total_fat = sum(meal.macros.fat for meal in self.meals)

        return Macros(protein=total_protein, carbs=total_carbs, fat=total_fat)

    def get_total_calories(self) -> int:
        """Calculate total calories for the day"""
        return self.get_total_macros().calculate_calories()


class WeekPlan(BaseModel):
    """Complete week meal plan"""

    client_name: str = Field(..., description="Client name")
    week_number: int = Field(default=1, description="Week number")

    days: List[DayPlan] = Field(default_factory=list, description="7-day meal plans")

    lean_body_mass: float = Field(..., description="Calculated LBM in lbs")
    protocol: str = Field(..., description="SHREDDED or MASSIVE")

    class Config:
        json_schema_extra = {
            "example": {
                "client_name": "Ahmed Hassan",
                "week_number": 1,
                "lean_body_mass": 165,
                "protocol": "SHREDDED",
                "days": []
            }
        }
