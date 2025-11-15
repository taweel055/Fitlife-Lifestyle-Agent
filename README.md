# Fitlife Lifestyle Agent - Meal Plan Generator

An automated meal plan generation system for nutrition consulting that supports **SHREDDED** (fat loss) and **MASSIVE** (muscle gain) protocols with supplement prescriptions and bilingual output (English/Arabic).

## Features

### Core Functionality
- ✅ **Client Profile Management** - Collect and store client information
- ✅ **LBM Calculator** - Automatic lean body mass calculations
- ✅ **Macro Calculator** - Protocol-specific macronutrient targets
- ✅ **Meal Plan Generator** - Complete 7-day meal plans with timing
- ✅ **Food Database** - Comprehensive food library with nutritional info
- ✅ **Supplement Recommendations** - Goal-based supplement stacks
- ✅ **Markdown Export** - Professional meal plan documents
- 🔜 **Arabic Translation** - Bilingual output support (Phase 2)
- 🔜 **PDF Export** - Branded PDF reports (Phase 2)

### Protocols Supported

#### SHREDDED Protocol (Fat Loss)
- **LOW Days** (Non-training): 300p/120c - 6 regular meals
- **MEDIUM Days** (Training): 250p/220c - 3 training + 4 regular meals
- **HIGH Days** (Weekly): 190p/730c - Includes sugary carb options
- **Cardio**: 30 min HIIT 5x/week OR 15,000 steps/day

#### MASSIVE Protocol (Muscle Gain)
- **LOW Days** (Non-training): 300p/240c - 6 regular meals
- **MEDIUM Days** (Training): 310p/450c - 3 training + 4 regular meals
- **HIGH Days** (2x/week): 220p/730c - Includes sugary carb options
- **Cardio**: 12 min HIIT 3x/week OR 12,000 steps/day

## Installation

### Prerequisites
- Python 3.10 or higher
- pip (Python package manager)

### Setup
```bash
# Clone the repository
git clone https://github.com/taweel055/Fitlife-Lifestyle-Agent.git
cd Fitlife-Lifestyle-Agent

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

## Usage

### Interactive Mode (Recommended)
```bash
python main.py
```

Follow the interactive prompts to:
1. Enter client information (name, weight, body fat %, etc.)
2. Select protocol (SHREDDED or MASSIVE)
3. Choose training days and HIGH days
4. Generate complete meal plan with supplements

### Demo Mode
Run a quick demo with sample client data:
```bash
python main.py
# Select option 2 from the menu
```

### Programmatic Usage
```python
from src.models import Client, Protocol
from src.generators import MealPlanGenerator
from src.database import SupplementDatabase
from src.exporters import MarkdownExporter

# Create client
client = Client(
    name="Ahmed Hassan",
    weight=180,
    weight_unit="lbs",
    body_fat_percentage=15.0,
    protocol=Protocol.SHREDDED,
    training_days=["Monday", "Wednesday", "Friday"],
    high_days=["Saturday"],
    language="en"
)

# Generate meal plan
generator = MealPlanGenerator()
week_plan = generator.generate_week_plan(client)

# Get supplements
supp_db = SupplementDatabase()
supplements = supp_db.get_recommended_stack(client.protocol)

