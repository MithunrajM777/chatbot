from pymongo import MongoClient
from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime
from difflib import SequenceMatcher
import os
import re

load_dotenv()

# OpenAI
client_ai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# MongoDB
mongo_client = MongoClient(os.getenv("MONGO_URI"))
db = mongo_client["chatbot_db"]
collection = db["knowledge_base"]
history_collection = db["chat_history"]

STOP_WORDS = {
    "what", "is", "are", "your", "how", "do", "i",
    "the", "a", "an", "to", "for", "of", "and", "you"
}


# ---------- Helpers ----------
def normalize(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    return text.strip()


def similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()


# ---------- Client Detection ----------
def detect_client(question: str):
    if not question:
        return "madurasolution"
    return "airtel_black" if "airtel" in question.lower() else "madurasolution"


# ---------- Greetings ----------
def is_greeting(message: str) -> bool:
    return bool(re.search(r"\b(hi|hello|hey|hai)\b", message.lower()))


# ---------- Common Intents ----------
def handle_common_intents(message, client):
    msg = normalize(message)

    # ✅ MaduraSolution only
    if client == "madurasolution":
        if any(k in msg for k in ["location", "office address", "office location"]):
            return (
                "📍 Office Address:\n"
                "13, Jainagar, Ponmeni,\n"
                "Madurai – 625016"
            )

        if any(k in msg for k in ["timing", "office time", "working hours"]):
            return (
                "⏰ Office Timings:\n"
                "9:00 AM – 6:00 PM"
            )

        if "co founder" in msg or "co-founder" in msg:
            return "🏢 Our Co-Founder is Mrs. Haniya Anand."

        if any(k in msg for k in ["founder", "ceo"]):
            return "🏢 Our Founder & CEO is Mr. Yogaanand."

        if msg in ["services", "our services", "what services do you offer", "services offered", "list of services", "service list",]:
            return (
                "💼 Our Services:\n"
                "• Web Development\n"
                "• Mobile App Development\n"
                "• AI & Automation\n"
                "• Software Testing\n"
                "• Digital Marketing\n"
                "• UI/UX Design"
            )

        if any(k in msg for k in ["email", "contact"]):
            return "📧 Email: support@madurasolution.com"

    return None


# ---------- Company Scope ----------
def is_company_related(question: str) -> bool:
    keywords = {
        "office", "salary", "leave", "hr", "email",
        "project", "client", "service", "airtel", "madura"
    }
    question = question.lower()
    return any(k in question for k in keywords)


# ---------- MongoDB Answer (FIXED) ----------
def get_answer_from_mongo(question):
    try:
        user_q = normalize(question)
        best_match = None
        best_score = 0

        for doc in collection.find():
            db_q = normalize(doc.get("Question", ""))
            score = similarity(user_q, db_q)

            if score > best_score:
                best_score = score
                best_match = doc.get("Answer")

        if best_score >= 0.60:
            return best_match

        return None

    except Exception as e:
        print("MongoDB error:", e)
        return None

# ---------- OpenAI ----------
OPENAI_ENABLED = True  # global flag

def get_answer_from_ai(user_question: str):
    try:
        response = client_ai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a professional customer support assistant."
                    )
                },
                {"role": "user", "content": user_question}
            ]
        )
        return response.choices[0].message.content

    except Exception as e:
        print("AI ERROR:", e)
        return None

# ---------- Chat History ----------
def save_chat_history(question, answer, source, client=None):
    history_collection.insert_one({
        "question": question,
        "answer": answer,
        "source": source,
        "client": client,
        "created_at": datetime.utcnow()
    })


def get_chat_history(limit=100):
    return list(
        history_collection
        .find()
        .sort("created_at", -1)
        .limit(limit)
    )
def ai_failed(reply: str):
    failure_phrases = [
        "i don't know",
        "i am not sure",
        "no information",
        "cannot help",
        "not available",
        "sorry"
    ]
    reply = reply.lower()
    return any(phrase in reply for phrase in failure_phrases)