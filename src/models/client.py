"""Client data model"""

from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator


class Protocol(str, Enum):
    """Training protocol type"""
    SHREDDED = "SHREDDED"  # Fat loss
    MASSIVE = "MASSIVE"    # Muscle gain


class WeightUnit(str, Enum):
    """Weight measurement units"""
    LBS = "lbs"
    KG = "kg"


class Language(str, Enum):
    """Output language preference"""
    ENGLISH = "en"
    ARABIC = "ar"


class Client(BaseModel):
    """Client profile and preferences"""

    name: str = Field(..., min_length=1, description="Client name")

    weight: float = Field(..., gt=0, description="Body weight")
    weight_unit: WeightUnit = Field(default=WeightUnit.LBS, description="Weight unit")

    body_fat_percentage: float = Field(
        ...,
        ge=5,
        le=50,
        description="Body fat percentage (5-50%)"
    )

    height: Optional[float] = Field(
        None,
        gt=0,
        description="Height (required for MASSIVE protocol)"
    )

    protocol: Protocol = Field(..., description="Training protocol")

    training_days: List[str] = Field(
        default_factory=list,
        description="Days of the week for training (e.g., ['Monday', 'Wednesday', 'Friday'])"
    )

    high_days: List[str] = Field(
        default_factory=list,
        description="High calorie days (1 for SHREDDED, 2 for MASSIVE)"
    )

    language: Language = Field(
        default=Language.ENGLISH,
        description="Preferred output language"
    )

    @field_validator('training_days', 'high_days')
    @classmethod
    def validate_days(cls, v):
        """Validate day names"""
        valid_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        for day in v:
            if day not in valid_days:
                raise ValueError(f"Invalid day: {day}. Must be one of {valid_days}")
        return v

    @field_validator('high_days')
    @classmethod
    def validate_high_days_count(cls, v, info):
        """Validate high days count based on protocol"""
        if 'protocol' in info.data:
            protocol = info.data['protocol']
            if protocol == Protocol.SHREDDED and len(v) > 1:
                raise ValueError("SHREDDED protocol allows only 1 HIGH day per week")
            elif protocol == Protocol.MASSIVE and len(v) > 2:
                raise ValueError("MASSIVE protocol allows only 2 HIGH days per week")
        return v

    def get_weight_in_lbs(self) -> float:
        """Convert weight to lbs if needed"""
        if self.weight_unit == WeightUnit.KG:
            return self.weight * 2.20462
        return self.weight

    def get_weight_in_kg(self) -> float:
        """Convert weight to kg if needed"""
        if self.weight_unit == WeightUnit.LBS:
            return self.weight / 2.20462
        return self.weight

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Ahmed Hassan",
                "weight": 180,
                "weight_unit": "lbs",
                "body_fat_percentage": 15.0,
                "height": 72,
                "protocol": "SHREDDED",
                "training_days": ["Monday", "Wednesday", "Friday"],
                "high_days": ["Saturday"],
                "language": "en"
            }
        }
