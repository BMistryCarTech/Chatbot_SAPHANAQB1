from langchain.agents import initialize_agent, AgentExecutor
from langchain.agents.agent_types import AgentType
from llm import get_llm
from tools import tools

def get_agent():
    llm = get_llm()
    router_agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent_type=AgentType.OPENAI_FUNCTIONS,
        verbose=True,
    )

    return AgentExecutor.from_agent_and_tools(
        agent=router_agent.agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True
    )
