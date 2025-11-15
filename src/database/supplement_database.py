"""Supplement Database and Recommendation Engine"""

from typing import List
from ..models import (
    Supplement, SupplementStack, SupplementTiming,
    SupplementPurpose, Protocol
)


class SupplementDatabase:
    """Database of supplements and recommendation engine"""

    # Core supplements database
    SUPPLEMENTS = {
        # ===== Universal Supplements =====
        'whey_protein': Supplement(
            name="Whey Protein Isolate",
            arabic_name="بروتين مصل اللبن",
            dose="25-40g",
            timing=SupplementTiming.POST_WORKOUT,
            purpose=SupplementPurpose.MUSCLE_RECOVERY,
            estimated_cost_per_month=45.0,
            is_optional=False,
            notes="Mix with water immediately post-workout. Isolate preferred for lower fat/carbs"
        ),
        'creatine': Supplement(
            name="Creatine Monohydrate",
            arabic_name="كرياتين مونوهيدرات",
            dose="5g",
            timing=SupplementTiming.DAILY,
            purpose=SupplementPurpose.MUSCLE_GAIN,
            estimated_cost_per_month=15.0,
            is_optional=False,
            notes="Take daily, timing doesn't matter. Stay hydrated."
        ),
        'omega3': Supplement(
            name="Omega-3 Fish Oil",
            arabic_name="زيت السمك أوميغا-3",
            dose="2-4g EPA+DHA",
            timing=SupplementTiming.DINNER,
            purpose=SupplementPurpose.INFLAMMATION,
            estimated_cost_per_month=25.0,
            is_optional=False,
            notes="Take with fatty meal for better absorption"
        ),
        'vitamin_d': Supplement(
            name="Vitamin D3",
            arabic_name="فيتامين د3",
            dose="2000-5000 IU",
            timing=SupplementTiming.BREAKFAST,
            purpose=SupplementPurpose.HEALTH,
            estimated_cost_per_month=10.0,
            is_optional=False,
            notes="Important for bone health and immunity"
        ),
        'magnesium': Supplement(
            name="Magnesium Glycinate",
            arabic_name="مغنيسيوم جليسينات",
            dose="200-400mg",
            timing=SupplementTiming.BEFORE_BED,
            purpose=SupplementPurpose.SLEEP,
            estimated_cost_per_month=15.0,
            is_optional=False,
            notes="Helps with sleep quality and recovery. Glycinate form is best absorbed."
        ),
        'multivitamin': Supplement(
            name="Multivitamin",
            arabic_name="فيتامينات متعددة",
            dose="1 tablet",
            timing=SupplementTiming.BREAKFAST,
            purpose=SupplementPurpose.MICRONUTRIENTS,
            estimated_cost_per_month=20.0,
            is_optional=False,
            notes="Fill nutritional gaps, take with food"
        ),

        # ===== Cutting-Specific =====
        'l_carnitine': Supplement(
            name="L-Carnitine",
            arabic_name="إل-كارنيتين",
            dose="2-3g",
            timing=SupplementTiming.PRE_WORKOUT,
            purpose=SupplementPurpose.FAT_LOSS,
            estimated_cost_per_month=30.0,
            is_optional=False,
            notes="Helps mobilize fat for energy during cardio"
        ),
        'caffeine': Supplement(
            name="Caffeine",
            arabic_name="كافيين",
            dose="200-400mg",
            timing=SupplementTiming.PRE_WORKOUT,
            purpose=SupplementPurpose.ENERGY,
            estimated_cost_per_month=15.0,
            is_optional=False,
            notes="Use pre-workout or early morning. Avoid after 2 PM."
        ),
        'green_tea': Supplement(
            name="Green Tea Extract",
            arabic_name="مستخلص الشاي الأخضر",
            dose="500mg EGCG",
            timing=SupplementTiming.MORNING,
            purpose=SupplementPurpose.FAT_LOSS,
            estimated_cost_per_month=20.0,
            is_optional=True,
            notes="Supports metabolism. Contains some caffeine."
        ),
        'cla': Supplement(
            name="CLA (Conjugated Linoleic Acid)",
            arabic_name="حمض اللينوليك المترافق",
            dose="3-6g",
            timing=SupplementTiming.DAILY,
            purpose=SupplementPurpose.FAT_LOSS,
            estimated_cost_per_month=25.0,
            is_optional=True,
            notes="May help with body composition. Take with meals."
        ),

        # ===== Bulking-Specific =====
        'beta_alanine': Supplement(
            name="Beta-Alanine",
            arabic_name="بيتا ألانين",
            dose="3-5g",
            timing=SupplementTiming.DAILY,
            purpose=SupplementPurpose.PERFORMANCE,
            estimated_cost_per_month=20.0,
            is_optional=False,
            notes="Improves endurance. May cause tingling (harmless)."
        ),
        'digestive_enzymes': Supplement(
            name="Digestive Enzymes",
            arabic_name="إنزيمات هاضمة",
            dose="1-2 capsules",
            timing=SupplementTiming.BREAKFAST,
            purpose=SupplementPurpose.DIGESTION,
            estimated_cost_per_month=25.0,
            is_optional=True,
            notes="Helps digest large meals and protein intake"
        ),
        'mass_gainer': Supplement(
            name="Mass Gainer",
            arabic_name="مكمل زيادة الوزن",
            dose="1-2 servings",
            timing=SupplementTiming.POST_WORKOUT,
            purpose=SupplementPurpose.MUSCLE_GAIN,
            estimated_cost_per_month=60.0,
            is_optional=True,
            notes="Only if struggling to eat enough calories"
        ),

        # ===== Performance & Optional =====
        'casein': Supplement(
            name="Casein Protein",
            arabic_name="بروتين الكازين",
            dose="30-40g",
            timing=SupplementTiming.BEFORE_BED,
            purpose=SupplementPurpose.MUSCLE_RECOVERY,
            estimated_cost_per_month=50.0,
            is_optional=True,
            notes="Slow-digesting protein for overnight recovery"
        ),
        'bcaa': Supplement(
            name="BCAAs",
            arabic_name="أحماض أمينية متفرعة السلسلة",
            dose="5-10g",
            timing=SupplementTiming.INTRA_WORKOUT,
            purpose=SupplementPurpose.MUSCLE_RECOVERY,
            estimated_cost_per_month=30.0,
            is_optional=True,
            notes="Can help during fasted training or long workouts"
        ),
    }

    def __init__(self):
        """Initialize supplement database"""
        pass

    def get_cutting_stack(self) -> SupplementStack:
        """Get CUTTING supplement stack for SHREDDED protocol"""
        supplements = [
            self.SUPPLEMENTS['whey_protein'],
            self.SUPPLEMENTS['l_carnitine'],
            self.SUPPLEMENTS['caffeine'],
            self.SUPPLEMENTS['omega3'],
            self.SUPPLEMENTS['magnesium'],
            self.SUPPLEMENTS['multivitamin'],
            self.SUPPLEMENTS['green_tea'],  # Optional
            self.SUPPLEMENTS['cla'],  # Optional
        ]

        stack = SupplementStack(
            stack_name="CUTTING STACK",
            goal="SHREDDED (Fat Loss)",
            supplements=supplements,
            total_estimated_cost_min=120,
            total_estimated_cost_max=180
        )

        return stack

    def get_bulking_stack(self) -> SupplementStack:
        """Get BULKING supplement stack for MASSIVE protocol"""
        supplements = [
            self.SUPPLEMENTS['whey_protein'],
            self.SUPPLEMENTS['creatine'],
            self.SUPPLEMENTS['beta_alanine'],
            self.SUPPLEMENTS['omega3'],
            self.SUPPLEMENTS['vitamin_d'],
            self.SUPPLEMENTS['magnesium'],
            self.SUPPLEMENTS['digestive_enzymes'],  # Optional
            self.SUPPLEMENTS['mass_gainer'],  # Optional
        ]

        stack = SupplementStack(
            stack_name="BULKING STACK",
            goal="MASSIVE (Muscle Gain)",
            supplements=supplements,
            total_estimated_cost_min=150,
            total_estimated_cost_max=220
        )

        return stack

    def get_recommended_stack(self, protocol: Protocol) -> SupplementStack:
        """
        Get recommended supplement stack based on protocol

        Args:
            protocol: SHREDDED or MASSIVE

        Returns:
            Appropriate supplement stack
        """
        if protocol == Protocol.SHREDDED:
            return self.get_cutting_stack()
        else:  # Protocol.MASSIVE
            return self.get_bulking_stack()

    def get_top_10_supplements(self) -> List[Supplement]:
        """Get top 10 most prescribed supplements"""
        top_10 = [
            self.SUPPLEMENTS['whey_protein'],      # 95% of clients
            self.SUPPLEMENTS['creatine'],          # 85% of clients
            self.SUPPLEMENTS['omega3'],            # 90% of clients
            self.SUPPLEMENTS['vitamin_d'],         # 80% of clients
            self.SUPPLEMENTS['magnesium'],         # 75% of clients
            self.SUPPLEMENTS['multivitamin'],      # 70% of clients
            self.SUPPLEMENTS['caffeine'],          # 65% of clients
            self.SUPPLEMENTS['l_carnitine'],       # 60% of cutting clients
            self.SUPPLEMENTS['casein'],            # 55% of clients
            self.SUPPLEMENTS['beta_alanine'],      # 45% of performance clients
        ]
        return top_10

    def get_all_supplements(self) -> List[Supplement]:
        """Get all supplements in database"""
        return list(self.SUPPLEMENTS.values())
