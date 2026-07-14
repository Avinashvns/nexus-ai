from typing import Any
from memory.manager import memory_manager

from agents.executor import agent_executor
from agents.planner import planner_agent
from core.logger import app_logger
from models import AgentRequest, AgentResponse, AgentState
from observability.metrics import ExecutionMetrics
from observability.tracing import generate_workflow_id


class WorkflowEngine:
    def __init__(self, max_retries: int = 2):
        self.max_retries = max_retries

    def run(self, task: str, session_id: str = "default") -> AgentResponse:
        workflow_id = generate_workflow_id()
        app_logger.info(f"Starting workflow: {task}")

        metrics = ExecutionMetrics()
        metrics.start_workflow()

        memory_context = memory_manager.build_context(
            session_id=session_id,
        )

        memory_manager.add_user_message(
            session_id=session_id,
            content=task,
        )

        state = AgentState(
            task=task,
            context={
                "conversation_memory": memory_context,
            },
        )

        execution_history: list[dict[str, Any]] = []

        plan_response = planner_agent.run(
            AgentRequest(
                task=task,
                context={
                    "conversation_memory": memory_context,
                },
            )
        )

        if not plan_response.success:
            return AgentResponse(
                success=False,
                output=None,
                metadata={
                    "stage": "planning",
                    "error": plan_response.metadata.get("error"),
                },
            )

        plan = self._normalize_plan(plan_response.output)

        for step in plan:
            agent_name = step["agent"]

            state.current_agent = agent_name

            app_logger.info(f"[{workflow_id}] Executing: {agent_name}")

            metrics.start_agent(agent_name)

            request = AgentRequest(
                task=step["task"],
                context=state.context,
            )

            response, attempts = self._execute_with_retry(
                agent_name=agent_name,
                request=request,
            )

            metrics.end_agent(
                agent_name=agent_name,
                success=response.success,
            )

            history_item = {
                "step_id": step["id"],
                "agent": agent_name,
                "success": response.success,
                "attempts": attempts,
            }

            execution_history.append(history_item)

            if not response.success:
                step["status"] = "failed"

                app_logger.error(f"[{workflow_id}] Workflow failed at: {agent_name}")

                workflow_metrics = metrics.finish_workflow(success=False)

                return AgentResponse(
                    success=False,
                    output=None,
                    metadata={
                        "workflow_id": workflow_id,
                        "failed_agent": agent_name,
                        "failed_step": step["id"],
                        "plan": plan,
                        "execution_history": execution_history,
                        "metrics": workflow_metrics,
                        "error": response.metadata.get("error"),
                    },
                )

            self._update_state(
                state=state,
                agent_name=agent_name,
                output=response.output,
            )

            step["status"] = "completed"

        state.completed = True

        workflow_metrics = metrics.finish_workflow(success=True)

        final_output = state.context.get(
            "final_output",
            state.context,
        )

        memory_manager.add_assistant_message(
            session_id=session_id,
            content=final_output,
        )

        app_logger.success(f"[{workflow_id}] Workflow completed successfully")

        return AgentResponse(
            success=True,
            output=final_output,
            metadata={
                "workflow_id": workflow_id,
                "workflow_completed": state.completed,
                "plan": plan,
                "execution_history": execution_history,
                "metrics": workflow_metrics,
            },
        )

    def _normalize_plan(
        self,
        plan: list[dict],
    ) -> list[dict]:
        agent_order = {
            "SearchAgent": 1,
            "RetrievalAgent": 2,
            "ReasoningAgent": 3,
            "CriticAgent": 4,
            "WriterAgent": 5,
        }

        return sorted(
            plan,
            key=lambda step: agent_order.get(
                step["agent"],
                999,
            ),
        )

    def _execute_with_retry(
        self,
        agent_name: str,
        request: AgentRequest,
    ) -> tuple[AgentResponse, int]:
        attempts = 0

        while attempts <= self.max_retries:
            attempts += 1

            app_logger.info(f"Executing {agent_name} - Attempt {attempts}")

            response = agent_executor.execute(
                agent_name=agent_name,
                request=request,
            )

            if response.success:
                return response, attempts

            if attempts <= self.max_retries:
                app_logger.warning(f"Retrying {agent_name}")

        return response, attempts

    def _update_state(
        self,
        state: AgentState,
        agent_name: str,
        output: Any,
    ) -> None:
        context_keys = {
            "SearchAgent": "search_results",
            "RetrievalAgent": "retrieved_context",
            "ReasoningAgent": "reasoning_output",
            "CriticAgent": "critic_output",
            "WriterAgent": "final_output",
        }

        key = context_keys.get(agent_name)

        if key:
            state.context[key] = output


workflow_engine = WorkflowEngine()
