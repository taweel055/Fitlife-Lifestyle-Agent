"""
Posture Issue Database
Comprehensive database of common posture issues with corrective exercises
"""

from typing import List, Optional, Dict
from .models import (
    PostureIssue,
    PostureFix,
    PostureSeverity,
    BodyRegion,
    PoseType
)


class PostureIssueDatabase:
    """Database of posture issues and their fixes"""

    def __init__(self):
        self._issues: Dict[str, PostureIssue] = {}
        self._fixes: Dict[str, PostureFix] = {}
        self._load_fixes()
        self._load_issues()

    def _load_fixes(self):
        """Load all corrective exercises and stretches"""
        fixes = [
            # NECK AND HEAD FIXES
            PostureFix(
                name="Chin Tucks",
                description="Strengthens deep neck flexors and corrects forward head posture",
                instructions=[
                    "Sit or stand with good posture",
                    "Look straight ahead",
                    "Gently tuck your chin back, creating a double chin",
                    "Hold for 5 seconds",
                    "Release and repeat"
                ],
                duration="10-15 reps",
                frequency="3x daily",
                difficulty="beginner",
                muscles_targeted=["deep neck flexors", "longus colli", "longus capitis"],
                category="strengthen"
            ),
            PostureFix(
                name="Neck Stretches",
                description="Releases tension in neck muscles",
                instructions=[
                    "Sit or stand tall",
                    "Gently tilt your head to the right, bringing ear toward shoulder",
                    "Hold for 30 seconds",
                    "Repeat on left side",
                    "Then gently look up and down, holding each position"
                ],
                duration="30 seconds each side",
                frequency="2-3x daily",
                difficulty="beginner",
                muscles_targeted=["upper trapezius", "levator scapulae", "scalenes"],
                category="stretch"
            ),
            PostureFix(
                name="Suboccipital Release",
                description="Releases tension at the base of the skull",
                instructions=[
                    "Lie on your back",
                    "Place two tennis balls in a sock, tied together",
                    "Position balls at the base of your skull",
                    "Relax your head weight onto the balls",
                    "Gently nod yes and no motions"
                ],
                duration="2-3 minutes",
                frequency="1x daily",
                difficulty="beginner",
                equipment_needed=["2 tennis balls", "sock"],
                muscles_targeted=["suboccipitals", "rectus capitis"],
                category="release"
            ),

            # SHOULDER FIXES
            PostureFix(
                name="Wall Angels",
                description="Improves shoulder mobility and upper back posture",
                instructions=[
                    "Stand with back against wall, feet 6 inches from wall",
                    "Press lower back, upper back, and head against wall",
                    "Raise arms to 90 degrees (goal post position)",
                    "Slowly slide arms up and down the wall",
                    "Keep contact with wall throughout"
                ],
                duration="10-15 reps",
                frequency="2x daily",
                difficulty="beginner",
                muscles_targeted=["lower trapezius", "rhomboids", "serratus anterior"],
                category="mobilize"
            ),
            PostureFix(
                name="Doorway Pec Stretch",
                description="Opens up tight chest muscles",
                instructions=[
                    "Stand in a doorway",
                    "Place forearms on door frame, elbows at 90 degrees",
                    "Step one foot forward through the doorway",
                    "Lean forward until you feel a stretch in your chest",
                    "Hold the stretch"
                ],
                duration="30-45 seconds",
                frequency="3x daily",
                difficulty="beginner",
                muscles_targeted=["pectoralis major", "pectoralis minor", "anterior deltoid"],
                category="stretch"
            ),
            PostureFix(
                name="Shoulder External Rotation",
                description="Strengthens rotator cuff and improves shoulder alignment",
                instructions=[
                    "Hold a resistance band with both hands",
                    "Keep elbows at sides, bent at 90 degrees",
                    "Rotate forearms outward, stretching the band",
                    "Keep shoulders down and back",
                    "Slowly return to starting position"
                ],
                duration="15 reps x 3 sets",
                frequency="Daily",
                difficulty="beginner",
                equipment_needed=["resistance band"],
                muscles_targeted=["infraspinatus", "teres minor", "posterior deltoid"],
                category="strengthen"
            ),
            PostureFix(
                name="Prone Y-T-W Raises",
                description="Strengthens upper back muscles for better shoulder position",
                instructions=[
                    "Lie face down on floor or bench",
                    "Y: Raise arms overhead at 45-degree angle, thumbs up",
                    "T: Raise arms straight out to sides, thumbs up",
                    "W: Pull elbows down and back, squeezing shoulder blades",
                    "Hold each position for 3-5 seconds"
                ],
                duration="10 reps each position",
                frequency="Daily",
                difficulty="intermediate",
                muscles_targeted=["lower trapezius", "middle trapezius", "rhomboids"],
                category="strengthen"
            ),
            PostureFix(
                name="Scapular Retraction",
                description="Strengthens muscles that pull shoulders back",
                instructions=[
                    "Stand or sit with good posture",
                    "Squeeze shoulder blades together and down",
                    "Imagine putting shoulder blades in your back pockets",
                    "Hold for 5-10 seconds",
                    "Release and repeat"
                ],
                duration="15 reps",
                frequency="Throughout the day",
                difficulty="beginner",
                muscles_targeted=["rhomboids", "middle trapezius", "lower trapezius"],
                category="strengthen"
            ),

            # UPPER BACK / THORACIC FIXES
            PostureFix(
                name="Thoracic Foam Roll Extension",
                description="Improves thoracic spine mobility and reduces kyphosis",
                instructions=[
                    "Lie on foam roller positioned across upper back",
                    "Support head with hands behind it",
                    "Keep hips on the ground",
                    "Slowly extend back over the roller",
                    "Move roller up and down the thoracic spine"
                ],
                duration="2-3 minutes",
                frequency="Daily",
                difficulty="beginner",
                equipment_needed=["foam roller"],
                muscles_targeted=["thoracic erectors", "rhomboids"],
                category="mobilize"
            ),
            PostureFix(
                name="Cat-Cow Stretch",
                description="Improves spinal mobility and awareness",
                instructions=[
                    "Start on hands and knees, wrists under shoulders",
                    "Cow: Drop belly, lift chest and tailbone, look up",
                    "Cat: Round spine toward ceiling, tuck chin and tailbone",
                    "Move slowly between positions",
                    "Breathe deeply with each movement"
                ],
                duration="10-15 cycles",
                frequency="2x daily",
                difficulty="beginner",
                muscles_targeted=["erector spinae", "rectus abdominis", "multifidus"],
                category="mobilize"
            ),
            PostureFix(
                name="Thread the Needle",
                description="Rotational stretch for thoracic spine",
                instructions=[
                    "Start on hands and knees",
                    "Reach right arm under your body toward the left",
                    "Let your right shoulder and head rest on the ground",
                    "Hold and breathe into the stretch",
                    "Return and repeat on other side"
                ],
                duration="30 seconds each side",
                frequency="2x daily",
                difficulty="beginner",
                muscles_targeted=["thoracic rotators", "latissimus dorsi", "rhomboids"],
                category="mobilize"
            ),

            # LOWER BACK FIXES
            PostureFix(
                name="Dead Bug",
                description="Core stabilization exercise that protects lower back",
                instructions=[
                    "Lie on back with arms reaching toward ceiling",
                    "Lift legs to tabletop position (90-degree bend)",
                    "Press lower back firmly into floor",
                    "Slowly lower opposite arm and leg toward floor",
                    "Return and alternate sides"
                ],
                duration="10 reps each side",
                frequency="Daily",
                difficulty="beginner",
                muscles_targeted=["transverse abdominis", "rectus abdominis", "obliques"],
                category="strengthen"
            ),
            PostureFix(
                name="Bird Dog",
                description="Strengthens core and back extensors",
                instructions=[
                    "Start on hands and knees, spine neutral",
                    "Extend right arm forward and left leg back",
                    "Keep hips and shoulders square to floor",
                    "Hold for 3-5 seconds",
                    "Return and alternate sides"
                ],
                duration="10 reps each side",
                frequency="Daily",
                difficulty="beginner",
                muscles_targeted=["erector spinae", "multifidus", "glutes", "core"],
                category="strengthen"
            ),
            PostureFix(
                name="Hip Flexor Stretch (Kneeling)",
                description="Releases tight hip flexors that cause anterior pelvic tilt",
                instructions=[
                    "Kneel on right knee, left foot forward",
                    "Keep torso upright, engage core",
                    "Shift weight forward until stretch is felt in right hip",
                    "Squeeze right glute for deeper stretch",
                    "Hold and repeat on other side"
                ],
                duration="45-60 seconds each side",
                frequency="2-3x daily",
                difficulty="beginner",
                muscles_targeted=["iliopsoas", "rectus femoris", "tensor fasciae latae"],
                category="stretch"
            ),
            PostureFix(
                name="Glute Bridge",
                description="Strengthens glutes and reduces anterior pelvic tilt",
                instructions=[
                    "Lie on back with knees bent, feet flat",
                    "Press through heels to lift hips toward ceiling",
                    "Squeeze glutes at top of movement",
                    "Keep core engaged throughout",
                    "Lower slowly and repeat"
                ],
                duration="15 reps x 3 sets",
                frequency="Daily",
                difficulty="beginner",
                muscles_targeted=["gluteus maximus", "hamstrings", "core"],
                category="strengthen"
            ),
            PostureFix(
                name="Psoas Release",
                description="Release tension in the psoas muscle",
                instructions=[
                    "Lie on your back",
                    "Place a softball or lacrosse ball just inside your hip bone",
                    "Carefully lower your weight onto the ball",
                    "Breathe deeply and relax into the pressure",
                    "Hold for 60-90 seconds each side"
                ],
                duration="60-90 seconds each side",
                frequency="Daily",
                difficulty="intermediate",
                equipment_needed=["softball or lacrosse ball"],
                muscles_targeted=["psoas major", "iliacus"],
                category="release"
            ),

            # HIP AND PELVIS FIXES
            PostureFix(
                name="90/90 Hip Stretch",
                description="Improves hip internal and external rotation",
                instructions=[
                    "Sit on floor with one leg in front (shin parallel to body)",
                    "Other leg to the side (also 90 degrees)",
                    "Sit tall, lean forward over front leg",
                    "Hold, then switch leg positions",
                    "Keep back straight throughout"
                ],
                duration="45 seconds each side",
                frequency="2x daily",
                difficulty="intermediate",
                muscles_targeted=["piriformis", "gluteus medius", "hip rotators"],
                category="mobilize"
            ),
            PostureFix(
                name="Pigeon Stretch",
                description="Deep hip opener targeting piriformis and glutes",
                instructions=[
                    "Start in plank or downward dog",
                    "Bring right knee forward toward right hand",
                    "Extend left leg straight behind you",
                    "Square hips to floor as much as possible",
                    "Fold forward for deeper stretch"
                ],
                duration="60-90 seconds each side",
                frequency="Daily",
                difficulty="intermediate",
                muscles_targeted=["piriformis", "gluteus maximus", "hip flexors"],
                category="stretch"
            ),
            PostureFix(
                name="Clamshells",
                description="Strengthens gluteus medius for hip stability",
                instructions=[
                    "Lie on side with knees bent at 45 degrees",
                    "Keep feet together",
                    "Lift top knee while keeping feet touching",
                    "Don't let hips roll backward",
                    "Lower slowly and repeat"
                ],
                duration="15 reps x 3 sets each side",
                frequency="Daily",
                difficulty="beginner",
                equipment_needed=["resistance band (optional)"],
                muscles_targeted=["gluteus medius", "gluteus minimus", "hip rotators"],
                category="strengthen"
            ),

            # KNEE FIXES
            PostureFix(
                name="VMO Strengthening (Terminal Knee Extension)",
                description="Strengthens inner quad for knee stability",
                instructions=[
                    "Sit with legs extended, rolled towel under knee",
                    "Press knee down into towel, straightening leg fully",
                    "Focus on tightening the inner quad (VMO)",
                    "Hold for 5 seconds",
                    "Relax and repeat"
                ],
                duration="15 reps x 3 sets",
                frequency="Daily",
                difficulty="beginner",
                equipment_needed=["rolled towel"],
                muscles_targeted=["vastus medialis oblique", "quadriceps"],
                category="strengthen"
            ),
            PostureFix(
                name="IT Band Foam Rolling",
                description="Releases tension in the IT band",
                instructions=[
                    "Lie on side with foam roller under outer thigh",
                    "Support yourself with arms and top leg",
                    "Roll slowly from hip to just above knee",
                    "Pause on tender spots for 20-30 seconds",
                    "Avoid rolling directly on the knee"
                ],
                duration="2-3 minutes each side",
                frequency="Daily",
                difficulty="intermediate",
                equipment_needed=["foam roller"],
                muscles_targeted=["IT band", "tensor fasciae latae", "vastus lateralis"],
                category="release"
            ),
            PostureFix(
                name="Wall Sit",
                description="Strengthens quads and improves knee stability",
                instructions=[
                    "Stand with back against wall",
                    "Slide down until thighs are parallel to floor",
                    "Keep knees over ankles, not past toes",
                    "Press lower back into wall",
                    "Hold the position"
                ],
                duration="30-60 seconds",
                frequency="3x daily",
                difficulty="beginner",
                muscles_targeted=["quadriceps", "glutes", "core"],
                category="strengthen"
            ),

            # ANKLE AND FOOT FIXES
            PostureFix(
                name="Calf Stretch (Wall)",
                description="Stretches gastrocnemius and soleus muscles",
                instructions=[
                    "Stand facing a wall, hands on wall",
                    "Step one foot back, keeping heel on ground",
                    "Bend front knee while keeping back leg straight",
                    "Feel stretch in back calf",
                    "For soleus, slightly bend back knee"
                ],
                duration="30 seconds each leg, both variations",
                frequency="3x daily",
                difficulty="beginner",
                muscles_targeted=["gastrocnemius", "soleus", "Achilles tendon"],
                category="stretch"
            ),
            PostureFix(
                name="Ankle Mobility (Knee to Wall)",
                description="Improves ankle dorsiflexion",
                instructions=[
                    "Stand facing a wall, toes 4-6 inches away",
                    "Keep heel on ground, drive knee toward wall",
                    "Touch wall without heel lifting",
                    "Move foot back to find your limit",
                    "Perform slow controlled reps"
                ],
                duration="15 reps each ankle",
                frequency="Daily",
                difficulty="beginner",
                muscles_targeted=["ankle dorsiflexors", "soleus", "gastrocnemius"],
                category="mobilize"
            ),
            PostureFix(
                name="Toe Yoga",
                description="Improves foot control and arch strength",
                instructions=[
                    "Sit or stand with feet flat on ground",
                    "Lift big toe while keeping other toes down",
                    "Then lift other toes while keeping big toe down",
                    "Spread all toes wide, then relax",
                    "Practice until you gain independent control"
                ],
                duration="10 reps each movement",
                frequency="Daily",
                difficulty="beginner",
                muscles_targeted=["intrinsic foot muscles", "arch muscles"],
                category="strengthen"
            ),
            PostureFix(
                name="Short Foot Exercise",
                description="Strengthens foot arch muscles",
                instructions=[
                    "Stand or sit with feet flat",
                    "Without curling toes, try to shorten your foot",
                    "Draw the ball of foot toward heel using arch",
                    "Hold for 5-10 seconds",
                    "Relax and repeat"
                ],
                duration="10 reps x 3 sets",
                frequency="Daily",
                difficulty="intermediate",
                muscles_targeted=["plantar intrinsic muscles", "arch muscles"],
                category="strengthen"
            ),

            # FULL BODY / GENERAL FIXES
            PostureFix(
                name="Wall Posture Check",
                description="Builds awareness of proper standing posture",
                instructions=[
                    "Stand with heels 2 inches from wall",
                    "Press buttocks, upper back, and head against wall",
                    "Chin should be level (not tilted up)",
                    "Small gap at lower back is normal",
                    "Hold position, memorize the feeling"
                ],
                duration="1-2 minutes",
                frequency="Several times daily",
                difficulty="beginner",
                muscles_targeted=["full body postural muscles"],
                category="mobilize"
            ),
            PostureFix(
                name="Plank",
                description="Full core strengthening for postural support",
                instructions=[
                    "Start on forearms and toes",
                    "Keep body in straight line from head to heels",
                    "Engage core, don't let hips sag or pike up",
                    "Keep neck neutral, look at floor",
                    "Breathe normally throughout"
                ],
                duration="30-60 seconds",
                frequency="Daily",
                difficulty="beginner",
                muscles_targeted=["transverse abdominis", "rectus abdominis", "obliques", "erectors"],
                category="strengthen"
            ),
            PostureFix(
                name="Child's Pose",
                description="Gentle stretch for back and relaxation",
                instructions=[
                    "Kneel on floor, sit back on heels",
                    "Fold forward, reaching arms overhead on floor",
                    "Rest forehead on floor",
                    "Breathe deeply into your back",
                    "Relax completely"
                ],
                duration="1-2 minutes",
                frequency="As needed",
                difficulty="beginner",
                muscles_targeted=["latissimus dorsi", "erector spinae", "shoulders"],
                category="stretch"
            ),
            PostureFix(
                name="Breathing Exercises (Diaphragmatic)",
                description="Improves core function and reduces tension",
                instructions=[
                    "Lie on back with knees bent",
                    "Place one hand on chest, one on belly",
                    "Breathe in through nose, belly rises (chest stays still)",
                    "Exhale slowly through mouth, belly falls",
                    "Practice slow, controlled breaths"
                ],
                duration="5-10 minutes",
                frequency="2x daily",
                difficulty="beginner",
                muscles_targeted=["diaphragm", "transverse abdominis", "pelvic floor"],
                category="mobilize"
            ),
        ]

        for fix in fixes:
            self._fixes[fix.name] = fix

    def _load_issues(self):
        """Load all posture issues with their associated fixes"""
        issues = [
            # HEAD AND NECK ISSUES
            PostureIssue(
                id="forward_head",
                name="Forward Head Posture",
                name_ar="وضعية الرأس الأمامية",
                description="Head positioned forward of the shoulders, often called 'tech neck' or 'text neck'. Common in people who use computers or phones frequently.",
                description_ar="وضع الرأس للأمام من الكتفين، يسمى أيضاً رقبة التكنولوجيا",
                body_region=BodyRegion.HEAD,
                severity=PostureSeverity.MODERATE,
                detected_in_poses=[PoseType.SIDE_VIEW_LEFT, PoseType.SIDE_VIEW_RIGHT],
                visual_indicators=[
                    "Ear is forward of the shoulder when viewed from the side",
                    "Chin juts forward",
                    "Neck appears to lean forward at an angle"
                ],
                potential_causes=[
                    "Prolonged computer/phone use",
                    "Poor workstation ergonomics",
                    "Weak deep neck flexors",
                    "Tight chest and front shoulder muscles"
                ],
                potential_consequences=[
                    "Neck pain and headaches",
                    "Increased stress on cervical spine",
                    "Temporomandibular joint (TMJ) issues",
                    "Reduced lung capacity"
                ],
                recommended_fixes=[
                    self._fixes["Chin Tucks"],
                    self._fixes["Neck Stretches"],
                    self._fixes["Suboccipital Release"],
                    self._fixes["Wall Posture Check"]
                ],
                priority=2
            ),
            PostureIssue(
                id="head_tilt",
                name="Head Tilt (Lateral)",
                name_ar="ميلان الرأس الجانبي",
                description="Head tilts to one side, one ear closer to the shoulder than the other.",
                body_region=BodyRegion.HEAD,
                severity=PostureSeverity.MINOR,
                detected_in_poses=[PoseType.FRONT_VIEW, PoseType.BACK_VIEW],
                visual_indicators=[
                    "One ear appears higher than the other",
                    "Head tilts consistently to one side",
                    "Neck appears curved to one side"
                ],
                potential_causes=[
                    "Muscle imbalance in neck",
                    "Habit of tilting head (phone use)",
                    "Vision or hearing compensation",
                    "Scoliosis"
                ],
                potential_consequences=[
                    "Neck muscle strain",
                    "Uneven muscle development",
                    "Tension headaches"
                ],
                recommended_fixes=[
                    self._fixes["Neck Stretches"],
                    self._fixes["Suboccipital Release"]
                ],
                priority=4
            ),

            # SHOULDER ISSUES
            PostureIssue(
                id="rounded_shoulders",
                name="Rounded Shoulders",
                name_ar="الكتفين المستديرين",
                description="Shoulders roll forward and inward, often accompanied by a hunched upper back.",
                body_region=BodyRegion.SHOULDERS,
                severity=PostureSeverity.MODERATE,
                detected_in_poses=[PoseType.SIDE_VIEW_LEFT, PoseType.SIDE_VIEW_RIGHT, PoseType.FRONT_VIEW],
                visual_indicators=[
                    "Shoulders roll forward when viewed from the side",
                    "Palms face backward when standing relaxed",
                    "Chest appears sunken",
                    "Upper back appears rounded"
                ],
                potential_causes=[
                    "Tight chest muscles (pectorals)",
                    "Weak upper back muscles",
                    "Prolonged sitting",
                    "Forward-reaching activities"
                ],
                potential_consequences=[
                    "Shoulder impingement",
                    "Reduced shoulder mobility",
                    "Neck and upper back pain",
                    "Breathing restrictions"
                ],
                recommended_fixes=[
                    self._fixes["Doorway Pec Stretch"],
                    self._fixes["Wall Angels"],
                    self._fixes["Scapular Retraction"],
                    self._fixes["Prone Y-T-W Raises"]
                ],
                priority=2
            ),
            PostureIssue(
                id="uneven_shoulders",
                name="Uneven Shoulder Height",
                name_ar="ارتفاع غير متساوي للكتفين",
                description="One shoulder sits higher than the other when standing relaxed.",
                body_region=BodyRegion.SHOULDERS,
                severity=PostureSeverity.MINOR,
                detected_in_poses=[PoseType.FRONT_VIEW, PoseType.BACK_VIEW],
                visual_indicators=[
                    "One shoulder appears higher when viewed from front or back",
                    "Collar line is uneven",
                    "One arm may hang lower than the other"
                ],
                potential_causes=[
                    "Muscle imbalance",
                    "Carrying bags on one shoulder",
                    "Scoliosis",
                    "Leg length discrepancy"
                ],
                potential_consequences=[
                    "Neck and shoulder tension",
                    "Muscle strain",
                    "Compensatory movement patterns"
                ],
                recommended_fixes=[
                    self._fixes["Neck Stretches"],
                    self._fixes["Scapular Retraction"],
                    self._fixes["Wall Angels"]
                ],
                priority=4
            ),
            PostureIssue(
                id="shoulder_internal_rotation",
                name="Excessive Shoulder Internal Rotation",
                name_ar="الدوران الداخلي المفرط للكتف",
                description="Shoulders excessively rotated inward, with palms facing backward.",
                body_region=BodyRegion.SHOULDERS,
                severity=PostureSeverity.MODERATE,
                detected_in_poses=[PoseType.FRONT_VIEW, PoseType.OVERHEAD_SQUAT],
                visual_indicators=[
                    "Thumbs point inward/backward when arms hang naturally",
                    "Back of hands visible from front view",
                    "Arms fall inward during overhead movements"
                ],
                potential_causes=[
                    "Tight internal rotators (lats, pecs, subscapularis)",
                    "Weak external rotators",
                    "Poor posture habits",
                    "Desk work"
                ],
                potential_consequences=[
                    "Shoulder impingement",
                    "Rotator cuff issues",
                    "Limited overhead mobility"
                ],
                recommended_fixes=[
                    self._fixes["Shoulder External Rotation"],
                    self._fixes["Doorway Pec Stretch"],
                    self._fixes["Wall Angels"]
                ],
                priority=3
            ),

            # UPPER BACK ISSUES
            PostureIssue(
                id="kyphosis",
                name="Excessive Thoracic Kyphosis (Hunchback)",
                name_ar="تقوس الظهر العلوي (الحداب)",
                description="Excessive rounding of the upper back, creating a hunched appearance.",
                body_region=BodyRegion.UPPER_BACK,
                severity=PostureSeverity.SEVERE,
                detected_in_poses=[PoseType.SIDE_VIEW_LEFT, PoseType.SIDE_VIEW_RIGHT],
                visual_indicators=[
                    "Pronounced curve in upper back",
                    "Shoulders appear to fall forward",
                    "Head positioned forward",
                    "Difficulty standing fully upright"
                ],
                potential_causes=[
                    "Prolonged sitting with poor posture",
                    "Weak back extensors",
                    "Tight chest and front body",
                    "Osteoporosis (in older adults)"
                ],
                potential_consequences=[
                    "Back pain",
                    "Breathing difficulties",
                    "Digestive issues",
                    "Balance problems"
                ],
                recommended_fixes=[
                    self._fixes["Thoracic Foam Roll Extension"],
                    self._fixes["Cat-Cow Stretch"],
                    self._fixes["Prone Y-T-W Raises"],
                    self._fixes["Doorway Pec Stretch"]
                ],
                priority=1
            ),
            PostureIssue(
                id="flat_upper_back",
                name="Flat Upper Back",
                name_ar="الظهر العلوي المسطح",
                description="Loss of natural thoracic curve, making the upper back appear flat.",
                body_region=BodyRegion.UPPER_BACK,
                severity=PostureSeverity.MINOR,
                detected_in_poses=[PoseType.SIDE_VIEW_LEFT, PoseType.SIDE_VIEW_RIGHT],
                visual_indicators=[
                    "Upper back appears very straight",
                    "Reduced natural curve",
                    "Stiff appearance when moving"
                ],
                potential_causes=[
                    "Over-correction of posture",
                    "Military posture habits",
                    "Hypermobility"
                ],
                potential_consequences=[
                    "Reduced shock absorption",
                    "Stiffness",
                    "Compensatory issues in other areas"
                ],
                recommended_fixes=[
                    self._fixes["Cat-Cow Stretch"],
                    self._fixes["Thoracic Foam Roll Extension"],
                    self._fixes["Thread the Needle"]
                ],
                priority=5
            ),

            # LOWER BACK ISSUES
            PostureIssue(
                id="anterior_pelvic_tilt",
                name="Anterior Pelvic Tilt",
                name_ar="ميلان الحوض الأمامي",
                description="Pelvis tilts forward, causing the stomach to protrude and lower back to over-arch.",
                body_region=BodyRegion.PELVIS,
                severity=PostureSeverity.MODERATE,
                detected_in_poses=[PoseType.SIDE_VIEW_LEFT, PoseType.SIDE_VIEW_RIGHT],
                visual_indicators=[
                    "Lower belly appears to stick out",
                    "Excessive arch in lower back",
                    "Belt line tilts down in front",
                    "Buttocks appear to stick out"
                ],
                potential_causes=[
                    "Tight hip flexors",
                    "Weak abdominals",
                    "Weak glutes",
                    "Prolonged sitting"
                ],
                potential_consequences=[
                    "Lower back pain",
                    "Hip pain",
                    "SI joint dysfunction",
                    "Hamstring strain"
                ],
                recommended_fixes=[
                    self._fixes["Hip Flexor Stretch (Kneeling)"],
                    self._fixes["Glute Bridge"],
                    self._fixes["Dead Bug"],
                    self._fixes["Plank"]
                ],
                priority=2
            ),
            PostureIssue(
                id="posterior_pelvic_tilt",
                name="Posterior Pelvic Tilt",
                name_ar="ميلان الحوض الخلفي",
                description="Pelvis tilts backward, causing flat back and tucked tailbone.",
                body_region=BodyRegion.PELVIS,
                severity=PostureSeverity.MODERATE,
                detected_in_poses=[PoseType.SIDE_VIEW_LEFT, PoseType.SIDE_VIEW_RIGHT],
                visual_indicators=[
                    "Flat lower back, reduced natural curve",
                    "Tailbone appears tucked under",
                    "Belt line tilts up in front",
                    "Buttocks appear flat"
                ],
                potential_causes=[
                    "Tight hamstrings",
                    "Tight glutes",
                    "Weak hip flexors",
                    "Prolonged sitting (slumped)"
                ],
                potential_consequences=[
                    "Lower back pain",
                    "Reduced shock absorption",
                    "Hip mobility issues"
                ],
                recommended_fixes=[
                    self._fixes["Cat-Cow Stretch"],
                    self._fixes["Hip Flexor Stretch (Kneeling)"],
                    self._fixes["Bird Dog"]
                ],
                priority=3
            ),
            PostureIssue(
                id="hyperlordosis",
                name="Hyperlordosis (Excessive Lower Back Arch)",
                name_ar="التقوس القطني المفرط",
                description="Excessive inward curve of the lower back.",
                body_region=BodyRegion.LOWER_BACK,
                severity=PostureSeverity.SEVERE,
                detected_in_poses=[PoseType.SIDE_VIEW_LEFT, PoseType.SIDE_VIEW_RIGHT],
                visual_indicators=[
                    "Very pronounced arch in lower back",
                    "Stomach protrudes forward",
                    "Upper body leans backward",
                    "Significant gap between lower back and wall when standing against it"
                ],
                potential_causes=[
                    "Tight hip flexors",
                    "Weak core muscles",
                    "Pregnancy or weight gain",
                    "Wearing high heels frequently"
                ],
                potential_consequences=[
                    "Chronic lower back pain",
                    "Spinal compression",
                    "Muscle spasms",
                    "Disc problems"
                ],
                recommended_fixes=[
                    self._fixes["Hip Flexor Stretch (Kneeling)"],
                    self._fixes["Dead Bug"],
                    self._fixes["Plank"],
                    self._fixes["Glute Bridge"],
                    self._fixes["Psoas Release"]
                ],
                priority=1
            ),

            # HIP ISSUES
            PostureIssue(
                id="hip_shift",
                name="Lateral Hip Shift",
                name_ar="انزياح الورك الجانبي",
                description="Hips shift to one side, creating an uneven stance.",
                body_region=BodyRegion.HIPS,
                severity=PostureSeverity.MODERATE,
                detected_in_poses=[PoseType.FRONT_VIEW, PoseType.BACK_VIEW],
                visual_indicators=[
                    "Hips appear shifted to one side",
                    "One hip higher than the other",
                    "Waist appears more curved on one side"
                ],
                potential_causes=[
                    "Muscle imbalance",
                    "Favoring one leg",
                    "SI joint dysfunction",
                    "Leg length difference"
                ],
                potential_consequences=[
                    "Lower back pain",
                    "Hip pain",
                    "Knee problems",
                    "Uneven gait"
                ],
                recommended_fixes=[
                    self._fixes["90/90 Hip Stretch"],
                    self._fixes["Clamshells"],
                    self._fixes["Glute Bridge"]
                ],
                priority=3
            ),
            PostureIssue(
                id="hip_rotation",
                name="Hip Rotation Imbalance",
                name_ar="عدم توازن دوران الورك",
                description="One or both hips have limited rotation, affecting movement patterns.",
                body_region=BodyRegion.HIPS,
                severity=PostureSeverity.MODERATE,
                detected_in_poses=[PoseType.OVERHEAD_SQUAT, PoseType.SINGLE_LEG_SQUAT_LEFT, PoseType.SINGLE_LEG_SQUAT_RIGHT],
                visual_indicators=[
                    "Knee caves in during squat",
                    "Foot turns out excessively",
                    "Asymmetric squat depth",
                    "Hip hiking during single leg movements"
                ],
                potential_causes=[
                    "Tight hip rotators",
                    "Weak glute medius",
                    "Capsular restrictions",
                    "Previous injury"
                ],
                potential_consequences=[
                    "Knee pain",
                    "Hip impingement",
                    "Lower back compensation",
                    "Groin strain"
                ],
                recommended_fixes=[
                    self._fixes["90/90 Hip Stretch"],
                    self._fixes["Pigeon Stretch"],
                    self._fixes["Clamshells"]
                ],
                priority=2
            ),

            # KNEE ISSUES
            PostureIssue(
                id="knee_valgus",
                name="Knee Valgus (Knock Knees)",
                name_ar="تقوس الركبة للداخل",
                description="Knees collapse inward, especially during movement like squatting.",
                body_region=BodyRegion.KNEES,
                severity=PostureSeverity.MODERATE,
                detected_in_poses=[PoseType.FRONT_VIEW, PoseType.OVERHEAD_SQUAT, PoseType.SINGLE_LEG_SQUAT_LEFT, PoseType.SINGLE_LEG_SQUAT_RIGHT],
                visual_indicators=[
                    "Knees point inward during standing or squatting",
                    "Knees touch while feet are apart",
                    "Knees cave in during descent in squat"
                ],
                potential_causes=[
                    "Weak hip abductors (glute medius)",
                    "Tight adductors",
                    "Poor ankle mobility",
                    "Weak VMO"
                ],
                potential_consequences=[
                    "ACL injury risk",
                    "Knee pain",
                    "IT band syndrome",
                    "Patellofemoral pain"
                ],
                recommended_fixes=[
                    self._fixes["Clamshells"],
                    self._fixes["VMO Strengthening (Terminal Knee Extension)"],
                    self._fixes["Ankle Mobility (Knee to Wall)"],
                    self._fixes["Glute Bridge"]
                ],
                priority=2
            ),
            PostureIssue(
                id="knee_varus",
                name="Knee Varus (Bow Legs)",
                name_ar="تقوس الركبة للخارج",
                description="Knees bow outward while feet are together.",
                body_region=BodyRegion.KNEES,
                severity=PostureSeverity.MINOR,
                detected_in_poses=[PoseType.FRONT_VIEW],
                visual_indicators=[
                    "Knees point outward with feet together",
                    "Visible gap between knees when standing",
                    "O-shaped appearance of legs"
                ],
                potential_causes=[
                    "Tight IT band",
                    "Tight lateral hip structures",
                    "Bone structure",
                    "Muscle imbalance"
                ],
                potential_consequences=[
                    "Lateral knee stress",
                    "Hip and ankle compensation",
                    "Arthritis risk"
                ],
                recommended_fixes=[
                    self._fixes["IT Band Foam Rolling"],
                    self._fixes["Pigeon Stretch"],
                    self._fixes["Wall Sit"]
                ],
                priority=4
            ),
            PostureIssue(
                id="hyperextended_knees",
                name="Hyperextended Knees",
                name_ar="فرط تمدد الركبتين",
                description="Knees lock backward past straight, creating a curved appearance.",
                body_region=BodyRegion.KNEES,
                severity=PostureSeverity.MODERATE,
                detected_in_poses=[PoseType.SIDE_VIEW_LEFT, PoseType.SIDE_VIEW_RIGHT],
                visual_indicators=[
                    "Knees appear to bend backward when standing",
                    "Legs form a backward C-curve",
                    "Knee joint appears pushed back"
                ],
                potential_causes=[
                    "Hypermobility",
                    "Weak quadriceps",
                    "Poor proprioception",
                    "Habit"
                ],
                potential_consequences=[
                    "Knee joint stress",
                    "Ligament laxity",
                    "Balance issues",
                    "Pain behind knee"
                ],
                recommended_fixes=[
                    self._fixes["Wall Sit"],
                    self._fixes["VMO Strengthening (Terminal Knee Extension)"],
                    self._fixes["Glute Bridge"]
                ],
                priority=3
            ),

            # ANKLE AND FOOT ISSUES
            PostureIssue(
                id="ankle_dorsiflexion_deficit",
                name="Limited Ankle Dorsiflexion",
                name_ar="محدودية ثني الكاحل",
                description="Reduced ability to bring the foot toward the shin, affecting squat depth and gait.",
                body_region=BodyRegion.ANKLES,
                severity=PostureSeverity.MODERATE,
                detected_in_poses=[PoseType.OVERHEAD_SQUAT, PoseType.INLINE_LUNGE_LEFT, PoseType.INLINE_LUNGE_RIGHT],
                visual_indicators=[
                    "Heels lift during deep squat",
                    "Limited forward knee travel",
                    "Compensatory forward lean during squat",
                    "Short stride length when walking"
                ],
                potential_causes=[
                    "Tight calf muscles (gastrocnemius, soleus)",
                    "Ankle joint restriction",
                    "Previous ankle injury",
                    "Wearing high heels frequently"
                ],
                potential_consequences=[
                    "Squat compensations",
                    "Knee pain",
                    "Achilles issues",
                    "Plantar fasciitis"
                ],
                recommended_fixes=[
                    self._fixes["Ankle Mobility (Knee to Wall)"],
                    self._fixes["Calf Stretch (Wall)"]
                ],
                priority=2
            ),
            PostureIssue(
                id="overpronation",
                name="Foot Overpronation (Flat Feet)",
                name_ar="الكب المفرط للقدم",
                description="Feet roll inward excessively, collapsing the arch.",
                body_region=BodyRegion.FEET,
                severity=PostureSeverity.MODERATE,
                detected_in_poses=[PoseType.FRONT_VIEW, PoseType.BACK_VIEW, PoseType.OVERHEAD_SQUAT],
                visual_indicators=[
                    "Arches appear flattened or collapsed",
                    "Ankles roll inward",
                    "Inner ankle bone more prominent",
                    "Shoe wear on inner edge"
                ],
                potential_causes=[
                    "Weak arch muscles",
                    "Tight calves",
                    "Hip weakness",
                    "Genetics"
                ],
                potential_consequences=[
                    "Plantar fasciitis",
                    "Shin splints",
                    "Knee valgus",
                    "Bunions"
                ],
                recommended_fixes=[
                    self._fixes["Short Foot Exercise"],
                    self._fixes["Toe Yoga"],
                    self._fixes["Calf Stretch (Wall)"]
                ],
                priority=2
            ),
            PostureIssue(
                id="supination",
                name="Foot Supination (High Arches)",
                name_ar="الاستلقاء المفرط للقدم",
                description="Feet roll outward with excessively high arches.",
                body_region=BodyRegion.FEET,
                severity=PostureSeverity.MINOR,
                detected_in_poses=[PoseType.FRONT_VIEW, PoseType.BACK_VIEW],
                visual_indicators=[
                    "Very high arches visible",
                    "Weight on outer edge of feet",
                    "Ankles roll outward slightly",
                    "Shoe wear on outer edge"
                ],
                potential_causes=[
                    "Tight calf muscles",
                    "Weak peroneals",
                    "Genetics",
                    "Neurological conditions"
                ],
                potential_consequences=[
                    "Ankle sprains",
                    "Stress fractures",
                    "IT band issues",
                    "Plantar fasciitis"
                ],
                recommended_fixes=[
                    self._fixes["Calf Stretch (Wall)"],
                    self._fixes["Ankle Mobility (Knee to Wall)"]
                ],
                priority=4
            ),

            # OVERHEAD SQUAT SPECIFIC ISSUES
            PostureIssue(
                id="arms_fall_forward",
                name="Arms Fall Forward in Overhead Position",
                name_ar="سقوط الذراعين للأمام",
                description="Unable to keep arms directly overhead during squat, arms fall forward.",
                body_region=BodyRegion.SHOULDERS,
                severity=PostureSeverity.MODERATE,
                detected_in_poses=[PoseType.OVERHEAD_SQUAT],
                visual_indicators=[
                    "Arms drift forward of the ears during descent",
                    "Unable to maintain vertical arm position",
                    "Compensatory forward lean of torso"
                ],
                potential_causes=[
                    "Tight latissimus dorsi",
                    "Tight pectorals",
                    "Limited thoracic extension",
                    "Limited shoulder flexion"
                ],
                potential_consequences=[
                    "Shoulder impingement",
                    "Lower back compensation",
                    "Limited overhead strength"
                ],
                recommended_fixes=[
                    self._fixes["Wall Angels"],
                    self._fixes["Thoracic Foam Roll Extension"],
                    self._fixes["Doorway Pec Stretch"],
                    self._fixes["Thread the Needle"]
                ],
                priority=2
            ),
            PostureIssue(
                id="excessive_forward_lean",
                name="Excessive Forward Lean",
                name_ar="الميل الأمامي المفرط",
                description="Torso leans too far forward during squat movements.",
                body_region=BodyRegion.FULL_BODY,
                severity=PostureSeverity.MODERATE,
                detected_in_poses=[PoseType.OVERHEAD_SQUAT],
                visual_indicators=[
                    "Chest falls toward thighs",
                    "Back angle becomes very horizontal",
                    "Weight shifts to toes",
                    "Heels may lift"
                ],
                potential_causes=[
                    "Limited ankle dorsiflexion",
                    "Tight hip flexors",
                    "Weak core",
                    "Limited hip mobility"
                ],
                potential_consequences=[
                    "Lower back strain",
                    "Loss of balance",
                    "Reduced power output"
                ],
                recommended_fixes=[
                    self._fixes["Ankle Mobility (Knee to Wall)"],
                    self._fixes["Hip Flexor Stretch (Kneeling)"],
                    self._fixes["Plank"],
                    self._fixes["Cat-Cow Stretch"]
                ],
                priority=2
            ),
            PostureIssue(
                id="squat_asymmetry",
                name="Squat Asymmetry",
                name_ar="عدم تناسق القرفصاء",
                description="Uneven weight distribution or movement pattern during squat.",
                body_region=BodyRegion.FULL_BODY,
                severity=PostureSeverity.MODERATE,
                detected_in_poses=[PoseType.OVERHEAD_SQUAT, PoseType.FRONT_VIEW],
                visual_indicators=[
                    "Shift to one side during descent",
                    "One hip drops lower than the other",
                    "Rotation of torso during squat",
                    "Uneven depth on each side"
                ],
                potential_causes=[
                    "Hip mobility difference side-to-side",
                    "Previous injury",
                    "Leg length discrepancy",
                    "Muscle imbalance"
                ],
                potential_consequences=[
                    "Overuse injury on dominant side",
                    "Joint wear",
                    "Performance limitation"
                ],
                recommended_fixes=[
                    self._fixes["90/90 Hip Stretch"],
                    self._fixes["Pigeon Stretch"],
                    self._fixes["Clamshells"],
                    self._fixes["Glute Bridge"]
                ],
                priority=3
            ),

            # SPINAL ISSUES
            PostureIssue(
                id="scoliosis_pattern",
                name="Scoliosis Pattern (Lateral Spinal Curve)",
                name_ar="نمط الجنف",
                description="Visible lateral curvature of the spine.",
                body_region=BodyRegion.SPINE,
                severity=PostureSeverity.SEVERE,
                detected_in_poses=[PoseType.BACK_VIEW, PoseType.FORWARD_BEND],
                visual_indicators=[
                    "Spine curves to the side when viewed from behind",
                    "Uneven shoulder heights",
                    "Uneven waist crease",
                    "One shoulder blade more prominent"
                ],
                potential_causes=[
                    "Congenital",
                    "Neuromuscular conditions",
                    "Muscle imbalance",
                    "Unknown (idiopathic)"
                ],
                potential_consequences=[
                    "Back pain",
                    "Breathing issues if severe",
                    "Cosmetic concerns",
                    "Progressive curvature"
                ],
                recommended_fixes=[
                    self._fixes["Cat-Cow Stretch"],
                    self._fixes["Plank"],
                    self._fixes["Bird Dog"],
                    self._fixes["Breathing Exercises (Diaphragmatic)"]
                ],
                priority=1,
                notes="Recommend professional evaluation if significant curvature is observed."
            ),

            # CORE ISSUES
            PostureIssue(
                id="weak_core",
                name="Core Instability",
                name_ar="عدم استقرار الجذع",
                description="Inability to maintain stable core during movement, leading to compensations.",
                body_region=BodyRegion.CORE,
                severity=PostureSeverity.MODERATE,
                detected_in_poses=[PoseType.OVERHEAD_SQUAT, PoseType.SINGLE_LEG_SQUAT_LEFT, PoseType.SINGLE_LEG_SQUAT_RIGHT],
                visual_indicators=[
                    "Excessive arching of lower back during movements",
                    "Ribcage flaring forward",
                    "Inability to maintain neutral spine",
                    "Torso wobbling during single leg stance"
                ],
                potential_causes=[
                    "Weak transverse abdominis",
                    "Weak obliques",
                    "Poor breathing patterns",
                    "Sedentary lifestyle"
                ],
                potential_consequences=[
                    "Lower back pain",
                    "Poor athletic performance",
                    "Injury susceptibility",
                    "Energy leakage during movements"
                ],
                recommended_fixes=[
                    self._fixes["Dead Bug"],
                    self._fixes["Plank"],
                    self._fixes["Bird Dog"],
                    self._fixes["Breathing Exercises (Diaphragmatic)"]
                ],
                priority=2
            ),
        ]

        for issue in issues:
            self._issues[issue.id] = issue

    def get_all_issues(self) -> List[PostureIssue]:
        """Get all posture issues"""
        return list(self._issues.values())

    def get_issue_by_id(self, issue_id: str) -> Optional[PostureIssue]:
        """Get a specific issue by ID"""
        return self._issues.get(issue_id)

    def get_issues_by_pose(self, pose_type: PoseType) -> List[PostureIssue]:
        """Get all issues detectable in a specific pose"""
        return [
            issue for issue in self._issues.values()
            if pose_type in issue.detected_in_poses
        ]

    def get_issues_by_region(self, region: BodyRegion) -> List[PostureIssue]:
        """Get all issues for a specific body region"""
        return [
            issue for issue in self._issues.values()
            if issue.body_region == region
        ]

    def get_issues_by_severity(self, severity: PostureSeverity) -> List[PostureIssue]:
        """Get all issues of a specific severity"""
        return [
            issue for issue in self._issues.values()
            if issue.severity == severity
        ]

    def get_all_fixes(self) -> List[PostureFix]:
        """Get all corrective exercises"""
        return list(self._fixes.values())

    def get_fix_by_name(self, name: str) -> Optional[PostureFix]:
        """Get a specific fix by name"""
        return self._fixes.get(name)

    def get_fixes_by_category(self, category: str) -> List[PostureFix]:
        """Get fixes by category (stretch, strengthen, mobilize, release)"""
        return [
            fix for fix in self._fixes.values()
            if fix.category == category
        ]

    def search_issues(self, query: str) -> List[PostureIssue]:
        """Search issues by name or description"""
        query_lower = query.lower()
        return [
            issue for issue in self._issues.values()
            if query_lower in issue.name.lower() or query_lower in issue.description.lower()
        ]
