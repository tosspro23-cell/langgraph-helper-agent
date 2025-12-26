def offline_retrieve(state):
    """
    Offline retrieval using locally stored llms.txt documentation.

    This node explicitly loads local documentation files to ensure
    offline mode does not rely on model internal knowledge.
    """
    docs = []

    paths = [
        "data/langgraph_llms.txt",
        "data/langchain_llms.txt",
    ]

    print("\n=== OFFLINE RETRIEVER TRIGGERED ===")

    for path in paths:
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
                docs.append(content)
                print(f"[OK] Loaded offline document: {path} ({len(content)} chars)")
        except FileNotFoundError:
            error_msg = f"[ERROR] Missing offline documentation file: {path}"
            print(error_msg)
            docs.append(error_msg)

    print("=== END OFFLINE RETRIEVER ===\n")

    return {
        "retrieved_context": docs
    }
