import streamlit as st
from sentiment import predict_sentiment
from gpt import chat_with_gpt
from llm_wrapper import LocalLLMResponder, FlanT5Responder
from easter_eggs import check_easter_eggs
from tts import speak, stop
import os
import uuid
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Geeky GPT Chatbot 🤖", layout="wide")

with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "speaking_id" not in st.session_state:
    st.session_state.speaking_id = None

# ---------------- SIDEBAR ---------------- #
with st.sidebar:
    st.title("⚙️ Settings")
    model_choice = st.selectbox(
        "Choose Model",
        ["GPT (via API)", "Phi-2 (Local_Download)", "FLAN-T5 (AWS SageMaker)"],
        index=0
    )
    st.radio("🧪 Style Mode", ["Normal", "Techy"], horizontal=True, key="style_mode")

    if model_choice == "GPT (via API)":
        api_key = st.text_input("Enter your OpenAI API key", type="password")
        if api_key:
            os.environ["OPENAI_API_KEY"] = api_key

    if model_choice == "FLAN-T5 (AWS SageMaker)":
        restapi_url = st.text_input("Paste your FLAN-T5 Invoke URL", type="password")
        if restapi_url and not restapi_url.startswith("https://"):
            st.error("⚠️ Invalid URL. Please enter a valid FLAN-T5 Invoke URL.")
        if restapi_url:
            st.session_state["lambda_invoke_url"] = restapi_url

    st.divider()
    st.title("🎨 Chat Bubble Legend")
    st.markdown("- 🟢 **Positive** → Green animated glow")
    st.markdown("- 🔴 **Negative** → Red animated glow")
    st.markdown("- 🟡 **Neutral** → Yellow animated glow")

# ---------------- MAIN APP ---------------- #
st.title("💬 Geeky GPT + BERT + Phi-2 + FLAN-T5 Chatbot")
user_input = st.chat_input("Type your message here...")

DEFAULT_CONTEXT = "This chat is to support the user, and you are friendly, taking care of the user. You are a helpful assistant."

# Lazy-load models based on choice
if model_choice == "Phi-2 (Local_Download)" and "local_llm" not in st.session_state:
    st.session_state.local_llm = LocalLLMResponder()

if model_choice == "FLAN-T5 (AWS SageMaker)" and "flan_t5" not in st.session_state:
    lambda_url = st.session_state.get("lambda_invoke_url") or os.getenv("LAMBDA_INVOKE_URL")
    if lambda_url:
        st.session_state.flan_t5 = FlanT5Responder(lambda_url)

if user_input:
    sentiment = predict_sentiment(user_input)["label"]
    override = check_easter_eggs(user_input)

    if override:
        reply, model_used = override, "Easter Egg"

    elif model_choice == "GPT (via API)" and os.getenv("OPENAI_API_KEY"):
        reply = chat_with_gpt(user_input, style=st.session_state.style_mode.lower())
        model_used = "GPT"

    elif model_choice == "FLAN-T5 (AWS SageMaker)" and "flan_t5" in st.session_state:
        reply, model_used = st.session_state.flan_t5.generate_response(user_input, context=DEFAULT_CONTEXT)
        if not reply or reply.strip().lower() in ["no answer found.", "no valid response format found."]:
            reply = "⚠️ No answer from the API."

    elif model_choice == "Phi-2 (Local_Download)" and "local_llm" in st.session_state:
        reply, model_used = st.session_state.local_llm.generate_response(user_input)

    else:
        reply, model_used = "⚠️ Model not selected or not initialized.", "Error"

    st.session_state.chat_history.append({
        "id": str(uuid.uuid4()),
        "user": user_input,
        "bot": reply,
        "sentiment": sentiment,
        "model": model_used
    })

# ---------------- CHAT UI ---------------- #
for msg in st.session_state.chat_history:
    sentiment_class = {
        "Positive": "positive-border",
        "Negative": "negative-border",
        "Neutral": "neutral-border"
    }.get(msg["sentiment"], "neutral-border")

    st.markdown(f"""
    <div class='chat-bubble user-bubble {sentiment_class}'>
        🧑‍💻 <b>You:</b><br>{msg['user']}
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([0.9, 0.1])
    with col1:
        st.markdown(f"""
        <div class='chat-bubble bot-bubble {sentiment_class}'>
            🤖 <b>{msg['model']}:</b><br>{msg['bot']}
        </div>
        """, unsafe_allow_html=True)
    with col2:
        if st.button("🔊 Speak", key=f"speak_{msg['id']}"):
            speak(msg["bot"])
        if st.button("🛑 Stop", key=f"stop_{msg['id']}"):
            stop()
