"""
Posture Analysis Data Models
Defines structures for posture assessment, issues, and fixes
"""

from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime


class PostureSeverity(str, Enum):
    """Severity levels for posture issues"""
    MINOR = "minor"
    MODERATE = "moderate"
    SEVERE = "severe"
    CRITICAL = "critical"


class BodyRegion(str, Enum):
    """Body regions for posture analysis"""
    HEAD = "head"
    NECK = "neck"
    SHOULDERS = "shoulders"
    UPPER_BACK = "upper_back"
    LOWER_BACK = "lower_back"
    SPINE = "spine"
    HIPS = "hips"
    PELVIS = "pelvis"
    KNEES = "knees"
    ANKLES = "ankles"
    FEET = "feet"
    CORE = "core"
    FULL_BODY = "full_body"


class PoseType(str, Enum):
    """Types of poses for assessment"""
    FRONT_VIEW = "front_view"
    SIDE_VIEW_LEFT = "side_view_left"
    SIDE_VIEW_RIGHT = "side_view_right"
    BACK_VIEW = "back_view"
    OVERHEAD_SQUAT = "overhead_squat"
    SINGLE_LEG_SQUAT_LEFT = "single_leg_squat_left"
    SINGLE_LEG_SQUAT_RIGHT = "single_leg_squat_right"
    FORWARD_BEND = "forward_bend"
    INLINE_LUNGE_LEFT = "inline_lunge_left"
    INLINE_LUNGE_RIGHT = "inline_lunge_right"


class PostureFix(BaseModel):
    """A corrective exercise or stretch for a posture issue"""
    name: str
    description: str
    instructions: List[str]
    duration: str = Field(description="Recommended duration, e.g., '30 seconds', '10 reps'")
    frequency: str = Field(description="How often to perform, e.g., '3x daily', '2x per week'")
    video_url: Optional[str] = None
    image_url: Optional[str] = None
    difficulty: str = Field(default="beginner", description="beginner, intermediate, advanced")
    equipment_needed: List[str] = Field(default_factory=list)
    muscles_targeted: List[str] = Field(default_factory=list)
    category: str = Field(default="stretch", description="stretch, strengthen, mobilize, release")


class PostureIssue(BaseModel):
    """A detected posture issue"""
    id: str
    name: str
    name_ar: Optional[str] = None  # Arabic name
    description: str
    description_ar: Optional[str] = None
    body_region: BodyRegion
    severity: PostureSeverity
    detected_in_poses: List[PoseType]
    visual_indicators: List[str] = Field(description="What to look for visually")
    potential_causes: List[str]
    potential_consequences: List[str]
    recommended_fixes: List[PostureFix]
    priority: int = Field(default=1, ge=1, le=10, description="1=highest priority")
    notes: Optional[str] = None


class PoseCapture(BaseModel):
    """A captured pose image with metadata"""
    pose_type: PoseType
    image_data: Optional[str] = Field(default=None, description="Base64 encoded image")
    captured_at: datetime = Field(default_factory=datetime.now)
    notes: Optional[str] = None
    landmarks_detected: bool = False
    quality_score: float = Field(default=0.0, ge=0.0, le=1.0)


class PostureAssessment(BaseModel):
    """Assessment results for a single pose"""
    pose_type: PoseType
    pose_capture: Optional[PoseCapture] = None
    issues_detected: List[PostureIssue] = Field(default_factory=list)
    overall_score: float = Field(default=100.0, ge=0.0, le=100.0)
    observations: List[str] = Field(default_factory=list)
    recommendations: List[str] = Field(default_factory=list)
    assessed_at: datetime = Field(default_factory=datetime.now)


class PostureReport(BaseModel):
    """Complete posture assessment report"""
    report_id: str
    client_name: str
    client_email: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)
    assessments: List[PostureAssessment] = Field(default_factory=list)
    all_issues: List[PostureIssue] = Field(default_factory=list)
    prioritized_fixes: List[PostureFix] = Field(default_factory=list)
    overall_score: float = Field(default=100.0, ge=0.0, le=100.0)
    summary: str = ""
    recommendations: List[str] = Field(default_factory=list)

    def calculate_overall_score(self) -> float:
        """Calculate overall posture score based on all assessments"""
        if not self.assessments:
            return 100.0

        total_score = sum(a.overall_score for a in self.assessments)
        avg_score = total_score / len(self.assessments)

        # Penalize for critical issues
        critical_count = sum(
            1 for issue in self.all_issues
            if issue.severity == PostureSeverity.CRITICAL
        )
        severe_count = sum(
            1 for issue in self.all_issues
            if issue.severity == PostureSeverity.SEVERE
        )

        penalty = (critical_count * 10) + (severe_count * 5)
        final_score = max(0, avg_score - penalty)

        return round(final_score, 1)

    def get_issues_by_severity(self) -> Dict[PostureSeverity, List[PostureIssue]]:
        """Group issues by severity"""
        result = {s: [] for s in PostureSeverity}
        for issue in self.all_issues:
            result[issue.severity].append(issue)
        return result

    def get_issues_by_region(self) -> Dict[BodyRegion, List[PostureIssue]]:
        """Group issues by body region"""
        result: Dict[BodyRegion, List[PostureIssue]] = {}
        for issue in self.all_issues:
            if issue.body_region not in result:
                result[issue.body_region] = []
            result[issue.body_region].append(issue)
        return result

    def get_priority_fixes(self, max_fixes: int = 5) -> List[PostureFix]:
        """Get top priority fixes based on issue severity"""
        # Sort issues by priority and severity
        sorted_issues = sorted(
            self.all_issues,
            key=lambda x: (
                x.priority,
                {'critical': 0, 'severe': 1, 'moderate': 2, 'minor': 3}[x.severity.value]
            )
        )

        # Collect unique fixes
        seen_fixes = set()
        priority_fixes = []

        for issue in sorted_issues:
            for fix in issue.recommended_fixes:
                if fix.name not in seen_fixes and len(priority_fixes) < max_fixes:
                    seen_fixes.add(fix.name)
                    priority_fixes.append(fix)

        return priority_fixes

    def generate_summary(self) -> str:
        """Generate a text summary of the assessment"""
        if not self.all_issues:
            return "Great posture! No significant issues detected."

        severity_counts = {s: 0 for s in PostureSeverity}
        for issue in self.all_issues:
            severity_counts[issue.severity] += 1

        summary_parts = [
            f"Posture Assessment Summary (Score: {self.overall_score}/100)",
            "",
            f"Total Issues Found: {len(self.all_issues)}",
        ]

        if severity_counts[PostureSeverity.CRITICAL] > 0:
            summary_parts.append(f"- Critical: {severity_counts[PostureSeverity.CRITICAL]}")
        if severity_counts[PostureSeverity.SEVERE] > 0:
            summary_parts.append(f"- Severe: {severity_counts[PostureSeverity.SEVERE]}")
        if severity_counts[PostureSeverity.MODERATE] > 0:
            summary_parts.append(f"- Moderate: {severity_counts[PostureSeverity.MODERATE]}")
        if severity_counts[PostureSeverity.MINOR] > 0:
            summary_parts.append(f"- Minor: {severity_counts[PostureSeverity.MINOR]}")

        # Top regions affected
        regions = self.get_issues_by_region()
        if regions:
            summary_parts.append("")
            summary_parts.append("Areas Needing Attention:")
            for region, issues in sorted(regions.items(), key=lambda x: -len(x[1])):
                summary_parts.append(f"- {region.value.replace('_', ' ').title()}: {len(issues)} issue(s)")

        return "\n".join(summary_parts)
