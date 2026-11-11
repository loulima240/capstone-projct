
"""
Your first AI web application.

Run with:  uv run streamlit run app.py

This is where the course starts. Every week from here builds on it.
"""

import streamlit as st
import anthropic
from courts import COURTS

import config

st.set_page_config(
    page_title="Capstone Project",
    page_icon=":robot_face:",
    layout="centered"
)

st.title("Welcome to PadelBudy")

st.markdown(
    "Your intelligent padel companion. "
    "Find courts, discover players and organize your games."
)


st.subheader("Find the perfect padel court for your game")


# --- Court search form ---

with st.form("court_search_form"):

    location = st.text_input(
        "Where would you like to play?",
        placeholder="e.g. Cascais, Estoril or Lisbon"
    )

    date = st.date_input(
        "When would you like to play?"
    )

    preferred_time = st.selectbox(
        "Preferred time",
        [
            "Any time",
            "Morning",
            "Afternoon",
            "Evening"
        ]
    )

    

    court_type = st.selectbox(
        "Court type",
        ["Any", "Indoor", "Outdoor"]
    )

    search_button = st.form_submit_button(
        "Search for courts"
    )



if search_button:
    # Save search results in session state
    results = []

    for court in COURTS:

        # Filter by location
        if location.lower() not in court["location"].lower():
            continue

        # Filter by date
        if str(date) != court["date"]:
            continue

        # Filter by court type
        if court_type != "Any" and court_type != court["court_type"]:
            continue

        # Filter by preferred time
        hour = int(court["time"].split(":")[0])

        if preferred_time == "Morning" and hour >= 12:
            continue

        if preferred_time == "Afternoon" and (hour < 12 or hour >= 18):
            continue

        if preferred_time == "Evening" and hour < 18:
            continue

        results.append(court)

    st.session_state.search_results = results

    # Reset previous selection when a new search is made
    st.session_state.pop("selected_court", None)
    st.session_state.find_players = False


# --- Display search results ---

if "search_results" in st.session_state:

    st.subheader("Available courts")

    results = st.session_state.search_results

    if results:
        st.info("These are demonstration results, not live availability.")

        for court in results:
            with st.container(border=True):
                st.subheader(court["name"])
                st.write(f"Location: {court['location']}")
                st.write(f"Date: {court['date']}")
                st.write(f"Time: {court['time']}")
                st.write(f"Court type: {court['court_type']}")
                st.write(f"Price: €{court['price']}")
                st.caption(court["provider"])

                if st.button(
                    "Select this court",
                    key=f"select_{court['id']}"
                ):
                    st.session_state.selected_court = court
                    st.rerun()

    else:
        st.warning("No demonstration courts found for these criteria.")


        # --- Organise your game ---

if "selected_court" in st.session_state:
    selected_court = st.session_state.selected_court

    st.divider()
    st.subheader("Organise Your Game")

    st.success(f"You selected: {selected_court['name']}")

    players = st.selectbox(
        "How many players do you already have?",
        [1, 2, 3, 4]
    )

    if players == 4:
        st.success("Great! You already have a full team of four players.")

    else:
        missing_players = 4 - players

        st.info(
            f"You need {missing_players} more player(s) "
            "to complete your game."
        )

        if st.button("Find Players"):
            st.session_state.find_players = True

    if st.session_state.get("find_players", False):
        st.subheader("Find Players")
        st.write(
            "This feature will help you find other players "
            "to complete your padel game."
        )




# --- Key check ---
if not config.API_KEY:
    st.error("No API key found.")
    st.markdown(
        "Create a `.env` file from `.env.example` and fill in the "
        "`ANTHROPIC_API_KEY` line with your Anthropic API key."
    )
    st.stop()

# --- Chat session: kept between interactions ---
if "client" not in st.session_state:
    st.session_state.client = anthropic.Anthropic(
        api_key=config.API_KEY
    )

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- History ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- User input ---
if prompt := st.chat_input("Type something..."):
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            with st.spinner("Thinking..."):
                response = st.session_state.client.messages.create(
                    model=config.MODEL,
                    max_tokens=config.MAX_TOKENS,
                    system=config.SYSTEM_PROMPT,
                    messages=st.session_state.messages
                )

            answer = "\n".join(
                block.text
                for block in response.content
                if block.type == "text"
            )

            st.markdown(answer)

            st.session_state.messages.append(
                {"role": "assistant", "content": answer}
            )

        except Exception as e:
            st.error(f"The API call failed: {type(e).__name__}")
            st.caption(str(e)[:300])

with st.sidebar:
    st.subheader("What is happening")
    st.markdown(
        "Every message you send goes to the API, and the reply comes back here.\n\n"
        "`st.session_state` keeps the conversation between interactions. "
        "Without it, the model would forget everything after each message."
    )

    st.divider()
    st.caption(f"Model: `{config.MODEL}`")
    st.caption(
        f"Messages this session: {len(st.session_state.messages)}"
    )

    if st.button("Clear conversation"):
        st.session_state.messages = []
        st.rerun()
