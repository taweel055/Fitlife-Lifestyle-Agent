"""Lean Body Mass Calculator"""

import math
from ..models import Client


class LBMCalculator:
    """Calculate Lean Body Mass (LBM)"""

    @staticmethod
    def calculate_lbm(client: Client) -> float:
        """
        Calculate Lean Body Mass
        Formula: LBM = Body Weight × (1 - Body Fat %)

        Args:
            client: Client object with weight and body fat percentage

        Returns:
            Lean Body Mass in pounds
        """
        weight_lbs = client.get_weight_in_lbs()
        body_fat_decimal = client.body_fat_percentage / 100.0

        lbm = weight_lbs * (1 - body_fat_decimal)

        return round(lbm, 1)

    @staticmethod
    def calculate_protein_per_meal(lbm: float) -> int:
        """
        Calculate protein per meal
        Formula: Round up to nearest 5g of: (LBM ÷ 8) × 2

        Args:
            lbm: Lean Body Mass in pounds

        Returns:
            Protein per meal in grams (rounded up to nearest 5g)
        """
        protein = (lbm / 8) * 2
        protein_rounded = math.ceil(protein / 5) * 5

        return int(protein_rounded)

    @staticmethod
    def get_client_lbm_and_protein(client: Client) -> tuple[float, int]:
        """
        Get both LBM and protein per meal for a client

        Args:
            client: Client object

        Returns:
            Tuple of (lbm, protein_per_meal)
        """
        lbm = LBMCalculator.calculate_lbm(client)
        protein_per_meal = LBMCalculator.calculate_protein_per_meal(lbm)

        return (lbm, protein_per_meal)
