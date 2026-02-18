# 🤖 AI Customer Support Chatbot

An AI-powered Customer Support Chatbot built using **Flask**, **MongoDB Atlas**, and **OpenAI**, designed to provide automated support with intelligent fallback to human agents when required.

---

## 📌 Project Overview

This chatbot automates first-level customer support by answering user queries through:
- System-defined rules
- MongoDB-based knowledge base
- AI-powered responses
- Human agent handoff when all automated methods fail

It is suitable for **business websites**, **customer service portals**, and **internal support systems**.

---

## ✨ Key Features

- 👋 Greeting detection
- 🧠 Rule-based intent handling
- 📚 MongoDB FAQ matching
- 🤖 AI fallback responses
- 👨‍💼 Human support escalation
- ⏰ Time-based support logic (9 AM – 6 PM)
- 🗂 Chat history storage
- ☁ Cloud-ready deployment

---

## 🏗️ Technology Stack

### Frontend
- HTML
- CSS
- JavaScript

### Backend
- Python (Flask)

### Database
- MongoDB Atlas (Cloud)

### AI
- OpenAI API

### Hosting
- Render (Cloud hosting)

---

## 🧩 System Architecture
    User
↓
Chat UI
↓
Flask Backend
↓
Greeting Handler
↓
Common Intent Rules
↓
MongoDB Knowledge Base
↓
AI Fallback
↓
Human Support Handoff

---

## ⚙️ Workflow

1. User sends a message
2. System checks greeting
3. System handles predefined intents
4. MongoDB searches for relevant answers
5. AI generates a response if needed
6. Human support is contacted if all fail

---

## 🗄️ Database Structure

### Collections

- `knowledge_base`
- `chat_history`

MongoDB Atlas automatically creates collections when data is inserted.

---

## 🔐 Environment Variables

Create a `.env` file (DO NOT commit it):

OPENAI_API_KEY=your_openai_api_key
MONGO_URI=your_mongodb_atlas_uri

## 🚀 Deployment

The chatbot is deployed using **Render**.

### Required Files:
- `requirements.txt`
- `Procfile`
- `app.py`

Start command: 
        gunicorn app:app
    
## 🧪 Testing

Sample test inputs:
hi
ceo
office timing
network issue
random text


---

## 🧑‍💼 Human Support Handoff

If automated systems fail, the chatbot provides:
- Support email
- Contact number
- Response time information

---

## 🔮 Future Enhancements

- Live agent dashboard
- WhatsApp integration
- Multi-language support
- Analytics dashboard
- CRM integration

---

## 📄 License

This project is licensed under the **MIT License**.

---

## 👨‍💻 Author

**Mithun Raj**  
AI Chatbot Developer  

---

## ⭐ Acknowledgements

- Flask Community
- MongoDB Atlas
- OpenAI
- Render

