# Nexus AI

> A Production-Grade Multi-Agent AI Platform Built From Scratch

Nexus AI is a modular AI platform designed to orchestrate LLMs, autonomous agents, tools, retrieval systems, memory, and persistent workflows through a production-oriented architecture.

The project focuses on building the core internals of an agentic AI framework from scratch instead of relying on high-level orchestration frameworks such as LangChain, LangGraph, CrewAI, or AutoGen.

---

## Overview

Nexus AI is not designed as a single chatbot.

It is a reusable AI platform where specialized agents and tools can be integrated into a common workflow execution system.

The current v1 platform includes specialized agents for:

* Planning
* Search
* Retrieval
* Reasoning
* Critique
* Response generation

The modular architecture is designed to support additional agent types in future versions.

The current v1 implementation provides the foundational infrastructure required to build and execute multi-agent AI workflows.

---

## Key Features

### Multi-Agent Architecture

Nexus AI provides a modular agent system with:

* Base agent abstraction
* Agent interfaces
* Planner Agent
* Search Agent
* Retrieval Agent
* Reasoning Agent
* Critic Agent
* Writer Agent
* Centralized Agent Executor

Agents communicate through shared workflow state and structured request/response models.

### Workflow Orchestration

The custom workflow engine manages the complete execution lifecycle.

Features include:

* Task planning
* Agent execution ordering
* Shared workflow state
* Agent communication
* Retry handling
* Execution history
* Workflow metrics
* Failure tracking
* Persistent workflow status

### LLM Layer

The LLM infrastructure includes:

* Ollama integration
* LLM client abstraction
* LLM routing
* Prompt management
* Structured JSON output

The architecture is designed to support additional LLM providers in the future.

### Retrieval-Augmented Generation

Nexus AI includes a custom RAG pipeline built using:

* PyMuPDF
* Sentence Transformers
* FAISS

The pipeline supports:

1. PDF ingestion
2. Text extraction
3. Document chunking
4. Embedding generation
5. Vector indexing
6. Semantic retrieval
7. Context injection into agent workflows

### Persistent Memory

Conversation memory is persisted using SQLAlchemy.

The memory layer supports:

* User messages
* Assistant messages
* Session-based memory
* User-scoped memory
* Context reconstruction
* Persistent conversation history

Memory survives application restarts.

### Workflow Persistence

Workflow execution data is stored in the database.

Persisted information includes:

* Workflow ID
* User ID
* Session ID
* Task
* Workflow status
* Execution metrics
* Agent execution history
* Creation timestamp
* Completion timestamp

### Authentication and User Isolation

Nexus AI provides JWT-based authentication.

Security features include:

* User registration
* Password hashing with Argon2
* User authentication
* JWT access tokens
* Protected API endpoints
* Authenticated user dependencies
* User-scoped conversation memory
* User-scoped workflow data

### Production Hardening

The API includes production-oriented safeguards:

* Centralized exception handlers
* Structured error responses
* Request validation
* File upload validation
* Upload size limits
* PDF content-type validation
* Security headers
* Configuration validation

### Observability

Workflow execution includes:

* Structured logging
* Workflow IDs
* Agent execution metrics
* Execution history
* Retry tracking
* Success and failure metrics

### Containerization

Nexus AI is containerized using Docker and Docker Compose.

Container features include:

* Production Dockerfile
* Docker Compose runtime
* Persistent database volume
* Persistent log volume
* Container healthcheck
* Ollama host integration
* Automatic restart policy

---

## System Architecture

```text
User
  |
  v
FastAPI API
  |
  +-------------------+
  | JWT Authentication|
  +-------------------+
  |
  v
Workflow Engine
  |
  +--------------------+
  |                    |
  v                    v
Planner Agent      Memory Manager
  |                    |
  v                    v
Execution Plan     Persistent Memory
  |
  v
Agent Executor
  |
  +-------------+-------------+-------------+
  |             |             |             |
  v             v             v             v
Search       Retrieval     Reasoning      Critic
Agent          Agent         Agent         Agent
  |             |             |             |
  +-------------+-------------+-------------+
                        |
                        v
                   Writer Agent
                        |
                        v
                  Final Response
                        |
          +-------------+-------------+
          |                           |
          v                           v
 Workflow Persistence         Execution Metrics
```

---

## Technology Stack

| Category          | Technology            |
| ----------------- | --------------------- |
| Language          | Python 3.12           |
| Backend           | FastAPI               |
| Validation        | Pydantic              |
| Configuration     | Pydantic Settings     |
| LLM               | Ollama                |
| Embeddings        | Sentence Transformers |
| Vector Search     | FAISS                 |
| PDF Parsing       | PyMuPDF               |
| ORM               | SQLAlchemy            |
| Authentication    | JWT                   |
| Password Hashing  | Argon2                |
| HTTP Client       | HTTPX                 |
| Retry             | Tenacity              |
| Logging           | Loguru                |
| JSON              | orjson                |
| Deployment        | Docker                |
| Container Runtime | Docker Compose        |

---

## Project Structure

