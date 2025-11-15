"""Supplement data models"""

from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field


class SupplementTiming(str, Enum):
    """When to take the supplement"""
    MORNING = "Morning"
    BREAKFAST = "With Breakfast"
    PRE_WORKOUT = "Pre-Workout"
    INTRA_WORKOUT = "Intra-Workout"
    POST_WORKOUT = "Post-Workout"
    DINNER = "With Dinner"
    BEFORE_BED = "Before Bed"
    DAILY = "Daily (any time)"


class SupplementPurpose(str, Enum):
    """Primary purpose of the supplement"""
    MUSCLE_RECOVERY = "Muscle recovery"
    ENERGY = "Energy & focus"
    FAT_LOSS = "Fat mobilization"
    MUSCLE_GAIN = "Muscle growth"
    PERFORMANCE = "Performance enhancement"
    HEALTH = "General health"
    INFLAMMATION = "Inflammation control"
    SLEEP = "Sleep & recovery"
    DIGESTION = "Digestive support"
    MICRONUTRIENTS = "Micronutrient support"


class Supplement(BaseModel):
    """Individual supplement recommendation"""

    name: str = Field(..., description="Supplement name")
    arabic_name: Optional[str] = Field(None, description="Supplement name in Arabic")

    dose: str = Field(..., description="Recommended dosage (e.g., '5g', '2-3 capsules')")
    timing: SupplementTiming = Field(..., description="When to take")
    purpose: SupplementPurpose = Field(..., description="Primary purpose")

    estimated_cost_per_month: Optional[float] = Field(
        None,
        description="Estimated monthly cost in USD"
    )

    is_optional: bool = Field(
        default=False,
        description="Whether this supplement is optional"
    )

    notes: Optional[str] = Field(
        None,
        description="Additional notes or instructions"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Whey Protein Isolate",
                "arabic_name": "بروتين مصل اللبن",
                "dose": "25-40g",
                "timing": "POST_WORKOUT",
                "purpose": "MUSCLE_RECOVERY",
                "estimated_cost_per_month": 45.0,
                "is_optional": False,
                "notes": "Mix with water immediately post-workout"
            }
        }


class SupplementStack(BaseModel):
    """Complete supplement recommendation stack"""

    stack_name: str = Field(..., description="Stack name (e.g., 'CUTTING', 'BULKING')")
    goal: str = Field(..., description="Primary goal (SHREDDED or MASSIVE)")

    supplements: List[Supplement] = Field(
        default_factory=list,
        description="List of recommended supplements"
    )

    total_estimated_cost_min: Optional[float] = Field(
        None,
        description="Minimum estimated monthly cost"
    )
    total_estimated_cost_max: Optional[float] = Field(
        None,
        description="Maximum estimated monthly cost"
    )

    def get_required_supplements(self) -> List[Supplement]:
        """Get only required (non-optional) supplements"""
        return [s for s in self.supplements if not s.is_optional]

    def get_optional_supplements(self) -> List[Supplement]:
        """Get only optional supplements"""
        return [s for s in self.supplements if s.is_optional]

    def calculate_total_cost(self) -> tuple[float, float]:
        """
        Calculate total cost range
        Returns: (min_cost, max_cost)
        """
        required = [s for s in self.supplements if not s.is_optional and s.estimated_cost_per_month]
        optional = [s for s in self.supplements if s.is_optional and s.estimated_cost_per_month]

        min_cost = sum(s.estimated_cost_per_month for s in required)
        max_cost = min_cost + sum(s.estimated_cost_per_month for s in optional)

        return (min_cost, max_cost)

    class Config:
        json_schema_extra = {
            "example": {
                "stack_name": "CUTTING STACK",
                "goal": "SHREDDED",
                "supplements": [],
                "total_estimated_cost_min": 120,
                "total_estimated_cost_max": 180
            }
        }
