from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = FAISS.load_local("indian_news_index",embeddings, allow_dangerous_deserialization=True)

def local_search(query:str, k:int=3)->list[str]:
    docs = vectorstore.similarity_search(query, k=k)
    results=[]
    for d in docs:
        src=d.metadata.get("source","local KB")
        results.append(f"Source: {src}\n{d.page_content}")
    return results