```text
nexus-ai/
|
├── agents/                 # Agent implementations and execution
├── api/                    # FastAPI routes, schemas, middleware
├── auth/                   # JWT authentication and security
├── configs/                # Application settings
├── core/                   # Logging and core utilities
├── database/               # Database models and repositories
├── llm/                    # LLM clients and routing
├── memory/                 # Persistent conversation memory
├── models/                 # Shared application models
├── observability/          # Metrics and tracing
├── prompts/                # Prompt management
├── rag/                    # RAG and vector retrieval pipeline
├── tests/                  # Unit and integration tests
├── tools/                  # Tool registry and execution
├── workflow/               # Workflow orchestration engine
|
├── .env.example
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── main.py
├── requirements.txt
└── README.md
```

---

## Getting Started

### Prerequisites

Ensure the following are installed:

* Python 3.12
* Conda
* Docker
* Docker Compose
* Ollama

The default Nexus AI model is:

```text
qwen3:4b
```

Pull the model using Ollama:

```bash
ollama pull qwen3:4b
```

---

## Local Development Setup

Clone the repository:

```bash
git clone <your-repository-url>
cd nexus-ai
```

Create the Conda environment:

```bash
conda create -n nexus-ai python=3.12
conda activate nexus-ai
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create the environment file:

### Windows PowerShell

```powershell
Copy-Item .env.example .env
```

### Linux or macOS

```bash
cp .env.example .env
```

Update the JWT secret in `.env` before running the application.

Start Ollama:

```bash
ollama serve
```

Run Nexus AI:

```bash
uvicorn main:app --reload
```

The API will be available at:

```text
http://localhost:8000
```

Interactive API documentation:

```text
http://localhost:8000/docs
```

---

## Docker Deployment

Ensure Ollama is running on the host machine.

Build and start Nexus AI:

```bash
docker compose up -d --build
```

Check container status:

```bash
docker compose ps
```

Inspect application logs:

```bash
docker compose logs -f nexus-ai
```

Stop the application:

```bash
docker compose down
```

Docker Compose persists:

* Application database
* Application logs

using dedicated Docker volumes.

---

## API Overview

### Health Check

```text
GET /health
```

### User Registration

```text
POST /auth/register
```

### User Login

```text
POST /auth/login
```

### Chat

```text
POST /chat
```

Requires JWT authentication.

### Document Upload

```text
POST /documents/upload
```

Accepts validated PDF documents.

### Workflow History

```text
GET /workflows/{workflow_id}
```

Requires JWT authentication and enforces workflow ownership.

---

## Authentication

Register a user and login through the authentication API.

The login endpoint returns a JWT access token.

Protected endpoints require:

```text
Authorization: Bearer <access-token>
```

Authentication is used to isolate user memory and workflow execution data.

---

## Testing

Nexus AI includes unit and integration tests for critical platform components.

Run authentication tests:

```bash
python -m tests.unit.test_authentication
```

Run authentication API tests:

```bash
python -m tests.integration.test_auth_api
```

Run protected API tests:

```bash
python -m tests.integration.test_protected_chat
```

Run user isolation tests:

```bash
python -m tests.integration.test_user_isolation
```

Run workflow persistence tests:

```bash
python -m tests.integration.test_workflow_persistence
```

Run workflow execution data tests:

```bash
python -m tests.integration.test_workflow_execution_data
```

Run production hardening tests:

```bash
python -m tests.integration.test_production_hardening
```

Run Nexus AI v1 regression tests:

```bash
python -m tests.integration.test_nexus_v1_regression
```

Run container runtime tests after starting Docker Compose:

```bash
python -m tests.integration.test_container_runtime
```

---

## Engineering Principles

Nexus AI follows three core engineering principles.

### Build Core AI Infrastructure From Scratch

Core orchestration components are implemented directly in the project:

* Agent system
* Workflow engine
* Tool registry
* Memory layer
* Prompt manager
* State management
* Agent executor
* LLM router

### Use Mature Infrastructure Libraries

Mature libraries are used where rebuilding the functionality would not provide architectural value.

Examples include:

* FastAPI
* FAISS
* SQLAlchemy
* Sentence Transformers
* PyMuPDF
* Ollama

### Framework Independence

Nexus AI v1 does not depend on high-level agent orchestration frameworks.

The following frameworks are intentionally excluded from v1:

* LangChain
* LangGraph
* CrewAI
* AutoGen

The goal is to understand and implement the underlying agentic AI architecture directly.

---

## Future Roadmap

Potential v2 improvements include:

* PostgreSQL
* Redis
* MCP integration
* Agent-to-Agent communication
* LangGraph integration
* Celery workers
* Browser Agent
* SQL Agent
* GitHub Agent
* Code execution
* Multimodal support
* Voice support
* Production monitoring
* Kubernetes deployment

---

## Project Status

Nexus AI v1 is currently in final release validation.

Core platform architecture, persistence, authentication, user isolation, production hardening, and containerization are implemented.

---

## Author

**Avinash Singh**

AI / Machine Learning Engineer

GitHub: Avinashvns

---

## License

This project is intended for educational, engineering portfolio, and research purposes.
