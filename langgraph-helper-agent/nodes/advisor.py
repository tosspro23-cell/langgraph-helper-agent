from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import os

def synthesize_answer(state):
    llm = ChatOpenAI(
        model="openai/gpt-4o-mini",
        api_key=os.getenv("OPENROUTER_API_KEY"),
        base_url="https://openrouter.ai/api/v1",
        temperature=0.3
    )

    prompt = ChatPromptTemplate.from_template(
        """
        You are a technical advisor for LangGraph and LangChain.

        Question:
        {query}

        Context:
        {context}

        Provide a clear, structured, and explanatory answer.
        """
    )

    response = llm.invoke(
        prompt.format(
            query=state["query"],
            context="\n".join(state.get("retrieved_context", []))
        )
    )

    return {"final_answer": response.content}
