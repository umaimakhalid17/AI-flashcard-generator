# 🃏 FlashAI — AI Flashcard Generator

A sleek Streamlit app that turns any topic into smart flashcards using **Groq API** (completely free & blazing fast!).

![Python](https://img.shields.io/badge/Python-3.9+-blue) ![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-red) ![Groq](https://img.shields.io/badge/Groq-LLaMA_3.3_70B-orange) ![Free](https://img.shields.io/badge/API-Free-green)

## ✨ Features

- **100% Free AI** — Uses Groq (LLaMA 3.3 70B), no credit card needed
- **⚡ Blazing Fast** — Groq's hardware makes generation near-instant
- **3D Flip Cards** — Click any card to flip with a smooth 3D animation
- **4 Card Styles** — Q&A Pairs, Fill in the Blank, True/False, Definition Style
- **Difficulty Control** — Easy / Medium / Hard / Mixed
- **Browse Mode** — Filter & flip cards at your own pace
- **Quiz Mode** — Card-by-card self-test with score tracking & progress bar
- **Export** — Download as JSON or plain-text study sheet

## 🚀 Setup (Local)

```bash
git clone https://github.com/yourusername/flashai.git
cd flashai
pip install -r requirements.txt
streamlit run app.py
```

Get your **free** Groq API key at [console.groq.com](https://console.groq.com) → paste it in the sidebar.

## ☁️ Deploy on Streamlit Cloud

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io) and connect your repo
3. Set main file as `app.py` and deploy
4. Add your Groq key in **Settings → Secrets**:
```toml
GROQ_API_KEY = "gsk_your_key_here"
```

## 🛠 Tech Stack

| Tool | Purpose |
|------|---------|
| Streamlit | UI framework |
| Groq API (LLaMA 3.3 70B) | Flashcard generation (free & fast!) |
| CSS 3D transforms | Card flip animations |
| Python requests | API calls |

## 📁 Project Structure

```
flashai/
├── app.py              # Main Streamlit app
├── requirements.txt    # Dependencies
└── README.md
```

---
*Part of the 1-project-per-day GitHub streak 🔥*
