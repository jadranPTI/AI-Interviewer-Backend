# 🤖 AI Interview Bot — LangChain + Gemini

A terminal-based interview bot that generates questions, collects answers, and evaluates you using Gemini AI.

---

## 📁 Folder Structure

```
interview_bot/
│
├── main.py                        ← Entry point, run this file
│
├── .env                           ← Your Gemini API key goes here
├── requirements.txt               ← Python dependencies
│
└── app/
    ├── chains/
    │   ├── question_chain.py      ← Generates 15 questions using LangChain + Gemini
    │   └── evaluation_chain.py    ← Evaluates answers and returns report
    │
    ├── prompts/
    │   └── prompts.py             ← All prompt templates in one place
    │
    └── utils/
        └── helpers.py             ← Terminal display helpers (print functions)
```

---

## ⚙️ Installation

### Step 1 — Make sure Python is installed
```bash
python --version   # Should be 3.9 or above
```

### Step 2 — Create a virtual environment (recommended)
```bash
python -m venv venv

# Activate on Windows:
venv\Scripts\activate

# Activate on Mac/Linux:
source venv/bin/activate
```

### Step 3 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 4 — Add your Gemini API Key
Open the `.env` file and replace the placeholder:
```
GOOGLE_API_KEY=your_actual_api_key_here
```

> 🔑 Get your free Gemini API key at: https://aistudio.google.com/app/apikey

---

## ▶️ Run the Bot

```bash
python main.py
```

---

## 🔄 How It Works (Simple Flow)

```
1. You enter: domain + experience
        ↓
2. Gemini generates 15 questions:
   - 5 Technical
   - 5 Behavioral  
   - 5 Situational
        ↓
3. Questions appear one by one in terminal
   You type your answer → press Enter → next question
        ↓
4. After all 15 answers, AI evaluates everything
        ↓
5. You get a full report:
   - Scores (Technical / Communication / Problem Solving / Overall)
   - Strengths
   - Areas to Improve
   - Best Practices to Learn
   - Final Verdict (Hire / Reject / etc.)
```

---

## 📦 Dependencies Explained

| Package | Why |
|---|---|
| `langchain` | Chain management, prompt templates |
| `langchain-google-genai` | Connects LangChain to Gemini |
| `python-dotenv` | Reads your API key from .env file |

---

## 🚀 Next Steps (After Terminal Version Works)

1. **Add FastAPI** — wrap `run_interview()` logic into REST endpoints
2. **Add Frontend** — React/HTML form to collect domain + experience
3. **Add streaming** — stream AI responses live to the frontend