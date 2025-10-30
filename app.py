import streamlit as st
import json

# Load data
with open("basic_info.json") as f:
    data = json.load(f)

st.title("UC Davis Faculty Directory")

# --- Tag filter ---
tags = sorted(set(tag for v in data.values() for tag in v.get("tag", [])))
selected_tag = st.selectbox("Filter by tag", ["All"] + tags)

# --- Filtered faculty list ---
filtered = {
    k: v for k, v in data.items()
    if selected_tag == "All" or selected_tag in v.get("tag", [])
}
selected_name = st.selectbox("Select Professor", [""] + list(filtered.keys()))

# --- Display selected professor info ---
if selected_name:
    prof = filtered[selected_name]
    st.subheader(selected_name)

    # Only show fields that exist
    if prof.get("email"):
        st.write(f"**Email:** {prof['email']}")

    if prof.get("tag"):
        st.write(f"**Tags:** {', '.join(prof['tag'])}")

    if prof.get("profile_url"):
        st.markdown(f"[Profile Link]({prof['profile_url']})")

    if prof.get("websites"):
        st.markdown("**Websites:**<br>" + "<br>".join(prof["websites"]),
                    unsafe_allow_html=True)

    if prof.get("description"):
        desc = prof["description"].replace("\n", "<br>")
        st.markdown(f"**Description:**<br>{desc}", unsafe_allow_html=True)