# 📁 Project Structure Overview

## Repository: Fitlife-Lifestyle-Agent

### 🎯 Purpose
Automated meal plan generation system for nutrition consulting supporting SHREDDED (fat loss) and MASSIVE (muscle gain) protocols.

---

## 📂 Directory Structure

```
Fitlife-Lifestyle-Agent/
│
├── 📄 main.py                      # Main application entry point (CLI)
├── 📄 test_functionality.py        # Comprehensive test suite (7 tests)
├── 📄 requirements.txt             # Python dependencies
├── 📄 README.md                    # Full documentation
├── 📄 VALIDATION_REPORT.md         # Test results and validation
├── 📄 .gitignore                   # Git ignore rules
│
├── 📁 src/                         # Source code
│   ├── 📄 __init__.py
│   │
│   ├── 📁 models/                  # Data models (Pydantic)
│   │   ├── client.py              # Client profile, protocols
│   │   ├── meal.py                # Meal, DayPlan, WeekPlan
│   │   ├── food.py                # Food items, categories
│   │   ├── supplement.py          # Supplements, stacks
│   │   └── macros.py              # Macronutrient calculations
│   │
│   ├── 📁 calculators/             # Calculation engines
│   │   ├── lbm_calculator.py      # Lean body mass
│   │   └── macro_calculator.py    # Protocol macros
│   │
│   ├── 📁 database/                # Data stores
│   │   ├── food_database.py       # 41 food items
│   │   └── supplement_database.py # Supplement stacks
│   │
│   ├── 📁 generators/              # Meal plan generation
│   │   └── meal_plan_generator.py # Complete week plans
│   │
│   ├── 📁 exporters/               # Export functionality
│   │   └── markdown_exporter.py   # MD export with tables
│   │
│   └── 📁 utils/                   # Utilities
│       └── input_collector.py     # Interactive input
│
├── 📁 examples/                    # Example scripts
│   └── example_usage.py           # 6 usage examples
│
└── 📁 output/                      # Generated meal plans
    └── (auto-created when exporting)
```

---

## 📊 File Statistics

| Category | Count |
|----------|-------|
| Python modules | 19 |
| Total files | 25+ |
| Lines of code | 3,700+ |
| Test suites | 7 |
| Example scripts | 6 |

---

## 🎯 Key Components

### 1. Models (5 modules)
- `client.py` - Client profiles with validation
- `meal.py` - Meal plans and day structures
- `food.py` - Food items with macros
- `supplement.py` - Supplement recommendations
- `macros.py` - Macronutrient calculations

### 2. Calculators (2 modules)
- `lbm_calculator.py` - Body composition
- `macro_calculator.py` - Protocol specifications

### 3. Databases (2 modules)
- `food_database.py` - 41 food items
- `supplement_database.py` - CUTTING & BULKING stacks

### 4. Generators (1 module)
- `meal_plan_generator.py` - Complete meal plans

### 5. Exporters (1 module)
- `markdown_exporter.py` - Professional documents

### 6. Utils (1 module)
- `input_collector.py` - Interactive CLI

---

## 🔧 Core Technologies

- **Language**: Python 3.10+
- **Validation**: Pydantic 2.5+
- **Web Framework**: FastAPI 0.104+ (for future API)
- **Templates**: Jinja2 3.1+
- **PDF**: ReportLab 4.0+ (Phase 2)

---

## 📝 Documentation Files

| File | Purpose |
|------|---------|
| README.md | Full user documentation |
| VALIDATION_REPORT.md | Test results and validation |
| PROJECT_SUMMARY.md | This file (structure overview) |

---

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run application
python main.py

# Run tests
python test_functionality.py

# See examples
python examples/example_usage.py
```

---

## 📦 Exports Generated

When generating a meal plan, the app creates:

1. **Week Plan**: `ClientName_PROTOCOL_Week1_TIMESTAMP.md`
   - 7-day complete schedule
   - Meal timing and macros
   - Food suggestions

2. **Supplements**: `ClientName_PROTOCOL_Supplements_TIMESTAMP.md`
   - Required vs optional
   - Dosage and timing
   - Monthly costs

3. **Summary**: `ClientName_PROTOCOL_Summary_TIMESTAMP.md`
   - Client stats
   - LBM and targets
   - Protocol details

All saved to `output/` directory.

---

## ✅ Quality Assurance

- **Test Coverage**: 7/7 tests passing (100%)
- **Type Hints**: Throughout codebase
- **Validation**: Pydantic models
- **Documentation**: Inline + README
- **Error Handling**: Comprehensive

---

## 🎯 Development Status

- **Phase 1**: ✅ COMPLETE (Production Ready)
- **Phase 2**: Planned (Arabic, PDF, Database)
- **Phase 3**: Future (WhatsApp, Web, Mobile)

---

**Last Updated**: 2025-11-15
**Status**: Production Ready ✅
