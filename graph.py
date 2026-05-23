from langgraph.graph import StateGraph, END
from typing import TypedDict
from agents.retriever import retriever_agent
from agents.advocate import advocate_agent
from agents.refuter import refuter_agent
from agents.judge import judge_agent

class DebateSate(TypedDict):
    claim:str
    evidence:list
    advocate_argument:str
    refuter_argument:str
    verdict:str
    confidence:str
    reasoning:str
    sources:str

workflow = StateGraph(DebateSate)
workflow.add_node("retrieve", retriever_agent)
workflow.add_node("advocate",advocate_agent)
workflow.add_node("refuter",refuter_agent)
workflow.add_node("judge", judge_agent)

workflow.set_entry_point("retrieve")

workflow.add_edge("retrieve", "advocate")
workflow.add_edge("retrieve","refuter")

workflow.add_edge("advocate","judge")
workflow.add_edge("refuter","judge")

workflow.add_edge("judge",END)

app=workflow.compile()

def run_debate(claim:str)->dict:
    initial_state={
        "claim":claim,
        "evidence":[],
        "advocate_argument":"",
        "refuter_argument":"",
        "verdict":"",
        "confidence":0.0,
        "reasoning":"",
        "sources":[]
    }
    result=app.invoke(initial_state)
    return result

def confidence_router(state: DebateSate)->str:
    if state["confidence"]<0.5:
        return "retrieve"
    return END

workflow.add_conditional_edges(
    "judge",
    confidence_router,
    {"retrieve":"retrieve", END:END}
)