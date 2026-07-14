from agents.base import BaseAgent
from core.logger import app_logger
from llm.prompts import prompt_manager
from llm.router import llm_router
from models import AgentRequest, AgentResponse


class CriticAgent(BaseAgent):
    def __init__(self):
        super().__init__("CriticAgent")

    def run(self, request: AgentRequest) -> AgentResponse:
        try:
            app_logger.info(f"{self.name} reviewing response")

            critic_prompt = prompt_manager.load("critic.txt")

            reasoning_output = request.context.get(
                "reasoning_output",
                ""
            )

            prompt = f"""
{critic_prompt}

User Task:
{request.task}

Analysis:
{reasoning_output}
"""

            output = llm_router.generate(prompt)

            app_logger.success(
                f"{self.name} review completed"
            )

            return AgentResponse(
                success=True,
                output=output,
                metadata={
                    "agent": self.name,
                },
            )

        except Exception as error:
            app_logger.error(
                f"{self.name}: {error}"
            )

            return AgentResponse(
                success=False,
                output="",
                metadata={
                    "error": str(error),
                },
            )


critic_agent = CriticAgent()