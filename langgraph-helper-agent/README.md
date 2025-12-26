# LangGraph Helper Agent

A **dual-mode AI technical advisor** built with **LangGraph** to help developers understand, design, and reason about **LangGraph** and **LangChain** systems.

This project is designed as an **assignment-grade, production-minded reference implementation**, emphasizing **explicit control, safety, and explainability** over speculative or implicit agent behavior.

---

## 1. Project Overview

The **LangGraph Helper Agent** is intentionally positioned as a **technical advisor**, not a pure code generator.

It helps developers:

- Understand *why* certain LangGraph patterns exist  
- Compare architectural alternatives and trade-offs  
- Reason about state, control flow, and scalability  
- Avoid hallucination, especially for future-facing questions  

The agent supports **explicit Offline and Online modes**, fully controlled by the user via CLI flags or environment variables.

---

## 2. Design Philosophy

### 2.1 Technical Advisor over Code Generator

Most failures in agent systems happen **before code is written**—in architecture, state design, and control flow.

Accordingly, this agent optimizes for:

- Decision quality  
- Conceptual clarity  
- System-level thinking  

Rather than generating large amounts of code, the agent explains **design rationale**, **trade-offs**, and **best practices**.

---

### 2.2 Coverage-First Offline Mode

Offline mode prioritizes **coverage and completeness** over narrow precision.

Instead of returning a single “best” snippet, the agent aggregates multiple relevant perspectives to help developers form a **correct mental model**, even without internet access.

This reduces misunderstanding when documentation is incomplete or fragmented.

---

### 2.3 Simplicity as a Scalability Strategy

The system intentionally starts with:

- A minimal graph topology  
- A small, explicit state schema  
- Clear node responsibilities  

This simplicity is deliberate.  
It makes the system easier to reason about, debug, and extend into production features like persistence, memory, and evaluation.

---

## 3. High-Level Architecture

### 3.1 Graph Overview

The agent is implemented as a single **LangGraph StateGraph** with explicit, mode-based routing:

```
User Input
   ↓
[ Router ]
   ↓
   ├─ offline → [ Offline Retriever ] → [ Advisor ] → END
   └─ online  → [ Online Retriever  ] → [ Advisor ] → END
```

Both paths converge into the same **Advisor** node to ensure consistent answer quality and structure.

---

### 3.2 Why StateGraph (Not MessageGraph)

This project deliberately uses **StateGraph** instead of MessageGraph.

Reasons:

- Explicit state management  
- Deterministic routing  
- Clear separation of control logic and LLM behavior  
- Easier debugging and long-term scalability  

MessageGraph-style implicit, history-driven decisions are intentionally avoided to prevent behavioral drift and hidden coupling.

---

## 4. Agent State Schema

The agent uses a minimal, explicit state schema:

- **query**  
  The original user question (immutable input).

- **mode**  
  Execution mode: `offline` or `online`.

- **retrieved_context**  
  Aggregated knowledge from offline documents or online search.

- **final_answer**  
  The synthesized, structured response returned to the user.

Raw message history is intentionally excluded to keep reasoning transparent and deterministic.

---

## 5. Node Responsibilities

Each node follows a **single-responsibility principle**.

### Router
- Reads execution mode
- Selects retrieval path
- Contains control logic only

### Offline Retriever
- Uses local documentation (e.g. `llms.txt`)
- Aggregates multiple relevant sections
- Optimized for conceptual completeness

### Online Retriever
- Executes live web search (DuckDuckGo via `ddgs`)
- Focuses on freshness and recency
- Does not persist external data

### Advisor
- Synthesizes retrieved context
- Explains concepts and trade-offs
- Produces structured, educational answers
- Maintains consistent tone across modes

---

## 6. Operating Modes

### Offline Mode
- No internet access
- Uses local documentation only
- Deterministic and reproducible
- Ideal for restricted environments

### Online Mode
- Enables live web search
- Retrieves recent updates and announcements
- Avoids speculation if evidence is weak

---

## 7. Mode Switching

### Command Line

```bash
python main.py --mode offline "How do I use LangGraph checkpointers?"
python main.py --mode online "What are the latest LangGraph features?"
```

### Environment Variable

```bash
export AGENT_MODE=online
python main.py "What are the latest LangGraph features?"
```

Mode selection is **explicit** and never inferred from the question text.

---

## 8. LLM Configuration

### Default Model

The current implementation uses **OpenRouter-compatible models** (e.g. GPT-4o-mini, Qwen, etc.) via LangChain.

This choice was made because:

- Stable free-tier availability  
- Consistent API behavior  
- Avoids Gemini free-tier instability  

The LLM is used **only in the Advisor node**; it never controls routing.

---

### API Key Setup (OpenRouter)

1. Create an API key at:  
   https://openrouter.ai/

2. Set environment variable:

```bash
export OPENROUTER_API_KEY=your_key_here
```

---

## 9. Offline Data Strategy

### Data Sources

Offline mode relies on locally downloaded documentation:

- LangChain  
  https://docs.langchain.com/llms.txt  
  https://docs.langchain.com/llms-full.txt

- LangGraph  
  https://langchain-ai.github.io/langgraph/llms.txt  
  https://langchain-ai.github.io/langgraph/llms-full.txt

---

### Data Preparation

- Documents are stored locally
- Retrieved as plain text
- Aggregated for conceptual coverage
- No vector database required at this stage

---

### Data Update Strategy

To refresh offline data:

1. Re-download latest `llms.txt` files
2. Replace local copies

No automation is enforced to keep the system transparent and auditable.

---

## 10. Online Data Strategy

### External Services

- DuckDuckGo search via `ddgs` (free tier)

### Rationale

Online retrieval is used to:

- Validate recency-sensitive questions
- Access latest LangGraph / LangChain updates
- Complement offline knowledge

If search results are weak or inconclusive, the agent will **explicitly state uncertainty**.

---

## 11. LangGraph vs LangChain Roles

- **LangGraph**
  - Orchestration layer
  - State management
  - Routing and control flow

- **LangChain**
  - Capability layer
  - LLM abstractions
  - Prompt templates and utilities

LangChain components never drive control flow directly.

---

## 12. Example Questions

- How do I add persistence to a LangGraph agent?
- What is the difference between StateGraph and MessageGraph?
- How can I implement human-in-the-loop workflows?
- How should retries and errors be handled?
- What are best practices for state design in LangGraph?

The agent answers by explaining **principles**, not just snippets.

---

## 13. How to Run

### Setup

```bash
pip install -r requirements.txt
```

### Run

```bash
python main.py "How do I add persistence to a LangGraph agent?"
```

Online mode:

```bash
export AGENT_MODE=online
python main.py "What are the latest LangGraph features?"
```

---

## 14. Summary

This project demonstrates how **LangGraph can be used as a system design tool**, not just an agent framework.

By keeping behavior explicit and state controlled, the agent remains:

- Predictable  
- Debuggable  
- Production-extensible  

This makes it suitable for both technical evaluation and real-world system design.
