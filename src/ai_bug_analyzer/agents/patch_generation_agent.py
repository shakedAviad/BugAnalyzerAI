from __future__ import annotations

from domain.models import GeneratedPatch
from domain.schemas import PatchGenerationInputSchema
from infrastructure.llm.factory import create_chat_model
from langchain.agents import create_agent

PATCH_GENERATION_SYSTEM_PROMPT: str = """
You are updating an existing Python file.

You will receive the current full file content and a fix plan.

Your task is to return the FULL UPDATED FILE CONTENT for each file.

Critical rules:
1. Return the complete updated file content, not a diff.
2. Do not return only the changed lines.
3. Do not return only a function or a code snippet.
4. Preserve all existing valid code unless it must be changed to fix the bug.
5. Keep imports, function definitions, and unrelated logic intact.
6. Apply only the minimal required fix.
7. The returned file content must be a complete valid replacement for the original file.
""".strip()


def build_patch_generation_agent():
    return create_agent(
        model=create_chat_model(),
        tools=[],
        system_prompt=PATCH_GENERATION_SYSTEM_PROMPT,
        response_format=GeneratedPatch,
    )


def generate_patch(input_data: PatchGenerationInputSchema) -> GeneratedPatch:
    agent = build_patch_generation_agent()

    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": (
                        f"Project path: {input_data.project_path}\n"
                        f"Fix summary: {input_data.fix_summary}\n"
                        f"Fix rationale: {input_data.fix_rationale}\n"
                        f"Planned changes:\n"
                        + "\n".join(
                            [
                                (
                                    f"- File: {change.file_path} | "
                                    f"Reason: {change.reason} | "
                                    f"Change type: {change.change_type} | "
                                    f"Target symbol: {change.target_symbol or 'None'}"
                                    f"Original content: {change.original_content}"
                                )
                                for change in input_data.changes
                            ]
                        )
                    ),
                }
            ]
        }
    )

    structured_response = result["structured_response"]

    if not isinstance(structured_response, GeneratedPatch):
        raise TypeError("Agent did not return PatchGenerationOutputSchema.")

    return structured_response
