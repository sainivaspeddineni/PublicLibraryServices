import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(
    page_title="Library Services Explainer",
    page_icon="📚",
    layout="centered"
)

st.markdown("""
<style>

/* Full page background image ONLY */
.stApp {
    background-image: url("https://tse4.mm.bing.net/th/id/OIP.tgQYDIWK0Z67zJ1pohyo4QHaEK?rs=1&pid=ImgDetMain&o=7&rm=3");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}

/* Remove default padding */
.block-container {
    padding-top: 1rem;
}

/* Header section */
.header-box {
    text-align: center;
    margin-bottom: 20px;
}

.header-title {
    padding: 0.8em;
    font-size: 36px;
    font-weight: 700;
    color: #ffffff;
}

.header-subtitle {
    border-radius: 2em;
    background-color: #ffffff;
    font-size: 16px;
    color: #444;
}

/* Image container */
.image-container {
    position: relative;
    text-align: center;
}

/* Answer card */
.response-box {
    background: rgb(14, 17, 23);
    color: #ffffff;
    padding: 24px;
    margin-top: 25px;
    border-radius: 16px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.15);
    font-size: 16px;
    line-height: 1.7;
}

/* Footer */
.footer {
    text-align: center;
    color: #444;
    font-size: 14px;
    margin-top: 30px;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="header-box">
    <div class="header-title">📚 Public Library Services Explainer</div>
    <div class="header-subtitle">
        Learn about memberships, borrowing rules, and digital resources
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="image-container">
    <img src="https://images.unsplash.com/photo-1524995997946-a1c2e315a42f"
         style="width:100%; height:320px; object-fit:cover; border-radius:18px;">
</div>
""", unsafe_allow_html=True)

user_input = st.text_input(
    "",
    placeholder="🔍 Ask about library services (e.g., borrowing limits)",
    key="search_box"
)

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
    api_key="AIzaSyD-9GNwa9i42Dbk0IEzuaGkbM0fSA9xoes"  # ⚠️ use env var in production
)

MODEL_NAME = "gemini-3-flash-preview"

if user_input:
    with st.spinner("Explaining..."):
        contents = [
            types.Content(
                role="system",
                parts=[types.Part.from_text(text=SYSTEM_PROMPT)],
            ),
            types.Content(
                role="user",
                parts=[types.Part.from_text(text=user_input)],
            ),
        ]

        config = types.GenerateContentConfig(
            temperature=0.25,
            thinking_config=types.ThinkingConfig(thinking_level="HIGH")
        )

        response_text = ""
        for chunk in client.models.generate_content_stream(
            model=MODEL_NAME,
            contents=contents,
            config=config,
        ):
            response_text += chunk.text or ""

        st.markdown(
            f'<div class="response-box">{response_text}</div>',
            unsafe_allow_html=True
        )

st.markdown(
    '<div class="footer">⚠️ Explanation-only bot. No book issuing or account management.</div>',
    unsafe_allow_html=True
)
