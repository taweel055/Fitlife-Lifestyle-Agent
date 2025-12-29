#!/usr/bin/env python3
"""
Fitlife Posture Analysis App
Mobile-friendly web app for comprehensive posture assessment
"""

import sys
import os
import json
import base64
from datetime import datetime
from typing import Dict, List, Optional
import streamlit as st

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.posture import (
    PostureAnalyzer,
    PostureIssueDatabase,
    PoseType,
    PostureAssessment,
    PostureReport,
    PostureSeverity,
    BodyRegion
)

# Page configuration - must be first Streamlit command
st.set_page_config(
    page_title="Posture Analysis",
    page_icon="🧍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for mobile-friendly design
st.markdown("""
<style>
    /* Mobile-first responsive design */
    .main-header {
        font-size: 2rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
        padding: 0.5rem;
    }

    .sub-header {
        font-size: 1.3rem;
        font-weight: 600;
        color: #333;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
        border-bottom: 2px solid #667eea;
        padding-bottom: 0.3rem;
    }

    .instruction-box {
        background: linear-gradient(135deg, #e0e5ec 0%, #f5f7fa 100%);
        padding: 1rem;
        border-radius: 0.75rem;
        border-left: 4px solid #667eea;
        margin: 0.5rem 0;
    }

    .success-box {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        padding: 1rem;
        border-radius: 0.75rem;
        border-left: 4px solid #28a745;
        margin: 0.5rem 0;
    }

    .warning-box {
        background: linear-gradient(135deg, #fff3cd 0%, #ffeeba 100%);
        padding: 1rem;
        border-radius: 0.75rem;
        border-left: 4px solid #ffc107;
        margin: 0.5rem 0;
    }

    .danger-box {
        background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
        padding: 1rem;
        border-radius: 0.75rem;
        border-left: 4px solid #dc3545;
        margin: 0.5rem 0;
    }

    .issue-card {
        background: #ffffff;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #6c757d;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }

    .issue-card.minor { border-left-color: #17a2b8; }
    .issue-card.moderate { border-left-color: #ffc107; }
    .issue-card.severe { border-left-color: #fd7e14; }
    .issue-card.critical { border-left-color: #dc3545; }

    .fix-card {
        background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        border: 1px solid #a5d6a7;
    }

    .pose-step {
        background: linear-gradient(135deg, #fff 0%, #f8f9fa 100%);
        padding: 1rem;
        border-radius: 0.75rem;
        border: 2px solid #e9ecef;
        margin: 0.5rem 0;
        text-align: center;
    }

    .pose-step.active {
        border-color: #667eea;
        background: linear-gradient(135deg, #f0f3ff 0%, #e8ecff 100%);
    }

    .pose-step.completed {
        border-color: #28a745;
        background: linear-gradient(135deg, #f0fff4 0%, #e8f5e9 100%);
    }

    .score-display {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        padding: 1rem;
    }

    .score-display.excellent { color: #28a745; }
    .score-display.good { color: #17a2b8; }
    .score-display.fair { color: #ffc107; }
    .score-display.poor { color: #dc3545; }

    /* Camera container styles */
    .camera-container {
        background: #000;
        border-radius: 1rem;
        padding: 1rem;
        text-align: center;
        margin: 1rem 0;
    }

    /* Mobile optimizations */
    @media (max-width: 768px) {
        .main-header { font-size: 1.5rem; }
        .sub-header { font-size: 1.1rem; }
        .score-display { font-size: 2.5rem; }
    }

    /* Hide Streamlit branding for cleaner mobile look */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Progress bar styling */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #667eea, #764ba2);
    }

    /* Button styling */
    .stButton > button {
        width: 100%;
        border-radius: 0.5rem;
        font-weight: 600;
        padding: 0.75rem 1.5rem;
    }

    .stButton > button[kind="primary"] {
        background: linear-gradient(90deg, #667eea, #764ba2);
        border: none;
    }
</style>
""", unsafe_allow_html=True)


def init_session_state():
    """Initialize session state variables"""
    if 'page' not in st.session_state:
        st.session_state.page = 'welcome'
    if 'client_name' not in st.session_state:
        st.session_state.client_name = ''
    if 'current_pose_index' not in st.session_state:
        st.session_state.current_pose_index = 0
    if 'assessments' not in st.session_state:
        st.session_state.assessments = []
    if 'pose_answers' not in st.session_state:
        st.session_state.pose_answers = {}
    if 'report' not in st.session_state:
        st.session_state.report = None
    if 'selected_poses' not in st.session_state:
        st.session_state.selected_poses = []
    if 'analyzer' not in st.session_state:
        st.session_state.analyzer = PostureAnalyzer()


def get_pose_display_name(pose_type: PoseType) -> str:
    """Get user-friendly display name for pose"""
    names = {
        PoseType.FRONT_VIEW: "Front View",
        PoseType.SIDE_VIEW_LEFT: "Left Side View",
        PoseType.SIDE_VIEW_RIGHT: "Right Side View",
        PoseType.BACK_VIEW: "Back View",
        PoseType.OVERHEAD_SQUAT: "Overhead Squat",
        PoseType.SINGLE_LEG_SQUAT_LEFT: "Single Leg Squat (Left)",
        PoseType.SINGLE_LEG_SQUAT_RIGHT: "Single Leg Squat (Right)",
        PoseType.FORWARD_BEND: "Forward Bend",
        PoseType.INLINE_LUNGE_LEFT: "Inline Lunge (Left)",
        PoseType.INLINE_LUNGE_RIGHT: "Inline Lunge (Right)"
    }
    return names.get(pose_type, pose_type.value.replace("_", " ").title())


def get_pose_emoji(pose_type: PoseType) -> str:
    """Get emoji for pose type"""
    emojis = {
        PoseType.FRONT_VIEW: "🧍",
        PoseType.SIDE_VIEW_LEFT: "🧍",
        PoseType.SIDE_VIEW_RIGHT: "🧍",
        PoseType.BACK_VIEW: "🧍",
        PoseType.OVERHEAD_SQUAT: "🏋️",
        PoseType.SINGLE_LEG_SQUAT_LEFT: "🦵",
        PoseType.SINGLE_LEG_SQUAT_RIGHT: "🦵",
        PoseType.FORWARD_BEND: "🙇",
        PoseType.INLINE_LUNGE_LEFT: "🚶",
        PoseType.INLINE_LUNGE_RIGHT: "🚶"
    }
    return emojis.get(pose_type, "🧍")


def show_welcome_page():
    """Welcome page with app introduction"""
    st.markdown('<div class="main-header">🧍 Posture Analysis</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="instruction-box">
        <h4>Welcome to Your Posture Assessment</h4>
        <p>This app will guide you through a comprehensive posture analysis to identify any
        issues and provide personalized corrective exercises.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### What You'll Need:")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        - A smartphone or tablet
        - A well-lit room
        - A friend to help (or a timer/mirror)
        - Comfortable, fitted clothing
        """)

    with col2:
        st.markdown("""
        - About 10-15 minutes
        - Clear space to move
        - Flat surface to stand on
        """)

    st.markdown("---")

    st.markdown("### How It Works:")
    st.markdown("""
    1. **Capture Poses** - Take photos from different angles
    2. **Answer Questions** - Evaluate what you see in each pose
    3. **Get Results** - Receive a detailed report with your posture score
    4. **Fix Issues** - Get personalized exercises for each problem area
    """)

    st.markdown("---")

    # Client name input
    client_name = st.text_input(
        "Enter your name to get started:",
        value=st.session_state.client_name,
        placeholder="Your name"
    )

    if st.button("Start Assessment", type="primary", use_container_width=True):
        if client_name:
            st.session_state.client_name = client_name
            st.session_state.page = 'pose_selection'
            st.rerun()
        else:
            st.error("Please enter your name to continue.")


def show_pose_selection_page():
    """Page to select which poses to assess"""
    st.markdown('<div class="main-header">Select Assessments</div>', unsafe_allow_html=True)

    st.markdown(f"**Client:** {st.session_state.client_name}")

    st.markdown("""
    <div class="instruction-box">
        <p>Select which assessments you'd like to perform. For a complete analysis,
        we recommend at least the <strong>Core 4</strong> assessments.</p>
    </div>
    """, unsafe_allow_html=True)

    # Core assessments (required for basic analysis)
    st.markdown("### Core Assessments (Recommended)")

    core_poses = [
        PoseType.FRONT_VIEW,
        PoseType.SIDE_VIEW_LEFT,
        PoseType.BACK_VIEW,
        PoseType.OVERHEAD_SQUAT
    ]

    selected_core = []
    cols = st.columns(2)
    for i, pose in enumerate(core_poses):
        with cols[i % 2]:
            if st.checkbox(
                f"{get_pose_emoji(pose)} {get_pose_display_name(pose)}",
                value=True,
                key=f"core_{pose.value}"
            ):
                selected_core.append(pose)

    st.markdown("### Advanced Assessments (Optional)")

    advanced_poses = [
        PoseType.SIDE_VIEW_RIGHT,
        PoseType.SINGLE_LEG_SQUAT_LEFT,
        PoseType.SINGLE_LEG_SQUAT_RIGHT,
        PoseType.FORWARD_BEND,
        PoseType.INLINE_LUNGE_LEFT,
        PoseType.INLINE_LUNGE_RIGHT
    ]

    selected_advanced = []
    cols = st.columns(2)
    for i, pose in enumerate(advanced_poses):
        with cols[i % 2]:
            if st.checkbox(
                f"{get_pose_emoji(pose)} {get_pose_display_name(pose)}",
                value=False,
                key=f"adv_{pose.value}"
            ):
                selected_advanced.append(pose)

    st.markdown("---")

    total_selected = len(selected_core) + len(selected_advanced)
    st.info(f"Selected: {total_selected} assessment(s)")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Back", use_container_width=True):
            st.session_state.page = 'welcome'
            st.rerun()

    with col2:
        if st.button("Continue", type="primary", use_container_width=True, disabled=total_selected == 0):
            st.session_state.selected_poses = selected_core + selected_advanced
            st.session_state.current_pose_index = 0
            st.session_state.assessments = []
            st.session_state.pose_answers = {}
            st.session_state.page = 'phone_setup'
            st.rerun()


def show_phone_setup_page():
    """Instructions for setting up the phone"""
    st.markdown('<div class="main-header">Phone Setup</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="instruction-box">
        <h4>How to Position Your Phone</h4>
        <p>For accurate results, proper phone positioning is essential.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Setup Instructions:")

    st.markdown("""
    **1. Find a Stable Surface**
    - Use a table, shelf, or tripod at hip height
    - Make sure the phone won't fall or move

    **2. Position the Phone**
    - Place phone 6-8 feet (2-2.5 meters) away
    - Keep phone straight (not tilted)
    - Use landscape orientation for better view

    **3. Lighting**
    - Face a window or light source
    - Avoid backlighting (light behind you)
    - Ensure your whole body is well-lit

    **4. Background**
    - Use a plain background if possible
    - Ensure enough contrast to see your body

    **5. What to Wear**
    - Fitted clothing (not baggy)
    - Shorts and tank top are ideal
    - Remove bulky shoes if possible
    """)

    st.markdown("---")

    st.markdown("""
    <div class="warning-box">
        <strong>Tip:</strong> If you're alone, use your phone's timer feature
        (usually 3 or 10 seconds) to give yourself time to get into position.
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Back", use_container_width=True):
            st.session_state.page = 'pose_selection'
            st.rerun()

    with col2:
        if st.button("I'm Ready!", type="primary", use_container_width=True):
            st.session_state.page = 'assessment'
            st.rerun()


def show_assessment_page():
    """Main assessment page with pose-by-pose evaluation"""
    poses = st.session_state.selected_poses
    current_index = st.session_state.current_pose_index

    if current_index >= len(poses):
        # All poses completed, generate report
        generate_report()
        st.session_state.page = 'results'
        st.rerun()
        return

    current_pose = poses[current_index]
    analyzer = st.session_state.analyzer

    # Progress indicator
    progress = (current_index) / len(poses)
    st.progress(progress)
    st.caption(f"Assessment {current_index + 1} of {len(poses)}")

    # Pose header
    st.markdown(f'<div class="main-header">{get_pose_emoji(current_pose)} {get_pose_display_name(current_pose)}</div>', unsafe_allow_html=True)

    # Get instructions
    instructions = analyzer.get_pose_instructions(current_pose)

    # Setup instructions
    with st.expander("Setup Instructions", expanded=True):
        st.markdown("**How to position yourself:**")
        for step in instructions.get('setup', []):
            st.markdown(f"- {step}")
        st.markdown(f"**Duration:** {instructions.get('duration', 'Hold for 5 seconds')}")

    st.markdown("---")

    # Camera section
    st.markdown("### Capture Your Pose")

    st.markdown("""
    <div class="instruction-box">
        <p>Take a photo or have someone take one for you. Then answer the questions below
        based on what you observe in the photo.</p>
    </div>
    """, unsafe_allow_html=True)

    # Camera input
    camera_photo = st.camera_input(
        "Take a photo",
        key=f"camera_{current_pose.value}",
        help="Position yourself according to the instructions above"
    )

    if camera_photo:
        st.success("Photo captured! Now answer the questions below.")

    st.markdown("---")

    # Assessment questions
    st.markdown("### Assessment Questions")
    st.markdown("*Based on what you see in the photo (or mirror), answer the following:*")

    questions = analyzer.get_questions_for_pose(current_pose)

    pose_key = current_pose.value
    if pose_key not in st.session_state.pose_answers:
        st.session_state.pose_answers[pose_key] = {}

    all_answered = True

    for q in questions:
        q_id = q['id']
        answer = st.radio(
            q['question'],
            options=q['options'],
            key=f"q_{pose_key}_{q_id}",
            index=None if q_id not in st.session_state.pose_answers[pose_key] else
                  q['options'].index(st.session_state.pose_answers[pose_key].get(q_id, q['options'][0]))
        )

        if answer:
            st.session_state.pose_answers[pose_key][q_id] = answer
        else:
            all_answered = False

    st.markdown("---")

    # Navigation
    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        if current_index > 0:
            if st.button("Previous", use_container_width=True):
                st.session_state.current_pose_index -= 1
                st.rerun()

    with col2:
        if st.button("Skip This Pose", use_container_width=True):
            st.session_state.current_pose_index += 1
            st.rerun()

    with col3:
        if st.button(
            "Next" if current_index < len(poses) - 1 else "Finish",
            type="primary",
            use_container_width=True,
            disabled=not all_answered
        ):
            # Save assessment
            answers = st.session_state.pose_answers.get(pose_key, {})
            assessment = analyzer.analyze_pose(current_pose, answers)
            st.session_state.assessments.append(assessment)

            st.session_state.current_pose_index += 1
            st.rerun()

    if not all_answered:
        st.warning("Please answer all questions to continue.")


def generate_report():
    """Generate the final posture report"""
    analyzer = st.session_state.analyzer

    report = analyzer.create_full_report(
        client_name=st.session_state.client_name,
        assessments=st.session_state.assessments
    )

    st.session_state.report = report


def show_results_page():
    """Display the assessment results"""
    report = st.session_state.report

    if not report:
        st.error("No report available. Please complete the assessment first.")
        if st.button("Start Over"):
            reset_assessment()
        return

    st.markdown('<div class="main-header">Your Posture Report</div>', unsafe_allow_html=True)

    # Score display
    score = report.overall_score
    score_class = (
        "excellent" if score >= 90 else
        "good" if score >= 70 else
        "fair" if score >= 50 else
        "poor"
    )

    st.markdown(f"""
    <div class="score-display {score_class}">
        {score:.0f}/100
    </div>
    <p style="text-align: center; font-size: 1.2rem; color: #666;">
        {report.client_name}'s Posture Score
    </p>
    """, unsafe_allow_html=True)

    # Summary
    st.markdown("---")
    st.markdown("### Summary")

    if report.all_issues:
        st.markdown(f"""
        <div class="warning-box">
            <strong>Issues Found:</strong> {len(report.all_issues)}<br>
            {report.summary.replace(chr(10), '<br>')}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="success-box">
            <strong>Great news!</strong> No significant posture issues detected.
            Keep up your healthy habits!
        </div>
        """, unsafe_allow_html=True)

    # Issues by severity
    if report.all_issues:
        st.markdown("---")
        st.markdown("### Detected Issues")

        issues_by_severity = report.get_issues_by_severity()

        for severity in [PostureSeverity.CRITICAL, PostureSeverity.SEVERE,
                        PostureSeverity.MODERATE, PostureSeverity.MINOR]:
            issues = issues_by_severity.get(severity, [])
            if issues:
                severity_label = {
                    PostureSeverity.CRITICAL: "Critical",
                    PostureSeverity.SEVERE: "Severe",
                    PostureSeverity.MODERATE: "Moderate",
                    PostureSeverity.MINOR: "Minor"
                }[severity]

                st.markdown(f"#### {severity_label} Issues ({len(issues)})")

                for issue in issues:
                    with st.expander(f"{issue.name}", expanded=severity in [PostureSeverity.CRITICAL, PostureSeverity.SEVERE]):
                        st.markdown(f"**Description:** {issue.description}")

                        st.markdown("**What to look for:**")
                        for indicator in issue.visual_indicators:
                            st.markdown(f"- {indicator}")

                        st.markdown("**Potential causes:**")
                        for cause in issue.potential_causes:
                            st.markdown(f"- {cause}")

                        st.markdown("**If not addressed:**")
                        for consequence in issue.potential_consequences:
                            st.markdown(f"- {consequence}")

    # Priority fixes
    st.markdown("---")
    st.markdown("### Your Corrective Exercise Program")

    if report.prioritized_fixes:
        st.markdown("""
        <div class="instruction-box">
            <p>These exercises are specifically selected to address your posture issues.
            Start with 2-3 exercises and gradually add more as you improve.</p>
        </div>
        """, unsafe_allow_html=True)

        for i, fix in enumerate(report.prioritized_fixes, 1):
            with st.expander(f"{i}. {fix.name} ({fix.category.title()})", expanded=i <= 3):
                st.markdown(f"**{fix.description}**")

                st.markdown(f"**Frequency:** {fix.frequency}")
                st.markdown(f"**Duration:** {fix.duration}")
                st.markdown(f"**Difficulty:** {fix.difficulty.title()}")

                if fix.equipment_needed:
                    st.markdown(f"**Equipment:** {', '.join(fix.equipment_needed)}")

                st.markdown("**Instructions:**")
                for j, step in enumerate(fix.instructions, 1):
                    st.markdown(f"{j}. {step}")

                if fix.muscles_targeted:
                    st.markdown(f"*Targets: {', '.join(fix.muscles_targeted)}*")
    else:
        st.markdown("""
        <div class="success-box">
            No corrective exercises needed! Consider these maintenance exercises:
            <ul>
                <li>Daily stretching routine</li>
                <li>Core strengthening exercises</li>
                <li>Regular movement breaks</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    # Recommendations
    st.markdown("---")
    st.markdown("### Recommendations")

    for rec in report.recommendations:
        st.markdown(f"- {rec}")

    # Download report
    st.markdown("---")
    st.markdown("### Save Your Report")

    report_md = generate_markdown_report(report)

    st.download_button(
        label="Download Report (Markdown)",
        data=report_md,
        file_name=f"posture_report_{report.client_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.md",
        mime="text/markdown",
        use_container_width=True
    )

    # Action buttons
    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Start New Assessment", use_container_width=True):
            reset_assessment()

    with col2:
        if st.button("View Issue Database", use_container_width=True):
            st.session_state.page = 'database'
            st.rerun()


def generate_markdown_report(report: PostureReport) -> str:
    """Generate a markdown version of the report"""
    lines = [
        f"# Posture Assessment Report",
        f"",
        f"**Client:** {report.client_name}",
        f"**Date:** {report.created_at.strftime('%Y-%m-%d %H:%M')}",
        f"**Report ID:** {report.report_id}",
        f"",
        f"---",
        f"",
        f"## Overall Score: {report.overall_score:.0f}/100",
        f"",
        f"### Summary",
        f"",
        report.summary,
        f"",
    ]

    if report.all_issues:
        lines.extend([
            f"---",
            f"",
            f"## Detected Issues",
            f"",
        ])

        for issue in report.all_issues:
            lines.extend([
                f"### {issue.name}",
                f"",
                f"**Severity:** {issue.severity.value.title()}",
                f"",
                f"**Description:** {issue.description}",
                f"",
                f"**Visual Indicators:**",
            ])
            for indicator in issue.visual_indicators:
                lines.append(f"- {indicator}")

            lines.extend([
                f"",
                f"**Potential Causes:**",
            ])
            for cause in issue.potential_causes:
                lines.append(f"- {cause}")

            lines.extend([
                f"",
                f"**Potential Consequences:**",
            ])
            for consequence in issue.potential_consequences:
                lines.append(f"- {consequence}")

            lines.append("")

    if report.prioritized_fixes:
        lines.extend([
            f"---",
            f"",
            f"## Corrective Exercise Program",
            f"",
        ])

        for i, fix in enumerate(report.prioritized_fixes, 1):
            lines.extend([
                f"### {i}. {fix.name}",
                f"",
                f"**Category:** {fix.category.title()}",
                f"",
                f"**Description:** {fix.description}",
                f"",
                f"**Frequency:** {fix.frequency}",
                f"",
                f"**Duration:** {fix.duration}",
                f"",
                f"**Difficulty:** {fix.difficulty.title()}",
                f"",
            ])

            if fix.equipment_needed:
                lines.append(f"**Equipment:** {', '.join(fix.equipment_needed)}")
                lines.append("")

            lines.append("**Instructions:**")
            for j, step in enumerate(fix.instructions, 1):
                lines.append(f"{j}. {step}")

            if fix.muscles_targeted:
                lines.append("")
                lines.append(f"*Targets: {', '.join(fix.muscles_targeted)}*")

            lines.append("")

    lines.extend([
        f"---",
        f"",
        f"## Recommendations",
        f"",
    ])

    for rec in report.recommendations:
        lines.append(f"- {rec}")

    lines.extend([
        f"",
        f"---",
        f"",
        f"*Report generated by Fitlife Posture Analysis*",
    ])

    return "\n".join(lines)


def show_database_page():
    """Browse the issue and exercise database"""
    st.markdown('<div class="main-header">Exercise Database</div>', unsafe_allow_html=True)

    db = PostureIssueDatabase()

    tab1, tab2 = st.tabs(["Issues", "Exercises"])

    with tab1:
        st.markdown("### All Posture Issues")

        # Filter by body region
        regions = list(BodyRegion)
        selected_region = st.selectbox(
            "Filter by Body Region",
            ["All"] + [r.value.replace("_", " ").title() for r in regions]
        )

        issues = db.get_all_issues()

        if selected_region != "All":
            region_enum = BodyRegion(selected_region.lower().replace(" ", "_"))
            issues = [i for i in issues if i.body_region == region_enum]

        for issue in issues:
            severity_color = {
                PostureSeverity.MINOR: "#17a2b8",
                PostureSeverity.MODERATE: "#ffc107",
                PostureSeverity.SEVERE: "#fd7e14",
                PostureSeverity.CRITICAL: "#dc3545"
            }[issue.severity]

            with st.expander(f"{issue.name} ({issue.severity.value.title()})"):
                st.markdown(f"**Region:** {issue.body_region.value.replace('_', ' ').title()}")
                st.markdown(f"**Description:** {issue.description}")

                st.markdown("**Visual Indicators:**")
                for indicator in issue.visual_indicators:
                    st.markdown(f"- {indicator}")

                st.markdown("**Recommended Exercises:**")
                for fix in issue.recommended_fixes:
                    st.markdown(f"- {fix.name}")

    with tab2:
        st.markdown("### All Corrective Exercises")

        # Filter by category
        categories = ["All", "Stretch", "Strengthen", "Mobilize", "Release"]
        selected_category = st.selectbox("Filter by Category", categories)

        fixes = db.get_all_fixes()

        if selected_category != "All":
            fixes = [f for f in fixes if f.category == selected_category.lower()]

        for fix in fixes:
            with st.expander(f"{fix.name} ({fix.category.title()})"):
                st.markdown(f"**{fix.description}**")

                st.markdown(f"**Frequency:** {fix.frequency}")
                st.markdown(f"**Duration:** {fix.duration}")
                st.markdown(f"**Difficulty:** {fix.difficulty.title()}")

                if fix.equipment_needed:
                    st.markdown(f"**Equipment:** {', '.join(fix.equipment_needed)}")

                st.markdown("**Instructions:**")
                for i, step in enumerate(fix.instructions, 1):
                    st.markdown(f"{i}. {step}")

                if fix.muscles_targeted:
                    st.markdown(f"*Targets: {', '.join(fix.muscles_targeted)}*")

    st.markdown("---")

    if st.button("Back to Results", use_container_width=True):
        st.session_state.page = 'results'
        st.rerun()


def reset_assessment():
    """Reset the assessment to start over"""
    st.session_state.page = 'welcome'
    st.session_state.current_pose_index = 0
    st.session_state.assessments = []
    st.session_state.pose_answers = {}
    st.session_state.report = None
    st.session_state.selected_poses = []
    st.rerun()


def main():
    """Main application entry point"""
    init_session_state()

    # Navigation sidebar
    with st.sidebar:
        st.markdown("### Navigation")

        if st.button("Home", use_container_width=True):
            st.session_state.page = 'welcome'
            st.rerun()

        if st.session_state.report:
            if st.button("View Report", use_container_width=True):
                st.session_state.page = 'results'
                st.rerun()

        if st.button("Exercise Database", use_container_width=True):
            st.session_state.page = 'database'
            st.rerun()

        st.markdown("---")

        if st.button("Start Over", use_container_width=True):
            reset_assessment()

    # Page routing
    page = st.session_state.page

    if page == 'welcome':
        show_welcome_page()
    elif page == 'pose_selection':
        show_pose_selection_page()
    elif page == 'phone_setup':
        show_phone_setup_page()
    elif page == 'assessment':
        show_assessment_page()
    elif page == 'results':
        show_results_page()
    elif page == 'database':
        show_database_page()
    else:
        show_welcome_page()


if __name__ == "__main__":
    main()
