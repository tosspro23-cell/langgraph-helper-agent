import os
import sys
from graph import build_graph

def main():
    query = sys.argv[1]
    mode = os.getenv("AGENT_MODE", "offline")

    app = build_graph()

    result = app.invoke(
        {
            "query": query,
            "mode": mode,
            "retrieved_context": [],
            "final_answer": "",
        }
    )

    print(result["final_answer"])

if __name__ == "__main__":
    main()
