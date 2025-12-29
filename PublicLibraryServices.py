import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(
    page_title="Public Library Services Explainer Bot",
    page_icon="📚",
    layout="centered"
)

st.title("📚 Public Library Services & Usage Explainer Bot")
st.caption("Explain-only AI assistant for public library services")

SYSTEM_PROMPT = """
You are a Public Library Services & Usage Explainer Bot.
Your role is strictly informational.

You may explain:
- Library membership rules
- Book borrowing and return processes
- Borrowing limits and overdue policies
- Digital library resources

You must NOT:
- Issue, renew, or reserve books
- Create or manage user accounts
- Access personal data
- Perform transactions

If asked to perform actions, politely refuse and explain that you only provide information.
Use simple, friendly language.
"""

client = genai.Client(
    api_key="AIzaSyD-9GNwa9i42Dbk0IEzuaGkbM0fSA9xoes"  # ⚠️ Paste locally only
)

MODEL_NAME = "gemini-3-flash-preview"

user_input = st.text_input(
    "Ask about library services:",
    placeholder="How does book borrowing work?"
)

if st.button("Explain") and user_input:
    with st.spinner("Explaining..."):
        contents = [
            types.Content(
                role="system",
                parts=[
                    types.Part.from_text(text=SYSTEM_PROMPT)
                ],
            ),
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(text=user_input)
                ],
            ),
        ]

        config = types.GenerateContentConfig(
            temperature=0.25,
            thinking_config=types.ThinkingConfig(
                thinking_level="HIGH"
            )
        )

        response_text = ""

        for chunk in client.models.generate_content_stream(
            model=MODEL_NAME,
            contents=contents,
            config=config,
        ):
            response_text += chunk.text or ""

        st.success("Explanation")
        st.write(response_text)

st.markdown("---")
st.caption(
    "⚠️ This bot provides explanations only. "
    "It does not issue books or manage user accounts."
)
