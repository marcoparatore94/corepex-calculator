import streamlit as st

# --- COREPEX functions (unchanged) ---
def corepex_dfs(margins, lvsi, pe_type, lymphadenectomy):
    score = 0
    if margins == "positive":
        score += 40
    if lvsi == "positive":
        score += 26
    if pe_type == "total":
        score += 22
    if lymphadenectomy == "no":
        score += 12
    return score

def corepex_os(margins, lvsi, pe_type, timing):
    score = 0
    if margins == "positive":
        score += 27
    if lvsi == "positive":
        score += 16
    if pe_type == "total":
        score += 21
    if timing == "persistence":
        score += 36
    elif timing == "recurrence":
        score += 21
    return score

def risk_group(score):
    if score <= 25:
        return "Group 1 (low risk)", "green", 1
    elif score <= 50:
        return "Group 2 (intermediate risk)", "orange", 2
    elif score <= 75:
        return "Group 3 (high risk)", "red", 3
    else:
        return "Group 4 (very high risk)", "darkred", 4

# --- Survival estimates from COREPEX (5-year) ---
DFS_ESTIMATES = {
    1: {"value": 43.7, "ci": (35.1, 52.3)},
    2: {"value": 24.9, "ci": (18.4, 31.4)},
    3: {"value": 22.2, "ci": (13.0, 31.4)},
    4: {"value": 8.0,  "ci": (0.0, 15.4)},
}

OS_ESTIMATES = {
    1: {"value": 54.3, "ci": (43.1, 65.5)},
    2: {"value": 40.4, "ci": (32.6, 48.2)},
    3: {"value": 24.0, "ci": (16.7, 31.2)},
    4: {"value": 4.3,  "ci": (0.0, 12.1)},
}

# --- Page config & intro ---
st.set_page_config(page_title="COREPEX Calculator", page_icon="🩺")
st.title("COREPEX Calculator 🩺")
st.markdown("""
Implements the prognostic score from the **COREPEX study** (Bizzarri et al., Obstetrics & Gynecology, 2025).
Displays 5-year **Disease-Free Survival (DFS)** and **Overall Survival (OS)** estimates by risk group.
Use for patient counseling and surveillance planning; not a treatment recommendation.
""")

# --- Single input section ---
st.header("Clinical data entry")
margins = st.selectbox("Margins", ["negative", "positive"])
lvsi = st.selectbox("LVSI", ["negative", "positive"])
pe_type = st.selectbox("PE Type", ["anterior", "total"])
lymphadenectomy = st.selectbox("Lymphadenectomy", ["yes", "no"])
timing = st.selectbox("Timing (for OS)", ["naive", "persistence", "recurrence"])

# --- Calculate scores & groups ---
dfs_score = corepex_dfs(margins, lvsi, pe_type, lymphadenectomy)
os_score = corepex_os(margins, lvsi, pe_type, timing)
dfs_group_label, dfs_color, dfs_group_id = risk_group(dfs_score)
os_group_label, os_color, os_group_id = risk_group(os_score)

# --- Map to survival estimates ---
dfs_est = DFS_ESTIMATES[dfs_group_id]
os_est = OS_ESTIMATES[os_group_id]

# --- Results section ---
st.header("Results")
st.markdown(f"<h3>DFS Score: {dfs_score} → <span style='color:{dfs_color}'>{dfs_group_label}</span></h3>", unsafe_allow_html=True)
st.markdown(f"- 5-year DFS: {dfs_est['value']:.1f}% (95% CI {dfs_est['ci'][0]:.1f}–{dfs_est['ci'][1]:.1f})")
st.markdown(f"<h3>OS Score: {os_score} → <span style='color:{os_color}'>{os_group_label}</span></h3>", unsafe_allow_html=True)
st.markdown(f"- 5-year OS: {os_est['value']:.1f}% (95% CI {os_est['ci'][0]:.1f}–{os_est['ci'][1]:.1f})")

# --- Footnote ---
st.caption("COREPEX score components: margins, LVSI, PE type, lymphadenectomy (DFS); margins, LVSI, PE type, timing (OS).")
