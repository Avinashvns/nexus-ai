from agents.executor import agent_executor
from models import AgentRequest
from rag.pipeline import rag_pipeline


def main():
    print("Starting Specialized Agents Integration Test")

    rag_pipeline.ingest_pdf(
        "tests/data/sample.pdf"
    )

    task = "Explain what Nexus AI does."

    retrieval_response = agent_executor.execute(
        agent_name="RetrievalAgent",
        request=AgentRequest(
            task=task,
        ),
    )

    assert retrieval_response.success is True

    reasoning_response = agent_executor.execute(
        agent_name="ReasoningAgent",
        request=AgentRequest(
            task=task,
            context={
                "retrieved_context": retrieval_response.output,
            },
        ),
    )

    assert reasoning_response.success is True

    critic_response = agent_executor.execute(
        agent_name="CriticAgent",
        request=AgentRequest(
            task=task,
            context={
                "reasoning_output": reasoning_response.output,
            },
        ),
    )

    assert critic_response.success is True

    writer_response = agent_executor.execute(
        agent_name="WriterAgent",
        request=AgentRequest(
            task=task,
            context={
                "critic_output": critic_response.output,
            },
        ),
    )

    assert writer_response.success is True

    print("\nFinal Response:")
    print(writer_response.output)

    print("\nSpecialized Agents Integration Test Passed")


if __name__ == "__main__":
    main()