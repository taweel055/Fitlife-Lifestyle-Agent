#!/usr/bin/env python3
"""
Fitlife Lifestyle Agent - Comprehensive Web UI
Streamlit-based user interface for meal plan generation
"""

import sys
import os
from datetime import datetime
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.models import Client, Protocol, WeightUnit, Language, DayType
from src.generators import MealPlanGenerator
from src.database import SupplementDatabase, FoodDatabase
from src.exporters import MarkdownExporter
from src.calculators import LBMCalculator, MacroCalculator

# Page configuration
st.set_page_config(
    page_title="Fitlife Lifestyle Agent",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.8rem;
        font-weight: bold;
        background: linear-gradient(90deg, #1f77b4, #ff7f0e);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.8rem;
        font-weight: 600;
        color: #333;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
        border-bottom: 3px solid #1f77b4;
        padding-bottom: 0.5rem;
    }
    .info-box {
        background: linear-gradient(135deg, #f0f2f6 0%, #e9ecef 100%);
        padding: 1.5rem;
        border-radius: 0.75rem;
        border-left: 5px solid #1f77b4;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .success-box {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        padding: 1.5rem;
        border-radius: 0.75rem;
        border-left: 5px solid #28a745;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .metric-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        padding: 1.5rem;
        border-radius: 0.75rem;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        border: 1px solid #e9ecef;
    }
    .meal-card {
        background: #ffffff;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ff7f0e;
        margin: 0.5rem 0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .protocol-card {
        background: linear-gradient(135deg, #fff 0%, #f8f9fa 100%);
        padding: 1.5rem;
        border-radius: 0.75rem;
        border: 2px solid #e9ecef;
        margin: 1rem 0;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 10px 20px;
        border-radius: 8px 8px 0 0;
    }
    </style>
""", unsafe_allow_html=True)


def main():
    """Main application"""
    
    # Header
    st.markdown('<div class="main-header">💪 Fitlife Lifestyle Agent</div>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #666; font-size: 1.2rem; margin-bottom: 2rem;">Professional Meal Plan Generation System</p>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("📋 Navigation")
        page = st.radio(
            "Select Page",
            ["🏠 Home", "💬 Chat Input", "👤 Generate Meal Plan", "📊 View Results", "🍽️ Food Database", "ℹ️ About"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # Quick info
        if 'client' in st.session_state:
            st.success("✅ Meal plan generated!")
            st.caption(f"Client: {st.session_state['client'].name}")
            st.caption(f"Protocol: {st.session_state['client'].protocol.value}")
    
    if page == "🏠 Home":
        show_home()
    elif page == "💬 Chat Input":
        show_chat_input()
    elif page == "👤 Generate Meal Plan":
        show_meal_plan_generator()
    elif page == "📊 View Results":
        show_results()
    elif page == "🍽️ Food Database":
        show_food_database()
    elif page == "ℹ️ About":
        show_about()


def show_chat_input():
    """Chat-based member data input interface"""
    st.markdown('<div class="sub-header">💬 Chat-Based Member Input</div>', unsafe_allow_html=True)
    
    # Initialize chat state
    if 'chat_messages' not in st.session_state:
        st.session_state.chat_messages = []
        # Add welcome message
        st.session_state.chat_messages.append({
            "role": "assistant",
            "content": "👋 Hello! I'm here to help you create a personalized meal plan. Let's start by collecting some information about your client.\n\n**What's the client's name?**"
        })
    
    if 'chat_client_data' not in st.session_state:
        st.session_state.chat_client_data = {
            'name': None,
            'weight': None,
            'weight_unit': WeightUnit.LBS,
            'body_fat_percentage': None,
            'height': None,
            'protocol': None,
            'training_days': [],
            'high_days': [],
            'language': Language.ENGLISH,
            'week_number': 1
        }
    
    if 'chat_step' not in st.session_state:
        st.session_state.chat_step = 'name'
    
    # Display chat messages
    for message in st.session_state.chat_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Type your response here..."):
        # Add user message
        st.session_state.chat_messages.append({"role": "user", "content": prompt})
        
        # Process the input based on current step
        response = process_chat_input(prompt, st.session_state.chat_step, st.session_state.chat_client_data)
        
        # Add assistant response
        st.session_state.chat_messages.append({"role": "assistant", "content": response})
        
        # Rerun to show new messages
        st.rerun()
    
    # Show current progress
    st.markdown("---")
    with st.expander("📋 Current Progress", expanded=False):
        progress_data = []
        if st.session_state.chat_client_data['name']:
            progress_data.append(("✅ Name", st.session_state.chat_client_data['name']))
        else:
            progress_data.append(("⏳ Name", "Not provided"))
        
        if st.session_state.chat_client_data['weight']:
            progress_data.append(("✅ Weight", f"{st.session_state.chat_client_data['weight']} {st.session_state.chat_client_data['weight_unit'].value}"))
        else:
            progress_data.append(("⏳ Weight", "Not provided"))
        
        if st.session_state.chat_client_data['body_fat_percentage']:
            progress_data.append(("✅ Body Fat %", f"{st.session_state.chat_client_data['body_fat_percentage']}%"))
        else:
            progress_data.append(("⏳ Body Fat %", "Not provided"))
        
        if st.session_state.chat_client_data['height']:
            progress_data.append(("✅ Height", f"{st.session_state.chat_client_data['height']} inches"))
        else:
            progress_data.append(("⏳ Height", "Optional (required for MASSIVE)"))
        
        if st.session_state.chat_client_data['protocol']:
            progress_data.append(("✅ Protocol", st.session_state.chat_client_data['protocol'].value))
        else:
            progress_data.append(("⏳ Protocol", "Not selected"))
        
        if st.session_state.chat_client_data['training_days']:
            progress_data.append(("✅ Training Days", ", ".join(st.session_state.chat_client_data['training_days'])))
        else:
            progress_data.append(("⏳ Training Days", "Not selected"))
        
        if st.session_state.chat_client_data['high_days']:
            progress_data.append(("✅ HIGH Days", ", ".join(st.session_state.chat_client_data['high_days'])))
        else:
            progress_data.append(("⏳ HIGH Days", "Not selected"))
        
        df_progress = pd.DataFrame(progress_data, columns=["Field", "Value"])
        st.dataframe(df_progress, use_container_width=True, hide_index=True)
        
        # Generate button (when all required fields are filled)
        if (st.session_state.chat_client_data['name'] and 
            st.session_state.chat_client_data['weight'] and 
            st.session_state.chat_client_data['body_fat_percentage'] and
            st.session_state.chat_client_data['protocol'] and
            st.session_state.chat_client_data['training_days'] and
            st.session_state.chat_client_data['high_days']):
            
            # Check protocol-specific requirements
            can_generate = True
            if st.session_state.chat_client_data['protocol'] == Protocol.MASSIVE:
                if not st.session_state.chat_client_data['height']:
                    can_generate = False
            
            if can_generate:
                st.markdown("---")
                if st.button("🚀 Generate Meal Plan", type="primary", use_container_width=True):
                    generate_from_chat_data(st.session_state.chat_client_data)
                    st.success("✅ Meal plan generated! Navigate to 'View Results' to see it.")
                    st.rerun()
    
    # Reset button
    if st.button("🔄 Start Over", use_container_width=True):
        st.session_state.chat_messages = []
        st.session_state.chat_client_data = {
            'name': None,
            'weight': None,
            'weight_unit': WeightUnit.LBS,
            'body_fat_percentage': None,
            'height': None,
            'protocol': None,
            'training_days': [],
            'high_days': [],
            'language': Language.ENGLISH,
            'week_number': 1
        }
        st.session_state.chat_step = 'name'
        st.session_state.chat_messages.append({
            "role": "assistant",
            "content": "👋 Hello! I'm here to help you create a personalized meal plan. Let's start by collecting some information about your client.\n\n**What's the client's name?**"
        })
        st.rerun()


def process_chat_input(prompt: str, current_step: str, client_data: dict) -> str:
    """Process user input and return appropriate response"""
    prompt_lower = prompt.lower().strip()
    
    if current_step == 'name':
        # Extract name
        name = prompt.strip()
        if len(name) > 0:
            client_data['name'] = name
            st.session_state.chat_step = 'weight'
            return f"Great! Nice to meet you, {name}. 👋\n\n**What's {name}'s current body weight?** (Please provide the number, e.g., 180)"
        else:
            return "Please provide a valid name."
    
    elif current_step == 'weight':
        # Try to extract weight and unit
        weight_str = prompt_lower.replace('lbs', '').replace('lb', '').replace('kg', '').replace('kilograms', '').replace('pounds', '').strip()
        
        # Check for unit in input
        if 'kg' in prompt_lower or 'kilogram' in prompt_lower:
            client_data['weight_unit'] = WeightUnit.KG
        else:
            client_data['weight_unit'] = WeightUnit.LBS
        
        try:
            # Extract number
            import re
            numbers = re.findall(r'\d+\.?\d*', prompt)
            if numbers:
                weight = float(numbers[0])
                if weight > 0:
                    client_data['weight'] = weight
                    st.session_state.chat_step = 'body_fat'
                    unit_text = "kg" if client_data['weight_unit'] == WeightUnit.KG else "lbs"
                    return f"Got it! {client_data['name']} weighs {weight} {unit_text}.\n\n**What's {client_data['name']}'s body fat percentage?** (Please provide a number between 5-50, e.g., 15)"
                else:
                    return "Please provide a valid weight greater than 0."
            else:
                return "I couldn't find a weight number. Please provide the weight as a number (e.g., 180 or 180 lbs)."
        except:
            return "I couldn't understand the weight. Please provide it as a number (e.g., 180 or 180 lbs)."
    
    elif current_step == 'body_fat':
        try:
            import re
            numbers = re.findall(r'\d+\.?\d*', prompt)
            if numbers:
                body_fat = float(numbers[0])
                if 5 <= body_fat <= 50:
                    client_data['body_fat_percentage'] = body_fat
                    st.session_state.chat_step = 'protocol'
                    
                    # Calculate LBM preview
                    try:
                        temp_client = Client(
                            name=client_data['name'],
                            weight=client_data['weight'],
                            weight_unit=client_data['weight_unit'],
                            body_fat_percentage=body_fat,
                            protocol=Protocol.SHREDDED,
                            training_days=[],
                            high_days=[]
                        )
                        lbm = LBMCalculator.calculate_lbm(temp_client)
                        protein_per_meal = LBMCalculator.calculate_protein_per_meal(lbm)
                        lbm_preview = f"\n\n📊 **Preview:** LBM = {lbm:.1f} lbs | Protein per meal = {protein_per_meal}g"
                    except:
                        lbm_preview = ""
                    
                    return f"Perfect! Body fat percentage is {body_fat}%.{lbm_preview}\n\n**Which protocol would you like to use?**\n\n• Type **SHREDDED** for fat loss\n• Type **MASSIVE** for muscle gain"
                else:
                    return "Body fat percentage should be between 5% and 50%. Please provide a valid number."
            else:
                return "I couldn't find a body fat percentage. Please provide a number between 5-50 (e.g., 15)."
        except:
            return "I couldn't understand the body fat percentage. Please provide a number between 5-50."
    
    elif current_step == 'protocol':
        if 'shredded' in prompt_lower or 'fat loss' in prompt_lower or 'cutting' in prompt_lower:
            client_data['protocol'] = Protocol.SHREDDED
            st.session_state.chat_step = 'height'
            return f"Excellent! We'll use the **SHREDDED** protocol for fat loss. 🔥\n\n**What's {client_data['name']}'s height in inches?** (This is optional for SHREDDED, but you can skip by typing 'skip')"
        elif 'massive' in prompt_lower or 'muscle gain' in prompt_lower or 'bulking' in prompt_lower:
            client_data['protocol'] = Protocol.MASSIVE
            st.session_state.chat_step = 'height'
            return f"Excellent! We'll use the **MASSIVE** protocol for muscle gain. 💪\n\n**What's {client_data['name']}'s height in inches?** (Required for MASSIVE protocol)"
        else:
            return "Please specify either **SHREDDED** (for fat loss) or **MASSIVE** (for muscle gain)."
    
    elif current_step == 'height':
        if 'skip' in prompt_lower and client_data['protocol'] == Protocol.SHREDDED:
            st.session_state.chat_step = 'training_days'
            return f"Height skipped (optional for SHREDDED).\n\n**Which days will {client_data['name']} be training?**\n\nPlease list the days separated by commas (e.g., Monday, Wednesday, Friday)\n\nAvailable days: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday"
        else:
            try:
                import re
                numbers = re.findall(r'\d+\.?\d*', prompt)
                if numbers:
                    height = float(numbers[0])
                    if height > 0:
                        client_data['height'] = height
                        st.session_state.chat_step = 'training_days'
                        return f"Height recorded: {height} inches.\n\n**Which days will {client_data['name']} be training?**\n\nPlease list the days separated by commas (e.g., Monday, Wednesday, Friday)\n\nAvailable days: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday"
                    else:
                        return "Please provide a valid height greater than 0."
                else:
                    if client_data['protocol'] == Protocol.SHREDDED:
                        return "I couldn't find a height number. You can type 'skip' to skip this, or provide a number."
                    else:
                        return "I couldn't find a height number. Please provide the height in inches (required for MASSIVE protocol)."
            except:
                if client_data['protocol'] == Protocol.SHREDDED:
                    return "I couldn't understand the height. You can type 'skip' to skip this, or provide a number."
                else:
                    return "I couldn't understand the height. Please provide it in inches (required for MASSIVE protocol)."
    
    elif current_step == 'training_days':
        valid_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        days_input = [d.strip() for d in prompt.split(',')]
        days_found = []
        
        for day_input in days_input:
            day_input_clean = day_input.strip().title()
            if day_input_clean in valid_days:
                days_found.append(day_input_clean)
        
        if days_found:
            client_data['training_days'] = days_found
            max_high_days = 1 if client_data['protocol'] == Protocol.SHREDDED else 2
            st.session_state.chat_step = 'high_days'
            return f"Great! Training days set: {', '.join(days_found)}.\n\n**Which days will be HIGH calorie days?**\n\nPlease list {max_high_days} day(s) separated by commas (e.g., Saturday)\n\nAvailable days: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday\n\n*Note: {client_data['protocol'].value} protocol allows {max_high_days} HIGH day(s) per week*"
        else:
            return "I couldn't recognize the days. Please list valid day names separated by commas (e.g., Monday, Wednesday, Friday).\n\nValid days: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday"
    
    elif current_step == 'high_days':
        valid_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        days_input = [d.strip() for d in prompt.split(',')]
        days_found = []
        
        for day_input in days_input:
            day_input_clean = day_input.strip().title()
            if day_input_clean in valid_days:
                days_found.append(day_input_clean)
        
        max_high_days = 1 if client_data['protocol'] == Protocol.SHREDDED else 2
        
        if days_found:
            if len(days_found) <= max_high_days:
                client_data['high_days'] = days_found
                st.session_state.chat_step = 'complete'
                
                # Summary
                summary = f"Perfect! HIGH days set: {', '.join(days_found)}.\n\n"
                summary += "✅ **All information collected!**\n\n"
                summary += "**Summary:**\n"
                summary += f"• Name: {client_data['name']}\n"
                summary += f"• Weight: {client_data['weight']} {client_data['weight_unit'].value}\n"
                summary += f"• Body Fat: {client_data['body_fat_percentage']}%\n"
                if client_data['height']:
                    summary += f"• Height: {client_data['height']} inches\n"
                summary += f"• Protocol: {client_data['protocol'].value}\n"
                summary += f"• Training Days: {', '.join(client_data['training_days'])}\n"
                summary += f"• HIGH Days: {', '.join(client_data['high_days'])}\n\n"
                summary += "**You can now generate the meal plan using the button in the progress section below!** 🚀"
                
                return summary
            else:
                return f"Too many HIGH days! {client_data['protocol'].value} protocol allows only {max_high_days} HIGH day(s). Please provide {max_high_days} day(s) or fewer."
        else:
            return f"I couldn't recognize the days. Please list {max_high_days} valid day name(s) separated by commas.\n\nValid days: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday"
    
    else:
        return "All information has been collected! Please use the 'Generate Meal Plan' button in the progress section to create the meal plan."


def generate_from_chat_data(client_data: dict):
    """Generate meal plan from chat-collected data"""
    try:
        # Create client object
        client = Client(
            name=client_data['name'],
            weight=client_data['weight'],
            weight_unit=client_data['weight_unit'],
            body_fat_percentage=client_data['body_fat_percentage'],
            height=client_data['height'] if client_data['protocol'] == Protocol.MASSIVE else None,
            protocol=client_data['protocol'],
            training_days=client_data['training_days'],
            high_days=client_data['high_days'],
            language=client_data['language']
        )
        
        # Generate meal plan
        generator = MealPlanGenerator()
        week_plan = generator.generate_week_plan(client, week_number=client_data['week_number'])
        
        # Get supplement recommendations
        supp_db = SupplementDatabase()
        supplement_stack = supp_db.get_recommended_stack(client.protocol)
        
        # Get protocol summary
        summary = generator.get_protocol_summary(client)
        
        # Export to markdown
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        week_md = MarkdownExporter.export_week_plan(week_plan, include_food_suggestions=True)
        week_filename = f"{client.name.replace(' ', '_')}_{client.protocol.value}_Week{client_data['week_number']}_{timestamp}.md"
        week_path = MarkdownExporter.save_to_file(week_md, week_filename)
        
        supp_md = MarkdownExporter.export_supplement_stack(supplement_stack)
        supp_filename = f"{client.name.replace(' ', '_')}_{client.protocol.value}_Supplements_{timestamp}.md"
        supp_path = MarkdownExporter.save_to_file(supp_md, supp_filename)
        
        summary_md = MarkdownExporter.export_protocol_summary(summary)
        summary_filename = f"{client.name.replace(' ', '_')}_{client.protocol.value}_Summary_{timestamp}.md"
        summary_path = MarkdownExporter.save_to_file(summary_md, summary_filename)
        
        # Store results in session state
        st.session_state['week_plan'] = week_plan
        st.session_state['supplement_stack'] = supplement_stack
        st.session_state['summary'] = summary
        st.session_state['client'] = client
        st.session_state['week_path'] = week_path
        st.session_state['supp_path'] = supp_path
        st.session_state['summary_path'] = summary_path
        st.session_state['week_md'] = week_md
        st.session_state['supp_md'] = supp_md
        st.session_state['summary_md'] = summary_md
        
        # Add success message to chat
        st.session_state.chat_messages.append({
            "role": "assistant",
            "content": f"🎉 **Meal plan generated successfully!**\n\n✅ Week Plan: {week_filename}\n✅ Supplements: {supp_filename}\n✅ Summary: {summary_filename}\n\nNavigate to 'View Results' to see the detailed meal plan!"
        })
        
    except Exception as e:
        st.session_state.chat_messages.append({
            "role": "assistant",
            "content": f"❌ Error generating meal plan: {str(e)}\n\nPlease check the information and try again."
        })


def show_home():
    """Home page with comprehensive overview"""
    st.markdown('<div class="sub-header">Welcome to Fitlife Lifestyle Agent</div>', unsafe_allow_html=True)
    
    # Feature cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>🎯 Protocols</h3>
            <p style="font-size: 0.9rem;">SHREDDED & MASSIVE</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>🍽️ Meal Plans</h3>
            <p style="font-size: 0.9rem;">7-day plans with timing</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>💊 Supplements</h3>
            <p style="font-size: 0.9rem;">Personalized stacks</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h3>📊 Analytics</h3>
            <p style="font-size: 0.9rem;">Macro tracking & charts</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Quick start guide
    st.markdown("""
    <div class="info-box">
        <h4>🚀 Quick Start Guide</h4>
        <ol style="line-height: 2;">
            <li>Navigate to <strong>Generate Meal Plan</strong> from the sidebar</li>
            <li>Fill in your client's information (name, weight, body fat %)</li>
            <li>Select the appropriate protocol (SHREDDED for fat loss, MASSIVE for muscle gain)</li>
            <li>Choose training days and HIGH calorie days</li>
            <li>Click <strong>Generate Meal Plan</strong> to create your personalized plan</li>
            <li>View detailed results and download markdown files</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
    
    # Protocol comparison
    st.markdown("### 📋 Protocol Comparison")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="protocol-card">
            <h4 style="color: #dc3545; margin-top: 0;">🔥 SHREDDED Protocol (Fat Loss)</h4>
            <p><strong>Goal:</strong> Maximize fat loss while preserving muscle</p>
            <hr>
            <p><strong>LOW Days</strong> (Non-training):</p>
            <ul>
                <li>300g Protein / 120g Carbs</li>
                <li>6 regular meals</li>
            </ul>
            <p><strong>MEDIUM Days</strong> (Training):</p>
            <ul>
                <li>250g Protein / 220g Carbs</li>
                <li>3 training meals + 4 regular meals</li>
            </ul>
            <p><strong>HIGH Days</strong> (Weekly refeed):</p>
            <ul>
                <li>190g Protein / 730g Carbs</li>
                <li>Includes sugary carb options</li>
                <li>1 HIGH day per week</li>
            </ul>
            <p><strong>Cardio:</strong> 30 min HIIT 5x/week OR 15,000 steps/day</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="protocol-card">
            <h4 style="color: #28a745; margin-top: 0;">💪 MASSIVE Protocol (Muscle Gain)</h4>
            <p><strong>Goal:</strong> Maximize muscle growth with strategic nutrition</p>
            <hr>
            <p><strong>LOW Days</strong> (Non-training):</p>
            <ul>
                <li>300g Protein / 240g Carbs</li>
                <li>6 regular meals</li>
            </ul>
            <p><strong>MEDIUM Days</strong> (Training):</p>
            <ul>
                <li>310g Protein / 450g Carbs</li>
                <li>3 training meals + 4 regular meals</li>
            </ul>
            <p><strong>HIGH Days</strong> (Weekly refeed):</p>
            <ul>
                <li>220g Protein / 730g Carbs</li>
                <li>Includes sugary carb options</li>
                <li>2 HIGH days per week</li>
            </ul>
            <p><strong>Cardio:</strong> 12 min HIIT 3x/week OR 12,000 steps/day</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Key features
    st.markdown("---")
    st.markdown("### ✨ Key Features")
    
    feature_cols = st.columns(3)
    
    with feature_cols[0]:
        st.markdown("""
        **📊 Advanced Calculations**
        - Automatic LBM calculation
        - Protein per meal optimization
        - Macro distribution by day type
        """)
    
    with feature_cols[1]:
        st.markdown("""
        **🍽️ Comprehensive Food Database**
        - 40+ food items with macros
        - Preferred vs sparingly categories
        - Arabic translations available
        """)
    
    with feature_cols[2]:
        st.markdown("""
        **💊 Smart Supplement Stacks**
        - Protocol-specific recommendations
        - Cost estimates included
        - Required vs optional supplements
        """)


def show_meal_plan_generator():
    """Comprehensive meal plan generator form"""
    st.markdown('<div class="sub-header">Generate Meal Plan</div>', unsafe_allow_html=True)
    
    # Use tabs for better organization
    tab1, tab2, tab3 = st.tabs(["📝 Client Information", "⚙️ Protocol Settings", "📋 Review & Generate"])
    
    with tab1:
        st.markdown("### Client Information")
        
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Client Name *", placeholder="e.g., Ahmed Hassan", key="name")
            weight = st.number_input("Body Weight *", min_value=0.1, value=180.0, step=0.1, key="weight")
            weight_unit = st.selectbox("Weight Unit", [WeightUnit.LBS, WeightUnit.KG], format_func=lambda x: x.value.upper(), key="weight_unit")
        
        with col2:
            body_fat = st.number_input("Body Fat Percentage *", min_value=5.0, max_value=50.0, value=15.0, step=0.1, key="body_fat")
            height = st.number_input("Height (inches)", min_value=0.1, value=72.0, step=0.1, help="Required for MASSIVE protocol", key="height")
        
        # Real-time LBM calculation preview
        if weight > 0 and body_fat > 0:
            try:
                temp_client = Client(
                    name=name or "Preview",
                    weight=weight,
                    weight_unit=weight_unit,
                    body_fat_percentage=body_fat,
                    protocol=Protocol.SHREDDED,  # Default for preview
                    training_days=[],
                    high_days=[]
                )
                lbm = LBMCalculator.calculate_lbm(temp_client)
                protein_per_meal = LBMCalculator.calculate_protein_per_meal(lbm)
                
                st.info(f"📊 **Preview:** LBM = {lbm:.1f} lbs | Protein per meal = {protein_per_meal}g")
            except:
                pass
    
    with tab2:
        st.markdown("### Protocol Selection")
        
        protocol = st.radio(
            "Select Protocol *",
            [Protocol.SHREDDED, Protocol.MASSIVE],
            format_func=lambda x: f"{x.value} - {'Fat Loss' if x == Protocol.SHREDDED else 'Muscle Gain'}",
            key="protocol",
            horizontal=True
        )
        
        # Show protocol details
        if protocol == Protocol.SHREDDED:
            specs = MacroCalculator.SHREDDED_SPECS
            st.info("🔥 **SHREDDED Protocol**: Optimized for fat loss while preserving muscle mass")
        else:
            specs = MacroCalculator.MASSIVE_SPECS
            st.info("💪 **MASSIVE Protocol**: Optimized for muscle growth and strength gains")
        
        # Show macro breakdown
        col1, col2, col3 = st.columns(3)
        
        with col1:
            low_macros = MacroCalculator.calculate_day_macros(protocol, DayType.LOW)
            st.metric("LOW Day", f"{low_macros.protein}p/{low_macros.carbs}c")
        
        with col2:
            medium_macros = MacroCalculator.calculate_day_macros(protocol, DayType.MEDIUM)
            st.metric("MEDIUM Day", f"{medium_macros.protein}p/{medium_macros.carbs}c")
        
        with col3:
            high_macros = MacroCalculator.calculate_day_macros(protocol, DayType.HIGH)
            st.metric("HIGH Day", f"{high_macros.protein}p/{high_macros.carbs}c")
        
        st.markdown("---")
        st.markdown("### Training Schedule")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Training Days**")
            training_days = st.multiselect(
                "Select training days",
                ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                default=["Monday", "Wednesday", "Friday"],
                help="Days when the client will train",
                key="training_days"
            )
        
        with col2:
            max_high_days = 1 if protocol == Protocol.SHREDDED else 2
            st.markdown(f"**HIGH Days** (max {max_high_days})")
            high_days = st.multiselect(
                "Select HIGH calorie days",
                ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                default=["Saturday"] if protocol == Protocol.SHREDDED else ["Saturday", "Sunday"],
                max_selections=max_high_days,
                help=f"High calorie refeed days ({max_high_days} allowed for {protocol.value})",
                key="high_days"
            )
        
        st.markdown("---")
        st.markdown("### Output Settings")
        
        col1, col2 = st.columns(2)
        
        with col1:
            language = st.selectbox(
                "Output Language",
                [Language.ENGLISH, Language.ARABIC],
                format_func=lambda x: "English" if x == Language.ENGLISH else "Arabic (العربية)",
                key="language"
            )
        
        with col2:
            week_number = st.number_input("Week Number", min_value=1, value=1, step=1, key="week_number")
    
    with tab3:
        st.markdown("### Review & Generate")
        
        # Validation summary
        validation_errors = []
        
        if not name:
            validation_errors.append("❌ Client name is required")
        if not training_days:
            validation_errors.append("❌ At least one training day must be selected")
        if not high_days:
            validation_errors.append("❌ At least one HIGH day must be selected")
        if len(high_days) > max_high_days:
            validation_errors.append(f"❌ {protocol.value} protocol allows only {max_high_days} HIGH day(s)")
        if protocol == Protocol.MASSIVE and not height:
            validation_errors.append("❌ Height is required for MASSIVE protocol")
        
        if validation_errors:
            st.error("**Please fix the following issues:**")
            for error in validation_errors:
                st.markdown(f"- {error}")
        else:
            st.success("✅ All fields are valid!")
            
            # Show summary
            st.markdown("#### 📋 Summary")
            summary_data = {
                "Field": ["Name", "Weight", "Body Fat %", "Height", "Protocol", "Training Days", "HIGH Days", "Language", "Week"],
                "Value": [
                    name or "N/A",
                    f"{weight} {weight_unit.value}",
                    f"{body_fat}%",
                    f"{height} inches" if height else "N/A",
                    protocol.value,
                    ", ".join(training_days) if training_days else "None",
                    ", ".join(high_days) if high_days else "None",
                    "English" if language == Language.ENGLISH else "Arabic",
                    str(week_number)
                ]
            }
            st.dataframe(pd.DataFrame(summary_data), use_container_width=True, hide_index=True)
        
        # Generate button
        if st.button("🚀 Generate Meal Plan", type="primary", use_container_width=True, disabled=len(validation_errors) > 0):
            generate_meal_plan(name, weight, weight_unit, body_fat, height, protocol, training_days, high_days, language, week_number)


def generate_meal_plan(name, weight, weight_unit, body_fat, height, protocol, training_days, high_days, language, week_number):
    """Generate meal plan and store in session state"""
    try:
        # Create client object
        client = Client(
            name=name,
            weight=weight,
            weight_unit=weight_unit,
            body_fat_percentage=body_fat,
            height=height if protocol == Protocol.MASSIVE else None,
            protocol=protocol,
            training_days=training_days,
            high_days=high_days,
            language=language
        )
        
        # Generate meal plan with progress
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        status_text.text("⏳ Initializing generator...")
        progress_bar.progress(10)
        generator = MealPlanGenerator()
        
        status_text.text("⏳ Generating meal plan...")
        progress_bar.progress(30)
        week_plan = generator.generate_week_plan(client, week_number=week_number)
        
        status_text.text("⏳ Getting supplement recommendations...")
        progress_bar.progress(60)
        supp_db = SupplementDatabase()
        supplement_stack = supp_db.get_recommended_stack(client.protocol)
        
        status_text.text("⏳ Generating protocol summary...")
        progress_bar.progress(80)
        summary = generator.get_protocol_summary(client)
        
        status_text.text("⏳ Exporting to markdown...")
        progress_bar.progress(90)
        
        # Export to markdown
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        week_md = MarkdownExporter.export_week_plan(week_plan, include_food_suggestions=True)
        week_filename = f"{client.name.replace(' ', '_')}_{client.protocol.value}_Week{week_number}_{timestamp}.md"
        week_path = MarkdownExporter.save_to_file(week_md, week_filename)
        
        supp_md = MarkdownExporter.export_supplement_stack(supplement_stack)
        supp_filename = f"{client.name.replace(' ', '_')}_{client.protocol.value}_Supplements_{timestamp}.md"
        supp_path = MarkdownExporter.save_to_file(supp_md, supp_filename)
        
        summary_md = MarkdownExporter.export_protocol_summary(summary)
        summary_filename = f"{client.name.replace(' ', '_')}_{client.protocol.value}_Summary_{timestamp}.md"
        summary_path = MarkdownExporter.save_to_file(summary_md, summary_filename)
        
        progress_bar.progress(100)
        status_text.text("✅ Complete!")
        
        # Store results in session state
        st.session_state['week_plan'] = week_plan
        st.session_state['supplement_stack'] = supplement_stack
        st.session_state['summary'] = summary
        st.session_state['client'] = client
        st.session_state['week_path'] = week_path
        st.session_state['supp_path'] = supp_path
        st.session_state['summary_path'] = summary_path
        st.session_state['week_md'] = week_md
        st.session_state['supp_md'] = supp_md
        st.session_state['summary_md'] = summary_md
        
        st.success("✅ Meal plan generated successfully!")
        st.balloons()
        
        # Auto-navigate to results
        st.info("👈 Navigate to 'View Results' to see your detailed meal plan!")
        
    except Exception as e:
        st.error(f"❌ Error generating meal plan: {str(e)}")
        st.exception(e)


def show_results():
    """Comprehensive results display"""
    st.markdown('<div class="sub-header">View Results</div>', unsafe_allow_html=True)
    
    if 'week_plan' not in st.session_state:
        st.info("👈 Please generate a meal plan first from the 'Generate Meal Plan' page")
        return
    
    client = st.session_state['client']
    week_plan = st.session_state['week_plan']
    supplement_stack = st.session_state['supplement_stack']
    summary = st.session_state['summary']
    
    # Client info header
    st.markdown("### 👤 Client Profile")
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Name", client.name)
    with col2:
        st.metric("Weight", f"{client.weight} {client.weight_unit.value}")
    with col3:
        st.metric("Body Fat", f"{client.body_fat_percentage}%")
    with col4:
        st.metric("LBM", f"{week_plan.lean_body_mass:.1f} lbs")
    with col5:
        st.metric("Protocol", client.protocol.value)
    
    st.markdown("---")
    
    # Week overview with charts
    st.markdown("### 📅 Week Overview")
    
    # Calculate weekly totals
    weekly_protein = sum(day.get_total_macros().protein for day in week_plan.days)
    weekly_carbs = sum(day.get_total_macros().carbs for day in week_plan.days)
    weekly_fat = sum(day.get_total_macros().fat for day in week_plan.days)
    weekly_calories = sum(day.get_total_calories() for day in week_plan.days)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Weekly Protein", f"{weekly_protein:.0f}g")
    with col2:
        st.metric("Weekly Carbs", f"{weekly_carbs:.0f}g")
    with col3:
        st.metric("Weekly Fat", f"{weekly_fat:.0f}g")
    with col4:
        st.metric("Weekly Calories", f"{weekly_calories:,} cal")
    
    # Macro distribution chart
    st.markdown("#### Macro Distribution by Day")
    
    days_data = []
    for day in week_plan.days:
        macros = day.get_total_macros()
        days_data.append({
            'Day': day.day_name,
            'Type': day.day_type.value,
            'Protein': macros.protein,
            'Carbs': macros.carbs,
            'Fat': macros.fat,
            'Calories': day.get_total_calories()
        })
    
    df_days = pd.DataFrame(days_data)
    
    # Create stacked bar chart
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=df_days['Day'],
        y=df_days['Protein'],
        name='Protein',
        marker_color='#1f77b4'
    ))
    fig.add_trace(go.Bar(
        x=df_days['Day'],
        y=df_days['Carbs'],
        name='Carbs',
        marker_color='#ff7f0e'
    ))
    fig.add_trace(go.Bar(
        x=df_days['Day'],
        y=df_days['Fat'],
        name='Fat',
        marker_color='#2ca02c'
    ))
    
    fig.update_layout(
        barmode='stack',
        title='Daily Macronutrient Distribution',
        xaxis_title='Day',
        yaxis_title='Grams',
        height=400,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Calories chart
    fig_cal = px.bar(
        df_days,
        x='Day',
        y='Calories',
        color='Type',
        title='Daily Calorie Intake',
        color_discrete_map={'LOW': '#dc3545', 'MEDIUM': '#ffc107', 'HIGH': '#28a745'}
    )
    fig_cal.update_layout(height=350)
    st.plotly_chart(fig_cal, use_container_width=True)
    
    st.markdown("---")
    
    # Detailed day-by-day breakdown
    st.markdown("### 📆 Daily Meal Plans")
    
    for day_plan in week_plan.days:
        day_type_color = {
            'LOW': '#dc3545',
            'MEDIUM': '#ffc107',
            'HIGH': '#28a745'
        }.get(day_plan.day_type.value, '#6c757d')
        
        with st.expander(f"📅 **{day_plan.day_name}** - {day_plan.day_type.value} DAY {'🏋️' if day_plan.is_training_day else ''}", expanded=False):
            total_macros = day_plan.get_total_macros()
            total_calories = day_plan.get_total_calories()
            
            # Day summary metrics
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                st.metric("Protein", f"{total_macros.protein}g")
            with col2:
                st.metric("Carbs", f"{total_macros.carbs}g")
            with col3:
                st.metric("Fat", f"{total_macros.fat}g")
            with col4:
                st.metric("Calories", f"{total_calories} cal")
            with col5:
                st.metric("Meals", len(day_plan.meals))
            
            if day_plan.is_training_day and day_plan.training_time:
                st.info(f"🏋️ Training scheduled for {day_plan.training_time}")
            
            st.markdown("---")
            st.markdown("#### Meals")
            
            # Display each meal with details
            for idx, meal in enumerate(day_plan.meals, 1):
                meal_macros = meal.get_total_macros()
                meal_cals = meal.get_total_calories()
                
                meal_type_badge = {
                    'REGULAR': '📝',
                    'PRE_WORKOUT': '⚡',
                    'INTRA_WORKOUT': '💧',
                    'POST_WORKOUT': '🔋'
                }.get(meal.meal_type.value, '📝')
                
                st.markdown(f"""
                <div class="meal-card">
                    <h5>{meal_type_badge} {meal.name} - {meal.meal_type.value.replace('_', ' ')} {f"({meal.time})" if meal.time else ""}</h5>
                    <p><strong>Macros:</strong> {meal_macros.protein}g Protein | {meal_macros.carbs}g Carbs | {meal_macros.fat}g Fat | <strong>{meal_cals} calories</strong></p>
                </div>
                """, unsafe_allow_html=True)
                
                # Food suggestions
                if meal.protein_sources or meal.carb_sources or meal.fat_sources or meal.vegetables:
                    suggestion_cols = st.columns(4)
                    
                    with suggestion_cols[0]:
                        if meal.protein_sources:
                            st.markdown(f"**Protein:**<br>{'<br>'.join(['• ' + f for f in meal.protein_sources])}", unsafe_allow_html=True)
                    
                    with suggestion_cols[1]:
                        if meal.carb_sources:
                            st.markdown(f"**Carbs:**<br>{'<br>'.join(['• ' + f for f in meal.carb_sources])}", unsafe_allow_html=True)
                    
                    with suggestion_cols[2]:
                        if meal.fat_sources:
                            st.markdown(f"**Fats:**<br>{'<br>'.join(['• ' + f for f in meal.fat_sources])}", unsafe_allow_html=True)
                    
                    with suggestion_cols[3]:
                        if meal.vegetables:
                            st.markdown(f"**Vegetables:**<br>{'<br>'.join(['• ' + f for f in meal.vegetables])}", unsafe_allow_html=True)
                
                if meal.notes:
                    st.info(f"💡 {meal.notes}")
                
                st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Supplements section
    st.markdown("### 💊 Supplement Recommendations")
    
    required = supplement_stack.get_required_supplements()
    optional = supplement_stack.get_optional_supplements()
    min_cost, max_cost = supplement_stack.calculate_total_cost()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Required Supplements", len(required))
    with col2:
        st.metric("Estimated Monthly Cost", f"${min_cost:.0f} - ${max_cost:.0f}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### ✅ Required Supplements")
        for supp in required:
            st.markdown(f"""
            **{supp.name}**
            - Dosage: {supp.dose}
            - Timing: {supp.timing.value}
            - Purpose: {supp.purpose.value}
            {f"- Cost: ${supp.estimated_cost_per_month:.0f}/month" if supp.estimated_cost_per_month else ""}
            {f"- Notes: {supp.notes}" if supp.notes else ""}
            """)
            st.markdown("---")
    
    with col2:
        st.markdown("#### 🔹 Optional Supplements")
        if optional:
            for supp in optional:
                st.markdown(f"""
                **{supp.name}**
                - Dosage: {supp.dose}
                - Timing: {supp.timing.value}
                - Purpose: {supp.purpose.value}
                {f"- Cost: ${supp.estimated_cost_per_month:.0f}/month" if supp.estimated_cost_per_month else ""}
                {f"- Notes: {supp.notes}" if supp.notes else ""}
                """)
                st.markdown("---")
        else:
            st.info("No optional supplements recommended for this protocol.")
    
    st.markdown("---")
    
    # Protocol summary
    st.markdown("### 📊 Protocol Summary")
    
    summary_cols = st.columns(2)
    
    with summary_cols[0]:
        st.json({
            "Protocol": summary.get('protocol', 'N/A'),
            "Cardio": summary.get('cardio', 'N/A'),
            "Training Days": summary.get('training_days', []),
            "HIGH Days": summary.get('high_days', [])
        })
    
    with summary_cols[1]:
        st.json({
            "LBM": f"{week_plan.lean_body_mass:.1f} lbs",
            "Protein per Meal": summary.get('protein_per_meal', 'N/A'),
            "Week Number": week_plan.week_number
        })
    
    # Download section
    st.markdown("---")
    st.markdown("### 📥 Download Files")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.download_button(
            label="📄 Download Week Plan",
            data=st.session_state['week_md'],
            file_name=os.path.basename(st.session_state['week_path']),
            mime="text/markdown",
            use_container_width=True
        )
    
    with col2:
        st.download_button(
            label="💊 Download Supplements",
            data=st.session_state['supp_md'],
            file_name=os.path.basename(st.session_state['supp_path']),
            mime="text/markdown",
            use_container_width=True
        )
    
    with col3:
        st.download_button(
            label="📊 Download Summary",
            data=st.session_state['summary_md'],
            file_name=os.path.basename(st.session_state['summary_path']),
            mime="text/markdown",
            use_container_width=True
        )


def show_food_database():
    """Food database browser"""
    st.markdown('<div class="sub-header">Food Database</div>', unsafe_allow_html=True)
    
    food_db = FoodDatabase()
    all_foods = food_db.get_all_foods()
    
    st.markdown(f"**Total Foods:** {len(all_foods)} items")
    
    # Filter options
    col1, col2 = st.columns(2)
    
    with col1:
        from src.models import FoodCategory
        category_filter = st.selectbox(
            "Filter by Category",
            ["All"] + [cat.value for cat in FoodCategory],
            key="category_filter"
        )
    
    with col2:
        search_term = st.text_input("🔍 Search foods", placeholder="e.g., chicken, rice, almonds")
    
    # Filter foods
    filtered_foods = all_foods
    
    if category_filter != "All":
        from src.models import FoodCategory
        filtered_foods = [f for f in filtered_foods if f.category.value == category_filter]
    
    if search_term:
        search_lower = search_term.lower()
        filtered_foods = [
            f for f in filtered_foods
            if search_lower in f.name.lower() or (f.arabic_name and search_lower in f.arabic_name.lower())
        ]
    
    st.markdown(f"**Showing {len(filtered_foods)} foods**")
    
    # Display foods
    for food in filtered_foods:
        with st.expander(f"🍽️ {food.name} {f'({food.arabic_name})' if food.arabic_name else ''} - {food.category.value}"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"""
                **Serving Size:** {food.serving_size} ({food.serving_size_grams}g)
                
                **Macros per serving:**
                - Protein: {food.protein_per_serving}g
                - Carbs: {food.carbs_per_serving}g
                - Fat: {food.fat_per_serving}g
                - Calories: {food.get_macros().calculate_calories()} cal
                """)
            
            with col2:
                if food.notes:
                    st.info(f"💡 {food.notes}")
            
            # Macro breakdown chart
            macros_data = {
                'Macro': ['Protein', 'Carbs', 'Fat'],
                'Grams': [food.protein_per_serving, food.carbs_per_serving, food.fat_per_serving]
            }
            fig = px.bar(
                pd.DataFrame(macros_data),
                x='Macro',
                y='Grams',
                title=f'{food.name} - Macro Breakdown',
                color='Macro',
                color_discrete_map={'Protein': '#1f77b4', 'Carbs': '#ff7f0e', 'Fat': '#2ca02c'}
            )
            fig.update_layout(height=250, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)


def show_about():
    """Comprehensive about page"""
    st.markdown('<div class="sub-header">About Fitlife Lifestyle Agent</div>', unsafe_allow_html=True)
    
    st.markdown("""
    ### 🎯 Overview
    
    Fitlife Lifestyle Agent is an automated meal plan generation system for nutrition consulting 
    that supports **SHREDDED** (fat loss) and **MASSIVE** (muscle gain) protocols with supplement 
    prescriptions and bilingual output (English/Arabic).
    
    ### ✨ Features
    
    - ✅ **Client Profile Management** - Collect and store client information
    - ✅ **LBM Calculator** - Automatic lean body mass calculations
    - ✅ **Macro Calculator** - Protocol-specific macronutrient targets
    - ✅ **Meal Plan Generator** - Complete 7-day meal plans with timing
    - ✅ **Food Database** - Comprehensive food library with nutritional info
    - ✅ **Supplement Recommendations** - Goal-based supplement stacks
    - ✅ **Markdown Export** - Professional meal plan documents
    - ✅ **Visual Analytics** - Charts and graphs for macro tracking
    - ✅ **Food Browser** - Searchable food database
    
    ### 📋 Protocols
    
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
    
    ### 🛠️ Technical Details
    
    Built with Python, Streamlit, Plotly, and Pandas for a modern, user-friendly interface.
    
    ### 📊 Calculations
    
    **Lean Body Mass (LBM):**
    ```
    LBM = Body Weight × (1 - Body Fat %)
    ```
    
    **Protein Per Meal:**
    ```
    Protein = Round up to nearest 5g of: (LBM ÷ 8) × 2
    ```
    
    **Calories:**
    ```
    Calories = (Protein × 4) + (Carbs × 4) + (Fat × 9)
    ```
    """)
    
    st.markdown("---")
    st.markdown("**Built with ❤️ for nutrition professionals**")


if __name__ == "__main__":
    main()
