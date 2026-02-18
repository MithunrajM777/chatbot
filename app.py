from flask import Flask, render_template, request, jsonify
from mongo_chatbot_ai import (
    is_greeting,
    get_answer_from_mongo,
    get_answer_from_ai,
    is_company_related,
    detect_client,
    handle_common_intents,
    save_chat_history,
    get_chat_history
)

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_message = data.get("message", "").strip()

        if not user_message:
            return jsonify({"reply": "Please type a message."})

        client = detect_client(user_message)

        # 1️⃣ GREETING
        if is_greeting(user_message):
            reply = (
        "Hello 👋😊\n"
        "I’m the Customer support Helpdesk.\n"
        "How can I help you today?"
        )
            save_chat_history(user_message, reply, "system", client)
            return jsonify({"reply": reply})


        # 2️⃣ COMMON INTENTS
        intent_reply = handle_common_intents(user_message, client)
        if intent_reply:
            save_chat_history(user_message, intent_reply, "system", client)
            return jsonify({"reply": intent_reply})

        # 3️⃣ MONGODB FAQ
        mongo_reply = get_answer_from_mongo(user_message)
        if mongo_reply:
            save_chat_history(user_message, mongo_reply, "mongo", client)
            return jsonify({"reply": mongo_reply})
        # 4️⃣ AI FALLBACK
        ai_reply = get_answer_from_ai(user_message)

        if ai_reply:
            save_chat_history(user_message, ai_reply, "ai", client)
            return jsonify({"reply": ai_reply})

        # 5️⃣ HUMAN HANDOFF (FINAL FAIL)
        human_reply = (
            "🤝 I’m unable to help with this right now.\n\n"
            "Let me connect you with a human support agent.\n"
            "📧 Email: support@madurasolution.com\n"
            "📞 Phone: +91-9944063964 & +91-9944063664\n\n"
            "⏰ Our team will respond within 24–48 hours."
        )

        save_chat_history(user_message, human_reply, "human", client)
        return jsonify({"reply": human_reply})

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"reply": "⚠️ Internal server error"})


@app.route("/admin")
def admin():
    chats = get_chat_history(200)
    return render_template("admin.html", chats=chats)


@app.route("/history")
def history():
    chats = get_chat_history(100)
    return jsonify(chats)


if __name__ == "__main__":
    app.run(debug=True, port=5200)