# Export to markdown
week_md = MarkdownExporter.export_week_plan(week_plan)
MarkdownExporter.save_to_file(week_md, "meal_plan.md")
```

## Project Structure

```
Fitlife-Lifestyle-Agent/
│
├── main.py                      # Application entry point
├── requirements.txt             # Python dependencies
├── README.md                    # This file
│
├── src/
│   ├── __init__.py
│   │
│   ├── models/                  # Data models
│   │   ├── client.py           # Client profile
│   │   ├── meal.py             # Meal and day plans
│   │   ├── food.py             # Food items
│   │   ├── supplement.py       # Supplements
│   │   └── macros.py           # Macronutrients
│   │
│   ├── calculators/             # Calculation engines
│   │   ├── lbm_calculator.py   # Lean body mass
│   │   └── macro_calculator.py # Macronutrient targets
│   │
│   ├── database/                # Food and supplement data
│   │   ├── food_database.py    # 40+ food items
│   │   └── supplement_database.py  # Supplement stacks
│   │
│   ├── generators/              # Meal plan generation
│   │   └── meal_plan_generator.py
│   │
│   ├── exporters/               # Export functionality
│   │   └── markdown_exporter.py
│   │
│   └── utils/                   # Utilities
│       └── input_collector.py  # Interactive input
│
└── output/                      # Generated meal plans (auto-created)
```

## Food Database

### Protein Sources
**Preferred**: Chicken breast, turkey breast, 96/4 ground beef, egg whites, white fish
**Sparingly**: 93/7 ground meats, salmon, whey protein, flank steak

### Carbohydrate Sources
**Preferred**: White rice, brown rice, cream of rice, potatoes, sweet potatoes, oats
**Sparingly**: Whole wheat bread, pasta, bagels
**HIGH Days Only**: Fruit juice, fresh fruit, skittles, twizzlers, jelly

### Fat Sources
Almonds, walnuts, peanut butter, almond butter, avocado, olive oil, coconut oil, fish oil

### Vegetables (Free Carbs)
Broccoli, asparagus, green beans, spinach, bell peppers, cauliflower, zucchini

## Supplement Stacks

### CUTTING Stack (SHREDDED)
- Whey Protein Isolate (25-40g post-workout)
- L-Carnitine (2-3g pre-workout)
- Caffeine (200-400mg pre-workout)
- Omega-3 (2-4g with dinner)
- Magnesium (200-400mg before bed)
- Multivitamin (with breakfast)
- *Optional*: Green Tea Extract, CLA

**Est. Cost**: $120-180/month

### BULKING Stack (MASSIVE)
- Whey Protein Isolate (25-40g post-workout)
- Creatine Monohydrate (5g daily)
- Beta-Alanine (3-5g daily)
- Omega-3 (2-4g with dinner)
- Vitamin D3 (2000-5000 IU)
- Magnesium (200-400mg before bed)
- *Optional*: Digestive Enzymes, Mass Gainer

**Est. Cost**: $150-220/month

## Output Examples

The application generates three markdown files per client:

1. **Week Plan** - Complete 7-day meal schedule with:
   - Meal timing
   - Macronutrient breakdown per meal
   - Daily totals
   - Food suggestions for each meal

2. **Supplement Stack** - Personalized supplement recommendations with:
   - Required vs optional supplements
   - Dosage and timing
   - Purpose and benefits
   - Cost estimates

3. **Protocol Summary** - Overview including:
   - Client stats and LBM
   - Training schedule
   - Macro targets for each day type
   - Cardio requirements

All files are saved to the `output/` directory with timestamps.

## Calculations

### Lean Body Mass (LBM)
```
LBM = Body Weight × (1 - Body Fat %)
```

### Protein Per Meal
```
Protein = Round up to nearest 5g of: (LBM ÷ 8) × 2
```

### Calories
```
Calories = (Protein × 4) + (Carbs × 4) + (Fat × 9)
```

## Development Roadmap

### Phase 1 (✅ COMPLETE)
- [x] Client input collection
- [x] LBM and macro calculators
- [x] Meal plan generator (both protocols)
- [x] Food database (40+ items)
- [x] Supplement recommendation engine
- [x] Markdown export

### Phase 2 (Planned)
- [ ] Arabic translation
- [ ] PDF export with branding
- [ ] Database storage (SQLite)
- [ ] Client history tracking

### Phase 3 (Future)
- [ ] WhatsApp integration
- [ ] Automated weekly plan generation
- [ ] Progress tracking & adjustments
- [ ] Email delivery system
- [ ] Web interface

## Contributing

This is a private project for Abdallah's nutrition consulting business. For questions or issues, please contact the development team.

## License

Copyright © 2024 Fitlife Lifestyle Agent. All rights reserved.

## Support

For technical support or feature requests, please create an issue in the repository or contact the maintainer.

---

**Built with ❤️ for nutrition professionals**
