import streamlit as st
from langgraph_backend import chatbot
from langchain_core.messages import HumanMessage
import uuid


#utility functions
def generate_thread_id():
    thread_id=uuid.uuid4()
    return thread_id

def reset_chat():
    thread_id=generate_thread_id()
    st.session_state['thread_id']=thread_id
    add_thread(st.session_state['thread_id'])
    st.session_state['message_history'] = []
def add_thread(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)
def load_conversation(thread_id):
    state = chatbot.get_state(config={'configurable': {'thread_id': thread_id}})
    # Check if messages key exists in state values, return empty list if not
    return state.values.get('messages', [])

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Puku · AI Assistant",
    page_icon="✦",
    layout="centered",
)



# ── Injected CSS & animations ──────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400&display=swap');

/* ── Reset & base ── */
html, body, [data-testid="stAppViewContainer"] {
    background: #08090d !important;
}

[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(ellipse 80% 50% at 50% -10%, rgba(99,102,241,.18) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 90%, rgba(236,72,153,.10) 0%, transparent 55%),
        #08090d !important;
}

[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stBottom"] { background: transparent !important; }
.block-container { padding: 0 !important; max-width: 760px !important; }

* { font-family: 'DM Mono', monospace; }

/* ── Hero header ── */
.nova-header {
    text-align: center;
    padding: 3.2rem 0 1.8rem;
    animation: fadeDown .7s cubic-bezier(.22,1,.36,1) both;
}
.nova-header .logo {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 2.6rem;
    letter-spacing: -.02em;
    background: linear-gradient(135deg, #e0e7ff 0%, #a5b4fc 40%, #f9a8d4 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1;
}
.nova-header .sub {
    margin-top: .45rem;
    font-size: .72rem;
    letter-spacing: .18em;
    text-transform: uppercase;
    color: rgba(165,180,252,.45);
}
.nova-divider {
    width: 48px; height: 2px;
    margin: 1.1rem auto 0;
    background: linear-gradient(90deg, #6366f1, #f472b6);
    border-radius: 2px;
}

/* ── Chat container ── */
.chat-wrap {
    padding: 0 1.2rem 1rem;
}

/* ── Messages ── */
[data-testid="stChatMessage"] {
    background: transparent !important;
    border: none !important;
    padding: .15rem 0 !important;
    animation: slideUp .45s cubic-bezier(.22,1,.36,1) both;
}

/* User bubble */
[data-testid="stChatMessage"][data-testid*="user"] .stMarkdown,
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) [data-testid="stMarkdownContainer"] p {
    background: linear-gradient(135deg, #4f46e5 0%, #6366f1 100%) !important;
    color: #eef2ff !important;
    border-radius: 18px 18px 4px 18px !important;
    padding: .75rem 1.1rem !important;
    display: inline-block;
    max-width: 82%;
    box-shadow: 0 4px 24px rgba(99,102,241,.28);
}

/* Assistant bubble */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) [data-testid="stMarkdownContainer"] p {
    background: rgba(255,255,255,.04) !important;
    border: 1px solid rgba(255,255,255,.07) !important;
    color: #e2e8f0 !important;
    border-radius: 18px 18px 18px 4px !important;
    padding: .75rem 1.1rem !important;
    display: inline-block;
    max-width: 88%;
    backdrop-filter: blur(12px);
    box-shadow: 0 2px 16px rgba(0,0,0,.3);
}

/* Avatars */
[data-testid="chatAvatarIcon-user"] {
    background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
    border-radius: 50% !important;
    color: white !important;
    font-size: .7rem !important;
}
[data-testid="chatAvatarIcon-assistant"] {
    background: linear-gradient(135deg, #1e1b4b, #312e81) !important;
    border: 1px solid rgba(99,102,241,.4) !important;
    border-radius: 50% !important;
    color: #a5b4fc !important;
    font-size: .7rem !important;
}

/* ── Chat input ── */
[data-testid="stChatInput"] {
    background: rgba(255,255,255,.04) !important;
    border: 1px solid rgba(255,255,255,.1) !important;
    border-radius: 16px !important;
    backdrop-filter: blur(16px) !important;
    box-shadow: 0 0 0 0 rgba(99,102,241,0), 0 8px 32px rgba(0,0,0,.4) !important;
    transition: border-color .25s, box-shadow .25s !important;
}
[data-testid="stChatInput"]:focus-within {
    border-color: rgba(99,102,241,.6) !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,.15), 0 8px 32px rgba(0,0,0,.4) !important;
}
[data-testid="stChatInput"] textarea {
    color: #e2e8f0 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: .85rem !important;
    background: transparent !important;
}
[data-testid="stChatInput"] textarea::placeholder {
    color: rgba(148,163,184,.35) !important;
}
[data-testid="stChatInput"] button {
    background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
    border-radius: 10px !important;
    border: none !important;
    transition: opacity .2s, transform .15s !important;
}
[data-testid="stChatInput"] button:hover {
    opacity: .85 !important;
    transform: scale(1.06) !important;
}

/* ── Empty state ── */
.empty-state {
    text-align: center;
    padding: 3.5rem 2rem;
    animation: fadeUp .8s .2s cubic-bezier(.22,1,.36,1) both;
}
.empty-state .orb {
    width: 72px; height: 72px;
    margin: 0 auto 1.4rem;
    border-radius: 50%;
    background: linear-gradient(135deg, #4f46e5 0%, #ec4899 100%);
    display: flex; align-items: center; justify-content: center;
    font-size: 1.8rem;
    box-shadow: 0 0 40px rgba(99,102,241,.35), 0 0 80px rgba(236,72,153,.15);
    animation: pulse 3s ease-in-out infinite;
}
.empty-state h3 {
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 1.25rem;
    color: #e2e8f0;
    margin-bottom: .5rem;
}
.empty-state p {
    font-size: .78rem;
    color: rgba(148,163,184,.55);
    line-height: 1.6;
    max-width: 320px;
    margin: 0 auto;
}
.suggestions {
    display: flex;
    flex-wrap: wrap;
    gap: .5rem;
    justify-content: center;
    margin-top: 1.4rem;
}
.chip {
    background: rgba(99,102,241,.12);
    border: 1px solid rgba(99,102,241,.25);
    color: #a5b4fc;
    border-radius: 999px;
    padding: .4rem .9rem;
    font-size: .72rem;
    letter-spacing: .03em;
    cursor: pointer;
    transition: background .2s, border-color .2s, transform .15s;
}
.chip:hover {
    background: rgba(99,102,241,.22);
    border-color: rgba(99,102,241,.5);
    transform: translateY(-1px);
}

/* ── Keyframes ── */
@keyframes fadeDown {
    from { opacity: 0; transform: translateY(-18px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(18px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes slideUp {
    from { opacity: 0; transform: translateY(12px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes pulse {
    0%, 100% { box-shadow: 0 0 40px rgba(99,102,241,.35), 0 0 80px rgba(236,72,153,.15); }
    50%       { box-shadow: 0 0 60px rgba(99,102,241,.55), 0 0 100px rgba(236,72,153,.25); }
}

/* ── Typing indicator ── */
.typing-dots {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    padding: .6rem .9rem;
    background: rgba(255,255,255,.04);
    border: 1px solid rgba(255,255,255,.07);
    border-radius: 18px 18px 18px 4px;
    margin: .25rem 0;
}
.typing-dots span {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: #a5b4fc;
    animation: bounce .9s ease-in-out infinite;
}
.typing-dots span:nth-child(2) { animation-delay: .15s; }
.typing-dots span:nth-child(3) { animation-delay: .30s; }
@keyframes bounce {
    0%, 80%, 100% { transform: scale(.75); opacity: .4; }
    40%            { transform: scale(1.1); opacity: 1;  }
}

/* Scrollbar */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(99,102,241,.3); border-radius: 4px; }
</style>
""", unsafe_allow_html=True)


# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="nova-header">
    <div class="logo">✦ Puku</div>
    <div class="sub">Powered by LangGraph · Always thinking</div>
    <div class="nova-divider"></div>
</div>
""", unsafe_allow_html=True)

# ── Session state ──────────────────────────────────────────────────────────────
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []
if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()
if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = []

add_thread(st.session_state['thread_id'])

# ── Sidebar ─────────────────────────────────────────────────────────────────────
st.sidebar.title('Chatbot')
if st.sidebar.button('New Chat'):
    reset_chat()

st.sidebar.header('My Conversations')
st.sidebar.text("Current Thread ID:")
for thread_id in st.session_state['chat_threads']:
   if st.sidebar.button(str(thread_id)):
       st.session_state['thread_id'] = thread_id
       messages = load_conversation(thread_id)

       temp_messages = []

       for msg in messages:
            if isinstance(msg, HumanMessage):
                role='user'
            else:
                role='assistant'
            temp_messages.append({'role': role, 'content': msg.content})

       st.session_state['message_history'] = temp_messages
# ── Input ──────────────────────────────────────────────────────────────────────
user_input = st.chat_input("Ask anything…")

CONFIG = {'configurable': {'thread_id': st.session_state['thread_id']}}

if user_input:
    # Append & render user message
    st.session_state['message_history'].append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):
        st.markdown(user_input)

    # Stream assistant response
    with st.chat_message('assistant'):
        ai_message = st.write_stream(
            message_chunk.content
            for message_chunk, metadata in chatbot.stream(
                {'messages': [HumanMessage(content=user_input)]},
                config=CONFIG,
                stream_mode='messages',
            )
            if message_chunk.content
        )

    st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})