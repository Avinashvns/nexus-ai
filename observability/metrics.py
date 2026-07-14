from time import perf_counter
from typing import Any


class ExecutionMetrics:
    def __init__(self):
        self._workflow_start: float | None = None
        self._agent_starts: dict[str, float] = {}

        self._agent_metrics: list[
            dict[str, Any]
        ] = []

    def start_workflow(self) -> None:
        self._workflow_start = perf_counter()

    def start_agent(
        self,
        agent_name: str,
    ) -> None:
        self._agent_starts[agent_name] = (
            perf_counter()
        )

    def end_agent(
        self,
        agent_name: str,
        success: bool,
    ) -> None:
        start_time = self._agent_starts.pop(
            agent_name,
            None,
        )

        if start_time is None:
            return

        duration = perf_counter() - start_time

        self._agent_metrics.append(
            {
                "agent": agent_name,
                "success": success,
                "duration_seconds": round(
                    duration,
                    4,
                ),
            }
        )

    def finish_workflow(
        self,
        success: bool,
    ) -> dict[str, Any]:
        duration = 0.0

        if self._workflow_start is not None:
            duration = (
                perf_counter()
                - self._workflow_start
            )

        metrics = {
            "workflow_success": success,
            "workflow_duration_seconds": round(
                duration,
                4,
            ),
            "agent_count": len(
                self._agent_metrics
            ),
            "agents": self._agent_metrics.copy(),
        }

        self.reset()

        return metrics

    def reset(self) -> None:
        self._workflow_start = None
        self._agent_starts.clear()
        self._agent_metrics.clear()