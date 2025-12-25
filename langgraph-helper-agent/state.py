from typing import TypedDict, Literal, List

class AgentState(TypedDict):
    query: str
    mode: Literal["offline", "online"]
    retrieved_context: List[str]
    final_answer: str
