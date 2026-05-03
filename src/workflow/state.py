from typing import TypedDict, List, Dict, Any, Optional


class AgentState(TypedDict):
    user_query: str
    agent_type: Optional[str]
    messages: List[Dict[str, Any]]
    context: Dict[str, Any]
    response: str