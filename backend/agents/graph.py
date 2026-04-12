from functools import partial

from langgraph.graph import END, StateGraph
from sqlalchemy.orm import Session

from agents.critic_agent import critic_node
from agents.gap_agent import gap_node
from agents.market_agent import market_node
from agents.profile_agent import profile_node
from agents.roadmap_agent import roadmap_node
from agents.state import GraphState
from repositories.vector_repo import VectorRepository


def build_graph(llm, db: Session):
    """Compiles the LangGraph Supervisor-pattern graph.
    Nodes are isolated per agent; each node only updates its own state keys.
    """
    vector_repo = VectorRepository(db=db)

    graph = StateGraph(GraphState)

    graph.add_node("profile", partial(profile_node, llm=llm))
    graph.add_node("market", partial(market_node, llm=llm, vector_repo=vector_repo))
    graph.add_node("gap", partial(gap_node, llm=llm))
    graph.add_node("roadmap", partial(roadmap_node, llm=llm))
    graph.add_node("critic", partial(critic_node, llm=llm))

    graph.set_entry_point("profile")
    graph.add_edge("profile", "market")
    graph.add_edge("market", "gap")
    graph.add_edge("gap", "roadmap")
    graph.add_edge("roadmap", "critic")
    graph.add_edge("critic", END)

    return graph.compile()
