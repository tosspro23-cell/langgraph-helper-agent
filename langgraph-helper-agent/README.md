# LangGraph Helper Agent

A LangGraph-based technical advisor agent designed to help developers understand, design, and reason about LangGraph and LangChain systems.

---

## 1. Project Overview

This project implements a **LangGraph Helper Agent** focused on system design and architectural reasoning rather than pure code generation.

The agent is intentionally positioned as a **technical advisor**, helping developers understand:

- Why certain designs are recommended
- How different approaches compare
- What trade-offs exist in production-grade agent systems

The goal is to provide clear, structured guidance that supports long-term system thinking rather than short-term code output.

---

## 2. Design Philosophy

### 2.1 Technical Advisor over Code Generator

This agent optimizes for **decision quality**, not code throughput.

Most real-world issues in LangGraph-based systems arise **before code is written**—in architecture, state design, and control-flow decisions.  
Accordingly, the agent focuses on explaining concepts, rationale, and trade-offs instead of producing narrowly scoped code snippets.

---

### 2.2 Coverage-First Offline Mode

Offline mode prioritizes **conceptual coverage and completeness** over narrowly deterministic answers.

Instead of retrieving a single “best” document chunk, the agent aggregates multiple relevant perspectives to help developers build a correct **mental model**, even without internet access.

This approach reduces the risk of misunderstanding when documentation is incomplete or outdated.

---

### 2.3 Simplicity as a Scalability Strategy

The system intentionally starts with:

- A minimal graph
- A small, explicit state schema
- Clear node responsibilities

This simplicity is deliberate.  
Rather than optimizing for feature richness, the design optimizes for **clarity, predictability, and long-term extensibility**.

---

## 3. High-Level Architecture

### 3.1 Graph Overview

The agent is implemented as a single **LangGraph StateGraph** with mode-aware routing:

```text
User Input
   ↓
Mode Router
   ↓
Knowledge Retrieval
  ├─ Offline Knowledge Aggregator
  └─ Online Knowledge Retriever
   ↓
Advisor Answer Synthesizer
   ↓
Final Response
```

Both offline and online paths converge into the same synthesis node to ensure consistent answer structure and quality.

---

### 3.2 Why StateGraph (Not MessageGraph)

This project intentionally uses **StateGraph** instead of MessageGraph to keep agent behavior explicit, predictable, and scalable.

StateGraph enables:

- Explicit state management
- Deterministic routing decisions
- Clear separation between control logic and language generation
- Easier debugging and reasoning as the system grows

Implicit message-driven decision making is intentionally avoided, as it can cause behavior drift when the agent adapts too strongly to conversational context rather than architectural intent.

---

## 4. Agent State Schema

The agent uses a minimal and explicit state schema:

- `query`  
  The original user question and immutable starting point.

- `mode`  
  Execution mode: `offline` or `online`.

- `retrieved_context`  
  Aggregated knowledge retrieved from documentation or online sources.

- `final_answer`  
  The synthesized, structured response returned to the user.

Raw message history is intentionally excluded to avoid hidden coupling between nodes and to keep system reasoning transparent.

---

## 5. Node Responsibilities

Each node follows a **single-responsibility principle**, ensuring clarity and maintainability.

---

### Mode Router

- Reads the execution mode from state
- Selects the appropriate retrieval path
- Contains control logic only
- Does not perform retrieval or generation

---

### Offline Knowledge Aggregator

- Uses locally indexed documentation (e.g. `llms.txt`)
- Retrieves multiple relevant segments
- Prioritizes conceptual coverage and completeness
- Writes aggregated content into `retrieved_context`

This mode is optimized for learning and architectural understanding rather than precision recall.

---

### Online Knowledge Retriever

- Uses free-tier online search services
- Focuses on information freshness
- Does not persist external data
- Acts as a complement to offline knowledge

---

### Advisor Answer Synthesizer

This node represents the core value of the agent as a **technical advisor**.

Responsibilities include:

- Combining retrieved knowledge
- Explaining concepts and rationale
- Highlighting trade-offs and alternatives
- Producing structured, educational responses

The output style is consistent regardless of the retrieval source.

---

## 6. Operating Modes

### 6.1 Offline Mode

