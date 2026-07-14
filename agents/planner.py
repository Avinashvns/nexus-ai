import json
from typing import Any

from agents.base import BaseAgent
from core.logger import app_logger
from llm.prompts import prompt_manager
from llm.router import llm_router
from models import AgentRequest, AgentResponse


class PlannerAgent(BaseAgent):
    ALLOWED_AGENTS = {
        "SearchAgent",
        "RetrievalAgent",
        "ReasoningAgent",
        "CriticAgent",
        "WriterAgent",
    }

    REQUIRED_FIELDS = {
        "id",
        "task",
        "agent",
        "priority",
        "status",
    }

    def __init__(self):
        super().__init__(name="PlannerAgent")

    def validate_plan(self, plan: Any) -> bool:
        if not isinstance(plan, list) or not plan:
            return False

        for step in plan:
            if not isinstance(step, dict):
                return False

            if not self.REQUIRED_FIELDS.issubset(step):
                return False

            if step["agent"] not in self.ALLOWED_AGENTS:
                return False

            if step["status"] != "pending":
                return False

            if not isinstance(step["id"], int):
                return False

            if not isinstance(step["priority"], int):
                return False

            if not isinstance(step["task"], str) or not step["task"].strip():
                return False

        return True

    def _repair_plan(self, invalid_response: str) -> Any:
        repair_prompt = f"""
            The following execution plan is invalid.

            Fix it and return ONLY valid JSON.

            Allowed agents:
            - SearchAgent
            - RetrievalAgent
            - ReasoningAgent
            - CriticAgent
            - WriterAgent

            Required format:
            [
            {{
                "id": 1,
                "task": "task description",
                "agent": "AgentName",
                "priority": 1,
                "status": "pending"
            }}
            ]

            Invalid plan:
            {invalid_response}
        """

        repaired_response = llm_router.generate(repair_prompt)

        return json.loads(repaired_response)

    def run(self, request: AgentRequest) -> AgentResponse:
        try:
            planner_prompt = prompt_manager.load("planner.txt")

            conversation_memory = request.context.get(
                "conversation_memory",
                "",
            )

            prompt = f"""
                {planner_prompt}

                Conversation Memory:
                {conversation_memory or "No previous conversation."}

                User Task:
                {request.task}
                """

            response = llm_router.generate(prompt)

            try:
                plan = json.loads(response)
            except json.JSONDecodeError:
                app_logger.warning("Invalid JSON received. Attempting repair.")

                plan = self._repair_plan(response)

            if not self.validate_plan(plan):
                app_logger.warning("Invalid plan structure. Attempting repair.")

                plan = self._repair_plan(response)

            if not self.validate_plan(plan):
                raise ValueError("Planner failed to generate a valid execution plan")

            app_logger.success("Execution plan created and validated")

            return AgentResponse(
                success=True,
                output=plan,
                metadata={
                    "agent": self.name,
                    "task_count": len(plan),
                },
            )

        except Exception as error:
            app_logger.error(f"Planner Agent Error: {error}")

            return AgentResponse(
                success=False,
                output=[],
                metadata={
                    "agent": self.name,
                    "error": str(error),
                },
            )


planner_agent = PlannerAgent()
