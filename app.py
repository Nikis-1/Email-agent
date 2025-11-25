
import streamlit as st
import google.generativeai as genai
import json
import os

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-2.0-flash")

with open("prompts.json", "r") as f:
    PROMPTS = json.load(f)

def load_inbox():
    inbox_path = os.path.join(os.path.dirname(__file__), "inbox.json")
    try:
        with open(inbox_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Failed to load inbox.json: {e}")
        return []

MOCK_EMAILS = load_inbox()

if "email_data" not in st.session_state:
    st.session_state.email_data = {e["id"]: {"category": None, "actions": None} for e in MOCK_EMAILS}

if "drafts" not in st.session_state:
    st.session_state.drafts = {}

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

def ask_gemini(prompt, email=None, all_emails=None):
    if all_emails:
        inbox_text = "\n\n".join(
            [
                f"Email #{i+1}\nSubject: {e['subject']}\nFrom: {e['from']}\nBody: {e['body']}"
                for i, e in enumerate(all_emails)
            ]
        )
        text = f"{prompt}\n\nHere is the entire mailbox:\n{inbox_text}"
    else:
        text = (
            f"{prompt}\n\nEmail:\n"
            f"Subject: {email['subject']}\nFrom: {email['from']}\nBody: {email['body']}"
        )

    try:
        response = model.generate_content(
            text,
            safety_settings=None,
            generation_config={
                "temperature": 0.2,
                "top_p": 0.8,
                "top_k": 40
            }
        )
        return response.text
    except Exception as e:
        return f"Error: {e}"

tab1, tab2, tab3 = st.tabs(["Inbox", "Agent", "Prompt Config"])

with tab1:
    st.title("Inbox Processor")

    selected_subject = st.selectbox(
        "Select an email",
        [e["subject"] for e in MOCK_EMAILS]
    )

    email = next(e for e in MOCK_EMAILS if e["subject"] == selected_subject)
    email_id = email["id"]
    state = st.session_state.email_data[email_id]

    st.subheader("Email Preview")
    st.write(f"**Subject:** {email['subject']}")
    st.write(f"**From:** {email['from']}")
    st.write(f"**Timestamp:** {email['timestamp']}")
    st.write(f"**Body:** {email['body']}")
    st.write("---")

    if st.button("Categorize Email"):
        result = ask_gemini(PROMPTS["categorize_prompt"], email)
        state["category"] = result
        st.success("Categorized!")

    if state["category"]:
        st.info(f"**Category:** {state['category']}")

    if st.button("Extract Actions"):
        result = ask_gemini(PROMPTS["action_prompt"], email)
        state["actions"] = result
        st.success("Actions extracted!")

    if state["actions"]:
        st.markdown("**Extracted Actions:**")
        st.code(state["actions"], language="json")

    if "replies" not in st.session_state:
        st.session_state.replies = {}

    if st.button("Generate Reply"):
        reply = ask_gemini(PROMPTS["reply_prompt"], email)
        st.session_state.replies[email_id] = reply

    if email_id in st.session_state.replies:
        edited = st.text_area(
            "Edit Reply",
            st.session_state.replies[email_id],
            key=f"edit_reply_{email_id}"
        )

        if "drafts" not in st.session_state:
            st.session_state.drafts = {}

        if st.button("Save Draft"):
            st.session_state.drafts[email_id] = edited
            st.success("Draft saved!")

    if email_id in st.session_state.drafts:
        st.subheader("Saved Draft for this email")
        st.code(st.session_state.drafts[email_id])

with tab2:
    st.title("Email Agent")

    mode = st.radio(
        "Choose context mode:",
        ["Single Email", "Entire Mailbox"],
        horizontal=True
    )

    if mode == "Single Email":
        selected_subject2 = st.selectbox(
            "Select email for context",
            [e["subject"] for e in MOCK_EMAILS],
            key="agent_email"
        )
        e2 = next(e for e in MOCK_EMAILS if e["subject"] == selected_subject2)

        st.write("### Email Context")
        st.write(f"**From:** {e2['from']}")
        st.write(e2["body"])

    else:
        st.write("### Using Entire Mailbox as context")
        st.info(f"Total emails loaded: {len(MOCK_EMAILS)}")

    for role, msg in st.session_state.chat_history:
        if role == "user":
            st.chat_message("user").write(msg)
        else:
            st.chat_message("assistant").write(msg)

    prompt_text = "Ask something about this email…" if mode == "Single Email" else "Ask something about your entire mailbox…"
    user_input = st.chat_input(prompt_text)

    if user_input:
        st.session_state.chat_history.append(("user", user_input))

        if mode == "Single Email":
            full_prompt = f"{PROMPTS['agent_prompt']}\n\nUser question: {user_input}"
            response = ask_gemini(full_prompt, email=e2)

        else:
            full_prompt = f"{PROMPTS['agent_prompt']}\n\nUser question (mailbox): {user_input}"
            response = ask_gemini(full_prompt, all_emails=MOCK_EMAILS)

        st.session_state.chat_history.append(("assistant", response))
        st.rerun()

with tab3:
    st.title("Prompt Configuration")

    st.write("Edit and save your prompts dynamically.")

    new_cat = st.text_area("Categorization Prompt", PROMPTS["categorize_prompt"])
    new_action = st.text_area("Action Extraction Prompt", PROMPTS["action_prompt"])
    new_reply = st.text_area("Reply Prompt", PROMPTS["reply_prompt"])
    new_agent = st.text_area("Agent Prompt", PROMPTS["agent_prompt"])

    if st.button("Save Prompts"):
        PROMPTS["categorize_prompt"] = new_cat
        PROMPTS["action_prompt"] = new_action
        PROMPTS["reply_prompt"] = new_reply
        PROMPTS["agent_prompt"] = new_agent

        with open("prompts.json", "w") as f:
            json.dump(PROMPTS, f, indent=4)

        st.success("Prompts saved!")





