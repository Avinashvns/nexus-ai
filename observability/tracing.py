from uuid import uuid4


def generate_workflow_id() -> str:
    return str(uuid4())