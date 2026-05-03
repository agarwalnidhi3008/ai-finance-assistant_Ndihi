from langgraph.graph import StateGraph, END
from src.workflow.state import AgentState
from src.workflow.router import route_query
from src.agents.finance_qa_agent import finance_qa_agent
from src.agents.market_agent import market_agent
from src.agents.portfolio_agent import portfolio_agent


def finance_qa_node(state: AgentState):
    return finance_qa_agent(state)


def portfolio_node(state: AgentState):
    return portfolio_agent(state)


def market_node(state: AgentState):
    return market_agent(state)


def goal_node(state: AgentState):
    state["agent_type"] = "goal"
    state["response"] = "Goal Planning Agent selected."
    return state


def news_node(state: AgentState):
    state["agent_type"] = "news"
    state["response"] = "News Agent selected."
    return state


def tax_node(state: AgentState):
    state["agent_type"] = "tax"
    state["response"] = "Tax Agent selected."
    return state


def build_graph():
    workflow = StateGraph(AgentState)

    workflow.add_node("finance_qa", finance_qa_node)
    workflow.add_node("portfolio", portfolio_node)
    workflow.add_node("market", market_node)
    workflow.add_node("goal", goal_node)
    workflow.add_node("news", news_node)
    workflow.add_node("tax", tax_node)

    workflow.set_conditional_entry_point(
        route_query,
        {
            "finance_qa": "finance_qa",
            "portfolio": "portfolio",
            "market": "market",
            "goal": "goal",
            "news": "news",
            "tax": "tax",
        },
    )

    workflow.add_edge("finance_qa", END)
    workflow.add_edge("portfolio", END)
    workflow.add_edge("market", END)
    workflow.add_edge("goal", END)
    workflow.add_edge("news", END)
    workflow.add_edge("tax", END)

    return workflow.compile()