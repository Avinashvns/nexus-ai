from agents.critic import critic_agent
from agents.reasoning import reasoning_agent
from agents.registry import agent_registry
from agents.retrieval import retrieval_agent
from agents.writer import writer_agent
from agents.search import search_agent


agent_registry.register(retrieval_agent)
agent_registry.register(reasoning_agent)
agent_registry.register(critic_agent)
agent_registry.register(writer_agent)
agent_registry.register(search_agent)