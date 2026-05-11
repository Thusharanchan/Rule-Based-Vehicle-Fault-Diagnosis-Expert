import streamlit as st

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="AutoExpert AI", page_icon="🚗", layout="centered")

# --- KNOWLEDGE BASE (30 SCENARIOS) ---
knowledge_base = {
    "Engine": [
        {"question": "Is there blue smoke coming from the exhaust?", "fault": "Oil burning in combustion", "solution": "Check piston rings and valve seals."},
        {"question": "Is the engine sputtering at high speeds?", "fault": "Clogged fuel filter", "solution": "Replace the fuel filter."},
        {"question": "Is the engine overheating while driving?", "fault": "Faulty thermostat", "solution": "Check coolant levels and replace thermostat."},
        {"question": "Is there a loud knocking sound from the engine block?", "fault": "Rod bearing failure", "solution": "Immediate mechanical inspection required."},
        {"question": "Is there thick white smoke from the exhaust?", "fault": "Coolant leaking into cylinders", "solution": "Check for a blown head gasket."},
        {"question": "Is there a significant loss of power (Limp Mode)?", "fault": "Turbocharger or Sensor failure", "solution": "Scan for ECU error codes."},
        {"question": "Does the engine vibrate heavily while idling?", "fault": "Worn engine mounts", "solution": "Inspect and replace rubber engine mounts."},
        {"question": "Is there a high-pitched whistling near the engine?", "fault": "Vacuum leak", "solution": "Check air hoses for cracks or disconnections."}
    ],
    "Electrical": [
        {"question": "Do you hear a clicking sound when trying to start?", "fault": "Dead or weak battery", "solution": "Jumpstart or replace the battery."},
        {"question": "Are your headlights dimming while driving?", "fault": "Failing alternator", "solution": "Test the alternator voltage output."},
        {"question": "Is a specific electronic component (like radio) not working?", "fault": "Blown fuse", "solution": "Check the fuse box and replace the blown fuse."},
        {"question": "Do the turn signals blink much faster than usual?", "fault": "Burnt out bulb", "solution": "Replace the turn signal bulb."},
        {"question": "Is there a burning plastic smell inside the cabin?", "fault": "Electrical short circuit", "solution": "Disconnect battery and inspect wiring harness."},
        {"question": "Are power windows moving very slowly or not at all?", "fault": "Faulty window regulator/motor", "solution": "Replace the window motor assembly."},
        {"question": "Does the dashboard clock/radio reset every time you start?", "fault": "Poor battery terminal connection", "solution": "Clean and tighten battery terminals."},
        {"question": "Are the dashboard warning lights flickering randomly?", "fault": "Faulty Ground (GND) wire", "solution": "Clean the main engine-to-chassis ground strap."}
    ],
    "Steering": [
        {"question": "Does the steering wheel vibrate at high speeds?", "fault": "Unbalanced wheels", "solution": "Get a professional wheel balancing."},
        {"question": "Is there a screeching noise when you turn the wheel?", "fault": "Low power steering fluid", "solution": "Top up fluid and check for leaks."},
        {"question": "Does the car pull to one side while driving straight?", "fault": "Wheel misalignment", "solution": "Perform a professional wheel alignment."},
        {"question": "Is the steering wheel unusually stiff or hard to turn?", "fault": "Failing power steering pump", "solution": "Inspect pump and belt tension."},
        {"question": "Is there a 'clunk' sound when turning the wheel fully?", "fault": "Worn CV joint", "solution": "Replace the CV axle assembly."},
        {"question": "Does the steering wheel feel 'loose' or have too much play?", "fault": "Worn tie rod ends", "solution": "Replace tie rod ends immediately."},
        {"question": "Is the steering wheel off-center while driving straight?", "fault": "Bent steering linkage", "solution": "Inspect for suspension damage and re-align."}
    ],
    "Chassis": [
        {"question": "Do you hear a clunking noise when driving over bumps?", "fault": "Worn suspension bushings", "solution": "Inspect and replace control arm bushings."},
        {"question": "Is the car 'bouncing' excessively after hitting a dip?", "fault": "Worn shock absorbers", "solution": "Replace the shock absorbers."},
        {"question": "Is there a constant grinding noise from the wheels?", "fault": "Wheel bearing failure", "solution": "Replace the wheel bearing immediately."},
        {"question": "Does the car sag in one specific corner?", "fault": "Broken coil spring", "solution": "Replace the damaged suspension spring."},
        {"question": "Is there a loud squeak when going over speed bumps?", "fault": "Dry or worn ball joints", "solution": "Lubricate or replace the ball joints."},
        {"question": "Does the car lean excessively during cornering?", "fault": "Worn sway bar links", "solution": "Replace the stabilizer/sway bar links."},
        {"question": "Is there a rattling sound coming from under the car?", "fault": "Loose exhaust heat shield", "solution": "Tighten or secure the metal heat shields."}
    ]
}

# --- LOGIC & UI (Same as previous, using Session State) ---
if "step" not in st.session_state:
    st.session_state.step = "select_domain"
    st.session_state.domain = None
    st.session_state.q_index = 0
    st.session_state.history = []

st.title("🚗 AutoExpert: Smart Diagnosis")
st.write("Professional Vehicle Fault Diagnosis Expert System")
st.divider()

if st.session_state.step == "select_domain":
    st.subheader("Select the affected area:")
    domains = list(knowledge_base.keys())
    for domain in domains:
        if st.button(f"Analyze {domain}", use_container_width=True):
            st.session_state.domain = domain
            st.session_state.step = "diagnosing"
            st.rerun()

elif st.session_state.step == "diagnosing":
    current_rules = knowledge_base[st.session_state.domain]
    if st.session_state.q_index < len(current_rules):
        rule = current_rules[st.session_state.q_index]
        st.info(f"System: {st.session_state.domain}")
        st.subheader(rule["question"])
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Yes", use_container_width=True):
                st.session_state.history.append(rule)
                st.session_state.step = "show_result"
                st.rerun()
        with col2:
            if st.button("❌ No", use_container_width=True):
                st.session_state.q_index += 1
                st.rerun()
    else:
        st.warning("No specific fault identified in this category.")
        if st.button("Try Another Category"):
            st.session_state.step = "select_domain"
            st.session_state.q_index = 0
            st.rerun()

elif st.session_state.step == "show_result":
    res = st.session_state.history[-1]
    st.success(f"**Diagnosis:** {res['fault']}")
    st.info(f"**Solution:** {res['solution']}")
    st.divider()
    if st.button("Check Another Symptom"):
        st.session_state.step = "select_domain"
        st.session_state.q_index = 0
        st.rerun()
