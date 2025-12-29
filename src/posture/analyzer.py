"""
Posture Analyzer
Analyzes captured poses and detects posture issues
"""

from typing import List, Dict, Optional, Tuple
from datetime import datetime
import uuid

from .models import (
    PostureIssue,
    PostureSeverity,
    BodyRegion,
    PoseType,
    PostureAssessment,
    PostureReport,
    PoseCapture,
    PostureFix
)
from .issue_database import PostureIssueDatabase


class PostureAnalyzer:
    """
    Analyzes posture based on user input about observed issues.
    In a production environment, this would use computer vision/ML models.
    This implementation uses a questionnaire-based approach for manual assessment.
    """

    def __init__(self):
        self.issue_db = PostureIssueDatabase()
        self._assessment_questions = self._build_assessment_questions()

    def _build_assessment_questions(self) -> Dict[PoseType, List[Dict]]:
        """Build assessment questions for each pose type"""
        return {
            PoseType.FRONT_VIEW: [
                {
                    "id": "shoulder_level",
                    "question": "Are the shoulders level (same height)?",
                    "options": ["Yes, level", "No, left is higher", "No, right is higher"],
                    "issue_mapping": {
                        "No, left is higher": "uneven_shoulders",
                        "No, right is higher": "uneven_shoulders"
                    }
                },
                {
                    "id": "head_tilt",
                    "question": "Is the head centered or tilted to one side?",
                    "options": ["Centered", "Tilted left", "Tilted right"],
                    "issue_mapping": {
                        "Tilted left": "head_tilt",
                        "Tilted right": "head_tilt"
                    }
                },
                {
                    "id": "hip_level",
                    "question": "Are the hips level (same height)?",
                    "options": ["Yes, level", "No, shifted to one side"],
                    "issue_mapping": {
                        "No, shifted to one side": "hip_shift"
                    }
                },
                {
                    "id": "knee_alignment",
                    "question": "How do the knees align when standing?",
                    "options": ["Straight/neutral", "Pointing inward (knock knees)", "Pointing outward (bow legs)"],
                    "issue_mapping": {
                        "Pointing inward (knock knees)": "knee_valgus",
                        "Pointing outward (bow legs)": "knee_varus"
                    }
                },
                {
                    "id": "foot_arches",
                    "question": "How do the foot arches look?",
                    "options": ["Normal arches", "Flat/collapsed arches", "Very high arches"],
                    "issue_mapping": {
                        "Flat/collapsed arches": "overpronation",
                        "Very high arches": "supination"
                    }
                },
                {
                    "id": "hand_position",
                    "question": "When arms hang naturally, which way do the palms face?",
                    "options": ["Toward the body (thumbs forward)", "Backward (thumbs toward body)", "Inward (thumbs back)"],
                    "issue_mapping": {
                        "Backward (thumbs toward body)": "shoulder_internal_rotation",
                        "Inward (thumbs back)": "shoulder_internal_rotation"
                    }
                }
            ],

            PoseType.SIDE_VIEW_LEFT: [
                {
                    "id": "head_position",
                    "question": "Where is the ear relative to the shoulder?",
                    "options": ["Directly above shoulder", "Forward of shoulder", "Behind shoulder"],
                    "issue_mapping": {
                        "Forward of shoulder": "forward_head"
                    }
                },
                {
                    "id": "shoulder_position",
                    "question": "How do the shoulders appear from the side?",
                    "options": ["Neutral/back", "Rounded forward"],
                    "issue_mapping": {
                        "Rounded forward": "rounded_shoulders"
                    }
                },
                {
                    "id": "upper_back_curve",
                    "question": "How does the upper back curve look?",
                    "options": ["Normal curve", "Excessive rounding (hunchback)", "Too flat"],
                    "issue_mapping": {
                        "Excessive rounding (hunchback)": "kyphosis",
                        "Too flat": "flat_upper_back"
                    }
                },
                {
                    "id": "lower_back_curve",
                    "question": "How does the lower back curve look?",
                    "options": ["Normal curve", "Excessive arch", "Too flat/tucked under"],
                    "issue_mapping": {
                        "Excessive arch": "hyperlordosis",
                        "Too flat/tucked under": "posterior_pelvic_tilt"
                    }
                },
                {
                    "id": "pelvis_position",
                    "question": "How does the pelvis position look?",
                    "options": ["Neutral", "Tilted forward (belly sticking out)", "Tilted backward (tailbone tucked)"],
                    "issue_mapping": {
                        "Tilted forward (belly sticking out)": "anterior_pelvic_tilt",
                        "Tilted backward (tailbone tucked)": "posterior_pelvic_tilt"
                    }
                },
                {
                    "id": "knee_position",
                    "question": "How do the knees look from the side?",
                    "options": ["Slightly bent or straight", "Pushed backward (hyperextended)"],
                    "issue_mapping": {
                        "Pushed backward (hyperextended)": "hyperextended_knees"
                    }
                }
            ],

            PoseType.SIDE_VIEW_RIGHT: [
                {
                    "id": "head_position",
                    "question": "Where is the ear relative to the shoulder?",
                    "options": ["Directly above shoulder", "Forward of shoulder", "Behind shoulder"],
                    "issue_mapping": {
                        "Forward of shoulder": "forward_head"
                    }
                },
                {
                    "id": "shoulder_position",
                    "question": "How do the shoulders appear from the side?",
                    "options": ["Neutral/back", "Rounded forward"],
                    "issue_mapping": {
                        "Rounded forward": "rounded_shoulders"
                    }
                },
                {
                    "id": "upper_back_curve",
                    "question": "How does the upper back curve look?",
                    "options": ["Normal curve", "Excessive rounding (hunchback)", "Too flat"],
                    "issue_mapping": {
                        "Excessive rounding (hunchback)": "kyphosis",
                        "Too flat": "flat_upper_back"
                    }
                },
                {
                    "id": "lower_back_curve",
                    "question": "How does the lower back curve look?",
                    "options": ["Normal curve", "Excessive arch", "Too flat/tucked under"],
                    "issue_mapping": {
                        "Excessive arch": "hyperlordosis",
                        "Too flat/tucked under": "posterior_pelvic_tilt"
                    }
                },
                {
                    "id": "pelvis_position",
                    "question": "How does the pelvis position look?",
                    "options": ["Neutral", "Tilted forward (belly sticking out)", "Tilted backward (tailbone tucked)"],
                    "issue_mapping": {
                        "Tilted forward (belly sticking out)": "anterior_pelvic_tilt",
                        "Tilted backward (tailbone tucked)": "posterior_pelvic_tilt"
                    }
                },
                {
                    "id": "knee_position",
                    "question": "How do the knees look from the side?",
                    "options": ["Slightly bent or straight", "Pushed backward (hyperextended)"],
                    "issue_mapping": {
                        "Pushed backward (hyperextended)": "hyperextended_knees"
                    }
                }
            ],

            PoseType.BACK_VIEW: [
                {
                    "id": "shoulder_blades",
                    "question": "How do the shoulder blades look?",
                    "options": ["Flat against back", "One sticks out more", "Both stick out (winging)"],
                    "issue_mapping": {
                        "One sticks out more": "scoliosis_pattern",
                        "Both stick out (winging)": "rounded_shoulders"
                    }
                },
                {
                    "id": "spine_alignment",
                    "question": "Does the spine appear straight or curved?",
                    "options": ["Straight", "Curves to the left", "Curves to the right", "S-shaped curve"],
                    "issue_mapping": {
                        "Curves to the left": "scoliosis_pattern",
                        "Curves to the right": "scoliosis_pattern",
                        "S-shaped curve": "scoliosis_pattern"
                    }
                },
                {
                    "id": "waist_crease",
                    "question": "Is the waist crease even on both sides?",
                    "options": ["Yes, even", "No, uneven"],
                    "issue_mapping": {
                        "No, uneven": "hip_shift"
                    }
                },
                {
                    "id": "heel_alignment",
                    "question": "Do the heels appear to roll inward or outward?",
                    "options": ["Straight", "Rolling inward", "Rolling outward"],
                    "issue_mapping": {
                        "Rolling inward": "overpronation",
                        "Rolling outward": "supination"
                    }
                }
            ],

            PoseType.OVERHEAD_SQUAT: [
                {
                    "id": "arms_position",
                    "question": "During the squat, do the arms stay overhead?",
                    "options": ["Yes, arms stay up", "Arms fall forward"],
                    "issue_mapping": {
                        "Arms fall forward": "arms_fall_forward"
                    }
                },
                {
                    "id": "torso_lean",
                    "question": "How much does the torso lean forward?",
                    "options": ["Minimal lean (upright)", "Moderate lean", "Excessive forward lean"],
                    "issue_mapping": {
                        "Excessive forward lean": "excessive_forward_lean"
                    }
                },
                {
                    "id": "knee_tracking",
                    "question": "How do the knees track during the squat?",
                    "options": ["Over toes", "Cave inward (valgus)", "Push outward excessively"],
                    "issue_mapping": {
                        "Cave inward (valgus)": "knee_valgus"
                    }
                },
                {
                    "id": "heel_position",
                    "question": "Do the heels stay on the ground?",
                    "options": ["Yes, heels stay down", "Heels lift up"],
                    "issue_mapping": {
                        "Heels lift up": "ankle_dorsiflexion_deficit"
                    }
                },
                {
                    "id": "squat_symmetry",
                    "question": "Is the squat symmetrical or do you shift to one side?",
                    "options": ["Symmetrical", "Shift to one side"],
                    "issue_mapping": {
                        "Shift to one side": "squat_asymmetry"
                    }
                },
                {
                    "id": "lower_back",
                    "question": "What happens to the lower back at the bottom of the squat?",
                    "options": ["Maintains neutral", "Rounds (butt wink)", "Over-arches"],
                    "issue_mapping": {
                        "Rounds (butt wink)": "posterior_pelvic_tilt",
                        "Over-arches": "anterior_pelvic_tilt"
                    }
                },
                {
                    "id": "feet_position",
                    "question": "What happens to the feet during the squat?",
                    "options": ["Stay flat", "Roll inward (pronate)", "Roll outward"],
                    "issue_mapping": {
                        "Roll inward (pronate)": "overpronation"
                    }
                },
                {
                    "id": "core_stability",
                    "question": "Does the ribcage flare forward during the squat?",
                    "options": ["No, ribcage stays down", "Yes, ribcage flares up/forward"],
                    "issue_mapping": {
                        "Yes, ribcage flares up/forward": "weak_core"
                    }
                }
            ],

            PoseType.SINGLE_LEG_SQUAT_LEFT: [
                {
                    "id": "hip_drop",
                    "question": "Does the opposite hip drop during the squat?",
                    "options": ["No, hips stay level", "Yes, hip drops"],
                    "issue_mapping": {
                        "Yes, hip drops": "hip_rotation"
                    }
                },
                {
                    "id": "knee_cave",
                    "question": "Does the knee cave inward?",
                    "options": ["No, tracks over toes", "Yes, caves inward"],
                    "issue_mapping": {
                        "Yes, caves inward": "knee_valgus"
                    }
                },
                {
                    "id": "balance",
                    "question": "Is there excessive wobbling or instability?",
                    "options": ["Stable", "Significant wobbling/instability"],
                    "issue_mapping": {
                        "Significant wobbling/instability": "weak_core"
                    }
                },
                {
                    "id": "foot_arch",
                    "question": "Does the arch of the foot collapse?",
                    "options": ["No, arch maintained", "Yes, arch collapses"],
                    "issue_mapping": {
                        "Yes, arch collapses": "overpronation"
                    }
                }
            ],

            PoseType.SINGLE_LEG_SQUAT_RIGHT: [
                {
                    "id": "hip_drop",
                    "question": "Does the opposite hip drop during the squat?",
                    "options": ["No, hips stay level", "Yes, hip drops"],
                    "issue_mapping": {
                        "Yes, hip drops": "hip_rotation"
                    }
                },
                {
                    "id": "knee_cave",
                    "question": "Does the knee cave inward?",
                    "options": ["No, tracks over toes", "Yes, caves inward"],
                    "issue_mapping": {
                        "Yes, caves inward": "knee_valgus"
                    }
                },
                {
                    "id": "balance",
                    "question": "Is there excessive wobbling or instability?",
                    "options": ["Stable", "Significant wobbling/instability"],
                    "issue_mapping": {
                        "Significant wobbling/instability": "weak_core"
                    }
                },
                {
                    "id": "foot_arch",
                    "question": "Does the arch of the foot collapse?",
                    "options": ["No, arch maintained", "Yes, arch collapses"],
                    "issue_mapping": {
                        "Yes, arch collapses": "overpronation"
                    }
                }
            ],

            PoseType.FORWARD_BEND: [
                {
                    "id": "spine_curve",
                    "question": "During forward bend, is there a visible hump on one side of the spine?",
                    "options": ["No, spine is even", "Yes, visible asymmetry"],
                    "issue_mapping": {
                        "Yes, visible asymmetry": "scoliosis_pattern"
                    }
                },
                {
                    "id": "hamstring_flexibility",
                    "question": "Can you touch your toes while keeping legs straight?",
                    "options": ["Yes, easily", "No, hamstrings very tight"],
                    "issue_mapping": {}
                }
            ],

            PoseType.INLINE_LUNGE_LEFT: [
                {
                    "id": "balance",
                    "question": "Can you maintain balance in the inline lunge?",
                    "options": ["Yes, stable", "No, significant wobbling"],
                    "issue_mapping": {
                        "No, significant wobbling": "weak_core"
                    }
                },
                {
                    "id": "knee_tracking",
                    "question": "Does the front knee cave inward?",
                    "options": ["No, tracks straight", "Yes, caves inward"],
                    "issue_mapping": {
                        "Yes, caves inward": "knee_valgus"
                    }
                },
                {
                    "id": "ankle_mobility",
                    "question": "Does the front heel lift off the ground?",
                    "options": ["No, heel stays down", "Yes, heel lifts"],
                    "issue_mapping": {
                        "Yes, heel lifts": "ankle_dorsiflexion_deficit"
                    }
                }
            ],

            PoseType.INLINE_LUNGE_RIGHT: [
                {
                    "id": "balance",
                    "question": "Can you maintain balance in the inline lunge?",
                    "options": ["Yes, stable", "No, significant wobbling"],
                    "issue_mapping": {
                        "No, significant wobbling": "weak_core"
                    }
                },
                {
                    "id": "knee_tracking",
                    "question": "Does the front knee cave inward?",
                    "options": ["No, tracks straight", "Yes, caves inward"],
                    "issue_mapping": {
                        "Yes, caves inward": "knee_valgus"
                    }
                },
                {
                    "id": "ankle_mobility",
                    "question": "Does the front heel lift off the ground?",
                    "options": ["No, heel stays down", "Yes, heel lifts"],
                    "issue_mapping": {
                        "Yes, heel lifts": "ankle_dorsiflexion_deficit"
                    }
                }
            ]
        }

    def get_questions_for_pose(self, pose_type: PoseType) -> List[Dict]:
        """Get assessment questions for a specific pose"""
        return self._assessment_questions.get(pose_type, [])

    def analyze_pose(
        self,
        pose_type: PoseType,
        answers: Dict[str, str],
        pose_capture: Optional[PoseCapture] = None
    ) -> PostureAssessment:
        """
        Analyze a pose based on questionnaire answers.

        Args:
            pose_type: The type of pose being assessed
            answers: Dictionary mapping question_id to selected answer
            pose_capture: Optional captured image data

        Returns:
            PostureAssessment with detected issues
        """
        detected_issues = []
        observations = []

        questions = self.get_questions_for_pose(pose_type)

        for question in questions:
            question_id = question["id"]
            if question_id in answers:
                answer = answers[question_id]
                issue_mapping = question.get("issue_mapping", {})

                if answer in issue_mapping:
                    issue_id = issue_mapping[answer]
                    issue = self.issue_db.get_issue_by_id(issue_id)
                    if issue and issue not in detected_issues:
                        detected_issues.append(issue)
                        observations.append(f"{question['question']} - {answer}")

        # Calculate score based on issues
        score = self._calculate_pose_score(detected_issues)

        # Generate recommendations
        recommendations = self._generate_recommendations(detected_issues)

        return PostureAssessment(
            pose_type=pose_type,
            pose_capture=pose_capture,
            issues_detected=detected_issues,
            overall_score=score,
            observations=observations,
            recommendations=recommendations
        )

    def _calculate_pose_score(self, issues: List[PostureIssue]) -> float:
        """Calculate a score based on detected issues"""
        if not issues:
            return 100.0

        base_score = 100.0
        severity_penalties = {
            PostureSeverity.MINOR: 5,
            PostureSeverity.MODERATE: 10,
            PostureSeverity.SEVERE: 20,
            PostureSeverity.CRITICAL: 30
        }

        total_penalty = sum(severity_penalties[issue.severity] for issue in issues)
        final_score = max(0, base_score - total_penalty)

        return round(final_score, 1)

    def _generate_recommendations(self, issues: List[PostureIssue]) -> List[str]:
        """Generate recommendations based on detected issues"""
        if not issues:
            return ["Great posture! Keep up the good work."]

        recommendations = []

        # Add general recommendation
        if len(issues) >= 3:
            recommendations.append(
                "Multiple posture issues detected. Consider working with a physical therapist for a comprehensive program."
            )

        # Add specific recommendations for severe/critical issues
        for issue in issues:
            if issue.severity in [PostureSeverity.SEVERE, PostureSeverity.CRITICAL]:
                recommendations.append(
                    f"Priority: Address {issue.name} - this is affecting multiple areas of your posture."
                )

        # Add fix-based recommendations
        all_fixes = []
        for issue in issues:
            all_fixes.extend(issue.recommended_fixes)

        # Get unique fixes sorted by category
        seen_fixes = set()
        for fix in all_fixes:
            if fix.name not in seen_fixes:
                seen_fixes.add(fix.name)
                recommendations.append(f"Exercise: {fix.name} ({fix.frequency})")

        return recommendations[:8]  # Limit to 8 recommendations

    def create_full_report(
        self,
        client_name: str,
        assessments: List[PostureAssessment],
        client_email: Optional[str] = None
    ) -> PostureReport:
        """
        Create a comprehensive posture report from multiple assessments.

        Args:
            client_name: Name of the client
            assessments: List of pose assessments
            client_email: Optional client email

        Returns:
            Complete PostureReport
        """
        # Collect all unique issues
        all_issues = []
        seen_issue_ids = set()

        for assessment in assessments:
            for issue in assessment.issues_detected:
                if issue.id not in seen_issue_ids:
                    all_issues.append(issue)
                    seen_issue_ids.add(issue.id)

        # Sort issues by priority and severity
        all_issues.sort(
            key=lambda x: (
                x.priority,
                {'critical': 0, 'severe': 1, 'moderate': 2, 'minor': 3}[x.severity.value]
            )
        )

        # Create report
        report = PostureReport(
            report_id=str(uuid.uuid4())[:8].upper(),
            client_name=client_name,
            client_email=client_email,
            assessments=assessments,
            all_issues=all_issues
        )

        # Calculate overall score
        report.overall_score = report.calculate_overall_score()

        # Get prioritized fixes
        report.prioritized_fixes = report.get_priority_fixes(max_fixes=10)

        # Generate summary
        report.summary = report.generate_summary()

        # Generate overall recommendations
        report.recommendations = self._generate_overall_recommendations(report)

        return report

    def _generate_overall_recommendations(self, report: PostureReport) -> List[str]:
        """Generate overall recommendations for the report"""
        recommendations = []

        if report.overall_score >= 90:
            recommendations.append(
                "Excellent posture! Maintain your current habits and continue with preventive exercises."
            )
        elif report.overall_score >= 70:
            recommendations.append(
                "Good posture with some areas for improvement. Focus on the corrective exercises below."
            )
        elif report.overall_score >= 50:
            recommendations.append(
                "Several posture issues detected. A consistent corrective exercise routine is recommended."
            )
        else:
            recommendations.append(
                "Significant posture issues detected. Consider consulting a physical therapist for a personalized program."
            )

        # Add category-based recommendations
        fix_categories = {}
        for fix in report.prioritized_fixes:
            cat = fix.category
            if cat not in fix_categories:
                fix_categories[cat] = 0
            fix_categories[cat] += 1

        if fix_categories.get('strengthen', 0) > 2:
            recommendations.append(
                "Focus on strengthening exercises to build postural muscle endurance."
            )
        if fix_categories.get('stretch', 0) > 2:
            recommendations.append(
                "Include regular stretching to address muscle tightness."
            )
        if fix_categories.get('mobilize', 0) > 1:
            recommendations.append(
                "Work on joint mobility to improve movement quality."
            )

        # Add lifestyle recommendations
        issues_by_region = report.get_issues_by_region()
        if BodyRegion.HEAD in issues_by_region or BodyRegion.NECK in issues_by_region:
            recommendations.append(
                "Lifestyle: Take regular breaks from screens and check your workstation ergonomics."
            )
        if BodyRegion.LOWER_BACK in issues_by_region or BodyRegion.PELVIS in issues_by_region:
            recommendations.append(
                "Lifestyle: Avoid prolonged sitting; stand and move every 30-60 minutes."
            )

        return recommendations

    def get_pose_instructions(self, pose_type: PoseType) -> Dict:
        """Get instructions for how to perform and capture a pose"""
        instructions = {
            PoseType.FRONT_VIEW: {
                "title": "Front View Assessment",
                "setup": [
                    "Stand facing the camera",
                    "Position phone at hip height, about 6-8 feet away",
                    "Make sure your entire body is visible from head to feet",
                    "Stand naturally with arms at your sides",
                    "Look straight ahead at the camera"
                ],
                "what_to_look_for": [
                    "Shoulder height symmetry",
                    "Head position (centered or tilted)",
                    "Hip alignment",
                    "Knee alignment",
                    "Foot arches"
                ],
                "duration": "Hold still for 5 seconds"
            },
            PoseType.SIDE_VIEW_LEFT: {
                "title": "Left Side View Assessment",
                "setup": [
                    "Stand with your left side facing the camera",
                    "Position phone at hip height, about 6-8 feet away",
                    "Make sure your entire body is visible from head to feet",
                    "Stand naturally with arms at your sides",
                    "Look straight ahead (not at the camera)"
                ],
                "what_to_look_for": [
                    "Head position relative to shoulders",
                    "Shoulder rounding",
                    "Upper back curve (kyphosis)",
                    "Lower back curve (lordosis)",
                    "Knee position"
                ],
                "duration": "Hold still for 5 seconds"
            },
            PoseType.SIDE_VIEW_RIGHT: {
                "title": "Right Side View Assessment",
                "setup": [
                    "Stand with your right side facing the camera",
                    "Position phone at hip height, about 6-8 feet away",
                    "Make sure your entire body is visible from head to feet",
                    "Stand naturally with arms at your sides",
                    "Look straight ahead (not at the camera)"
                ],
                "what_to_look_for": [
                    "Head position relative to shoulders",
                    "Shoulder rounding",
                    "Upper back curve (kyphosis)",
                    "Lower back curve (lordosis)",
                    "Knee position"
                ],
                "duration": "Hold still for 5 seconds"
            },
            PoseType.BACK_VIEW: {
                "title": "Back View Assessment",
                "setup": [
                    "Stand with your back facing the camera",
                    "Position phone at hip height, about 6-8 feet away",
                    "Make sure your entire body is visible from head to feet",
                    "Stand naturally with arms at your sides",
                    "Look straight ahead"
                ],
                "what_to_look_for": [
                    "Shoulder blade position",
                    "Spine alignment",
                    "Waist crease symmetry",
                    "Hip alignment",
                    "Heel position"
                ],
                "duration": "Hold still for 5 seconds"
            },
            PoseType.OVERHEAD_SQUAT: {
                "title": "Overhead Squat Assessment",
                "setup": [
                    "Stand facing the camera",
                    "Raise both arms straight overhead",
                    "Keep arms shoulder-width apart",
                    "Slowly squat down as low as you can",
                    "Hold the bottom position"
                ],
                "what_to_look_for": [
                    "Arms staying overhead",
                    "Forward lean of torso",
                    "Knee tracking",
                    "Heels staying on ground",
                    "Squat symmetry",
                    "Lower back position"
                ],
                "duration": "Perform 3 squats, hold bottom for 3 seconds each"
            },
            PoseType.SINGLE_LEG_SQUAT_LEFT: {
                "title": "Single Leg Squat - Left Leg",
                "setup": [
                    "Stand on your LEFT leg facing the camera",
                    "Extend right leg in front of you",
                    "Hold arms out for balance",
                    "Slowly squat down on your left leg",
                    "Go as low as you can with control"
                ],
                "what_to_look_for": [
                    "Hip dropping on one side",
                    "Knee caving inward",
                    "Balance and stability",
                    "Foot arch collapse"
                ],
                "duration": "Perform 3 squats per leg"
            },
            PoseType.SINGLE_LEG_SQUAT_RIGHT: {
                "title": "Single Leg Squat - Right Leg",
                "setup": [
                    "Stand on your RIGHT leg facing the camera",
                    "Extend left leg in front of you",
                    "Hold arms out for balance",
                    "Slowly squat down on your right leg",
                    "Go as low as you can with control"
                ],
                "what_to_look_for": [
                    "Hip dropping on one side",
                    "Knee caving inward",
                    "Balance and stability",
                    "Foot arch collapse"
                ],
                "duration": "Perform 3 squats per leg"
            },
            PoseType.FORWARD_BEND: {
                "title": "Forward Bend (Adam's Test)",
                "setup": [
                    "Stand facing away from camera (back view)",
                    "Keep feet together",
                    "Slowly bend forward at the waist",
                    "Let arms hang toward the floor",
                    "Keep legs straight"
                ],
                "what_to_look_for": [
                    "Spine symmetry (any humps or rotation)",
                    "Hamstring flexibility"
                ],
                "duration": "Hold bend for 5 seconds"
            },
            PoseType.INLINE_LUNGE_LEFT: {
                "title": "Inline Lunge - Left Leg Forward",
                "setup": [
                    "Stand on a line (real or imaginary)",
                    "Step left foot forward on the line",
                    "Right foot behind, also on the line",
                    "Lower into a lunge position",
                    "Keep torso upright"
                ],
                "what_to_look_for": [
                    "Balance",
                    "Knee tracking",
                    "Ankle mobility"
                ],
                "duration": "Hold for 5 seconds"
            },
            PoseType.INLINE_LUNGE_RIGHT: {
                "title": "Inline Lunge - Right Leg Forward",
                "setup": [
                    "Stand on a line (real or imaginary)",
                    "Step right foot forward on the line",
                    "Left foot behind, also on the line",
                    "Lower into a lunge position",
                    "Keep torso upright"
                ],
                "what_to_look_for": [
                    "Balance",
                    "Knee tracking",
                    "Ankle mobility"
                ],
                "duration": "Hold for 5 seconds"
            }
        }

        return instructions.get(pose_type, {
            "title": pose_type.value.replace("_", " ").title(),
            "setup": ["Follow general posture guidelines"],
            "what_to_look_for": ["General alignment"],
            "duration": "Hold for 5 seconds"
        })
