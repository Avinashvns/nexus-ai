from core.logger import app_logger
from models import AgentRequest, AgentResponse

import agents
from agents.registry import agent_registry


class AgentExecutor:
    def execute(
        self,
        agent_name: str,
        request: AgentRequest,
    ) -> AgentResponse:
        try:
            app_logger.info(
                f"Executing agent: {agent_name}"
            )

            agent = agent_registry.get(agent_name)

            response = agent.run(request)

            if response.success:
                app_logger.success(
                    f"Agent executed successfully: {agent_name}"
                )
            else:
                app_logger.warning(
                    f"Agent execution failed: {agent_name}"
                )

            return response

        except Exception as error:
            app_logger.error(
                f"Agent Executor Error: {agent_name} - {error}"
            )

            return AgentResponse(
                success=False,
                output=None,
                metadata={
                    "agent": agent_name,
                    "error": str(error),
                },
            )


agent_executor = AgentExecutor()