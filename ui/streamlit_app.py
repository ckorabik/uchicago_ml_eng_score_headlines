import streamlit as st
import requests

# Page setup
st.set_page_config(page_title="Score News Headlines UI", page_icon="🖥️")

st.title("Score News Headlines App")

# Text input
if "headlines" not in st.session_state:
    st.session_state.headlines = []


# Function to add another headline
def add_headline():
    st.session_state.headlines.append("")


# Display all headline inputs dynamically
for i in range(len(st.session_state.headlines)):
    st.session_state.headlines[i] = st.text_input(
        f"Headline {i+1}:", value=st.session_state.headlines[i], key=f"headline_{i}"
    )

# Button to add another headline
st.button("Add another headline", on_click=add_headline)

# Show current list of headlines
if any(st.session_state.headlines):
    st.write("**Input headlines:**")
    st.write([h for h in st.session_state.headlines if h.strip()])

# Submit button
if st.button("Score"):
    try:
        api_url = "http://0.0.0.0:8010/score_headlines"
        user_input = st.session_state.headlines
        payload = {"headlines": user_input}

        response = requests.post(api_url, json=payload)
        response.raise_for_status()

        st.success("Request successful! Headline labels shown below:")
        st.json(response.json())
    except requests.RequestException as e:
        st.error(f"Error sending POST request: {e}")
