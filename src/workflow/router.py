def route_query(state):
    query = state["user_query"].lower()

    if any(word in query for word in ["portfolio", "allocation", "diversification", "holdings"]):
        return "portfolio"

    if any(word in query for word in ["stock", "market", "price", "ticker", "quote"]):
        return "market"

    if any(word in query for word in ["goal", "retirement", "save", "saving", "college"]):
        return "goal"

    if any(word in query for word in ["tax", "ira", "401k", "roth"]):
        return "tax"

    if any(word in query for word in ["news", "headline", "latest"]):
        return "news"

    return "finance_qa"