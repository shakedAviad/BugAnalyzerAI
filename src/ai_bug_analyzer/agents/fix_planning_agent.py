from __future__ import annotations

from langchain.agents import create_agent

from ai_bug_analyzer.domain.schemas import FixPlanningInputSchema, FixPlanningOutputSchema
from ai_bug_analyzer.infrastructure.llm.factory import create_chat_model

FIX_PLANNING_SYSTEM_PROMPT: str = """
You are a senior Python bug fixing planner.

Your task is to create a minimal and correct fix plan for a failed project execution.

Return only a structured response that matches the required schema.

Rules:
1. Propose the smallest safe fix that is likely to solve the failure.
2. Only include files that are truly relevant to the fix.
3. Modify only the minimal set of files and code required to fix the issue.
4. Do not suggest unrelated refactors or improvements.
5. Use a confidence score between 0 and 1.
6. Add risk notes only when there is a real risk.
""".strip()


def build_fix_planning_agent():
    return create_agent(
        model=create_chat_model(),
        tools=[],
        system_prompt=FIX_PLANNING_SYSTEM_PROMPT,
        response_format=FixPlanningOutputSchema,
    )


def plan_fix(input_data: FixPlanningInputSchema) -> FixPlanningOutputSchema:
    agent = build_fix_planning_agent()

    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": (
                        f"Project path: {input_data.project_path}\n"
                        f"Command: {input_data.command}\n"
                        f"Failure type: {input_data.failure_type}\n"
                        f"Failure summary: {input_data.failure_summary}\n"
                        f"Root cause: {input_data.root_cause}\n"
                        f"Relevant files: {', '.join(str(file_path) for file_path in input_data.relevant_files) or 'None'}\n"
                        f"Relevant symbols: {', '.join(input_data.relevant_symbols) or 'None'}\n\n"
                        f"Stdout:\n{input_data.stdout}\n\n"
                        f"Stderr:\n{input_data.stderr}"
                    ),
                }
            ]
        }
    )

    structured_response = result["structured_response"]

    if not isinstance(structured_response, FixPlanningOutputSchema):
        raise TypeError("Agent did not return FixPlanningOutputSchema.")

    return structured_response
