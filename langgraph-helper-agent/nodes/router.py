def route_by_mode(state):
    if state["mode"] == "offline":
        return "offline_retrieval"
    return "online_retrieval"
