from src.workflow.graph import build_graph

app = build_graph()

test_queries = [
    "What is an ETF?",
    "I have 5000 in AAPL, 3000 in MSFT, 2000 in TSLA",
    "What is the price of NOW stock?",
    "Can I save enough for retirement?",
    "Explain Roth IRA tax benefits",
    "Give me latest market news",
]

for query in test_queries:
    result = app.invoke({
        "user_query": query,
        "agent_type": None,
        "messages": [],
        "context": {},
        "response": "",
    })

    print("\nQuery:", query)
    print("Agent:", result["agent_type"])
    print("Response:", result["response"])