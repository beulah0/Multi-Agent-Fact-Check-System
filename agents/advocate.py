from langchain_core.prompts import ChatPromptTemplate
from utils import get_llm

ADVOCATE_PROMPT = """ You are a FACT ADVOCATE. Your job is to build the strongest possible argument that the following claim is TRUE.
Claim: 
{claim}
Evidence available: 
{evidence}
Instructions:
- Use ONLY the evidence provided above
- Cite specific sources for every point you make
- Be persuasive but factual
- Structure: Opening statement -> 3 key supporting points with citations -> Conclusion
- If evidence is weak, acknowledge it but argue the best case possible

Build your TRUE argument:"""

def advocate_agent(state: dict) -> dict:
    claim = state["claim"]
    evidence = "\n\n".join(state["evidence"][:5])

    llm = get_llm(temperature=0.3)
    prompt = ChatPromptTemplate.from_template(ADVOCATE_PROMPT)
    chain = prompt | llm
    response = chain.invoke({
        "claim": claim,
        "evidence": evidence
    })

    print(f"[Advocate] Argument build ({len(response.content)} chars)")
    return {"advocate_argument": response.content}