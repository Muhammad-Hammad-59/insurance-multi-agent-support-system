# 🏥 Insurance Support AI

A multi-agent conversational AI system that automates insurance customer support using intelligent agent routing, LLM reasoning, and semantic search.

---

## 📋 Overview

Insurance Support AI is a smart chatbot that handles customer inquiries about:
- 📋 **Policy Details** — Coverage info, terms, and conditions
- 💳 **Billing & Payments** — Invoices, payment history, premium details
- 📊 **Claims** — Status tracking, claim information, filing assistance
- ❓ **General Questions** — FAQ and knowledge base retrieval

**How it works:**
1. User asks a question in the chat
2. **Supervisor agent** understands the intent and routes to the right specialist
3. Specialist agent (policy, billing, claims, or general help) handles the query
4. If info is missing, the system asks for clarification via the UI
5. Final answer is returned in a conversational format

---

## ✨ Key Features

✅ **Intelligent Routing** — Supervisor automatically routes to the right agent  
✅ **Direct Database Access** — Agents query real customer data  
✅ **Semantic Search** — FAQ answers powered by ChromaDB embeddings  
✅ **Multi-turn Conversations** — Session management for continuous chats  
✅ **Clarification Handling** — Asks for missing info in the UI (not terminal)  
✅ **Human Escalation** — Gracefully escalates complex issues  
✅ **Tool Calling** — Agents use functions to retrieve data  
✅ **Error Handling** — Robust error messages and fallbacks  

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **Backend** | FastAPI + LangGraph + Groq LLM |
| **Frontend** | React + Vite |
| **Database** | SQLite (customer/policy data) |
| **Vector DB** | ChromaDB (FAQ embeddings) |
| **LLM Framework** | LangChain + LangGraph |
| **API Calls** | Groq (fast inference) |
| **Observability** | OpenTelemetry + Phoenix (optional) |

---

## � Prerequisites

