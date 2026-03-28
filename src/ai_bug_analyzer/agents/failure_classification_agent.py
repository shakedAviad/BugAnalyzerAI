from __future__ import annotations

from langchain.agents import create_agent

from ai_bug_analyzer.domain.schemas import FailureClassificationInputSchema, FailureClassificationOutputSchema
from ai_bug_analyzer.infrastructure.llm.factory import create_chat_model

FAILURE_CLASSIFICATION_SYSTEM_PROMPT: str = """
You are a senior Python bug triage agent.

Your task is to classify a project execution failure based on the command result.

Return only a structured response that matches the required schema.

Rules:
1. Classify the failure as accurately as possible.
2. Prefer concrete root causes over vague descriptions.
3. Include only relevant files when they can be inferred from the error output.
4. Include only relevant symbols when they can be inferred from the error output.
5. Use a confidence score between 0 and 1.
6. If the failure type is unclear, use UNKNOWN.
""".strip()


def build_failure_classification_agent():
    return create_agent(
        model=create_chat_model(),
        tools=[],
        system_prompt=FAILURE_CLASSIFICATION_SYSTEM_PROMPT,
        response_format=FailureClassificationOutputSchema,
    )


def classify_failure(input_data: FailureClassificationInputSchema) -> FailureClassificationOutputSchema:
    agent = build_failure_classification_agent()

    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": (
                        f"Project path: {input_data.project_path}\n"
                        f"Command: {input_data.command}\n"
                        f"Exit code: {input_data.exit_code}\n"
                        f"Stdout:\n{input_data.stdout}\n\n"
                        f"Stderr:\n{input_data.stderr}"
                    ),
                }
            ]
        }
    )

    structured_response = result["structured_response"]

    if not isinstance(structured_response, FailureClassificationOutputSchema):
        raise TypeError("Agent did not return FailureClassificationOutputSchema.")

    return structured_response
