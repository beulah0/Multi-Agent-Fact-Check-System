from langchain_core.prompts import ChatPromptTemplate
from retrieval.web_search import tavily_search
from retrieval.vector_store import local_search
from retrieval.source_ranker import score_evidence
from utils import get_llm

def retriever_agent(state: dict) -> dict:
    claim = state["claim"]
    web_results = tavily_search(claim, max_results=5)
    local_results = local_search(claim, k=3)
    all_evidence= web_results + local_results
    ranked_evidence = sorted(
        all_evidence,
        key=score_evidence,
        reverse=True
    )
    ranked_evidence=ranked_evidence[:6]
    print(f"[Retriever] found {len(all_evidence)} evidence chunks")
    return {"evidence" : ranked_evidence}


