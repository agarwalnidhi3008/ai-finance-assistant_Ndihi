from src.core.llm import get_llm
import json


def extract_portfolio(query: str):
    llm = get_llm()

    prompt = f"""
    Extract the portfolio from the user query.

    Rules:
    - Return JSON only
    - Format: {{ "TICKER": amount }}
    - Example: {{ "AAPL": 5000, "MSFT": 3000 }}
    - If no portfolio is found, return EMPTY JSON {{ }}

    Query:
    {query}
    """

    response = llm.invoke(prompt)

    try:
        portfolio = json.loads(response.content)
        return portfolio
    except:
        return {}


def calculate_portfolio_metrics(portfolio: dict):
    if not portfolio:
        return None

    total_value = sum(portfolio.values())

    allocation = {
        asset: round((value / total_value) * 100, 2)
        for asset, value in portfolio.items()
    }

    return {
        "total_value": total_value,
        "allocation_percent": allocation
    }


def portfolio_agent(state):
    llm = get_llm()
    query = state["user_query"]

    portfolio = extract_portfolio(query)

    if not portfolio:
        state["agent_type"] = "portfolio"
        state["response"] = (
            "Please provide your portfolio in this format:\n"
            "Example: I have 5000 in AAPL, 3000 in MSFT"
        )
        return state

    metrics = calculate_portfolio_metrics(portfolio)

    prompt = f"""
    You are a financial education assistant.

    Analyze this portfolio in simple terms:
    - Explain diversification
    - Comment on allocation balance
    - Do NOT give investment advice

    Portfolio:
    {portfolio}

    Metrics:
    {metrics}
    """

    response = llm.invoke(prompt)

    state["agent_type"] = "portfolio"
    state["context"]["portfolio"] = portfolio
    state["context"]["metrics"] = metrics
    state["response"] = response.content
    return state