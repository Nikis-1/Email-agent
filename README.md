# 📧 AI Email Agent — Streamlit App

This is a Streamlit-based AI Email Assistant that:
- Analyzes emails  
- Answers questions about a SINGLE email or your ENTIRE inbox  
- Extracts actions  
- Categorizes emails  
- Generates replies  
- Uses **Google Gemini API**  
- Deploys **free** on Streamlit Cloud  

---

## 🚀 How to Run Locally

### 1. Clone this repository
```bash
git clone https://github.com/yourusername/email-agent.git
cd email-agent
2. Install dependencies
bash
Copy code
pip install -r requirements.txt
3. Add API Key
Create .streamlit/secrets.toml:

toml
Copy code
GEMINI_API_KEY = "your_api_key_here"
4. Run the app
bash
Copy code
streamlit run app.py
