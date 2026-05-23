from langchain_core.prompts import ChatPromptTemplate
from utils import get_llm

REFUTER_PROMPT = """You are a FACT REFUTER. Your job is to build the strongest possible argument that the following claim is FALSE or misleading.
Claim: 
{claim}
Evidence available: 
{evidence}
Instructions:
- Use ONLY the evidence provided above
- Cite specific sources for every counter-point
- Look for: missing context, outdated data, partial truth, contradicting figures, misattributed quotes
- Structure: Opening challenge -> 3 counter-points with citations -> Conclusion
- If you find no contradicting evidence, argue the claim is UNVERIFIABLE

Build your FALSE argument:"""

def refuter_agent(state:dict) -> dict:
    claim = state["claim"]
    evidence = "\n\n".join(state["evidence"][:5])

    llm = get_llm(temperature=0.3)
    prompt = ChatPromptTemplate.from_template(REFUTER_PROMPT)
    chain = prompt | llm

    response = chain.invoke({
        "claim":claim,
        "evidence": evidence
    })

    print(f"[Refuter] Argument built ({len(response.content)} chars)")
    return {"refuter_argument": response.content}