- No external web access
- Uses local documentation only
- Suitable for restricted or disconnected environments
- Optimized for conceptual depth and completeness

---

### 6.2 Online Mode

- Allows internet connectivity
- Uses free-tier external services
- Focuses on up-to-date information
- Complements offline knowledge

Execution mode can be controlled via environment variables or command-line flags.

---

## 7. LLM Configuration

### Language Model

This project uses **Google Gemini (free tier)** as the default language model via LangChain’s `ChatGoogleGenerativeAI`.

Gemini was chosen because:

- It provides a generous free tier
- It integrates cleanly with LangChain
- It is sufficient for advisory-style, reasoning-focused responses

---

### API Key Setup

To run the agent, a Gemini API key must be set as an environment variable.

1. Obtain an API key from Google AI Studio:  
   https://aistudio.google.com/app/apikey

2. Set the environment variable:

```bash
export GOOGLE_API_KEY=your_api_key_here
```

No API key is required to review the architecture or extend the system without executing LLM calls.

---

## 8. Offline Data Strategy

### Data Sources

In offline mode, the agent relies exclusively on locally available documentation.

Primary data sources include:

- LangChain documentation  
  https://docs.langchain.com/llms.txt  
  https://docs.langchain.com/llms-full.txt

- LangGraph documentation  
  https://langchain-ai.github.io/langgraph/llms.txt  
  https://langchain-ai.github.io/langgraph/llms-full.txt

These files are intended to be downloaded and indexed locally.

---

### Data Preparation Approach

Offline retrieval is designed to be **coverage-first**:

- Multiple relevant sections are retrieved per query
- The goal is conceptual completeness rather than narrow precision
- This supports architectural understanding without internet access

---

### Data Update Strategy

If documentation changes, users can refresh offline data by:

1. Re-downloading the latest `llms.txt` or `llms-full.txt` files
2. Re-indexing them using the same local ingestion process

No automated update mechanism is enforced to keep the system simple and transparent.

---

## 9. Online Data Strategy

In online mode, the agent is allowed to access external sources to complement offline documentation with up-to-date information.

### External Services

The architecture allows integration with free-tier providers such as:

- DuckDuckGo
- Tavily
- SerpAPI (free tier)

These services are intentionally not tightly coupled to the graph to preserve flexibility.

---

### Rationale

Online retrieval is used to:

- Access the latest LangGraph or LangChain updates
- Validate best practices against recent changes
- Complement offline knowledge without replacing it

API keys for external services can be configured as environment variables following each provider’s documentation.

---

## 10. LangGraph vs LangChain Usage

This project deliberately separates **behavior control** from **capability access**:

- **LangGraph** is used as the orchestration and control layer:
  - Defines execution order
  - Controls routing and decision logic
  - Manages explicit system state

- **LangChain** is used as a capability layer:
  - LLM abstractions
  - Prompt templates
  - Retrieval and utility components

LangChain components are orchestrated by LangGraph but do not drive system flow.

---

## 11. Example Questions

The agent is designed to handle questions such as:

- How do I add persistence to a LangGraph agent?
- What is the difference between StateGraph and MessageGraph?
- How can I implement human-in-the-loop workflows with LangGraph?
- How should errors and retries be handled in LangGraph nodes?
- What are best practices for state management in LangGraph?

Rather than returning isolated code snippets, the agent explains underlying concepts, trade-offs, and architectural considerations.

---

## 12. How to Run

### Setup

1. Clone the repository
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set required environment variables (for online mode):

```bash
export GOOGLE_API_KEY=your_api_key_here
```

---

### Run the Agent

```bash
python main.py "How do I add persistence to a LangGraph agent?"
```

To enable online mode:

```bash
export AGENT_MODE=online
python main.py "What are the latest LangGraph features?"
```

The project is designed to be runnable on any machine with Python and minimal setup.

---

## 13. Summary

This project demonstrates how **LangGraph can be used as a system design tool**, not just an agent orchestration framework.

By making agent behavior, state, and control flow explicit, the system remains:

- Easier to reason about
- Easier to debug
- Easier to extend across different project contexts

The result is an agent designed for architectural correctness and long-term scalability rather than prompt-based implicit behavior.
