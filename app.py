
import streamlit as st
import anthropic
import config
from courts import COURTS
from players import PLAYERS, create_player_profile
import json

# --- Page configuration ---

st.set_page_config(
    page_title="PadelBudy",
    page_icon="🎾",
    layout="centered"
)

# --- Header ---

title_col, profile_col = st.columns([5, 1])

with title_col:
    st.title("🎾 PadelBudy")

with profile_col:
    st.write("")
    if st.button("👤 Sign in", use_container_width=True):
        st.info("Profile and account creation coming soon.")

st.markdown(
    "Your intelligent padel companion. "
    "Let's organise your next game!"
)

st.divider()

# --- API key check ---

if not config.API_KEY:
    st.error("No API key found. Please check your .env file.")
    st.stop()

# --- Claude client ---

if "client" not in st.session_state:
    st.session_state.client = anthropic.Anthropic(
        api_key=config.API_KEY
    )

# --- Conversation history ---

if "messages" not in st.session_state:
    st.session_state.messages = []
# --- Court search state ---

if "search_criteria" not in st.session_state:
    st.session_state.search_criteria = {}

if "search_results" not in st.session_state:
    st.session_state.search_results = []

if "selected_court" not in st.session_state:
    st.session_state.selected_court = None

# --- Welcome message ---

if not st.session_state.messages:
    with st.chat_message("assistant"):
        st.markdown(
            "Hi! I'm PadelBudy. 🎾\n\n"
            "I can help you find a padel court and organise "
            "your game. Where would you like to play?"
        )

# --- Display conversation ---

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- Claude tool definition ---

COURT_SEARCH_TOOL = {
    "name": "search_courts",
    "description": (
        "Search the PadelBudy court database using the user's "
        "location, date, preferred time and court type. "
        "Use this tool when all four criteria are available."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": "The city or location."
            },
            "date": {
                "type": "string",
                "description": "Date in YYYY-MM-DD format."
            },
            "preferred_time": {
                "type": "string",
                "enum": [
                    "Any time",
                    "Morning",
                    "Afternoon",
                    "Evening"
                ]
            },
            "court_type": {
                "type": "string",
                "enum": ["Any", "Indoor", "Outdoor"]
            }
        },
        "required": [
            "location",
            "date",
            "preferred_time",
            "court_type"
        ]
    }
}

# --- Court selection tool ---

COURT_SELECTION_TOOL = {
    "name": "select_court",
    "description": (
        "Register the court selected by the user. "
        "Only select a court that exists in the previous search results."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "court_id": {
                "type": "integer",
                "description": "The ID of the selected court."
            }
        },
        "required": ["court_id"]
    }
}

# --- Court search helper ---

def search_courts(location, date, preferred_time, court_type):
    results = []

    for court in COURTS:
        if location.lower() not in court["location"].lower():
            continue

        if court["date"] != str(date):
            continue

        if court_type != "Any" and court["court_type"] != court_type:
            continue

        if preferred_time == "Morning" and int(court["time"][:2]) >= 12:
            continue

        if preferred_time == "Afternoon" and not (
            12 <= int(court["time"][:2]) < 18
        ):
            continue

        if preferred_time == "Evening" and int(court["time"][:2]) < 18:
            continue

        results.append(court)

    return results
# --- Execute court search tool ---

# --- Execute tools ---

def execute_tool(tool_name, tool_input):

    if tool_name == "search_courts":

        results = search_courts(
            location=tool_input["location"],
            date=tool_input["date"],
            preferred_time=tool_input["preferred_time"],
            court_type=tool_input["court_type"]
        )

        st.session_state.search_criteria = tool_input.copy()
        st.session_state.search_results = results
        st.session_state.selected_court = None

        return results

    elif tool_name == "select_court":

        court_id = tool_input["court_id"]

        for court in st.session_state.search_results:
            if court["id"] == court_id:

                st.session_state.selected_court = court

                return {
                    "success": True,
                    "selected_court": court
                }

        return {
            "success": False,
            "error": "Court not found in previous search results."
        }

    return {"error": "Unknown tool"}


if prompt := st.chat_input("Talk to PadelBudy..."):

    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            with st.spinner("PadelBudy is thinking..."):

                # Copy the conversation for the API
                api_messages = list(st.session_state.messages)

                # First call to Claude, with the court search tool
                response = st.session_state.client.messages.create(
                    model=config.MODEL,
                    max_tokens=config.MAX_TOKENS,
                    system=config.SYSTEM_PROMPT,
                    tools=[COURT_SEARCH_TOOL, COURT_SELECTION_TOOL],
                    messages=api_messages
                )

                # Execute tools requested by Claude
                while response.stop_reason == "tool_use":

                    api_messages.append({
                        "role": "assistant",
                        "content": response.content
                    })

                    tool_results = []

                    for block in response.content:
                        if block.type == "tool_use":

                            result = execute_tool(
                                block.name,
                                block.input
                            )

                            tool_results.append({
                                "type": "tool_result",
                                "tool_use_id": block.id,
                                "content": json.dumps(
                                    result,
                                    ensure_ascii=False
                                )
                            })

                    api_messages.append({
                        "role": "user",
                        "content": tool_results
                    })

                    # Send tool results back to Claude
                    response = st.session_state.client.messages.create(
                        model=config.MODEL,
                        max_tokens=config.MAX_TOKENS,
                        system=config.SYSTEM_PROMPT,
                        tools=[COURT_SEARCH_TOOL, COURT_SELECTION_TOOL],
                        messages=api_messages
                    )

            # Extract Claude's final answer
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
            st.error(
                f"Something went wrong: {type(e).__name__}"
            )
            st.caption(str(e)[:300])

