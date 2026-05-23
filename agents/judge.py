from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from utils import get_llm

class Verdict(BaseModel):
    verdict: str = Field(description="TRUE, FALSE, or UNVERIFIABLE")
    confidence: float = Field(description="0.0 to 1.0 confidence score")
    reasoning: str = Field(description="2-3 sentence explanation")
    stronger_argument: str = Field(description="ADVOCATOR or REFUTER")
    key_evidence: list[str] = Field(description="top 3 evidence points used")

JUDGE_PROMPT = """You are an impartial FACT_CHECK JUDGE.
You have heard arguments from both sides. Make a final verdict.

Original Claim:
{claim}
ADVOCATE argued TRUE:
{advocate_argument}
REFUTER argued FALSE:
{refuter_argument}
ALL Evidence:
{evidence}

Evaluate both arguments critically. Consider:
- Which argument was better supported by evidence?
- Was any evidence misrepresented by either side?
- Is the claim verifiable given the available evidence?

Respond ONLY with a JSON object matching this schema:
{{
"verdict": "TRUE" | "FALSE" | "UNVERIFIABLE",
"confidence": ,
"reasoning": "<2-3 sentence explanation>",
"stronger_argument": "ADVOCATE" | "REFUTER",
"key_evidence": ["", "", ""]
}}"""

def judge_agent(state:dict)-> dict:
    llm = get_llm(temperature=0.0)
    prompt = ChatPromptTemplate.from_template(
    JUDGE_PROMPT + "\n{format_instructions}"
)
    parser = JsonOutputParser(pydantic_object=Verdict)
    chain = prompt | llm | parser

    result = chain.invoke({
        "claim": state["claim"],
        "advocate_argument": state["advocate_argument"],
        "refuter_argument": state["refuter_argument"],
        "evidence": "\n\n".join(state["evidence"][:5]),
        "format_instructions": parser.get_format_instructions()
    })

    return{
        "verdict": result["verdict"],
        "confidence": result["confidence"],
        "reasoning": result["reasoning"],
        "sources": result["key_evidence"]
    }