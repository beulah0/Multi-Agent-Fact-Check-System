import os
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


def build_knowledge_base():

    BASE_DIR = "./indian_news"

    documents = []

    # Traverse source folders
    for source in os.listdir(BASE_DIR):

        source_path = os.path.join(BASE_DIR, source)

        if os.path.isdir(source_path):

            for file in os.listdir(source_path):

                if file.endswith(".txt"):

                    file_path = os.path.join(source_path, file)

                    with open(file_path, "r", encoding="utf-8") as f:
                        text = f.read()

                    documents.append(
                        Document(
                            page_content=text,
                            metadata={
                                "source": source,
                                "file": file
                            }
                        )
                    )

    print(f"Loaded {len(documents)} documents")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    chunks = splitter.split_documents(documents)

    print(f"Created {len(chunks)} chunks")

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = FAISS.from_documents(chunks, embeddings)

    vectorstore.save_local("indian_news_index")

    print("FAISS index created successfully")


if __name__ == "__main__":
    build_knowledge_base()