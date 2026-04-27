"""
Vehicle Fault Diagnosis Expert System
app.py
"""

import streamlit as st
import time
import pandas as pd

# ==========================================
# PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="ProMechanic AI | Expert System",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
    <style>
    .main-header {
        font-size: 40px;
        color: #1E3A8A;
        font-weight: 800;
        text-align: center;
        margin-bottom: 5px;
    }
    .sub-header {
        font-size: 18px;
        color: #4B5563;
        text-align: center;
        margin-bottom: 30px;
    }
    .report-card {
        background-color: #F3F4F6;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #1E3A8A;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# KNOWLEDGE BASE (30 Distinct Faults)
# ==========================================
KNOWLEDGE_BASE = [
    # ---- ENGINE (6) ----
    {
        "id": "ENG_01", "category": "Engine", "fault": "Engine Misfire",
        "symptoms": ["Rough idle", "Check engine light flashing", "Loss of power"],
        "severity": "High",
        "description": "One or more engine cylinders are not firing correctly, leading to rough running and excessive emissions.",
        "recommendation": "Stop driving immediately to avoid catalytic converter damage. Inspect and replace spark plugs, ignition coils, or fuel injectors."
    },
    {
        "id": "ENG_02", "category": "Engine", "fault": "Engine Overheating",
        "symptoms": ["Temperature gauge high", "Coolant leaking", "Steam from hood"],
        "severity": "Critical",
        "description": "The engine temperature has exceeded safe operating levels, risking severe internal block/head gasket damage.",
        "recommendation": "Pull over safely and turn off the engine. Do not open the radiator cap while hot. Check coolant, thermostat, and water pump once cooled."
    },
    {
        "id": "ENG_03", "category": "Engine", "fault": "Starter Motor Failure",
        "symptoms": ["Clicking noise when turning key", "Engine doesn't crank", "Lights dim when starting"],
        "severity": "Medium",
        "description": "The starter motor is unable to engage or turn the engine flywheel. Usually due to internal wear or solenoid failure.",
        "recommendation": "Test battery voltage first to rule out dead battery. If battery is good, replace the starter assembly."
    },
    {
        "id": "ENG_04", "category": "Engine", "fault": "Alternator Failure",
        "symptoms": ["Battery light on", "Whining noise from engine", "Engine stalls while running"],
        "severity": "High",
        "description": "The alternator is failing to charge the battery or power the electrical system while the engine is running.",
        "recommendation": "Test alternator output using a multimeter. Inspect serpentine belt. Replace alternator if output is below 13.5V."
    },
    {
        "id": "ENG_05", "category": "Engine", "fault": "Oil Leak / Low Oil Pressure",
        "symptoms": ["Oil spots under car", "Low oil pressure light", "Knocking sound from engine"],
        "severity": "Critical",
        "description": "The engine is starved of oil pressure, causing metal-to-metal contact which leads to catastrophic failure.",
        "recommendation": "Turn engine off IMMEDIATELY. Check oil dipstick. Do not run until oil level is corrected and leak is fixed."
    },
    {
        "id": "ENG_06", "category": "Engine", "fault": "Fuel Pump Failure",
        "symptoms": ["Engine cranks but won't start", "Sputtering at high speeds", "Whining noise from rear"],
        "severity": "High",
        "description": "The fuel pump is not delivering sufficient fuel pressure to the injection system.",
        "recommendation": "Check fuel pump fuse and relay. Perform fuel pressure test. Replace fuel pump and fuel filter if pressure is low."
    },
    # ---- BRAKES (6) ----
    {
        "id": "BRK_01", "category": "Brakes", "fault": "Worn Brake Pads",
        "symptoms": ["Squealing or grinding noise when braking", "Longer stopping distance"],
        "severity": "Low",
        "description": "Brake pad friction material has reached its minimum thickness threshold.",
        "recommendation": "Inspect brake pads visually. Replace brake pads on both sides of the axle."
    },
    {
        "id": "BRK_02", "category": "Brakes", "fault": "Warped Brake Rotors",
        "symptoms": ["Steering wheel vibrates when braking", "Pulsating brake pedal"],
        "severity": "Medium",
        "description": "Excessive heat or uneven lug nut torque has caused the brake rotors to lose consistent flatness.",
        "recommendation": "Measure rotor runout. Resurface or replace brake rotors and install new pads."
    },
    {
        "id": "BRK_03", "category": "Brakes", "fault": "Brake Fluid Leak",
        "symptoms": ["Brake pedal goes to floor", "Red/brown fluid near wheels", "Brake warning light on"],
        "severity": "Critical",
        "description": "Hydraulic pressure in the braking system is compromised, severely limiting stopping capability.",
        "recommendation": "DO NOT DRIVE. Tow to shop. Inspect brake lines, hoses, and calipers for leaks. Repair and bleed system."
    },
    {
        "id": "BRK_04", "category": "Brakes", "fault": "Seized Brake Caliper",
        "symptoms": ["Vehicle pulls to one side when braking", "Burning smell from wheel", "Excessive brake dust on one wheel"],
        "severity": "High",
        "description": "The caliper piston or slide pins are stuck, keeping the brake pads engaged constantly.",
        "recommendation": "Inspect caliper for free movement. Rebuild or replace seized caliper, along with pads and potentially the rotor."
    },
    {
        "id": "BRK_05", "category": "Brakes", "fault": "ABS Sensor Failure",
        "symptoms": ["ABS light on", "Traction control light on", "Pulsation under normal braking"],
        "severity": "Medium",
        "description": "The Anti-lock Braking System wheel speed sensor is sending erratic or zero signal.",
        "recommendation": "Scan OBD2 codes for specific wheel sensor. Clean sensor mounting surface or replace sensor."
    },
    {
        "id": "BRK_06", "category": "Brakes", "fault": "Air in Brake Lines",
        "symptoms": ["Spongy brake pedal", "Needs pumping to stop"],
        "severity": "High",
        "description": "Air bubbles trapped in hydraulic fluid compress when braking, diminishing hydraulic force to calipers.",
        "recommendation": "Perform a complete brake hydraulic system flush and bleed sequence to remove air bubbles."
    },
    # ---- TRANSMISSION (6) ----
    {
        "id": "TRN_01", "category": "Transmission", "fault": "Low Transmission Fluid",
        "symptoms": ["Delayed engagement", "Slipping gears", "Red fluid leak under middle of car"],
        "severity": "High",
        "description": "Insufficient fluid levels are preventing optimal hydraulic line pressure within the automatic transmission.",
        "recommendation": "Check transmission fluid level (if dipstick equipped). Top off with correct specification fluid and inspect for pan/cooler leaks."
    },
    {
        "id": "TRN_02", "category": "Transmission", "fault": "Worn Clutch (Manual)",
        "symptoms": ["High RPMs without acceleration", "Burning smell when shifting", "Spongy clutch pedal"],
        "severity": "High",
        "description": "The clutch disc friction material is degraded, causing 'slipping' between engine and transmission.",
        "recommendation": "Remove transmission assembly. Replace clutch disc, pressure plate, and throw-out bearing. Resurface flywheel."
    },
    {
        "id": "TRN_03", "category": "Transmission", "fault": "Torque Converter Issue",
        "symptoms": ["Shuddering at certain speeds", "Overheating transmission", "Check engine light"],
        "severity": "High",
        "description": "The lock-up clutch inside the torque converter is failing or the stator is compromised.",
        "recommendation": "Perform diagnostic scan. Fluid pressure test. May require torque converter replacement."
    },
    {
        "id": "TRN_04", "category": "Transmission", "fault": "Worn Synchronizers (Manual)",
        "symptoms": ["Grinding noise when shifting", "Hard to get into gear", "Transmission pops out of gear"],
        "severity": "Medium",
        "description": "Synchronizer rings inside the manual transmission are worn, failing to match gear speeds during shifts.",
        "recommendation": "Requires internal transmission teardown and rebuild to replace worn brass synchronizer rings."
    },
    {
        "id": "TRN_05", "category": "Transmission", "fault": "Transmission Solenoid Failure",
        "symptoms": ["Erratic shifting", "Stuck in a specific gear", "Limp mode activated"],
        "severity": "High",
        "description": "Electromechanical solenoids controlling fluid flow to change gears have failed electrically or mechanically.",
        "recommendation": "Scan transmission control module (TCM) for codes. Drop transmission pan and replace faulty solenoids."
    },
    {
        "id": "TRN_06", "category": "Transmission", "fault": "Broken Transmission Mount",
        "symptoms": ["Thumping noise when accelerating", "Noticeable engine/transmission movement", "Clunking when shifting into Drive"],
        "severity": "Medium",
        "description": "The rubber/liquid-filled mount stabilizing the transmission to the chassis has torn or collapsed.",
        "recommendation": "Visually inspect all drivetrain mounts with a pry bar. Replace the broken transmission mount assembly."
    },
    # ---- ELECTRICAL (6) ----
    {
        "id": "ELE_01", "category": "Electrical", "fault": "Dead Battery",
        "symptoms": ["Nothing happens when turning key", "Interior lights flicker/dim", "Need jump start frequently"],
        "severity": "Medium",
        "description": "The starter battery lacks sufficient cold cranking amps (CCA) due to age, sulfation, or complete discharge.",
        "recommendation": "Load test the battery. If it drops below 9.6V under load, replace battery. Clean terminal connectors."
    },
    {
        "id": "ELE_02", "category": "Electrical", "fault": "Blown Fuse",
        "symptoms": ["Specific accessory not working", "Sudden loss of radio/lights"],
        "severity": "Low",
        "description": "A circuit over-current condition forced the sacrificial fuse element to melt, severing voltage flow.",
        "recommendation": "Locate fuse box and replace blown fuse with matching amperage rating. If it blows again, find the short circuit."
    },
    {
        "id": "ELE_03", "category": "Electrical", "fault": "Faulty Spark Plugs",
        "symptoms": ["Poor fuel economy", "Hard starting", "Sluggish acceleration"],
        "severity": "Low",
        "description": "Spark plug electrode wear or carbon fouling is resulting in weak combustion sparks.",
        "recommendation": "Extract and inspect spark plugs. Replace the set with OEM-recommended iridium or platinum plugs."
    },
    {
        "id": "ELE_04", "category": "Electrical", "fault": "Bad Ignition Coil",
        "symptoms": ["Engine misfire", "Check engine light", "Stalling"],
        "severity": "High",
        "description": "An ignition coil pack is failing to transform 12V into the high voltage necessary for the spark plug gap.",
        "recommendation": "Use OBD2 scanner to identify specific cylinder misfire (e.g., P0302). Swap coil to test. Replace faulty coil."
    },
    {
        "id": "ELE_05", "category": "Electrical", "fault": "Parasitic Battery Drain",
        "symptoms": ["Battery dies overnight", "Battery test shows good health", "Unexplained clicks when car is off"],
        "severity": "Medium",
        "description": "An onboard module, relay, or aftermarket accessory is not going to sleep, continuously drawing excessive amps.",
        "recommendation": "Perform a parasitic draw test with a multimeter in series. Pull fuses sequentially until amp draw drops to normal (< 50mA)."
    },
    {
        "id": "ELE_06", "category": "Electrical", "fault": "Faulty Mass Airflow Sensor (MAF)",
        "symptoms": ["Hesitation during acceleration", "Rich/lean running condition", "Rough idle"],
        "severity": "Medium",
        "description": "Dirt or sensor degradation is causing incorrect air density readings, throwing off air/fuel mix calculation.",
        "recommendation": "Clean MAF sensor with dedicated MAF cleaner spray. If symptoms persist, replace unit and clear codes."
    },
    # ---- STEERING (6) ----
    {
        "id": "STR_01", "category": "Steering", "fault": "Low Power Steering Fluid",
        "symptoms": ["Whining noise when turning", "Hard steering", "Red/Pink fluid leak near front"],
        "severity": "High",
        "description": "Leaking racks or hoses have permitted fluid to escape, causing cavitation in the hydraulic pump.",
        "recommendation": "Identify and repair fluid leak (often hoses). Refill power steering reservoir and bleed system by turning lock-to-lock."
    },
    {
        "id": "STR_02", "category": "Steering", "fault": "Worn Tie Rods",
        "symptoms": ["Uneven tire wear", "Loose steering wheel", "Clunking noise over bumps"],
        "severity": "High",
        "description": "The ball-and-socket joints linking the steering rack to the steering knuckle have worn loose.",
        "recommendation": "Safely raise vehicle and perform 9-3 o'clock wheel shake test to verify play. Replace tie rods and get a professional alignment."
    },
    {
        "id": "STR_03", "category": "Steering", "fault": "Bad Wheel Bearing",
        "symptoms": ["Humming/roaring noise that changes with speed", "Steering wheel play", "ABS light occasionally flashes"],
        "severity": "High",
        "description": "The roller or ball bearings in the hub are pitted or starved of grease.",
        "recommendation": "Jack up vehicle and perform 12-6 o'clock wheel shake test. Spin wheel to listen for roughness. Replace wheel hub bearing assembly."
    },
    {
        "id": "STR_04", "category": "Steering", "fault": "Worn Shock Absorbers/Struts",
        "symptoms": ["Bouncy ride", "Cupped tire wear", "Nose dives when braking"],
        "severity": "Medium",
        "description": "Hydraulic dampeners have lost their gas charge or internal fluid, failing to control suspension spring oscillations.",
        "recommendation": "Perform jounce/bounce test. Look for oil leaking from strut bodies. Replace shock absorbers/struts in pairs."
    },
    {
        "id": "STR_05", "category": "Steering", "fault": "Failing Power Steering Pump",
        "symptoms": ["Squealing noise when turning", "Stiff steering at low speeds", "Metal flakes in steering fluid"],
        "severity": "Medium",
        "description": "The hydraulic pump impeller or bearings are disintegrating internally.",
        "recommendation": "Check condition of serpentine belt first. If belt is fine, flush old fluid and replace the power steering pump."
    },
    {
        "id": "STR_06", "category": "Steering", "fault": "Loose Steering Rack",
        "symptoms": ["Wandering on highway", "Clunking when turning wheel", "Steering dead zone"],
        "severity": "High",
        "description": "Steering rack mounting bushings are deteriorated or internal rack-and-pinion gears are worn.",
        "recommendation": "Inspect rack bushings. If internal play is detected, replace the steering rack-and-pinion assembly and align."
    }
]

# ==========================================
# INFERENCE ENGINE (FORWARD CHAINING)
# ==========================================
def forward_chaining(observed_symptoms):
    """
    Infers potential vehicle faults based on selected symptoms mapping to the Knowledge Base.
    Matching logic calculates percentage match between observed and defined symptoms.
    """
    diagnoses = []
    observed_set = set(observed_symptoms)
    
    for rule in KNOWLEDGE_BASE:
        rule_symptoms = set(rule["symptoms"])
        matches = rule_symptoms.intersection(observed_set)
        
        match_count = len(matches)
        total_rule_symptoms = len(rule_symptoms)
        
        if match_count > 0:
            match_percentage = (match_count / total_rule_symptoms) * 100
            
            # Formulate Confidence
            if match_percentage == 100:
                confidence = "Very High"
            elif match_percentage >= 66:
                confidence = "High"
            elif match_percentage >= 33:
                confidence = "Medium"
            else:
                confidence = "Low"
                
            diagnoses.append({
                "fault": rule["fault"],
                "category": rule["category"],
                "severity": rule["severity"],
                "description": rule["description"],
                "recommendation": rule["recommendation"],
                "match_percentage": match_percentage,
                "confidence": confidence,
                "matched_symptoms": list(matches),
                "missing_symptoms": list(rule_symptoms - observed_set)
            })
            
    # Sort strictly by match percentage descending, then severity
    severity_order = {"Critical": 4, "High": 3, "Medium": 2, "Low": 1}
    diagnoses = sorted(
        diagnoses, 
        key=lambda x: (x["match_percentage"], severity_order.get(x["severity"], 0)), 
        reverse=True
    )
    return diagnoses

# ==========================================
# STREAMLIT USER INTERFACE
# ==========================================
def main():
    st.markdown("<div class='main-header'>🚘 ProMechanic AI Diagnostics</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>A Rule-Based Vehicle Fault Diagnosis Expert System</div>", unsafe_allow_html=True)
    
    # --- Sidebar Navigation ---
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/1995/1995470.png", width=120)  # External wrench/car icon, adjust/remove if offline
        st.markdown("## Navigation")
        app_mode = st.radio("Select View:", ["🔧 Diagnostics Panel", "📚 Knowledge Base", "ℹ️ About the System"])
        st.markdown("---")
        st.markdown("### System Specs")
        st.markdown("- **Architecture:** Forward Chaining\\n- **Rules Base:** 30 Unique Faults\\n- **Systems Covered:** Engine, Brakes, Transmission, Electrical, Steering")
        st.markdown("---")
        st.markdown("**Version:** 1.0.0-PRO")
        st.markdown("**Status:** Deployment Ready")

    # --- Mode: Diagnostics Panel ---
    if app_mode == "🔧 Diagnostics Panel":
        st.header("📋 Diagnostic Interview")
        st.write("Welcome to the service bay. Please systematically select all the symptoms you are experiencing with your vehicle to begin the diagnosis.")
        
        # Group symptoms dynamically for the UI
        grouped_symptoms = { "Engine": set(), "Brakes": set(), "Transmission": set(), "Electrical": set(), "Steering": set() }
        for item in KNOWLEDGE_BASE:
            for s in item["symptoms"]:
                grouped_symptoms[item["category"]].add(s)
                
        # UX Layout: Splitting into columns for better visibility
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("⚙️ Powertrain")
            eng_symptoms = st.multiselect("Engine Symptoms", sorted(list(grouped_symptoms["Engine"])))
            trn_symptoms = st.multiselect("Transmission Symptoms", sorted(list(grouped_symptoms["Transmission"])))
            
        with col2:
            st.subheader("🛑 Chassis")
            brk_symptoms = st.multiselect("Brake Symptoms", sorted(list(grouped_symptoms["Brakes"])))
            str_symptoms = st.multiselect("Steering Symptoms", sorted(list(grouped_symptoms["Steering"])))
            
        with col3:
            st.subheader("⚡ Electrical")
            ele_symptoms = st.multiselect("Electrical Symptoms", sorted(list(grouped_symptoms["Electrical"])))
            
        # Aggregate all selected symptoms across groups
        selected_symptoms = eng_symptoms + trn_symptoms + brk_symptoms + str_symptoms + ele_symptoms
        
        st.markdown("---")
        
        # Action button
        if st.button("🔍 RUN DIAGNOSTICS", use_container_width=True, type="primary"):
            if not selected_symptoms:
                st.warning("⚠️ **Input Required:** Please select at least one symptom to run the inference engine.")
            else:
                with st.spinner("🧠 AI reasoning engine analyzing symptoms..."):
                    time.sleep(1.2) # Artificial thinking delay for professional UX
                    results = forward_chaining(selected_symptoms)
                    
                if not results:
                    st.info("No matching faults found based on the provided symptoms. Ensure inputs are correct or consult a physical mechanic.")
                else:
                    st.success(f"✅ Diagnosis Complete! Analyzed {len(selected_symptoms)} symptoms and isolated {len(results)} potential faults.")
                    
                    st.markdown("### 📝 Official Diagnostic Report")
                    
                    # Highlight top diagnosis
                    top_fault = results[0]
                    if top_fault["match_percentage"] >= 66:
                        st.error(f"🚨 **High Probability Issue:** {top_fault['fault']} ({top_fault['category']} System)")
                    else:
                        st.warning(f"⚠️ **Most Likely Issue:** {top_fault['fault']} ({top_fault['category']} System)")
                        
                    # Build expanders for each diagnosis returned
                    for idx, res in enumerate(results):
                        # Color coding based on severity
                        sev_color = {
                            "Critical": "🔴 Critical",
                            "High": "🟠 High",
                            "Medium": "🟡 Medium",
                            "Low": "🟢 Low"
                        }
                        
                        match_conf = f"{res['match_percentage']:.0f}% Match"
                        label = f"{idx+1}. {res['fault']} | {match_conf} | {sev_color.get(res['severity'], '')}"
                        
                        # Expand top result by default
                        with st.expander(label, expanded=(idx == 0)):
                            st.write(f"**System:** {res['category']}")
                            st.write(f"**Diagnostic Description:** {res['description']}")
                            st.markdown(f"**Mechanic's Recommendation:** `{res['recommendation']}`")
                            
                            c1, c2 = st.columns(2)
                            with c1:
                                st.markdown("✅ **Correlated Symptoms:**")
                                for sys in res["matched_symptoms"]:
                                    st.markdown(f"- {sys}")
                            with c2:
                                if res["missing_symptoms"]:
                                    st.markdown("❌ **Unobserved Symptoms (Typical for this fault):**")
                                    for sys in res["missing_symptoms"]:
                                        st.markdown(f"- {sys}")
                                        
                    st.write("---")
                    st.caption("Disclaimer: This tool provides probabilistic estimates based on a rule-based expert system and does not replace certified professional mechanical diagnosis.")

    # --- Mode: Knowledge Base ---
    elif app_mode == "📚 Knowledge Base":
        st.header("🗄️ System Knowledge Base")
        st.write(f"The inference engine evaluates rules against **{len(KNOWLEDGE_BASE)}** modeled vehicle faults.")
        
        # Display as a dataframe
        df = pd.DataFrame(KNOWLEDGE_BASE)
        df["Symptoms Data"] = df["symptoms"].apply(lambda x: ", ".join(x))
        df_display = df[["id", "category", "fault", "severity", "Symptoms Data", "recommendation"]]
        df_display.columns = ["Rule ID", "System", "Fault Designation", "Severity", "Symptom Triggers", "Standard Recommendation"]
        
        st.dataframe(df_display, use_container_width=True, hide_index=True)
        
    # --- Mode: About System ---
    elif app_mode == "ℹ️ About the System":
        st.header("🧠 About ProMechanic AI")
        st.markdown(
            "This application is a **Rule-Based Expert System** using robust **Forward Chaining Logic** to diagnose automobile faults. "
            "It is structured efficiently to read user input (symptoms), match them against a predefined set of logical rules, and iterate "
            "probabilistically highest correlating faults."
        )
        st.subheader("Architectural Components")
        st.markdown("- **Knowledge Base:** Python dictionary acting as a deterministic fact repository containing over 30 unique vehicle issues.")
        st.markdown("- **Inference Engine:** Processes the raw symptoms against the Knowledge Base to determine rule satisfaction using forward-chaining mechanics.")
        st.markdown("- **User Interface:** Streamlit-powered WebUI designed for high accessibility and professional display.")
        
        st.info("Developed by: Senior AI Architect & Full-Stack Python Developer")
        
if __name__ == "__main__":
    main()
