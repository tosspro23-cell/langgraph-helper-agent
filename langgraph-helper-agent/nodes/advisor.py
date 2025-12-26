from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate

def synthesize_answer(state):
    llm = ChatGoogleGenerativeAI(model="gemini-pro")

    prompt = ChatPromptTemplate.from_template(
        """
You are a technical advisor helping developers design LangGraph systems.

Explain concepts, rationale, and trade-offs.
Avoid code-only answers.

Context:
{context}

Question:
{question}
"""
    )

    response = llm.invoke(
        prompt.format(
            context="\n".join(state["retrieved_context"]),
            question=state["query"],
        )
    )

    return {"final_answer": response.content}

