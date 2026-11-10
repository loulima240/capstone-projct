
"""
Your first AI web application.

Run with:  uv run streamlit run app.py

This is where the course starts. Every week from here builds on it.
"""

import streamlit as st
import anthropic

import config

st.set_page_config(
    page_title="Capstone Project",
    page_icon=":robot_face:",
    layout="centered"
)

st.title("My first AI app")

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