- **Python 3.9+**
- **Node.js 16+** and npm
- **Groq API Key** (free tier available at [console.groq.com](https://console.groq.com))
- (Optional) Phoenix for LLM tracing

---

## 🚀 Quick Start

### 1. Clone & Setup Backend

```bash
# Navigate to project root
cd insurance-support-ai

# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

Create `.env` file:
```env
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama3-70b-8192
```

Get a free Groq API key: [console.groq.com](https://console.groq.com)

### 3. Initialize Database

```bash
python scripts/setup_db.py
```

This creates SQLite database with sample customer data and FAQ data in ChromaDB.

### 4. Start Backend

```bash
uvicorn backend.main:app --reload --port 8000
```

✅ API running at: http://localhost:8000  
📚 API docs at: http://localhost:8000/docs

### 5. Setup Frontend

In a new terminal:

```bash
cd frontend
npm install
npm run dev
```

✅ UI running at: http://localhost:5173

---

## 🎯 Usage

### Chat Interface

1. Open http://localhost:5173
2. Type a question (e.g., "What is the status of claim CLM000001?")
3. The system will:
   - Route to the appropriate agent
   - Retrieve relevant data
   - Ask for missing info if needed
   - Return answer in conversational format

### Example Queries

```
"What does policy POL000004 cover?"
→ Routes to Policy Agent → Retrieves coverage details

"I want to know my billing status for policy POL000001"
→ Routes to Billing Agent → Shows payment history

"What's the status of claim CLM000001?"
→ Routes to Claims Agent → Returns claim status

"How do I file a claim?"
→ Routes to General Help Agent → Searches FAQ database
```

### API Endpoints

**POST `/api/chat`**
```json
{
  "message": "What is my policy coverage?",
  "session_id": "user-123",
  "policy_number": "POL000004"  // optional
}
```

**Response:**
```json
{
  "session_id": "user-123",
  "response": "Your policy covers...",
  "needs_clarification": false,
  "agent_used": "policy_agent"
}
```

**DELETE `/api/session/{session_id}`**
— Clear conversation history

**GET `/api/health`**
— Check if service is running

---

## 📁 Project Structure

```
insurance-support-ai/
├── backend/
│   ├── agents/
│   │   └── __init__.py           # All agent functions
│   ├── api/
│   │   └── routes.py             # FastAPI endpoints
│   ├── db/
│   │   ├── database.py           # SQLite queries
│   │   ├── seed_data.py          # Sample data
│   │   └── vector_store.py       # ChromaDB FAQ
│   ├── utils/
│   │   ├── llm.py                # Groq wrapper
│   │   ├── prompts.py            # Agent prompts
│   │   └── tracing.py            # Phoenix tracing
│   ├── graph.py                  # LangGraph workflow
│   └── main.py                   # FastAPI app
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ChatWindow.jsx    # Main chat UI
│   │   │   └── MessageBubble.jsx # Message display
│   │   ├── hooks/
│   │   │   └── useChat.js        # Chat logic
│   │   ├── services/
│   │   │   └── api.js            # API calls
│   │   └── pages/
│   │       └── App.jsx           # Root component
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
├── scripts/
│   └── setup_db.py               # Database setup
├── docs/
│   └── LIFECYCLE.md              # Project phases
├── chroma_db/                    # Vector database (generated)
├── requirements.txt
├── .env.example
└── README.md
```

---

## � How It Works

### Agent Workflow

```
User Message
    ↓
Supervisor Agent (Route decision)
    ├── Ask clarification if needed
    └── Route to specialist
         ├── Policy Agent → Database lookup
         ├── Billing Agent → Invoice/payment data
         ├── Claims Agent → Claim status lookup
         └── General Help Agent → FAQ search
    ↓
Final Answer Agent (Format response)
    ↓
Return to User
```

### Key Components

**1. Supervisor Agent**
- Analyzes user intent
- Asks for missing information (policy #, claim ID, etc.)
- Routes to appropriate specialist

**2. Specialist Agents**
- **Policy Agent:** Retrieves policy details, coverage
- **Billing Agent:** Shows invoices, payment history, premiums
- **Claims Agent:** Tracks claim status, claim details
- **General Help Agent:** Searches FAQ database with semantic search

**3. Graph State**
- Maintains conversation context
- Tracks customer/policy/claim IDs
- Manages clarification requests
- Handles escalations

---

## ⚙️ Configuration

### Backend Settings

Edit `.env`:
```env
# Groq LLM
GROQ_API_KEY=sk-...
GROQ_MODEL=llama3-70b-8192

# Optional: Phoenix Observability
# PHOENIX_API_ENDPOINT=http://localhost:6006
```

### Database

- **SQLite:** `backend/db/database.py` - Customer/policy data
- **ChromaDB:** `chroma_db/` - FAQ embeddings
- Edit `backend/db/seed_data.py` to add custom data

### Prompts

Agent system prompts in `backend/utils/prompts.py`:
- `SUPERVISOR_PROMPT` - Routing logic
- `POLICY_AGENT_PROMPT` - Policy queries
- `BILLING_AGENT_PROMPT` - Billing queries
- `CLAIMS_AGENT_PROMPT` - Claims queries  
- `GENERAL_HELP_PROMPT` - FAQ search

---

## 🧪 Development

### Running in Development Mode

**Terminal 1 — Backend:**
```bash
uvicorn backend.main:app --reload --port 8000
```

**Terminal 2 — Frontend:**
```bash
cd frontend && npm run dev
```

### View API Documentation

Open http://localhost:8000/docs in browser for interactive API docs (Swagger UI)

### Debugging

Backend logs show agent routing:
```
🔍 Supervisor called with n_iter: 0
➡️ Routing to claims_agent
Claims Agent: Your claim is approved...
🎯 Final Answer Agent compiling the final response
```

---

## 🔍 Optional: LLM Observability

Enable Phoenix tracing to see all LLM calls:

### Setup Phoenix

```bash
pip install arize-phoenix[otel]
phoenix serve
```

### Add to `.env`
```env
PHOENIX_API_ENDPOINT=http://localhost:6006
```

### View Traces

Open http://localhost:6006 to see:
- All Groq API calls
- Agent execution flow
- Token usage
- Execution timing

---

## 📝 Sample Data

The system comes with sample customers and policies in SQLite:

- **Customers:** POL000001 - POL000390
- **Claims:** CLM000001 - CLM000050  
- **FAQ:** 50+ insurance questions and answers

Run `python scripts/setup_db.py` to regenerate sample data.

---

## 🚢 Deployment

### Production Checklist

- [ ] Use environment variables for secrets (not hardcoded)
- [ ] Replace in-memory session store with Redis
- [ ] Enable HTTPS/TLS for API
- [ ] Set up database backups
- [ ] Configure CORS for your domain
- [ ] Enable Phoenix monitoring for observability
- [ ] Set up error logging (e.g., Sentry)
- [ ] Use production Groq API tier

### Docker (Example)

```dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY backend /app/backend
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 🐛 Troubleshooting

### Backend won't start
```bash
# Clear cache
rm -rf backend/__pycache__ venv
# Reinstall
python -m venv venv && pip install -r requirements.txt
```

### "Agent error: 'supervisor_agent'"
- Check `.env` has `GROQ_API_KEY`
- Verify Groq API key is valid
- Check OpenAI/Groq API quota

### Frontend won't load
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run dev
```

### No response from chat
- Ensure backend is running on port 8000
- Check network tab in browser DevTools
- Verify CORS settings in `backend/main.py`

---

## 📚 Documentation

- **[Project Lifecycle](docs/LIFECYCLE.md)** — Development phases & planning
- **[Phoenix Setup](docs/PHOENIX_SETUP.md)** — LLM observability guide (if enabled)

---

## 🎓 Learning Resources

- **LangGraph Docs:** https://langchain-ai.github.io/langgraph/
- **FastAPI Docs:** https://fastapi.tiangolo.com/
- **React Docs:** https://react.dev/
- **Groq API:** https://console.groq.com

---

## 📄 License

This project is provided as-is for educational and commercial use.

---

## 🤝 Support

For issues or questions:
1. Check troubleshooting section above
2. Review backend logs (printed in terminal)
3. Check API documentation at http://localhost:8000/docs
4. Verify `.env` configuration

---

**Happy Supporting!** 🎉

Built with ❤️ using LangGraph, FastAPI, and Groq
│   │   │   └── api.js             # API calls to backend
│   │   └── hooks/
│   │       └── useChat.js         # Chat state management
│   ├── index.html
│   └── package.json
├── docs/
│   └── LIFECYCLE.md               # Full dev lifecycle guide
├── scripts/
│   ├── setup_db.py                # One-time DB + vector store setup
│   └── run_dev.sh                 # Start all services
├── .env.example
└── requirements.txt
```

---

## ⚡ Quick Start

```bash
# 1. Clone and install
cd insurance-support-ai
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 2. Configure environment
cp .env.example .env
# → Add your OPENAI_API_KEY

# 3. Seed the database and vector store
python scripts/setup_db.py

# 4. Start the backend
uvicorn backend.main:app --reload --port 8000

# 5. Start the frontend (new terminal)
cd frontend && npm install && npm run dev
```

Then open **http://localhost:5173** in your browser.
