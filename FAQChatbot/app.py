import streamlit as st
from groq import Groq
from faq_data import faqs

# ════════════════════════════════════════════════════════
#  🔑  PASTE YOUR GROQ API KEY HERE
# ════════════════════════════════════════════════════════
GROQ_API_KEY = ""
# ════════════════════════════════════════════════════════

st.set_page_config(
    page_title="AskBot — FAQ Chatbot",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Mega CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,300;12..96,400;12..96,500;12..96,600;12..96,700;12..96,800&family=JetBrains+Mono:wght@300;400;500&display=swap');

/* ── Reset & Base ─────────────────────────────────────── */
*, *::before, *::after { box-sizing: border-box; }
html, body, [class*="css"] {
  font-family: 'Bricolage Grotesque', sans-serif !important;
  -webkit-font-smoothing: antialiased;
}

/* ── Full-bleed gradient background ─────────────────────── */
.stApp {
  background:
    radial-gradient(ellipse 80% 50% at 20% 0%, rgba(139,92,246,0.18) 0%, transparent 60%),
    radial-gradient(ellipse 60% 40% at 80% 10%, rgba(236,72,153,0.12) 0%, transparent 55%),
    radial-gradient(ellipse 50% 60% at 50% 100%, rgba(6,182,212,0.10) 0%, transparent 55%),
    #080811;
  min-height: 100vh;
}

/* ── Hide Streamlit chrome ───────────────────────────────── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }
[data-testid="stAppViewContainer"] > .main { padding: 0 !important; }

/* ── Layout wrapper ─────────────────────────────────────── */
.layout {
  display: grid;
  grid-template-columns: 280px 1fr;
  height: 100vh;
  overflow: hidden;
}

/* ══ LEFT SIDEBAR ══════════════════════════════════════════ */
.sidebar {
  background: rgba(255,255,255,0.025);
  border-right: 1px solid rgba(255,255,255,0.06);
  display: flex; flex-direction: column;
  padding: 1.5rem 1.2rem;
  overflow-y: auto;
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
}

.brand {
  display: flex; align-items: center; gap: 0.7rem;
  margin-bottom: 1.8rem; padding-bottom: 1.4rem;
  border-bottom: 1px solid rgba(255,255,255,0.06);
}
.brand-orb {
  width: 40px; height: 40px; border-radius: 12px; flex-shrink: 0;
  background: linear-gradient(135deg, #8b5cf6, #ec4899);
  display: flex; align-items: center; justify-content: center;
  font-size: 1.1rem;
  box-shadow: 0 0 20px rgba(139,92,246,0.4);
}
.brand-name {
  font-size: 1.15rem; font-weight: 800;
  background: linear-gradient(135deg, #c4b5fd, #f9a8d4);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  background-clip: text; line-height: 1;
}
.brand-sub { font-size: 0.68rem; color: rgba(255,255,255,0.25); margin-top: 2px; }

.sidebar-section-title {
  font-size: 0.62rem; font-weight: 700; letter-spacing: 0.16em;
  text-transform: uppercase; color: rgba(255,255,255,0.2);
  margin: 1.2rem 0 0.6rem; padding: 0 0.2rem;
}

.faq-group-label {
  font-size: 0.75rem; font-weight: 600; color: rgba(255,255,255,0.4);
  padding: 0.4rem 0.5rem 0.2rem;
}

.faq-chip {
  display: block; width: 100%;
  background: transparent;
  border: none; border-radius: 8px;
  padding: 0.45rem 0.65rem; margin-bottom: 2px;
  font-family: 'Bricolage Grotesque', sans-serif;
  font-size: 0.78rem; color: rgba(255,255,255,0.45);
  text-align: left; cursor: pointer;
  transition: all 0.15s ease;
}
.faq-chip:hover {
  background: rgba(139,92,246,0.12);
  color: #c4b5fd;
}

.sidebar-footer {
  margin-top: auto; padding-top: 1rem;
  border-top: 1px solid rgba(255,255,255,0.06);
  font-size: 0.68rem; color: rgba(255,255,255,0.15);
  font-family: 'JetBrains Mono', monospace;
  text-align: center; line-height: 1.6;
}

/* ══ RIGHT PANEL ═══════════════════════════════════════════ */
.main-panel {
  display: flex; flex-direction: column; height: 100vh; overflow: hidden;
}

/* Top bar */
.topbar {
  display: flex; align-items: center; justify-content: space-between;
  padding: 1.2rem 2rem;
  border-bottom: 1px solid rgba(255,255,255,0.05);
  background: rgba(255,255,255,0.015);
  backdrop-filter: blur(10px);
  flex-shrink: 0;
}
.topbar-title {
  font-size: 1rem; font-weight: 700; color: rgba(255,255,255,0.8);
}
.topbar-meta { font-size: 0.75rem; color: rgba(255,255,255,0.25); margin-top: 1px; }

.pill {
  display: inline-flex; align-items: center; gap: 0.4rem;
  background: rgba(139,92,246,0.12); border: 1px solid rgba(139,92,246,0.3);
  border-radius: 100px; padding: 0.25rem 0.8rem;
  font-size: 0.7rem; font-weight: 600;
  color: #c4b5fd; letter-spacing: 0.06em;
}
.pill-dot {
  width: 6px; height: 6px; border-radius: 50%;
  background: #a78bfa;
  animation: pulse-dot 2s infinite;
}
@keyframes pulse-dot {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.5; transform: scale(0.8); }
}

/* Stats row */
.stats-row {
  display: flex; gap: 1px;
  border-bottom: 1px solid rgba(255,255,255,0.05);
  flex-shrink: 0;
}
.stat-item {
  flex: 1; padding: 0.8rem 1.5rem;
  border-right: 1px solid rgba(255,255,255,0.04);
}
.stat-item:last-child { border-right: none; }
.stat-value {
  font-family: 'JetBrains Mono', monospace;
  font-size: 1.5rem; font-weight: 500;
  background: linear-gradient(135deg, #a78bfa, #f472b6);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  background-clip: text;
}
.stat-label {
  font-size: 0.62rem; text-transform: uppercase;
  letter-spacing: 0.12em; color: rgba(255,255,255,0.2);
  margin-top: 1px;
}

/* Chat area */
.chat-scroll {
  flex: 1; overflow-y: auto; padding: 2rem;
  scroll-behavior: smooth;
}
.chat-scroll::-webkit-scrollbar { width: 4px; }
.chat-scroll::-webkit-scrollbar-track { background: transparent; }
.chat-scroll::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.08); border-radius: 2px; }

/* Message bubbles */
.msg-wrap { display: flex; gap: 0.8rem; margin-bottom: 1.4rem; max-width: 820px; }
.msg-wrap.user { flex-direction: row-reverse; margin-left: auto; }

.avatar-badge {
  width: 34px; height: 34px; border-radius: 10px; flex-shrink: 0;
  display: flex; align-items: center; justify-content: center;
  font-size: 0.95rem;
}
.avatar-badge.bot {
  background: linear-gradient(135deg, rgba(139,92,246,0.25), rgba(236,72,153,0.25));
  border: 1px solid rgba(139,92,246,0.3);
}
.avatar-badge.usr {
  background: linear-gradient(135deg, rgba(6,182,212,0.2), rgba(59,130,246,0.2));
  border: 1px solid rgba(6,182,212,0.25);
}

.bubble {
  padding: 0.9rem 1.15rem;
  border-radius: 16px;
  font-size: 0.9rem;
  line-height: 1.65;
  max-width: 720px;
}
.bubble.bot-msg {
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.07);
  color: rgba(255,255,255,0.82);
  border-top-left-radius: 4px;
}
.bubble.user-msg {
  background: linear-gradient(135deg, rgba(139,92,246,0.2), rgba(236,72,153,0.15));
  border: 1px solid rgba(139,92,246,0.25);
  color: rgba(255,255,255,0.88);
  border-top-right-radius: 4px;
}
.bubble strong { color: #e2d9f3; }
.bubble code {
  background: rgba(0,0,0,0.3); color: #a78bfa;
  padding: 0.1rem 0.4rem; border-radius: 4px;
  font-family: 'JetBrains Mono', monospace; font-size: 0.82rem;
}

/* Welcome card */
.welcome-card {
  background: linear-gradient(135deg,
    rgba(139,92,246,0.08),
    rgba(236,72,153,0.06),
    rgba(6,182,212,0.05));
  border: 1px solid rgba(139,92,246,0.2);
  border-radius: 20px;
  padding: 2rem 2.4rem;
  max-width: 560px;
  margin: 1rem auto 2rem;
  text-align: center;
}
.welcome-orb {
  width: 56px; height: 56px; border-radius: 18px; margin: 0 auto 1rem;
  background: linear-gradient(135deg, #8b5cf6, #ec4899);
  display: flex; align-items: center; justify-content: center;
  font-size: 1.6rem;
  box-shadow: 0 8px 32px rgba(139,92,246,0.35);
}
.welcome-title {
  font-size: 1.4rem; font-weight: 800; color: rgba(255,255,255,0.9);
  margin-bottom: 0.5rem;
}
.welcome-sub { font-size: 0.88rem; color: rgba(255,255,255,0.38); line-height: 1.6; }
.welcome-tags {
  display: flex; flex-wrap: wrap; gap: 0.4rem;
  justify-content: center; margin-top: 1.2rem;
}
.tag {
  background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.08);
  border-radius: 100px; padding: 0.25rem 0.7rem;
  font-size: 0.72rem; color: rgba(255,255,255,0.4);
}

/* Input bar */
.input-bar {
  padding: 1rem 2rem 1.4rem;
  border-top: 1px solid rgba(255,255,255,0.05);
  flex-shrink: 0;
}

/* Streamlit chat input overrides */
[data-testid="stChatInput"],
[data-testid="stChatInput"] > div,
[data-testid="stChatInput"] > div > div,
[data-testid="stChatInput"] * {
  background: transparent !important;
  border: none !important;
  outline: none !important;
  box-shadow: none !important;
}
[data-testid="stChatInput"] {
  border-radius: 14px !important;
  background: rgba(18, 14, 35, 0.85) !important;
  border: 1px solid rgba(139,92,246,0.25) !important;
  padding: 0.2rem 0.4rem !important;
  transition: border-color 0.2s, box-shadow 0.2s !important;
}
[data-testid="stChatInput"]:focus-within {
  border-color: rgba(139,92,246,0.6) !important;
  box-shadow: 0 0 0 3px rgba(139,92,246,0.12) !important;
}
[data-testid="stChatInput"] textarea {
  background: transparent !important;
  color: rgba(220, 210, 255, 0.9) !important;
  font-family: 'Bricolage Grotesque', sans-serif !important;
  font-size: 0.93rem !important;
  caret-color: #a78bfa !important;
}
[data-testid="stChatInput"] textarea::placeholder {
  color: rgba(139,92,246,0.35) !important;
}
[data-testid="stChatInput"] button {
  background: linear-gradient(135deg, #8b5cf6, #ec4899) !important;
  border-radius: 10px !important;
  border: none !important;
}
[data-testid="stChatInput"] button:hover {
  opacity: 0.85 !important;
  box-shadow: 0 4px 16px rgba(139,92,246,0.4) !important;
}

/* Streamlit chat message overrides */
[data-testid="stChatMessage"] {
  background: transparent !important;
  border: none !important;
  padding: 0 !important;
  box-shadow: none !important;
}

/* Spinner */
.stSpinner > div { border-top-color: #8b5cf6 !important; }

/* Sidebar Streamlit overrides */
[data-testid="stSidebar"] { display: none !important; }

/* Buttons for FAQ chips in sidebar */
.stButton > button {
  background: transparent !important;
  border: 1px solid rgba(255,255,255,0.07) !important;
  border-radius: 8px !important;
  color: rgba(255,255,255,0.4) !important;
  font-family: 'Bricolage Grotesque', sans-serif !important;
  font-size: 0.78rem !important;
  font-weight: 400 !important;
  text-align: left !important;
  padding: 0.4rem 0.65rem !important;
  transition: all 0.15s !important;
}
.stButton > button:hover {
  background: rgba(139,92,246,0.1) !important;
  border-color: rgba(139,92,246,0.3) !important;
  color: #c4b5fd !important;
}

/* Clear button distinct */
.clear-btn > button {
  background: rgba(239,68,68,0.08) !important;
  border-color: rgba(239,68,68,0.2) !important;
  color: rgba(239,68,68,0.6) !important;
  border-radius: 10px !important;
  width: 100% !important;
}
.clear-btn > button:hover {
  background: rgba(239,68,68,0.15) !important;
  color: #f87171 !important;
}
</style>
""", unsafe_allow_html=True)

# ── FAQ context & system prompt ──────────────────────────────────────────────
FAQ_CONTEXT = "\n\n".join(f"Q: {f['question']}\nA: {f['answer']}" for f in faqs)

SYSTEM_PROMPT = f"""You are AskBot, a sharp and helpful AI FAQ assistant for CodeAlpha's AI Internship.
Use the FAQ knowledge base below as your primary source. Answer concisely and clearly.
Use markdown (bold, code, bullet lists) where it improves readability. Be friendly but efficient.

=== FAQ KNOWLEDGE BASE ===
{FAQ_CONTEXT}
=== END ==="""

# ── Session state ────────────────────────────────────────────────────────────
for key, val in [("messages", []), ("groq_history", []), ("total_queries", 0), ("inject_q", None)]:
    if key not in st.session_state:
        st.session_state[key] = val

# ── Groq call ────────────────────────────────────────────────────────────────
def ask_groq(user_message: str) -> str:
    client = Groq(api_key=GROQ_API_KEY)
    st.session_state.groq_history.append({"role": "user", "content": user_message})
    resp = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": SYSTEM_PROMPT}] + st.session_state.groq_history,
        temperature=0.4,
        max_tokens=600,
    )
    answer = resp.choices[0].message.content
    st.session_state.groq_history.append({"role": "assistant", "content": answer})
    if len(st.session_state.groq_history) > 20:
        st.session_state.groq_history = st.session_state.groq_history[-20:]
    return answer

# ── FAQ groups ───────────────────────────────────────────────────────────────
GROUPS = {
    "🎓 Internship": [],
    "🐍 Python":     [],
    "🤖 AI / ML":    [],
    "🔭 Other":      [],
}
for f in faqs:
    q = f["question"]
    if any(k in q for k in ["CodeAlpha","internship","task","certificate","submit","GitHub","contact"]):
        GROUPS["🎓 Internship"].append(q)
    elif any(k in q for k in ["Python","pip","virtual","Streamlit","scikit","NLTK","OpenCV"]):
        GROUPS["🐍 Python"].append(q)
    elif any(k in q for k in ["machine learning","deep learning","NLP","neural","TF-IDF","cosine",
                               "chatbot","TensorFlow","PyTorch","dataset","overfitting","AI","LSTM"]):
        GROUPS["🤖 AI / ML"].append(q)
    else:
        GROUPS["🔭 Other"].append(q)

# ════════════════════════════════════════════════════════
#  RENDER — Two-column custom layout using st.columns
# ════════════════════════════════════════════════════════
col_side, col_main = st.columns([1.05, 3.6], gap="small")

# ── LEFT SIDEBAR ─────────────────────────────────────────────────────────────
with col_side:
    st.markdown("""
    <div class="sidebar">
      <div class="brand">
        <div class="brand-orb">✦</div>
        <div>
          <div class="brand-name">AskBot</div>
          <div class="brand-sub">FAQ · GROQ AI · LLaMA 3.3</div>
        </div>
      </div>
      <div class="sidebar-section-title">Topics</div>
    </div>
    """, unsafe_allow_html=True)

    # FAQ groups with clickable buttons
    for group, questions in GROUPS.items():
        if questions:
            with st.expander(f"{group}  ({len(questions)})", expanded=False):
                for q in questions:
                    if st.button(q, key=f"q_{hash(q)}", use_container_width=True):
                        st.session_state.inject_q = q
                        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="clear-btn">', unsafe_allow_html=True)
        if st.button("⌫  Clear conversation", use_container_width=True):
            st.session_state.messages = []
            st.session_state.groq_history = []
            st.session_state.total_queries = 0
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    total = st.session_state.total_queries
    st.markdown(f"""
    <div class="sidebar-footer">
      llama-3.3-70b-versatile<br>
      {len(faqs)} FAQs loaded · {total} queries
    </div>
    """, unsafe_allow_html=True)

# ── RIGHT MAIN PANEL ──────────────────────────────────────────────────────────
with col_main:
    total = st.session_state.total_queries
    matched = sum(1 for m in st.session_state.messages if m["role"] == "assistant")
    rate = f"{int(matched/total*100)}%" if total > 0 else "—"

    # Top bar
    st.markdown(f"""
    <div class="topbar">
      <div>
        <div class="topbar-title">FAQ Assistant</div>
        <div class="topbar-meta">CodeAlpha AI Internship · Task 2</div>
      </div>
      <div class="pill"><div class="pill-dot"></div> Groq · LLaMA 3.3 70B</div>
    </div>
    """, unsafe_allow_html=True)

    # Stats
    st.markdown(f"""
    <div class="stats-row">
      <div class="stat-item">
        <div class="stat-value">{len(faqs)}</div>
        <div class="stat-label">FAQs Loaded</div>
      </div>
      <div class="stat-item">
        <div class="stat-value">{total}</div>
        <div class="stat-label">Queries Asked</div>
      </div>
      <div class="stat-item">
        <div class="stat-value">{rate}</div>
        <div class="stat-label">Response Rate</div>
      </div>
      <div class="stat-item">
        <div class="stat-value" style="font-size:0.95rem;margin-top:4px;">llama-3.3-70b</div>
        <div class="stat-label">Model</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Chat messages area ──────────────────────────────────────────────────
    if not st.session_state.messages:
        st.markdown("""
        <div style="padding: 2rem;">
          <div class="welcome-card">
            <div class="welcome-orb">✦</div>
            <div class="welcome-title">Hey, I'm AskBot</div>
            <div class="welcome-sub">
              Your AI-powered FAQ assistant, fuelled by Groq's LLaMA 3.<br>
              Ask me anything about the internship, Python, or AI/ML.
            </div>
            <div class="welcome-tags">
              <span class="tag">CodeAlpha</span>
              <span class="tag">Python</span>
              <span class="tag">Machine Learning</span>
              <span class="tag">NLP</span>
              <span class="tag">Streamlit</span>
              <span class="tag">YOLO</span>
              <span class="tag">TF-IDF</span>
              <span class="tag">Deep Learning</span>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown('<div style="padding: 1.5rem 2rem 0;">', unsafe_allow_html=True)
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                st.markdown(f"""
                <div class="msg-wrap user">
                  <div class="avatar-badge usr">👤</div>
                  <div class="bubble user-msg">{msg["content"]}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                import html as html_lib
                safe = html_lib.escape(msg["content"]).replace('\n', '<br>')
                st.markdown(f"""
                <div class="msg-wrap">
                  <div class="avatar-badge bot">✦</div>
                  <div class="bubble bot-msg">{msg["content"]}</div>
                </div>
                """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Chat input ──────────────────────────────────────────────────────────
    st.markdown('<div style="padding: 0 1rem;">', unsafe_allow_html=True)
    prompt = st.chat_input("Ask anything — internship, Python, AI, ML…")
    st.markdown('</div>', unsafe_allow_html=True)

    # Handle sidebar injection
    injected = st.session_state.inject_q
    if injected:
        st.session_state.inject_q = None
        user_query = injected
    elif prompt:
        user_query = prompt
    else:
        user_query = None

    # Process query
    if user_query:
        st.session_state.messages.append({"role": "user", "content": user_query})
        st.session_state.total_queries += 1

        with st.spinner(""):
            try:
                answer = ask_groq(user_query)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            except Exception as e:
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"⚠️ Error: `{e}`\n\nCheck that your `GROQ_API_KEY` is set correctly in `app.py`."
                })
        st.rerun()