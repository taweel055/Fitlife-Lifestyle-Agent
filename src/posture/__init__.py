"""
Posture Analysis Module
Comprehensive posture assessment system with camera-based analysis
"""

from .models import (
    PostureIssue,
    PostureSeverity,
    BodyRegion,
    PoseType,
    PostureAssessment,
    PostureFix,
    PostureReport
)

from .analyzer import PostureAnalyzer
from .issue_database import PostureIssueDatabase

__all__ = [
    'PostureIssue',
    'PostureSeverity',
    'BodyRegion',
    'PoseType',
    'PostureAssessment',
    'PostureFix',
    'PostureReport',
    'PostureAnalyzer',
    'PostureIssueDatabase'
]
