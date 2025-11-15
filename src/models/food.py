"""Food data models"""

from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field
from .macros import Macros


class FoodCategory(str, Enum):
    """Food category classifications"""
    PROTEIN_PREFERRED = "PROTEIN_PREFERRED"
    PROTEIN_SPARINGLY = "PROTEIN_SPARINGLY"
    CARB_PREFERRED = "CARB_PREFERRED"
    CARB_SPARINGLY = "CARB_SPARINGLY"
    CARB_SUGARY = "CARB_SUGARY"  # For HIGH days only
    FAT = "FAT"
    VEGETABLE = "VEGETABLE"


class Food(BaseModel):
    """Food item with nutritional information"""

    name: str = Field(..., description="Food name in English")
    arabic_name: Optional[str] = Field(None, description="Food name in Arabic")

    category: FoodCategory = Field(..., description="Food category")

    # Macros per standard serving
    protein_per_serving: float = Field(default=0, ge=0, description="Protein grams per serving")
    carbs_per_serving: float = Field(default=0, ge=0, description="Carbs grams per serving")
    fat_per_serving: float = Field(default=0, ge=0, description="Fat grams per serving")

    serving_size: str = Field(..., description="Standard serving size (e.g., '4 oz', '1 cup')")
    serving_size_grams: Optional[float] = Field(None, description="Serving size in grams")

    notes: Optional[str] = Field(None, description="Special notes or preparation tips")

    def get_macros(self) -> Macros:
        """Get macros as Macros object"""
        return Macros(
            protein=self.protein_per_serving,
            carbs=self.carbs_per_serving,
            fat=self.fat_per_serving
        )

    def calculate_serving_for_protein(self, target_protein: float) -> tuple[float, Macros]:
        """
        Calculate serving size needed to hit target protein
        Returns: (servings_needed, total_macros)
        """
        if self.protein_per_serving == 0:
            return (0, Macros(protein=0, carbs=0, fat=0))

        servings = target_protein / self.protein_per_serving
        return (
            round(servings, 2),
            Macros(
                protein=round(servings * self.protein_per_serving, 1),
                carbs=round(servings * self.carbs_per_serving, 1),
                fat=round(servings * self.fat_per_serving, 1)
            )
        )

    def calculate_serving_for_carbs(self, target_carbs: float) -> tuple[float, Macros]:
        """
        Calculate serving size needed to hit target carbs
        Returns: (servings_needed, total_macros)
        """
        if self.carbs_per_serving == 0:
            return (0, Macros(protein=0, carbs=0, fat=0))

        servings = target_carbs / self.carbs_per_serving
        return (
            round(servings, 2),
            Macros(
                protein=round(servings * self.protein_per_serving, 1),
                carbs=round(servings * self.carbs_per_serving, 1),
                fat=round(servings * self.fat_per_serving, 1)
            )
        )

    def calculate_serving_for_fat(self, target_fat: float) -> tuple[float, Macros]:
        """
        Calculate serving size needed to hit target fat
        Returns: (servings_needed, total_macros)
        """
        if self.fat_per_serving == 0:
            return (0, Macros(protein=0, carbs=0, fat=0))

        servings = target_fat / self.fat_per_serving
        return (
            round(servings, 2),
            Macros(
                protein=round(servings * self.protein_per_serving, 1),
                carbs=round(servings * self.carbs_per_serving, 1),
                fat=round(servings * self.fat_per_serving, 1)
            )
        )

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Chicken Breast",
                "arabic_name": "صدر دجاج",
                "category": "PROTEIN_PREFERRED",
                "protein_per_serving": 26,
                "carbs_per_serving": 0,
                "fat_per_serving": 3,
                "serving_size": "4 oz",
                "serving_size_grams": 113,
                "notes": "Skinless, boneless"
            }
        }
