import os
import sys
from graph import build_graph

def main():
    # Basic argument parsing
    if len(sys.argv) < 2:
        print("Usage: python main.py [--mode offline|online] <question>")
        sys.exit(1)

    # Default values
    mode = os.getenv("AGENT_MODE", "offline")
    query = None

    # Parse CLI arguments
    if "--mode" in sys.argv:
        idx = sys.argv.index("--mode")
        mode = sys.argv[idx + 1]
        query = sys.argv[idx + 2]
    else:
        query = sys.argv[1]

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
