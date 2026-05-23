from tavily import TavilyClient
import os
from dotenv import load_dotenv


# print(os.getenv("TAVILY_API_KEY"))
load_dotenv()
client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def tavily_search(query:str, max_results:int=5)-> list[str]:
    results = client.search(
        query=query,
        search_depth="advanced",
        include_domains=["thehindu.com", "ndtv.com", "timesofindia.com",
            "indianexpress.com", "pib.gov.in", "factcheck.afp.com"],
        max_results=max_results
    )
    evidence = []
    for r in results["results"]:
        evidence.append(f"Source: {r['url']}\n{r['content']}")
    return evidence