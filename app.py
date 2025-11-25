import streamlit as st
import google.generativeai as genai
import json
import os

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-2.0-flash")


@st.cache_data
def load_inbox():
    """Loads inbox.json once and caches it."""
    inbox_path = os.path.join(os.path.dirname(__file__), "inbox.json")
    with open(inbox_path, "r", encoding="utf-8") as f:
        return json.load(f)

@st.cache_data
def load_prompts():
    """Loads prompts.json."""
    with open("prompts.json", "r") as f:
        return json.load(f)

MOCK_EMAILS = load_inbox()
PROMPTS = load_prompts()


@st.cache_data(show_spinner=False)
def gemini_call_cached(full_text, cache_key):
    """LLM call cached to avoid repeated computation."""
    response = model.generate_content(
        full_text,
        safety_settings=None,
        generation_config={
            "temperature": 0.2,
            "top_p": 0.8,
            "top_k": 40,
        }
    )
    return response.text


def ask_gemini(prompt, email=None, all_emails=None):
    """Formats prompt + calls cached Gemini."""
    if all_emails:
        mailbox_str = "\n\n".join(
            [
                f"Email #{i+1}\nSubject: {e['subject']}\nFrom: {e['from']}\nBody: {e['body']}"
                for i, e in enumerate(all_emails)
            ]
        )
        full_text = f"{prompt}\n\nHere is the entire mailbox:\n{mailbox_str}"
        cache_key = "full_mailbox"
    else:
        full_text = (
            f"{prompt}\n\nEmail:\n"
            f"Subject: {email['subject']}\nFrom: {email['from']}\nBody: {email['body']}"
        )
        cache_key = f"email_{email['id']}"

    return gemini_call_cached(full_text, cache_key)



if "email_data" not in st.session_state:
    st.session_state.email_data = {e["id"]: {"category": None, "actions": None} for e in MOCK_EMAILS}

if "drafts" not in st.session_state:
    st.session_state.drafts = {}

if "replies" not in st.session_state:
    st.session_state.replies = {}

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []



tab1, tab2, tab3 = st.tabs(["Inbox", "Agent", "Prompts"])


with tab1:
    st.title("Inbox Processor")

    selected_subject = st.selectbox(
        "Select an email",
        [e["subject"] for e in MOCK_EMAILS]
    )

    email = next(e for e in MOCK_EMAILS if e["subject"] == selected_subject)
    eid = email["id"]
    state = st.session_state.email_data[eid]

    st.subheader("Email Preview")
    st.write(f"**Subject:** {email['subject']}")
    st.write(f"**From:** {email['from']}")
    st.write(f"**Timestamp:** {email['timestamp']}")
    st.write(f"**Body:** {email['body']}")
    st.write("---")

    if st.button("Categorize Email"):
        state["category"] = ask_gemini(PROMPTS["categorize_prompt"], email=email)
        st.success("Categorized!")

    if state["category"]:
        st.info(f"**Category:** {state['category']}")

    if st.button("Extract Actions"):
        state["actions"] = ask_gemini(PROMPTS["action_prompt"], email=email)
        st.success("Actions extracted!")

    if state["actions"]:
        st.markdown("**Extracted Actions:**")
        st.code(state["actions"])

    if st.button("Generate Reply"):
        reply = ask_gemini(PROMPTS["reply_prompt"], email=email)
        st.session_state.replies[eid] = reply

    if eid in st.session_state.replies:
        edited = st.text_area(
            "Edit Reply",
            st.session_state.replies[eid],
            key=f"reply_edit_{eid}"
        )

        if st.button("Save Draft"):
            st.session_state.drafts[eid] = edited
            st.success("Draft saved!")

    if eid in st.session_state.drafts:
        st.subheader("Saved Draft")
        st.code(st.session_state.drafts[eid])


with tab2:
    st.title("AI Email Agent")

    mode = st.radio("Choose context mode:", ["Single Email", "Entire Mailbox"], horizontal=True)

    if mode == "Single Email":
        subject2 = st.selectbox(
            "Select email for agent context",
            [e["subject"] for e in MOCK_EMAILS],
            key="agent_subject"
        )
        ctx_email = next(e for e in MOCK_EMAILS if e["subject"] == subject2)

        st.write("### Email Context")
        st.write(f"**Subject:** {ctx_email['subject']}")
        st.write(f"**From:** {ctx_email['from']}")
        st.write(f"**Timestamp:** {ctx_email['timestamp']}")
        st.write(ctx_email["body"])

    else:
        st.write("### Entire Mailbox")
        st.info(f"Loaded {len(MOCK_EMAILS)} emails.")

    
    for role, msg in st.session_state.chat_history:
        st.chat_message(role).write(msg)

    
    user_msg = st.chat_input("Ask a question about your email(s)…")

    if user_msg:
        st.session_state.chat_history.append(("user", user_msg))

        if mode == "Single Email":
            formatted = f"{PROMPTS['agent_prompt']}\n\nUser Question: {user_msg}"
            output = ask_gemini(formatted, email=ctx_email)
        else:
            formatted = f"{PROMPTS['agent_prompt']}\n\nMailbox Question: {user_msg}"
            output = ask_gemini(formatted, all_emails=MOCK_EMAILS)

        st.session_state.chat_history.append(("assistant", output))

with tab3:
    st.title("Prompt Configuration")

    new_cat = st.text_area("Categorization Prompt", PROMPTS["categorize_prompt"])
    new_action = st.text_area("Action Extraction Prompt", PROMPTS["action_prompt"])
    new_reply = st.text_area("Reply Prompt", PROMPTS["reply_prompt"])
    new_agent = st.text_area("Agent Prompt", PROMPTS["agent_prompt"])

    if st.button("Save Prompts"):
        updated = {
            "categorize_prompt": new_cat,
            "action_prompt": new_action,
            "reply_prompt": new_reply,
            "agent_prompt": new_agent
        }
        with open("prompts.json", "w") as f:
            json.dump(updated, f, indent=4)

        st.success("Prompts saved!")





