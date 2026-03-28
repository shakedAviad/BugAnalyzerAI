from __future__ import annotations

from langchain.agents import create_agent

from ai_bug_analyzer.domain.schemas import PatchGenerationInputSchema, PatchGenerationOutputSchema
from ai_bug_analyzer.infrastructure.llm.factory import create_chat_model

PATCH_GENERATION_SYSTEM_PROMPT: str = """
You are a senior Python code patch generator.

Your task is to generate a minimal and precise code patch plan based on an approved fix plan.

Return only a structured response that matches the required schema.

Rules:
1. Generate only the code changes required to implement the fix plan.
2. Do not modify unrelated files or unrelated parts of a file.
3. Keep changes as small and focused as possible.
4. Preserve the existing coding style unless the fix requires otherwise.
5. Do not invent files unless they are clearly required for the fix.
6. Each operation must target a specific file.
""".strip()


def build_patch_generation_agent():
    return create_agent(
        model=create_chat_model(),
        tools=[],
        system_prompt=PATCH_GENERATION_SYSTEM_PROMPT,
        response_format=PatchGenerationOutputSchema,
    )


def generate_patch(input_data: PatchGenerationInputSchema) -> PatchGenerationOutputSchema:
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

    if not isinstance(structured_response, PatchGenerationOutputSchema):
        raise TypeError("Agent did not return PatchGenerationOutputSchema.")

    return structured_response
