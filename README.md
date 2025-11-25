# 📫 AI Email Agent — Smart Inbox Assistant

A powerful Streamlit web app that analyzes emails, extracts actions, categorizes messages, and generates professional replies using **Google Gemini 2.0 Flash**.

This project is perfect for:  

- Personal email productivity  
- Founders, students, and professionals handling many emails  
- Demonstrating LLM workflow automation  
- AI-powered inbox triage  

---

## 🚀 Features

### 📥 1. Inbox Processing
- Select any email from your inbox (`inbox.json`)  
- View sender, subject, and body  
- Categorize the email (Urgent, Important, Spam, etc.)  
- Extract actionable tasks (deadlines, responsibilities)  
- Generate editable reply drafts  
- Save per-email drafts  

### 🤖 2. AI Email Agent (Chat Mode)
Ask questions such as:  
- “What is this email asking me to do?”  
- “Summarize this email.”  
- “Does any email mention travel plans?”  
- “Which emails are most urgent?”  

Choose the context mode:  
- **Single Email Mode** — context limited to one email  
- **Entire Mailbox Mode** — Gemini analyzes all emails at once  

### 🧠 3. Editable Prompt Configuration
- Full prompt editor for customizing:  
  - Categorization logic  
  - Action extraction format  
  - Reply tone  
  - Agent reasoning behavior  
- Prompts auto-save to `prompts.json`  

### ✨ 4. Clean, Lightweight UI
- Three-tab navigation  
- Per-email session state  
- Chat-like interface  
- Deployed on Streamlit Cloud for free  
- Zero backend required  

---

## 🗂 Project Structure
email-agent
│
├── app.py # Main Streamlit application
├── requirements.txt # Python dependencies
├── README.md # Documentation
│
├── inbox.json # Mock emails loaded into the app
├── prompts.json # Customizable AI prompts
│
└── .gitignore # GitHub ignored files

---

## 🔧 Local Installation

1️⃣ **Clone the repository**  
```bash
git clone https://github.com/your-username/email-agent.git
cd email-agent
2️⃣ Install dependencies
```bash
pip install -r requirements.txt
3️⃣ Run the app
```bash
streamlit run app.py

---

## 📬 Email Format (`inbox.json`)

Example:

```json
[
  {
    "id": 1,
    "subject": "Project Update Needed",
    "from": "manager@example.com",
    "body": "Can you send the latest update and timeline?"
  }
]

---

## 📘 Prompt Config (`prompts.json`)

You can customize all AI behaviors — categorization, action extraction, replies, and agent reasoning.  
Changes appear immediately when the app reloads.

---

## 🛠 Technologies Used

- Python 3.10+  
- Streamlit  
- Google Gemini Flash 2.0  
- JSON-based dynamic prompts  
- Session-state powered UI  

---

## 🤝 Contributing

Contributions are welcome!  
Open issues or submit PRs to improve prompts, UI, or model integration.

---

## ⭐ Support

If you find this project useful, consider starring the repo 🌟  
Your support helps the project grow and improve!
