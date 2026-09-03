# 🤖 Enterprise AI Support Agent

An AI-powered enterprise IT support system that uses **Retrieval-Augmented Generation (RAG)** to answer employee IT support questions from a trusted company knowledge base.

## ✨ Features

- 🤖 AI-powered IT support
- 🔎 Retrieval-Augmented Generation (RAG)
- 🧠 Semantic document search
- 🔤 Sentence Transformers for embeddings
- 📊 Cosine similarity for document retrieval
- 💎 Gemini for natural-language answer generation
- ⚡ FastAPI REST API
- 📚 Knowledge-base source tracking
- 👨‍💻 Human escalation for unsupported issues
- 🎫 Automatic support ticket creation
- 📋 Clear API responses for knowledge answers and escalations

## 🏗️ System Architecture

👤 User Query
↓
⚡ FastAPI API
↓
🔎 RAG Retrieval
↓
📚 Knowledge Base
↓
📄 Relevant Documents
↓
💎 Gemini AI
↓
💬 Knowledge Answer / 🎫 Human Escalation
↓
🛠️ Support Ticket

## 🛠️ Technology Stack

- 🐍 Python
- ⚡ FastAPI
- 💎 Google Gemini API
- 🔤 Sentence Transformers
- 📊 scikit-learn
- 🔢 NumPy
- 📄 JSON
- 🌐 REST API

## 📁 Project Structure

enterprise-ai-support-agent/
├── app/
│   ├── agent.py
│   ├── rag.py
│   ├── main.py
│   └── tools.py
├── data/
│   └── knowledge_base.json
├── README.md
└── requirements.txt

## 🔄 How It Works

1. 👤 The employee sends an IT support question.
2. ⚡ FastAPI receives the request.
3. 🔎 The RAG system searches the company knowledge base.
4. 🔤 Sentence Transformer embeddings find relevant documents.
5. 📊 Cosine similarity ranks the retrieved documents.
6. 💎 Gemini generates an answer using the retrieved information.
7. 📚 The API returns the answer and source documents.
8. 🎫 Unsupported issues are escalated to human IT support and a support ticket is created.

## 🧪 Example Queries

### 🔐 Password Reset

**Question:**  
How do I reset my password?

**Response:**  
Employees can reset a company password through the internal password portal. If the reset fails, contact the IT help desk.

**Source:** Password Reset

### 📶 WiFi Problem

**Question:**  
My WiFi is not working.

**Response:**  
If company WiFi is not connecting, restart WiFi, forget the network, reconnect, and verify the device has the latest network updates.

**Source:** WiFi Not Connecting

### 🎣 Phishing Email

**Question:**  
I think this email is phishing.

**Response:**  
Do not interact with suspicious links or attachments in a suspected phishing email. Report it through the organization's approved security process.

**Source:** Phishing Email

### 💻 Laptop Problem

**Question:**  
My laptop won't turn on.

**Response:**  
For a physically damaged company laptop, record the device ID and contact the IT help desk for hardware support.

**Source:** Laptop Broken

### 🏠 Remote Access

**Question:**  
How can I access company systems from home?

**Response:**  
Employees working remotely must connect through the approved company VPN. If VPN authentication fails, contact IT support.

**Source:** VPN Access

### 🎫 Unsupported Issue

**Question:**  
My employee ID card was lost.

**Response:**  
The system determines that sufficient knowledge is not available and escalates the request to human IT support.

A support ticket is automatically created.

## 🌐 API Endpoints

### ❤️ Health Check

**GET /**

Example response:

    {
        "message": "Enterprise AI Support Agent is running"
    }

### 💬 Support

**POST /support**

Request:

    {
        "query": "How do I reset my password?"
    }

Example response:

    {
        "type": "knowledge_answer",
        "answer": "Employees can reset a company password through the internal password portal.",
        "sources": [
            "Password Reset",
            "Forgotten Password",
            "Password Expired"
        ]
    }

## 🎫 Human Escalation

When the knowledge base does not contain enough information, the system **does not invent an answer**.

Instead, it creates a human-support ticket.

Example:

    {
        "type": "human_escalation",
        "answer": "I don't have enough information in the knowledge base. Please contact human IT support.",
        "ticket": {
            "ticket_id": "IT-XXXXXXXX",
            "status": "Created"
        },
        "sources": []
    }

## 🧠 Key AI Concepts Demonstrated

- 🔎 Retrieval-Augmented Generation
- 🔤 Text Embeddings
- 📊 Cosine Similarity
- 🧠 Semantic Search
- 💎 LLM-based Response Generation
- 🎯 Intent Detection
- 📚 Knowledge Grounding
- 👨‍💻 Human-in-the-loop Escalation
- 🌐 REST API Development
- 🎫 Automated Support Ticket Creation

## 🔐 Safety & Reliability

The system provides answers based on retrieved enterprise knowledge rather than freely generating unsupported information.

When relevant information cannot be found:

**Knowledge available → 💬 Answer**

**Knowledge unavailable → 🎫 Human escalation**

This helps reduce unsupported or hallucinated responses.

## 🎯 Project Goal

The goal of this project is to demonstrate how an enterprise can build an AI-powered IT support assistant that answers common employee questions using trusted internal knowledge while safely escalating unsupported issues to human support.

## 🚀 Future Enhancements

- 🔑 Employee authentication
- 🗄️ Production database integration
- 📊 Admin support dashboard
- 🎫 Real ticket-management integration
- 💬 Conversation history
- 📈 Analytics and monitoring
- 🔐 Enterprise security controls
- ☁️ Cloud deployment

## 👩‍💻 Author

**Srilakshmi Kummari**

Built as an **Enterprise AI / RAG project** demonstrating practical use of Generative AI, semantic search, and API development.
