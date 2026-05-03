from src.core.llm import get_llm

def finance_qa_agent(state):
    llm = get_llm()

    prompt = f"""
    You are a financial education assistant.

    Answer the following question in simple, beginner-friendly language.
    Do NOT give financial advice. Only provide educational information.

    Question: {state["user_query"]}
    """

    response = llm.invoke(prompt)

    state["agent_type"] = "finance_qa"
    state["response"] = response.content
    return state