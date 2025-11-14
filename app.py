import streamlit as st

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
        return "Group 1 (low risk)"
    elif score <= 50:
        return "Group 2 (intermediate risk)"
    elif score <= 75:
        return "Group 3 (high risk)"
    else:
        return "Group 4 (very high risk)"

st.title("COREPEX Calculator")

st.header("Disease-Free Survival (DFS)")
margins = st.selectbox("Margins", ["negative", "positive"])
lvsi = st.selectbox("LVSI", ["negative", "positive"])
pe_type = st.selectbox("PE Type", ["anterior", "total"])
lymphadenectomy = st.selectbox("Lymphadenectomy", ["yes", "no"])

dfs_score = corepex_dfs(margins, lvsi, pe_type, lymphadenectomy)
st.write("DFS Score:", dfs_score, "-", risk_group(dfs_score))

st.header("Overall Survival (OS)")
margins_os = st.selectbox("Margins (OS)", ["negative", "positive"])
lvsi_os = st.selectbox("LVSI (OS)", ["negative", "positive"])
pe_type_os = st.selectbox("PE Type (OS)", ["anterior", "total"])
timing = st.selectbox("Timing", ["naive", "persistence", "recurrence"])

os_score = corepex_os(margins_os, lvsi_os, pe_type_os, timing)
st.write("OS Score:", os_score, "-", risk_group(os_score))