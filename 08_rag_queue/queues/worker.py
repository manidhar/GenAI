from openai import OpenAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise EnvironmentError("GEMINI_API_KEY not found in environment. Set it in your .env file.")

base_url = os.getenv("base_url")
if not base_url:
    raise EnvironmentError("base_url not found in environment. Set it in your .env file.")

client = OpenAI(
    api_key=api_key,
    base_url=base_url
)

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

vector_store = QdrantVectorStore.from_existing_collection(
    embedding=embeddings,
    url="http://localhost:6333",
    collection_name="learning_rag"
)

def process_query(query: str):
    
    print("Searcing chunks: ",query)
    search_results=vector_store.similarity_search(query, k=3)
    
    context="\n\n\n".join([f"Page Content: {result.page_content}\nPage Number: {result.metadata['page_label']}\n File Location : {result.metadata['source']}"
    for result in search_results])

    SYSTEM_PROMPT="""
    You are helpful AI assistant who answers user query based on available context retrived from a pdf file along with page_contents and page number.
    
    You should only answer the user based on the following context and navigate the user to open the right page number to know more.
    
    Context: {context}
    """

    response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": query
        }
    ])
    print(response.choices[0].message.content)
    return response.choices[0].message.content



