from __future__ import annotations

from domain.models import FixPlan
from domain.schemas import FixPlanningInputSchema
from infrastructure.llm.factory import create_chat_model
from langchain.agents import create_agent

FIX_PLANNING_SYSTEM_PROMPT: str = """
You are an expert software engineer responsible for planning fixes for failing code.

Your task is to create a precise and minimal fix plan based on:
- Failure classification
- Execution results
- Project context

Your goal is to:
1. Identify the most likely location of the bug.
2. Propose a minimal and correct fix.
3. Clearly describe what needs to change and why.
4. Avoid unnecessary or unrelated modifications.

Critical rules:

1. Always prioritize fixing the ROOT CAUSE of the problem.
2. Do not blindly trust the file where the failure occurred — especially in test scenarios.
3. If a test fails:
   - Assume the test is correct unless there is strong evidence otherwise.
   - Prefer fixing the implementation code instead of modifying the test.
4. NEVER modify a test just to make it pass.
5. Only modify tests if:
   - The test is clearly incorrect, OR
   - The expected behavior is wrong by design
6. Keep the fix as small and focused as possible.
7. Do not introduce new features — only fix the bug.
8. Avoid speculative fixes — base your plan on the available evidence.
9. If multiple files are involved, prioritize the most likely source of the issue.

The output should:
- Clearly describe which file(s) to modify
- Explain what change is required
- Be actionable and deterministic

Return a structured response that strictly matches the expected schema.
""".strip()


def build_fix_planning_agent():
    return create_agent(
        model=create_chat_model(),
        tools=[],
        system_prompt=FIX_PLANNING_SYSTEM_PROMPT,
        response_format=FixPlan,
    )


def plan_fix(input_data: FixPlanningInputSchema) -> FixPlan:
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

    if not isinstance(structured_response, FixPlan):
        raise TypeError("Agent did not return FixPlan.")

    return structured_response
