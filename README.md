# 🤖 AskBot — FAQ Chatbot
### CodeAlpha AI Internship · Task 2

An AI-powered FAQ chatbot using **Groq API (LLaMA 3)** with a curated FAQ knowledge base as its context. The model answers questions grounded in the FAQ data, with the full intelligence of LLaMA 3 for natural conversation.

---

## ✨ Features

- **Groq API + LLaMA 3 8B** — fast, free AI responses
- **35+ FAQs** injected as system context (CodeAlpha, Python, AI/ML, Streamlit, YOLO…)
- **Multi-turn conversation** — remembers the last 10 exchanges
- **Sidebar FAQ browser** — click any question to ask it instantly
- **Native Streamlit chat UI** — no HTML rendering bugs, clean markdown support
- **API key input** in sidebar — no hardcoding, you paste your own key

---

## 🚀 Setup & Run

### 1. Get a free Groq API key
Visit [console.groq.com](https://console.groq.com) → sign up → create an API key (free tier is generous).

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the app
```bash
streamlit run app.py
```

### 4. Paste your Groq API key
The sidebar has a password-type input. Paste your key starting with `gsk_...` and start chatting.

---

## 🛠️ Tech Stack

| Component         | Technology                        |
|-------------------|-----------------------------------|
| UI Framework      | Streamlit                         |
| AI Model          | LLaMA 3 8B via Groq API           |
| FAQ Knowledge     | Custom dataset (faq_data.py)      |
| Language          | Python 3.8+                       |

---

## 🧠 How It Works

```
FAQ data (35+ Q&A pairs)
         │
         ▼
  System Prompt (injected as context)
         │
         ▼
  User Question → Groq API (LLaMA 3 8B)
         │
         ▼
  Grounded AI Answer (streamed to chat)
```

---

## 📁 Project Structure

```
CodeAlpha_FAQChatbot/
├── app.py              # Streamlit chat interface + Groq integration
├── faq_data.py         # FAQ dataset (35+ Q&A pairs)
├── faq_engine.py       # TF-IDF engine (kept for reference)
├── requirements.txt    # Dependencies
└── README.md
```

---

## 👤 Author
Built for **CodeAlpha AI Internship Program**
