from agents.base import BaseAgent
from core.logger import app_logger
from llm.prompts import prompt_manager
from llm.router import llm_router
from models import AgentRequest, AgentResponse


class ReasoningAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="ReasoningAgent")

    def run(
        self,
        request: AgentRequest,
    ) -> AgentResponse:
        try:
            app_logger.info(
                f"{self.name} analyzing task"
            )

            reasoning_prompt = prompt_manager.load(
                "reasoning.txt"
            )

            context = request.context.get(
                "retrieved_context",
                [],
            )

            conversation_memory = request.context.get(
                "conversation_memory",
                "",
            )

            prompt = f"""
                {reasoning_prompt}

                User Task:
                {request.task}

                Conversation Memory:
                {conversation_memory or "No previous conversation."}

                Retrieved Context:
                {context or "No retrieved document context."}
                """

            output = llm_router.generate(prompt)

            app_logger.success(
                f"{self.name} completed reasoning"
            )

            return AgentResponse(
                success=True,
                output=output,
                metadata={
                    "agent": self.name,
                    "context_count": len(context),
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


reasoning_agent = ReasoningAgent()