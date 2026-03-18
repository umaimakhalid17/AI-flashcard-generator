import streamlit as st
import json
import re
import random
import requests

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="FlashAI",
    page_icon="🃏",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
}

.stApp { background: #f0f2f7; }

section[data-testid="stSidebar"] {
    background: #ffffff !important;
    border-right: 1px solid #e2e5ef !important;
    box-shadow: 2px 0 12px rgba(0,0,0,0.04);
}
section[data-testid="stSidebar"] * { color: #374151 !important; }

.hero-wrap {
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #a78bfa 100%);
    border-radius: 20px;
    padding: 2rem 2.5rem;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
}
.hero-wrap::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 220px; height: 220px;
    border-radius: 50%;
    background: rgba(255,255,255,0.08);
}
.hero-title {
    font-size: 2.4rem;
    font-weight: 800;
    color: #ffffff;
    letter-spacing: -1.5px;
    line-height: 1.1;
    margin: 0 0 0.4rem 0;
}
.hero-sub {
    font-family: 'JetBrains Mono', monospace;
    color: rgba(255,255,255,0.7);
    font-size: 0.8rem;
    letter-spacing: 0.04em;
}

.pill-row { display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 1.5rem; }
.pill {
    background: #fff;
    border: 1px solid #e2e5ef;
    border-radius: 999px;
    padding: 5px 14px;
    font-size: 0.78rem;
    color: #6b7280;
    font-weight: 500;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06);
}
.pill b { color: #6366f1; }

/* 3D FLIP CARDS */
.flip-scene {
    perspective: 1000px;
    margin-bottom: 1.2rem;
    height: 210px;
    cursor: pointer;
}
.flip-card {
    width: 100%;
    height: 210px;
    position: relative;
    transform-style: preserve-3d;
    transition: transform 0.65s cubic-bezier(0.23, 1, 0.32, 1);
}
.flip-card.flipped { transform: rotateY(180deg); }

.flip-front, .flip-back {
    position: absolute;
    width: 100%;
    height: 100%;
    backface-visibility: hidden;
    -webkit-backface-visibility: hidden;
    border-radius: 16px;
    padding: 1.4rem;
    box-sizing: border-box;
}
.flip-front {
    background: #ffffff;
    border: 1px solid #e2e5ef;
    box-shadow: 0 4px 16px rgba(0,0,0,0.06);
    transition: box-shadow 0.3s ease, border-color 0.3s ease;
}
.flip-scene:hover .flip-front {
    box-shadow: 0 8px 28px rgba(99,102,241,0.15);
    border-color: #c7d2fe;
}
.flip-back {
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    transform: rotateY(180deg);
    box-shadow: 0 8px 24px rgba(99,102,241,0.3);
}

.card-num {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.62rem;
    color: #9ca3af;
    letter-spacing: 0.12em;
    margin-bottom: 0.6rem;
    text-transform: uppercase;
}
.card-q { font-size: 0.93rem; font-weight: 600; color: #111827; line-height: 1.55; }
.card-q-back {
    font-size: 0.78rem;
    color: rgba(255,255,255,0.75);
    line-height: 1.4;
    margin-bottom: 0.7rem;
    font-family: 'JetBrains Mono', monospace;
}
.card-a-back { font-size: 0.9rem; color: #ffffff; line-height: 1.55; font-weight: 500; }

.diff-badge {
    display: inline-block;
    font-size: 0.6rem;
    font-weight: 700;
    padding: 3px 10px;
    border-radius: 999px;
    letter-spacing: 0.08em;
    position: absolute;
    top: 1rem; right: 1rem;
    text-transform: uppercase;
}
.easy   { background: #dcfce7; color: #15803d; }
.medium { background: #fef9c3; color: #a16207; }
.hard   { background: #fee2e2; color: #b91c1c; }

.flip-hint {
    position: absolute;
    bottom: 0.8rem; right: 1.2rem;
    font-size: 0.62rem;
    color: #d1d5db;
    font-family: 'JetBrains Mono', monospace;
}

/* QUIZ */
.quiz-card-3d {
    background: #fff;
    border: 1px solid #e2e5ef;
    border-radius: 20px;
    padding: 2.5rem;
    text-align: center;
    box-shadow: 0 8px 32px rgba(0,0,0,0.06);
    transform: perspective(800px) rotateX(2deg);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    position: relative;
    overflow: hidden;
    margin-bottom: 1.5rem;
}
.quiz-card-3d::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 4px;
    background: linear-gradient(90deg, #6366f1, #8b5cf6, #a78bfa);
}
.quiz-card-3d:hover {
    transform: perspective(800px) rotateX(0deg) translateY(-3px);
    box-shadow: 0 16px 48px rgba(99,102,241,0.12);
}
.quiz-q {
    font-size: 1.2rem;
    font-weight: 700;
    color: #111827;
    line-height: 1.5;
    margin-top: 0.8rem;
}
.quiz-ans-box {
    background: linear-gradient(135deg, #ede9fe, #f0f9ff);
    border: 1px solid #c4b5fd;
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    font-size: 0.92rem;
    color: #4c1d95;
    line-height: 1.6;
    text-align: left;
    font-weight: 500;
    margin-bottom: 1rem;
    animation: slideUp 0.4s cubic-bezier(0.23, 1, 0.32, 1);
}
@keyframes slideUp {
    from { opacity: 0; transform: translateY(10px); }
    to   { opacity: 1; transform: translateY(0); }
}

.prog-track {
    background: #e2e5ef;
    border-radius: 999px;
    height: 6px;
    overflow: hidden;
    margin: 0.5rem 0 1.5rem;
}
.prog-fill {
    height: 100%;
    border-radius: 999px;
    background: linear-gradient(90deg, #6366f1, #a78bfa);
    transition: width 0.5s cubic-bezier(0.23, 1, 0.32, 1);
}

.score-card {
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    border-radius: 20px;
    padding: 2.5rem;
    text-align: center;
    color: #fff;
    box-shadow: 0 12px 40px rgba(99,102,241,0.35);
    margin-bottom: 1.5rem;
}
.score-big { font-size: 4rem; font-weight: 800; letter-spacing: -2px; line-height: 1; }
.score-label { opacity: 0.8; font-size: 0.9rem; margin-top: 0.5rem; }

.stButton > button {
    background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    padding: 0.6rem 1.5rem !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 12px rgba(99,102,241,0.25) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(99,102,241,0.4) !important;
}

.stTextArea textarea, .stTextInput input {
    background: #fff !important;
    border: 1px solid #e2e5ef !important;
    border-radius: 10px !important;
    color: #111827 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.85rem !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05) !important;
}
.stTextArea textarea:focus, .stTextInput input:focus {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.12) !important;
}
.stSelectbox > div > div {
    background: #fff !important;
    border: 1px solid #e2e5ef !important;
    border-radius: 10px !important;
    color: #111827 !important;
}

.empty-state {
    text-align: center;
    padding: 4rem 2rem;
    background: #fff;
    border-radius: 20px;
    border: 2px dashed #c7d2fe;
}
.empty-icon { font-size: 3.5rem; margin-bottom: 1rem; }
.empty-text {
    font-family: 'JetBrains Mono', monospace;
    color: #9ca3af;
    font-size: 0.85rem;
    line-height: 1.8;
}

label[data-testid="stWidgetLabel"] p {
    color: #6b7280 !important;
    font-size: 0.8rem !important;
    font-weight: 600 !important;
}
hr { border-color: #e2e5ef !important; }
.stMarkdown p { color: #6b7280; }
</style>

<script>
function flipCard(id) {
    const el = document.getElementById(id);
    if (el) el.classList.toggle('flipped');
}
</script>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
defaults = {
    "flashcards": [], "quiz_index": 0, "show_answer": False,
    "quiz_score": 0, "quiz_answered": set(), "mode": "Browse"
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    st.markdown("---")
    api_key = st.text_input(
        "Groq API Key",
        type="password",
        placeholder="gsk_...",
    )
    st.caption("🆓 Free key → [console.groq.com](https://console.groq.com)")
    st.markdown("---")
    num_cards = st.slider("Number of Cards", 3, 20, 8)
    difficulty = st.selectbox("Difficulty Mix", [
        "Mixed (Easy + Medium + Hard)", "Easy only", "Medium only", "Hard only"
    ])
    card_style = st.selectbox("Card Style", [
        "Q&A Pairs", "Fill in the Blank", "True/False", "Definition Style"
    ])
    st.markdown("---")
    if st.session_state.flashcards:
        st.markdown(f"**{len(st.session_state.flashcards)}** cards · **{st.session_state.quiz_score}** correct")
        if st.button("🗑 Clear All", use_container_width=True):
            st.session_state.flashcards = []
            st.session_state.quiz_index = 0
            st.session_state.show_answer = False
            st.session_state.quiz_score = 0
            st.session_state.quiz_answered = set()
            st.session_state.mode = "Browse"
            st.rerun()

# ── Generate via Groq ─────────────────────────────────────────────────────────
def generate_flashcards(api_key, topic, num_cards, difficulty, card_style):
    diff_map = {
        "Mixed (Easy + Medium + Hard)": "Mix easy, medium, and hard difficulty evenly.",
        "Easy only": "All easy — basic recall.",
        "Medium only": "All medium — application and understanding.",
        "Hard only": "All hard — analysis, edge cases, synthesis.",
    }
    style_map = {
        "Q&A Pairs": "Classic question and answer.",
        "Fill in the Blank": "Fill-in-the-blank with key term missing.",
        "True/False": "True/False with explanation in answer.",
        "Definition Style": "Front: term. Back: precise definition with context.",
    }

    prompt = f"""You are an expert educator. Generate exactly {num_cards} flashcards about:

TOPIC/TEXT:
{topic}

STYLE: {style_map[card_style]}
DIFFICULTY: {diff_map[difficulty]}

Reply ONLY with a valid JSON array. No markdown fences, no preamble, nothing else.
Each object must have exactly: "question" (string), "answer" (string), "difficulty" ("easy"|"medium"|"hard").
Start your reply with [ and end with ]"""

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 3000,
    }

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers=headers,
        json=payload,
        timeout=30
    )
    response.raise_for_status()
    raw = response.json()["choices"][0]["message"]["content"].strip()
    raw = re.sub(r"```json|```", "", raw).strip()
    return json.loads(raw)

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-wrap">
    <div class="hero-title">🃏 FlashAI</div>
    <div class="hero-sub">// powered by Groq · paste any topic → instant flashcards</div>
</div>
""", unsafe_allow_html=True)

if st.session_state.flashcards:
    cards = st.session_state.flashcards
    e = sum(1 for c in cards if c.get("difficulty") == "easy")
    m = sum(1 for c in cards if c.get("difficulty") == "medium")
    h = sum(1 for c in cards if c.get("difficulty") == "hard")
    st.markdown(f"""
    <div class="pill-row">
        <div class="pill">Total <b>{len(cards)}</b></div>
        <div class="pill">Easy <b>{e}</b></div>
        <div class="pill">Medium <b>{m}</b></div>
        <div class="pill">Hard <b>{h}</b></div>
    </div>""", unsafe_allow_html=True)

# ── Input ─────────────────────────────────────────────────────────────────────
with st.expander("✨ Generate New Flashcards", expanded=not bool(st.session_state.flashcards)):
    topic_input = st.text_area(
        "Topic or Paste any Text",
        height=150,
        placeholder="e.g. 'Photosynthesis' or paste a paragraph from your textbook..."
    )
    c1, c2 = st.columns([1, 3])
    with c1:
        gen_btn = st.button("⚡ Generate Cards", use_container_width=True)

    if gen_btn:
        if not api_key:
            st.error("Please enter your Groq API key in the sidebar.")
        elif not topic_input.strip():
            st.error("Please enter a topic or text.")
        else:
            with st.spinner("Generating with Groq (llama-3.3-70b)..."):
                try:
                    cards = generate_flashcards(api_key, topic_input.strip(), num_cards, difficulty, card_style)
                    st.session_state.flashcards = cards
                    st.session_state.quiz_index = 0
                    st.session_state.show_answer = False
                    st.session_state.quiz_score = 0
                    st.session_state.quiz_answered = set()
                    st.session_state.mode = "Browse"
                    st.success(f"✅ {len(cards)} flashcards generated!")
                    st.rerun()
                except json.JSONDecodeError:
                    st.error("Couldn't parse AI response. Please try again.")
                except requests.HTTPError as e:
                    st.error(f"API Error: {e.response.status_code} — {e.response.text}")
                except Exception as ex:
                    st.error(f"Error: {ex}")

st.markdown("---")

# ── Mode navigation ───────────────────────────────────────────────────────────
if st.session_state.flashcards:
    n1, n2 = st.columns(2)
    with n1:
        if st.button("📋  Browse Mode", use_container_width=True):
            st.session_state.mode = "Browse"
            st.rerun()
    with n2:
        if st.button("🎯  Quiz Mode", use_container_width=True):
            st.session_state.mode = "Quiz Mode"
            st.session_state.quiz_index = 0
            st.session_state.show_answer = False
            st.session_state.quiz_score = 0
            st.session_state.quiz_answered = set()
            random.shuffle(st.session_state.flashcards)
            st.rerun()

# ── Empty state ───────────────────────────────────────────────────────────────
if not st.session_state.flashcards:
    st.markdown("""
    <div class="empty-state">
        <div class="empty-icon">🃏</div>
        <div class="empty-text">No cards yet.<br>Enter a topic above and hit Generate.</div>
    </div>""", unsafe_allow_html=True)

# ── Browse ────────────────────────────────────────────────────────────────────
elif st.session_state.mode == "Browse":
    st.markdown("### 📋 Your Flashcards")
    st.caption("✨ Click any card to flip and reveal the answer")

    filter_d = st.radio("Filter by difficulty:", ["All", "Easy", "Medium", "Hard"], horizontal=True)

    show_cards = st.session_state.flashcards
    if filter_d != "All":
        show_cards = [c for c in show_cards if c.get("difficulty","").lower() == filter_d.lower()]

    cols = st.columns(2)
    for i, card in enumerate(show_cards):
        diff = card.get("difficulty", "medium").lower()
        cid  = f"fc_{i}"
        q_short = card['question'][:55] + ("..." if len(card['question']) > 55 else "")
        with cols[i % 2]:
            st.markdown(f"""
            <div class="flip-scene" onclick="flipCard('{cid}')">
              <div class="flip-card" id="{cid}">
                <div class="flip-front">
                  <span class="diff-badge {diff}">{diff}</span>
                  <div class="card-num">Card {i+1:02d} &nbsp;·&nbsp; click to flip</div>
                  <div class="card-q">{card['question']}</div>
                  <div class="flip-hint">tap → reveal</div>
                </div>
                <div class="flip-back">
                  <div class="card-num" style="color:rgba(255,255,255,0.5);">Answer</div>
                  <div class="card-q-back">Q: {q_short}</div>
                  <div class="card-a-back">{card['answer']}</div>
                </div>
              </div>
            </div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 💾 Export")
    fmt = st.radio("Format:", ["JSON", "Plain Text Study Sheet"], horizontal=True)
    if fmt == "JSON":
        st.download_button("⬇️ Download JSON",
                           data=json.dumps(st.session_state.flashcards, indent=2),
                           file_name="flashcards.json", mime="application/json")
    else:
        lines = []
        for i, c in enumerate(st.session_state.flashcards, 1):
            lines += [f"[{i}] [{c.get('difficulty','').upper()}]",
                      f"Q: {c['question']}", f"A: {c['answer']}", ""]
        st.download_button("⬇️ Download Study Sheet",
                           data="\n".join(lines),
                           file_name="flashcards.txt", mime="text/plain")

# ── Quiz ──────────────────────────────────────────────────────────────────────
elif st.session_state.mode == "Quiz Mode":
    cards = st.session_state.flashcards
    idx   = st.session_state.quiz_index
    total = len(cards)
    pct   = int((idx / total) * 100)

    st.markdown(f"### 🎯 Quiz Mode &nbsp;·&nbsp; Card {min(idx+1, total)} / {total}")
    st.markdown(f"""
    <div class="prog-track">
        <div class="prog-fill" style="width:{pct}%"></div>
    </div>""", unsafe_allow_html=True)

    if idx >= total:
        score = st.session_state.quiz_score
        pct_s = int((score / total) * 100)
        emoji = "🏆" if pct_s >= 90 else "✅" if pct_s >= 70 else "📚"
        msg   = "Outstanding!" if pct_s >= 90 else "Great job!" if pct_s >= 70 else "Keep studying!"
        st.markdown(f"""
        <div class="score-card">
            <div style="font-size:3rem">{emoji}</div>
            <div class="score-big">{pct_s}%</div>
            <div class="score-label">{score} / {total} correct &nbsp;·&nbsp; {msg}</div>
        </div>""", unsafe_allow_html=True)
        if st.button("🔄 Restart Quiz", use_container_width=True):
            st.session_state.quiz_index = 0
            st.session_state.show_answer = False
            st.session_state.quiz_score = 0
            st.session_state.quiz_answered = set()
            random.shuffle(st.session_state.flashcards)
            st.rerun()
    else:
        card = cards[idx]
        diff = card.get("difficulty", "medium").lower()

        st.markdown(f"""
        <div class="quiz-card-3d">
            <span class="diff-badge {diff}">{diff}</span>
            <div class="quiz-q">{card['question']}</div>
        </div>""", unsafe_allow_html=True)

        if not st.session_state.show_answer:
            if st.button("👁 Reveal Answer", use_container_width=True):
                st.session_state.show_answer = True
                st.rerun()
        else:
            st.markdown(f"""
            <div class="quiz-ans-box">
                <strong>Answer:</strong> {card['answer']}
            </div>""", unsafe_allow_html=True)
            b1, b2 = st.columns(2)
            with b1:
                if st.button("✅ Got it!", use_container_width=True):
                    if idx not in st.session_state.quiz_answered:
                        st.session_state.quiz_score += 1
                        st.session_state.quiz_answered.add(idx)
                    st.session_state.quiz_index += 1
                    st.session_state.show_answer = False
                    st.rerun()
            with b2:
                if st.button("❌ Missed it", use_container_width=True):
                    st.session_state.quiz_answered.add(idx)
                    st.session_state.quiz_index += 1
                    st.session_state.show_answer = False
                    st.rerun()