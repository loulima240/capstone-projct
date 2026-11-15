
"""
Player profiles for PadelBudy.

Demonstration profiles will later be replaced
or complemented by registered users stored in a database.
"""

import streamlit as st


# --- Demonstration player profiles ---

PLAYERS = [
    {
        "id": 1,
        "name": "João Silva",
        "age": 28,
        "location": "Cascais",
        "preferred_position": "Right",
        "dominant_hand": "Right",
        "level": "Intermediate"
    },
    {
        "id": 2,
        "name": "Maria Costa",
        "age": 25,
        "location": "Lisbon",
        "preferred_position": "Left",
        "dominant_hand": "Right",
        "level": "Beginner"
    },
    {
        "id": 3,
        "name": "Pedro Santos",
        "age": 32,
        "location": "Estoril",
        "preferred_position": "Right",
        "dominant_hand": "Left",
        "level": "Advanced"
    },
    {
        "id": 4,
        "name": "Ana Ferreira",
        "age": 27,
        "location": "Cascais",
        "preferred_position": "No preference",
        "dominant_hand": "Right",
        "level": "Intermediate"
    }
]


# --- Create a new player profile ---

def create_player_profile():

    st.subheader("Create Your Player Profile")

    with st.form("player_profile_form"):

        name = st.text_input("Full name")

        age = st.number_input(
            "Age",
            min_value=16,
            max_value=100,
            value=25
        )

        location = st.text_input(
            "Location",
            placeholder="e.g. Cascais, Estoril or Lisbon"
        )

        preferred_position = st.selectbox(
            "Preferred position",
            ["Right", "Left", "No preference"]
        )

        dominant_hand = st.selectbox(
            "Dominant hand",
            ["Right", "Left"]
        )

        level = st.selectbox(
            "Padel level",
            ["Beginner", "Intermediate", "Advanced"]
        )

        submitted = st.form_submit_button("Save profile")

        if submitted:

            if not name.strip() or not location.strip():
                st.error("Please fill in your name and location.")

            else:
                st.session_state.player_profile = {
                    "name": name,
                    "age": age,
                    "location": location,
                    "preferred_position": preferred_position,
                    "dominant_hand": dominant_hand,
                    "level": level
                }

                st.success("Your profile has been created!")
