from __future__ import annotations

from domain.models import FailureClassification
from domain.schemas import FailureClassificationInputSchema
from infrastructure.llm.factory import create_chat_model
from langchain.agents import create_agent

FAILURE_CLASSIFICATION_SYSTEM_PROMPT: str = """
You are an expert software engineer specializing in debugging and failure analysis.

Your task is to analyze a failed command execution and classify the failure.

You will receive:
- The executed command
- Exit code
- Standard output (stdout)
- Standard error (stderr)

Your job is to:
1. Identify the type of failure (e.g., test_failure, syntax_error, runtime_error, dependency_error, etc.).
2. Provide a short and clear summary of what happened.
3. Explain the most likely root cause of the failure.
4. Estimate your confidence level (0–1).
5. Identify relevant files and symbols involved in the failure.

Important rules:

1. Focus on identifying the ROOT CAUSE of the failure, not just where the error appeared.
2. Error messages often point to where the failure was detected, not where it originated.
3. If a test fails, distinguish between:
   - The test file where the failure occurred
   - The implementation code that likely caused the failure
4. Prefer implementation/source files over test files unless there is strong evidence the test itself is incorrect.
5. Do NOT mark a test file as the main relevant file if the failure is likely caused by the code under test.
6. Only mark a test file as relevant if:
   - The test itself is incorrect, OR
   - It provides essential context for understanding the failure
7. Relevant symbols should focus on functions, classes, or modules likely responsible for the failure (not just where the assertion failed).
8. Be concise and practical — avoid unnecessary explanations.

Return a structured response that strictly matches the expected schema.
""".strip()


def build_failure_classification_agent():
    return create_agent(
        model=create_chat_model(),
        tools=[],
        system_prompt=FAILURE_CLASSIFICATION_SYSTEM_PROMPT,
        response_format=FailureClassification,
    )


def classify_failure(input_data: FailureClassificationInputSchema) -> FailureClassification:
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

    if not isinstance(structured_response, FailureClassification):
        raise TypeError("Agent did not return FailureClassification.")

    return structured_response
