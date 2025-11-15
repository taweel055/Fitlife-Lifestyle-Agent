"""Macronutrient data model"""

from pydantic import BaseModel, Field


class Macros(BaseModel):
    """Macronutrient breakdown"""

    protein: float = Field(..., ge=0, description="Protein in grams")
    carbs: float = Field(..., ge=0, description="Carbohydrates in grams")
    fat: float = Field(..., ge=0, description="Fat in grams")

    def calculate_calories(self) -> int:
        """Calculate total calories from macros"""
        return int((self.protein * 4) + (self.carbs * 4) + (self.fat * 9))

    def __str__(self) -> str:
        """String representation"""
        return f"{self.protein}p/{self.carbs}c/{self.fat}f ({self.calculate_calories()} cal)"

    def scale(self, factor: float) -> 'Macros':
        """Scale macros by a factor"""
        return Macros(
            protein=round(self.protein * factor, 1),
            carbs=round(self.carbs * factor, 1),
            fat=round(self.fat * factor, 1)
        )

    def round_up(self, nearest: int = 5) -> 'Macros':
        """Round macros up to nearest specified value"""
        import math
        return Macros(
            protein=math.ceil(self.protein / nearest) * nearest,
            carbs=math.ceil(self.carbs / nearest) * nearest,
            fat=math.ceil(self.fat / nearest) * nearest
        )

    class Config:
        json_schema_extra = {
            "example": {
                "protein": 50,
                "carbs": 25,
                "fat": 4
            }
        }
