import yfinance as yf
from src.core.llm import get_llm


def extract_ticker(query: str):
    llm = get_llm()

    prompt = f"""
    Extract the stock ticker symbol from the user query.

    Rules:
    - Return ONLY the ticker symbol, such as AAPL, MSFT, TSLA, NVDA
    - If the query contains a company name, return its common ticker if obvious
      Example: Apple -> AAPL, Microsoft -> MSFT, Tesla -> TSLA, Nvidia -> NVDA
    - If no ticker or obvious company name is found, return NONE
    - Do not explain anything

    User query: {query}
    """

    response = llm.invoke(prompt)
    ticker = response.content.strip().upper()

    if ticker == "NONE" or len(ticker) > 6:
        return None

    return ticker


def get_stock_data(ticker: str) -> dict:
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="5d")

        if hist.empty:
            return {"error": f"No market data found for ticker '{ticker}'."}

        latest = hist.iloc[-1]
        previous = hist.iloc[-2] if len(hist) > 1 else latest

        latest_close = float(latest["Close"])
        previous_close = float(previous["Close"])
        change = latest_close - previous_close
        change_pct = (change / previous_close) * 100 if previous_close else 0

        return {
            "ticker": ticker,
            "latest_close": round(latest_close, 2),
            "previous_close": round(previous_close, 2),
            "change": round(change, 2),
            "change_percent": round(change_pct, 2),
            "volume": int(latest["Volume"]),
        }

    except Exception as e:
        return {"error": f"Unable to fetch market data for '{ticker}'. Error: {str(e)}"}


def market_agent(state):
    llm = get_llm()
    query = state["user_query"]

    ticker = extract_ticker(query)

    if not ticker:
        state["agent_type"] = "market"
        state["response"] = (
            "I can help with market data, but I need a stock ticker or company name. "
            "For example: 'What is the price of AAPL?' or 'How is Microsoft stock doing?'"
        )
        return state

    market_data = get_stock_data(ticker)

    if "error" in market_data:
        state["agent_type"] = "market"
        state["response"] = market_data["error"]
        return state

    prompt = f"""
    You are a market education assistant.

    Explain this market data in beginner-friendly language.
    Do not provide buy, sell, or hold advice.
    Keep the response educational and include a short disclaimer.

    User question:
    {query}

    Market data:
    {market_data}
    """

    response = llm.invoke(prompt)

    state["agent_type"] = "market"
    state["context"]["market_data"] = market_data
    state["response"] = response.content
    return state