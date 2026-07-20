# Insurance Policy Advisory Copilot

AI-powered Insurance Policy Advisory Assistant built using LangChain,
FastAPI, Streamlit, RAG, ChromaDB, Redis, and MCP.

This project demonstrates an enterprise-style Generative AI application
that can: - Answer insurance policy questions - Retrieve information
from policy documents - Classify customer intent - Route requests to
specialist agents - Provide grounded answers with citations

------------------------------------------------------------------------
This project has 2 major directtories -
1. app
2. frontend

app - It has all the backend python classes and functionality implementation
frontend - It has streamlit implementation

# Features

## AI Agent

-   LangChain based agent
-   Tool calling
-   Deterministic intent classification
-   Retrieval-Augmented Generation (RAG)
-   Conversation memory

## Insurance Capabilities

The assistant supports:

-   Policy coverage queries
-   Benefits and exclusions
-   Claim process information
-   Claim document requirements
-   Premium related questions
-   Policy renewal queries
-   Payment issues

## Specialist Agents

The project contains specialist agents:

-   Claim Specialist
    -   Claim status
    -   Claim process
    -   Required documents
-   Policy Specialist
    -   Coverage
    -   Benefits
    -   Exclusions
-   Renewal Specialist
    -   Policy renewal
    -   Premium payment
    -   Policy expiry

------------------------------------------------------------------------

# Technology Stack

  Component         Technology
  ----------------- -------------------
  Backend           FastAPI
  Frontend          Streamlit
  LLM Framework     LangChain
  Vector Database   ChromaDB
  Embeddings        OpenAI Embeddings
  Memory            Redis / Upstash
  Observability     LangSmith
  Protocol          MCP

------------------------------------------------------------------------

# Project Setup

## 1. Clone Repository

``` bash
git clone <repository-url>

cd insurance-policy-copilot
```

------------------------------------------------------------------------

## 2. Create Virtual Environment

### Windows

``` powershell
python -m venv venv

venv\Scripts\activate
```

### Linux / Mac

``` bash
python3 -m venv venv

source venv/bin/activate
```

------------------------------------------------------------------------

## 3. Install Dependencies

``` bash
pip install -r requirements.txt
```

------------------------------------------------------------------------

# Environment Configuration

Create a `.env` file:

``` env
OPENAI_API_KEY=your-openai-key

LANGSMITH_TRACING=true
LANGSMITH_API_KEY=your-langsmith-key
LANGSMITH_PROJECT=insurance-policy-copilot

UPSTASH_REDIS_REST_URL=your-upstash-url
UPSTASH_REDIS_REST_TOKEN=your-upstash-token
```

------------------------------------------------------------------------

# Knowledge Base Setup

Add insurance documents:

    data/
     └── knowledge_base/
          ├── health_policy.pdf
          ├── motor_policy.pdf
          ├── claim_guidelines.pdf
          ├── renewal_policy.pdf
          └── insurance_faq.pdf

Build vector database:

``` bash
python -m app.rag.ingest
```

Process: - Load documents - Split documents into chunks - Create
embeddings - Store vectors in ChromaDB

------------------------------------------------------------------------

# Run Application

## Backend

``` bash
uvicorn app.main:app --reload
```

API:

    http://localhost:8000

Swagger:

    http://localhost:8000/docs

## Frontend

``` bash
streamlit run frontend/streamlit.py
```

------------------------------------------------------------------------

# MCP Server

Run MCP server:

``` bash
python -m app.mcp_server.server
```

Available tools:

  Tool                      Purpose
  ------------------------- ----------------------------
  classify_intent           Identify customer request
  knowledge_retrieval       Search insurance documents
  calculate_premium         Calculate premium
  check_claim_eligibility   Check claim eligibility

------------------------------------------------------------------------

# Intent Categories

The assistant classifies queries into:

-   claim_intent_or_status
-   policy_information_query
-   renewal_or_lapse
-   premium_payment_issue
-   complaint_or_escalation
-   fraud_or_scam
-   general_faq

------------------------------------------------------------------------

# RAG Flow

    Customer Query

          |

    Intent Classification

          |

    Specialist Agent Routing

          |

    Knowledge Retrieval

          |

    LLM Response

          |

    Answer with Citations

------------------------------------------------------------------------

# Prompt Management

Prompt files:

    prompts/

    system_prompt.yaml

    classification_prompt.yaml

    rag_answer.yaml

    few_shot_examples.yaml

Benefits: - Easy maintenance - Version controlled prompts - Simple
updates

------------------------------------------------------------------------

# User Roles

Role based access:

  Role             Access
  ---------------- -----------------------------
  Customer         General policy information
  Agent            Product and premium details
  Claims Officer   Claim documents
  Admin            Full access

------------------------------------------------------------------------

# Testing

Run tests:

``` bash
pytest
```

Debug commands:

Check Python:

``` bash
python --version
```

Check packages:

``` bash
pip list
```

Check API:

``` bash
curl http://localhost:8000/health
```

------------------------------------------------------------------------

# Project Summary

Insurance Policy Advisory Copilot combines:

-   Generative AI
-   RAG
-   LangChain Agents
-   MCP tools
-   Vector Search
-   Role-based security

to provide a secure AI assistant for insurance policy guidance.
