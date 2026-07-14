from observability.tracing import (
    generate_workflow_id,
)


def main():
    id1 = generate_workflow_id()
    id2 = generate_workflow_id()

    assert id1 != id2

    assert len(id1) > 10
    assert len(id2) > 10

    print(id1)
    print(id2)

    print("\nWorkflow Tracing Test Passed")


if __name__ == "__main__":
    main()