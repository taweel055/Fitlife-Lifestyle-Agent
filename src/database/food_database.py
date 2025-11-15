"""Food Database with all food items"""

from typing import List, Optional
from ..models import Food, FoodCategory


class FoodDatabase:
    """Database of food items with nutritional information"""

    # All food items based on the specification
    FOODS = [
        # ===== PROTEINS - PREFERRED =====
        Food(
            name="Chicken Breast",
            arabic_name="صدر دجاج",
            category=FoodCategory.PROTEIN_PREFERRED,
            protein_per_serving=26,
            carbs_per_serving=0,
            fat_per_serving=3,
            serving_size="4 oz",
            serving_size_grams=113,
            notes="Skinless, boneless, grilled or baked"
        ),
        Food(
            name="Turkey Breast",
            arabic_name="صدر ديك رومي",
            category=FoodCategory.PROTEIN_PREFERRED,
            protein_per_serving=26,
            carbs_per_serving=0,
            fat_per_serving=1,
            serving_size="4 oz",
            serving_size_grams=113,
            notes="Skinless, boneless"
        ),
        Food(
            name="96/4 Ground Beef",
            arabic_name="لحم بقري مفروم",
            category=FoodCategory.PROTEIN_PREFERRED,
            protein_per_serving=24,
            carbs_per_serving=0,
            fat_per_serving=5,
            serving_size="4 oz",
            serving_size_grams=113,
            notes="Extra lean, 96% lean / 4% fat"
        ),
        Food(
            name="Egg Whites",
            arabic_name="بياض البيض",
            category=FoodCategory.PROTEIN_PREFERRED,
            protein_per_serving=25,
            carbs_per_serving=2,
            fat_per_serving=0,
            serving_size="1 cup",
            serving_size_grams=243,
            notes="Liquid egg whites or fresh"
        ),
        Food(
            name="White Fish (Tilapia)",
            arabic_name="سمك أبيض (بلطي)",
            category=FoodCategory.PROTEIN_PREFERRED,
            protein_per_serving=23,
            carbs_per_serving=0,
            fat_per_serving=3,
            serving_size="4 oz",
            serving_size_grams=113,
            notes="Baked or grilled"
        ),
        Food(
            name="White Fish (Cod)",
            arabic_name="سمك القد",
            category=FoodCategory.PROTEIN_PREFERRED,
            protein_per_serving=20,
            carbs_per_serving=0,
            fat_per_serving=1,
            serving_size="4 oz",
            serving_size_grams=113,
            notes="Baked or grilled"
        ),

        # ===== PROTEINS - SPARINGLY =====
        Food(
            name="93/7 Ground Beef",
            arabic_name="لحم بقري مفروم",
            category=FoodCategory.PROTEIN_SPARINGLY,
            protein_per_serving=22,
            carbs_per_serving=0,
            fat_per_serving=8,
            serving_size="4 oz",
            serving_size_grams=113,
            notes="93% lean / 7% fat"
        ),
        Food(
            name="93/7 Ground Turkey",
            arabic_name="ديك رومي مفروم",
            category=FoodCategory.PROTEIN_SPARINGLY,
            protein_per_serving=22,
            carbs_per_serving=0,
            fat_per_serving=8,
            serving_size="4 oz",
            serving_size_grams=113,
            notes="93% lean / 7% fat"
        ),
        Food(
            name="Salmon",
            arabic_name="سلمون",
            category=FoodCategory.PROTEIN_SPARINGLY,
            protein_per_serving=23,
            carbs_per_serving=0,
            fat_per_serving=13,
            serving_size="4 oz",
            serving_size_grams=113,
            notes="Wild-caught preferred, baked or grilled"
        ),
        Food(
            name="Whey Protein Powder",
            arabic_name="بروتين مصل اللبن",
            category=FoodCategory.PROTEIN_SPARINGLY,
            protein_per_serving=25,
            carbs_per_serving=3,
            fat_per_serving=1,
            serving_size="1 scoop (30g)",
            serving_size_grams=30,
            notes="Isolate preferred, mix with water"
        ),
        Food(
            name="Flank Steak",
            arabic_name="ستيك لحم بقري",
            category=FoodCategory.PROTEIN_SPARINGLY,
            protein_per_serving=23,
            carbs_per_serving=0,
            fat_per_serving=10,
            serving_size="4 oz",
            serving_size_grams=113,
            notes="Lean cut, grilled"
        ),

        # ===== CARBOHYDRATES - PREFERRED =====
        Food(
            name="White Rice",
            arabic_name="أرز أبيض",
            category=FoodCategory.CARB_PREFERRED,
            protein_per_serving=4,
            carbs_per_serving=45,
            fat_per_serving=0,
            serving_size="1 cup cooked",
            serving_size_grams=158,
            notes="Long grain, jasmine, or basmati"
        ),
        Food(
            name="Brown Rice",
            arabic_name="أرز بني",
            category=FoodCategory.CARB_PREFERRED,
            protein_per_serving=5,
            carbs_per_serving=45,
            fat_per_serving=2,
            serving_size="1 cup cooked",
            serving_size_grams=195,
            notes="Whole grain"
        ),
        Food(
            name="Cream of Rice",
            arabic_name="كريمة الأرز",
            category=FoodCategory.CARB_PREFERRED,
            protein_per_serving=2,
            carbs_per_serving=28,
            fat_per_serving=0,
            serving_size="1/4 cup dry",
            serving_size_grams=46,
            notes="Great for pre/post workout"
        ),
        Food(
            name="White Potato",
            arabic_name="البطاطس البيضاء",
            category=FoodCategory.CARB_PREFERRED,
            protein_per_serving=4,
            carbs_per_serving=37,
            fat_per_serving=0,
            serving_size="1 medium (6 oz)",
            serving_size_grams=170,
            notes="Baked or boiled"
        ),
        Food(
            name="Sweet Potato",
            arabic_name="البطاطا الحلوة",
            category=FoodCategory.CARB_PREFERRED,
            protein_per_serving=2,
            carbs_per_serving=27,
            fat_per_serving=0,
            serving_size="1 medium (5 oz)",
            serving_size_grams=130,
            notes="Baked or boiled"
        ),
        Food(
            name="Oats",
            arabic_name="الشوفان",
            category=FoodCategory.CARB_PREFERRED,
            protein_per_serving=5,
            carbs_per_serving=27,
            fat_per_serving=3,
            serving_size="1/2 cup dry",
            serving_size_grams=40,
            notes="Old-fashioned or quick oats"
        ),

        # ===== CARBOHYDRATES - SPARINGLY =====
        Food(
            name="Whole Wheat Bread",
            arabic_name="خبز القمح الكامل",
            category=FoodCategory.CARB_SPARINGLY,
            protein_per_serving=4,
            carbs_per_serving=12,
            fat_per_serving=1,
            serving_size="1 slice",
            serving_size_grams=28,
            notes="100% whole grain"
        ),
        Food(
            name="Whole Wheat Pasta",
            arabic_name="معكرونة القمح الكامل",
            category=FoodCategory.CARB_SPARINGLY,
            protein_per_serving=7,
            carbs_per_serving=37,
            fat_per_serving=1,
            serving_size="2 oz dry",
            serving_size_grams=56,
            notes="Whole grain"
        ),
        Food(
            name="Whole Wheat Bagel",
            arabic_name="خبز البيجل",
            category=FoodCategory.CARB_SPARINGLY,
            protein_per_serving=10,
            carbs_per_serving=48,
            fat_per_serving=2,
            serving_size="1 medium bagel",
            serving_size_grams=95,
            notes="Whole grain"
        ),

        # ===== CARBOHYDRATES - SUGARY (HIGH DAYS ONLY) =====
        Food(
            name="Fruit Juice (Orange)",
            arabic_name="عصير البرتقال",
            category=FoodCategory.CARB_SUGARY,
            protein_per_serving=2,
            carbs_per_serving=26,
            fat_per_serving=0,
            serving_size="1 cup",
            serving_size_grams=248,
            notes="100% juice, HIGH days only"
        ),
        Food(
            name="Banana",
            arabic_name="موز",
            category=FoodCategory.CARB_SUGARY,
            protein_per_serving=1,
            carbs_per_serving=27,
            fat_per_serving=0,
            serving_size="1 medium",
            serving_size_grams=118,
            notes="Fresh fruit, HIGH days only"
        ),
        Food(
            name="Apple",
            arabic_name="تفاح",
            category=FoodCategory.CARB_SUGARY,
            protein_per_serving=0,
            carbs_per_serving=25,
            fat_per_serving=0,
            serving_size="1 medium",
            serving_size_grams=182,
            notes="Fresh fruit, HIGH days only"
        ),
        Food(
            name="Skittles",
            arabic_name="سكيتلز",
            category=FoodCategory.CARB_SUGARY,
            protein_per_serving=0,
            carbs_per_serving=47,
            fat_per_serving=2,
            serving_size="2 oz",
            serving_size_grams=56,
            notes="HIGH days only, 50% of carbs allowed"
        ),
        Food(
            name="Twizzlers",
            arabic_name="تويزلرز",
            category=FoodCategory.CARB_SUGARY,
            protein_per_serving=1,
            carbs_per_serving=36,
            fat_per_serving=0,
            serving_size="4 pieces",
            serving_size_grams=45,
            notes="HIGH days only, 50% of carbs allowed"
        ),
        Food(
            name="Jelly/Jam",
            arabic_name="مربى",
            category=FoodCategory.CARB_SUGARY,
            protein_per_serving=0,
            carbs_per_serving=13,
            fat_per_serving=0,
            serving_size="1 tbsp",
            serving_size_grams=20,
            notes="HIGH days only, 50% of carbs allowed"
        ),

        # ===== FATS =====
        Food(
            name="Almonds",
            arabic_name="لوز",
            category=FoodCategory.FAT,
            protein_per_serving=6,
            carbs_per_serving=6,
            fat_per_serving=14,
            serving_size="1 oz (23 almonds)",
            serving_size_grams=28,
            notes="Raw or roasted, unsalted"
        ),
        Food(
            name="Walnuts",
            arabic_name="جوز",
            category=FoodCategory.FAT,
            protein_per_serving=4,
            carbs_per_serving=4,
            fat_per_serving=18,
            serving_size="1 oz (14 halves)",
            serving_size_grams=28,
            notes="Raw or roasted"
        ),
        Food(
            name="Peanut Butter",
            arabic_name="زبدة الفول السوداني",
            category=FoodCategory.FAT,
            protein_per_serving=8,
            carbs_per_serving=6,
            fat_per_serving=16,
            serving_size="2 tbsp",
            serving_size_grams=32,
            notes="Natural, no added sugar"
        ),
        Food(
            name="Almond Butter",
            arabic_name="زبدة اللوز",
            category=FoodCategory.FAT,
            protein_per_serving=7,
            carbs_per_serving=6,
            fat_per_serving=18,
            serving_size="2 tbsp",
            serving_size_grams=32,
            notes="Natural, no added sugar"
        ),
        Food(
            name="Avocado",
            arabic_name="أفوكادو",
            category=FoodCategory.FAT,
            protein_per_serving=3,
            carbs_per_serving=12,
            fat_per_serving=22,
            serving_size="1 medium",
            serving_size_grams=150,
            notes="Fresh"
        ),
        Food(
            name="Olive Oil",
            arabic_name="زيت الزيتون",
            category=FoodCategory.FAT,
            protein_per_serving=0,
            carbs_per_serving=0,
            fat_per_serving=14,
            serving_size="1 tbsp",
            serving_size_grams=14,
            notes="Extra virgin"
        ),
        Food(
            name="Coconut Oil",
            arabic_name="زيت جوز الهند",
            category=FoodCategory.FAT,
            protein_per_serving=0,
            carbs_per_serving=0,
            fat_per_serving=14,
            serving_size="1 tbsp",
            serving_size_grams=14,
            notes="Unrefined"
        ),
        Food(
            name="Fish Oil",
            arabic_name="زيت السمك",
            category=FoodCategory.FAT,
            protein_per_serving=0,
            carbs_per_serving=0,
            fat_per_serving=1,
            serving_size="1 capsule",
            serving_size_grams=1,
            notes="Omega-3 supplement"
        ),

        # ===== VEGETABLES (Free carbs when <25g meals) =====
        Food(
            name="Broccoli",
            arabic_name="بروكلي",
            category=FoodCategory.VEGETABLE,
            protein_per_serving=3,
            carbs_per_serving=6,
            fat_per_serving=0,
            serving_size="1 cup chopped",
            serving_size_grams=91,
            notes="Steamed or raw"
        ),
        Food(
            name="Asparagus",
            arabic_name="هليون",
            category=FoodCategory.VEGETABLE,
            protein_per_serving=3,
            carbs_per_serving=5,
            fat_per_serving=0,
            serving_size="1 cup",
            serving_size_grams=134,
            notes="Steamed or grilled"
        ),
        Food(
            name="Green Beans",
            arabic_name="فاصوليا خضراء",
            category=FoodCategory.VEGETABLE,
            protein_per_serving=2,
            carbs_per_serving=7,
            fat_per_serving=0,
            serving_size="1 cup",
            serving_size_grams=100,
            notes="Steamed or sautéed"
        ),
        Food(
            name="Spinach",
            arabic_name="سبانخ",
            category=FoodCategory.VEGETABLE,
            protein_per_serving=1,
            carbs_per_serving=1,
            fat_per_serving=0,
            serving_size="1 cup raw",
            serving_size_grams=30,
            notes="Raw or steamed"
        ),
        Food(
            name="Bell Peppers",
            arabic_name="فلفل حلو",
            category=FoodCategory.VEGETABLE,
            protein_per_serving=1,
            carbs_per_serving=6,
            fat_per_serving=0,
            serving_size="1 cup chopped",
            serving_size_grams=149,
            notes="Raw or roasted"
        ),
        Food(
            name="Cauliflower",
            arabic_name="قرنبيط",
            category=FoodCategory.VEGETABLE,
            protein_per_serving=2,
            carbs_per_serving=5,
            fat_per_serving=0,
            serving_size="1 cup chopped",
            serving_size_grams=107,
            notes="Steamed or roasted"
        ),
        Food(
            name="Zucchini",
            arabic_name="كوسة",
            category=FoodCategory.VEGETABLE,
            protein_per_serving=1,
            carbs_per_serving=3,
            fat_per_serving=0,
            serving_size="1 cup chopped",
            serving_size_grams=124,
            notes="Grilled or sautéed"
        ),
    ]

    def __init__(self):
        """Initialize food database"""
        self._foods = {food.name: food for food in self.FOODS}

    def get_all_foods(self) -> List[Food]:
        """Get all foods in database"""
        return list(self._foods.values())

    def get_food_by_name(self, name: str) -> Optional[Food]:
        """Get a specific food by name"""
        return self._foods.get(name)

    def get_foods_by_category(self, category: FoodCategory) -> List[Food]:
        """Get all foods in a specific category"""
        return [food for food in self._foods.values() if food.category == category]

    def get_protein_sources(self, preferred_only: bool = False) -> List[Food]:
        """Get protein sources"""
        if preferred_only:
            return self.get_foods_by_category(FoodCategory.PROTEIN_PREFERRED)
        return (
            self.get_foods_by_category(FoodCategory.PROTEIN_PREFERRED) +
            self.get_foods_by_category(FoodCategory.PROTEIN_SPARINGLY)
        )

    def get_carb_sources(self, preferred_only: bool = False, allow_sugary: bool = False) -> List[Food]:
        """Get carbohydrate sources"""
        carbs = []
        if preferred_only:
            carbs = self.get_foods_by_category(FoodCategory.CARB_PREFERRED)
        else:
            carbs = (
                self.get_foods_by_category(FoodCategory.CARB_PREFERRED) +
                self.get_foods_by_category(FoodCategory.CARB_SPARINGLY)
            )

        if allow_sugary:
            carbs += self.get_foods_by_category(FoodCategory.CARB_SUGARY)

        return carbs

    def get_fat_sources(self) -> List[Food]:
        """Get fat sources"""
        return self.get_foods_by_category(FoodCategory.FAT)

    def get_vegetables(self) -> List[Food]:
        """Get vegetable options"""
        return self.get_foods_by_category(FoodCategory.VEGETABLE)
