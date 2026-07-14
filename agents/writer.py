from agents.base import BaseAgent
from core.logger import app_logger
from llm.prompts import prompt_manager
from llm.router import llm_router
from models import AgentRequest, AgentResponse


class WriterAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="WriterAgent")

    def run(
        self,
        request: AgentRequest,
    ) -> AgentResponse:
        try:
            app_logger.info(
                f"{self.name} generating final response"
            )

            writer_prompt = prompt_manager.load(
                "writer.txt"
            )

            analysis = request.context.get(
                "critic_output",
                "",
            )

            prompt = f"""
{writer_prompt}

User Task:
{request.task}

Analysis:
{analysis}
"""

            output = llm_router.generate(prompt)

            app_logger.success(
                f"{self.name} completed final response"
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
                f"{self.name} Error: {error}"
            )

            return AgentResponse(
                success=False,
                output="",
                metadata={
                    "agent": self.name,
                    "error": str(error),
                },
            )


writer_agent = WriterAgent()