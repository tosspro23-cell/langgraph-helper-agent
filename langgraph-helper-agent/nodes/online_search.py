from duckduckgo_search import DDGS

def online_search(state):
    query = state["query"]
    results = []

    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=5):
            results.append(r["body"])

    return {
        "retrieved_context": results
    }
