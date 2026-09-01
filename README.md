# Enterprise AI Support Agent

An AI-powered IT Support Agent that uses RAG (Retrieval-Augmented Generation) to answer employee IT support questions from a knowledge base.

## Features

- AI-powered IT support
- FAISS document retrieval
- Sentence Transformer embeddings
- Google Gemini AI
- Knowledge base source retrieval
- Human escalation for unsupported questions
- FastAPI REST API

## Technologies

- Python
- FastAPI
- Google Gemini
- FAISS
- Sentence Transformers
- NumPy
- Pydantic

## How It Works

User asks an IT support question.

The system searches the knowledge base using FAISS.

Relevant documents are retrieved.

Gemini generates an answer using the retrieved information.

If the knowledge base does not contain enough information, the system escalates the issue to human IT support.

## Example

Question:

My company WiFi is not connecting.

The system retrieves:

WiFi Troubleshooting

and generates an answer based on the knowledge base.

## Human Escalation

If the knowledge base does not contain information about a question, the system does not guess.

Example:

What should I do if my laptop is stolen?

The system returns:

human_escalation

and asks the user to contact human IT support.

## API

### Health Check

GET /

### Support

POST /support

Example request:

{
  "query": "My company WiFi is not connecting"
}

## Project Structure

enterprise-ai-support-agent/

app/

main.py

agent.py

rag.py

tools.py

requirements.txt

README.md

## Installation

```bash
pip install -r requirements.txt
