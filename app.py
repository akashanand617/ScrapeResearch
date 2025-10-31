import streamlit as st
import json

# Load data
with open("basic_info.json") as f:
    data = json.load(f)

st.title("UC Davis Faculty Directory")

# --- Department filter (supports multi-select incl. All) ---
departments = sorted(set(v.get("department", "Unknown") for v in data.values()))
selected_depts = st.multiselect("Select Departments", ["All"] + departments, default=["All"])

# Filter by department(s)
if "All" in selected_depts or not selected_depts:
    dept_filtered = data
else:
    dept_filtered = {k: v for k, v in data.items() if v.get("department") in selected_depts}

# --- Tag filter (multi-select) ---
tags = sorted(set(tag for v in dept_filtered.values() for tag in v.get("tag", [])))
selected_tags = st.multiselect("Filter by Research Tag/Topic", tags)

# Apply tag filter
if selected_tags:
    final_filtered = {
        k: v for k, v in dept_filtered.items()
        if any(tag in v.get("tag", []) for tag in selected_tags)
    }
else:
    final_filtered = dept_filtered

# --- Faculty selection (autocomplete-enabled) ---
selected_name = st.selectbox("Search / Select Faculty Member", [""] + sorted(final_filtered.keys()))

# --- Display selected professor info ---
if selected_name:
    prof = final_filtered[selected_name]
    st.subheader(selected_name)

    if prof.get("email"):
        st.write(f"**Email:** {prof['email']}")

    if prof.get("department"):
        st.write(f"**Department:** {prof['department'].upper()}")

    if prof.get("tag"):
        st.write(f"**Tags/Research Areas:** {', '.join(prof['tag'])}")

    if prof.get("profile_url"):
        st.markdown(f"[Profile Link]({prof['profile_url']})")

    if prof.get("websites"):
        st.markdown("**Websites:**<br>" + "<br>".join(prof["websites"]), unsafe_allow_html=True)

    if prof.get("description"):
        desc = prof["description"].replace("\n", "<br>")
        st.markdown(f"**Description:**<br>{desc}", unsafe_allow_html=True)
