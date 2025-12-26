from ddgs import DDGS


def online_retrieve(state):
    """
    Perform a lightweight online search to retrieve fresh information.

    - No API key required
    - Free-tier friendly
    - Demonstrates real online mode behavior
    """
    query = state.get("query", "")
    results = []

    if not query:
        return {"retrieved_context": []}

    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=5):
            body = r.get("body")
            if body:
                results.append(body)

    # 🔍 DEBUG LOG
    print("\n=== ONLINE SEARCH TRIGGERED ===")
    print(f"Query: {query}")
    for i, r in enumerate(results, 1):
        print(f"{i}. {r[:120]}...")
    print("=== END ONLINE SEARCH ===\n")

    return {
        "retrieved_context": results
    }
