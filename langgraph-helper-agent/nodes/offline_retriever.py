def offline_retrieve(state):
    """
    Offline retrieval using locally stored llms.txt documentation.
    This ensures offline mode does not rely on model internal knowledge.
    """
    docs = []

    paths = [
        "data/langgraph_llms.txt",
        "data/langchain_llms.txt",
    ]

    for path in paths:
        try:
            with open(path, "r", encoding="utf-8") as f:
                docs.append(f.read())
        except FileNotFoundError:
            docs.append(f"[ERROR] Missing offline documentation file: {path}")

    return {
        "retrieved_context": docs
    }
