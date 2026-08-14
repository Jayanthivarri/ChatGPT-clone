# ChatGPT Clone with MCP Integration

## Project Overview

This project is a full-stack ChatGPT clone that provides an AI-powered conversational interface. It supports user authentication, chat sessions, conversation history, memory, real-time information retrieval, and tool-based AI responses.

The project also integrates an **MCP (Model Context Protocol) Server** to connect the application with external tools in a standardized way.

## Domain

**Artificial Intelligence / Generative AI**

## Use Case

The application can be used as an AI assistant for:

* General question answering
* Real-time information retrieval
* Mathematical calculations
* Weather information
* Time information
* User memory and personalized responses
* Web search
* Tool-based AI interactions
* MCP-based tool integration

## Problem Statement

Traditional chatbot applications mainly depend on an LLM to generate responses. However, an LLM alone may not have access to real-time information, user-specific data, or external tools.

The objective of this project is to build a ChatGPT-like application that combines an LLM with multiple tools, memory, web search, and MCP-based tool integration to provide more useful and context-aware responses.

## Solution Overview

The application uses a **React frontend** and **FastAPI backend** with LangGraph-based workflow orchestration.

When a user sends a message:

1. The frontend sends the request to the FastAPI backend.
2. The backend processes the user's message.
3. LangGraph manages the AI workflow.
4. The appropriate tool is selected based on the request.
5. Tools such as calculator, weather, time, memory, and web search can be executed.
6. MCP tools can be accessed through the MCP client and MCP server.
7. Tool results are provided to the LLM.
8. The LLM generates the final response.
9. The response is returned to the frontend.

## Key Features

* ChatGPT-style conversational interface
* User registration and authentication
* Login and logout functionality
* Multiple chat sessions
* Conversation history
* User memory
* AI-powered responses
* LangGraph-based agent workflow
* Calculator tool
* Weather tool
* Time tool
* Web search using SerpAPI
* MCP Server integration
* MCP tool discovery
* MCP tool execution
* Feedback functionality
* Chat session deletion
* REST API using FastAPI
* Docker support
* Frontend and backend deployment support

## Technology Stack

### Frontend

* React.js
* Vite
* JavaScript
* CSS
* Axios

### Backend

* Python
* FastAPI
* Uvicorn
* SQLAlchemy
* SQLite
* Pydantic

### AI / Generative AI

* Large Language Models
* LangGraph
* OpenRouter
* Prompt Engineering

### Tools and APIs

* SerpAPI
* MCP (Model Context Protocol)
* Calculator Tool
* Weather Tool
* Time Tool
* Memory Tool
* Web Search Tool

### Deployment / DevOps

* Docker
* Render
* Git
* GitHub

## Batch

**2025**,**talentsmart-batch2**

## Developer Full Name

**Varri Jayanthi**

## Project Resources

* GitHub Repository: https://github.com/Jayanthivarri/ChatGPT-clone
* Live Application: https://chatgpt-clone-3-o44o.onrender.com
* Backend API: https://chatgpt-clone-2-a5ev.onrender.com


## How to Setup / Run

### 1. Clone the Repository

```bash
git clone https://github.com/Jayanthivarri/ChatGPT-clone
cd Chatgpt_clone
```

### 2. Backend Setup

Navigate to the backend folder:

```bash
cd backend
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment on Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file and add the required API keys and configuration values.

Run the backend:

```bash
uvicorn app.main:app --reload
```

The backend will run at:

```text
http://127.0.0.1:8000
```

### 3. Frontend Setup

Open another terminal and navigate to the frontend:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Run the frontend:

```bash
npm run dev
```

The frontend will be available at:

```text
http://localhost:5173
```

### 4. MCP Server Setup

Navigate to the MCP server directory:

```bash
cd mcp_server
```

Install the required MCP dependencies.

Run the MCP server:

```bash
python server.py
```

The MCP server can then be connected to the backend through the configured MCP server URL.

### 5. Docker Setup

Build the backend Docker image:

```bash
docker build -t chatgpt-backend .
```

Run the Docker container:

```bash
docker run --env-file .env -p 8000:8000 chatgpt-backend
```

The backend will then be accessible at:

```text
http://localhost:8000
```

## Project Architecture

```text
                    ┌─────────────────┐
                    │    React UI     │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │    FastAPI      │
                    │     Backend     │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │    LangGraph    │
                    │   Agent Flow    │
                    └───────┬─────────┘
                            │
              ┌─────────────┼─────────────┐
              │             │             │
              ▼             ▼             ▼
        Local Tools    MCP Client       LLM
              │             │
              │             ▼
              │       ┌─────────────┐
              │       │ MCP Server  │
              │       └──────┬──────┘
              │              │
              │        ┌─────┴─────┐
              │        │ MCP Tools │
              │        └───────────┘
              │
        ┌─────┴───────────────────────┐
        │ Calculator / Weather / Time │
        │ Memory / SerpAPI            │
        └─────────────────────────────┘
```

## Conclusion

This project demonstrates how a modern AI chatbot can combine an LLM with conversational memory, external APIs, tool calling, LangGraph workflow orchestration, and MCP-based tool integration to create a more capable AI assistant.

