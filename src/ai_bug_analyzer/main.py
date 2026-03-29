from __future__ import annotations

from app.bootstrap import bootstrap_application
from app.graph import build_graph


def main() -> None:
    state = bootstrap_application()

    graph = build_graph()

    result = graph.invoke(
        state,
        config={
            "configurable": {
                "thread_id": "bug-analyzer-run-1",
            },
        },
    )

    final_outcome = result.get("final_outcome")

    if final_outcome is not None:
        print("\n=== FINAL RESULT ===")
        print(f"Status: {final_outcome.final_status}")
        print(f"Summary: {final_outcome.summary}")
        print(f"Iterations: {final_outcome.total_iterations}")
        print(f"Resolved: {final_outcome.resolved}")
        print(f"Changed files: {final_outcome.changed_files}")
    else:
        print("No final outcome was produced.")


if __name__ == "__main__":
    main()
