from agents.base import BaseAgent
from core.logger import app_logger
from models import AgentRequest, AgentResponse
from rag.pipeline import rag_pipeline


class RetrievalAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="RetrievalAgent")

    def run(
        self,
        request: AgentRequest,
    ) -> AgentResponse:
        try:
            app_logger.info(
                f"{self.name} retrieving context"
            )

            results = rag_pipeline.retrieve(
                query=request.task,
                top_k=3,
            )

            app_logger.success(
                f"{self.name} retrieved {len(results)} chunks"
            )

            return AgentResponse(
                success=True,
                output=results,
                metadata={
                    "agent": self.name,
                    "result_count": len(results),
                },
            )

        except Exception as error:
            app_logger.error(
                f"{self.name} Error: {error}"
            )

            return AgentResponse(
                success=False,
                output=[],
                metadata={
                    "agent": self.name,
                    "error": str(error),
                },
            )


retrieval_agent = RetrievalAgent()