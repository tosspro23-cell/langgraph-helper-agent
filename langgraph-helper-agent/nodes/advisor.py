from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

def synthesize_answer(state):
    llm = ChatGoogleGenerativeAI(
        model="models/gemini-1.5-flash",
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

    return {
        "final_answer": response.content
    }

