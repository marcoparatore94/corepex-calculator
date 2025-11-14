import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# --- COREPEX functions ---
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
        return "Group 1 (low risk)", "green"
    elif score <= 50:
        return "Group 2 (intermediate risk)", "orange"
    elif score <= 75:
        return "Group 3 (high risk)", "red"
    else:
        return "Group 4 (very high risk)", "darkred"

# --- Streamlit page config ---
st.set_page_config(page_title="COREPEX Calculator", page_icon="🩺")

# --- Intro ---
st.title("COREPEX Calculator 🩺")
st.markdown("""
This tool implements the prognostic score developed in the **COREPEX Study**  
(*Complications and Recurrence After Pelvic Exenteration for Gynecologic Malignancies*,  
Bizzarri et al., Obstetrics & Gynecology, 2025).

The score stratifies patients undergoing pelvic exenteration into risk groups for  
**Disease-Free Survival (DFS)** and **Overall Survival (OS)**.
""")

# --- Input section ---
st.header("Input Clinical Data")

st.subheader("Disease-Free Survival (DFS)")
margins = st.selectbox("Margins", ["negative", "positive"])
lvsi = st.selectbox("LVSI", ["negative", "positive"])
pe_type = st.selectbox("PE Type", ["anterior", "total"])
lymphadenectomy = st.selectbox("Lymphadenectomy", ["yes", "no"])

st.subheader("Overall Survival (OS)")
margins_os = st.selectbox("Margins (OS)", ["negative", "positive"])
lvsi_os = st.selectbox("LVSI (OS)", ["negative", "positive"])
pe_type_os = st.selectbox("PE Type (OS)", ["anterior", "total"])
timing = st.selectbox("Timing", ["naive", "persistence", "recurrence"])

# --- Calculate scores ---
dfs_score = corepex_dfs(margins, lvsi, pe_type, lymphadenectomy)
os_score = corepex_os(margins_os, lvsi_os, pe_type_os, timing)

dfs_group, dfs_color = risk_group(dfs_score)
os_group, os_color = risk_group(os_score)

# --- Output section ---
st.header("Results")

st.markdown(f"<h3>DFS Score: {dfs_score} → <span style='color:{dfs_color}'>{dfs_group}</span></h3>", unsafe_allow_html=True)
st.markdown(f"<h3>OS Score: {os_score} → <span style='color:{os_color}'>{os_group}</span></h3>", unsafe_allow_html=True)

# --- Graphs section ---
st.header("Visualizations")

chart_type = st.selectbox("Select chart type", ["Kaplan-Meier (simulated)", "Bar chart", "Pie chart"])

if chart_type == "Kaplan-Meier (simulated)":
    # Simulated survival curves
    time = np.linspace(0, 60, 61)
    survival_low = np.exp(-time/80)
    survival_high = np.exp(-time/30)

    fig, ax = plt.subplots()
    ax.plot(time, survival_low, label="Low risk", color="green")
    ax.plot(time, survival_high, label="High risk", color="red")
    ax.set_xlabel("Months")
    ax.set_ylabel("Survival probability")
    ax.set_title("Simulated Kaplan-Meier curves")
    ax.legend()
    st.pyplot(fig)

elif chart_type == "Bar chart":
    fig, ax = plt.subplots()
    ax.bar(["DFS Score", "OS Score"], [dfs_score, os_score], color=["blue", "purple"])
    ax.set_ylabel("Score")
    ax.set_title("COREPEX Scores")
    st.pyplot(fig)

elif chart_type == "Pie chart":
    labels = ["DFS", "OS"]
    values = [dfs_score, os_score]
    fig, ax = plt.subplots()
    ax.pie(values, labels=labels, autopct="%1.1f%%", colors=["skyblue", "lightcoral"])
    ax.set_title("Relative Scores")
    st.pyplot(fig)
