# AI Receptionist for Small Businesses

A comprehensive AI-powered receptionist system that handles customer inquiries, appointment scheduling, and contact management for small businesses.

## Features

### Customer-Facing Features
- **AI Chatbot**: Natural language conversations with customers
- **Appointment Scheduling**: Book, reschedule, and cancel appointments
- **Business Information**: Get hours, services, and contact details
- **FAQ System**: Common questions and answers
- **Live Chat Handoff**: Transfer to human agent when needed

### Admin Features
- **Dashboard**: Overview of messages, appointments, and analytics
- **Appointment Management**: View, edit, and manage all appointments
- **Contact Management**: Customer database and interaction history
- **Business Configuration**: Set hours, services, FAQs, and AI personality
- **Message History**: View all customer conversations

## Architecture

```
AI Receptionist System
├── Backend (FastAPI)
│   ├── AI Chat Engine
│   ├── Appointment System
│   ├── Contact Management
│   ├── Business Configuration
│   └── REST API
├── Frontend (React)
│   ├── Customer Chat Interface
│   ├── Admin Dashboard
│   └── Shared Components
└── Database (SQLite/PostgreSQL)
```

## Quick Start

### Prerequisites
- Python 3.9+
- Node.js 18+
- Git

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
python main.py
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

## Configuration

Set up environment variables:
- `OPENAI_API_KEY` for AI chat functionality
- `DATABASE_URL` for database connection
- `JWT_SECRET` for authentication

## License
MIT