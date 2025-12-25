from langgraph.graph import StateGraph, END
from state import AgentState
from nodes.router import route_by_mode
from nodes.offline_retriever import offline_retrieve
from nodes.online_retriever import online_retrieve
from nodes.advisor import synthesize_answer

def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("router", lambda s: s)
    graph.add_node("offline_retrieval", offline_retrieve)
    graph.add_node("online_retrieval", online_retrieve)
    graph.add_node("advisor", synthesize_answer)

    graph.set_entry_point("router")

    graph.add_conditional_edges(
        "router",
        route_by_mode,
        {
            "offline_retrieval": "offline_retrieval",
            "online_retrieval": "online_retrieval",
        },
    )

    graph.add_edge("offline_retrieval", "advisor")
    graph.add_edge("online_retrieval", "advisor")
    graph.add_edge("advisor", END)

    return graph.compile()
