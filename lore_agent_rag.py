import os
import time
from langchain_community.document_loaders import DirectoryLoader, UnstructuredMarkdownLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# --- CONFIGURATION ---
CONTEXT_DIR = "./lore_sync/Notes/"          # Path to your 52 files
DB_DIR = "./chroma_db"       # Local folder to save the vector index
MODEL_NAME = "phi3"        # Your local Ollama model

print("1. Loading context files...")
# Update the glob pattern (e.g., "**/*.py" or "**/*.txt") to match your files
loader = DirectoryLoader(CONTEXT_DIR, glob="**/*.md", loader_cls=UnstructuredMarkdownLoader)
docs = loader.load()
print(f"   Loaded {len(docs)} files.")

print("2. Splitting text into chunks...")
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, 
    chunk_overlap=200
)
chunks = text_splitter.split_documents(docs)
print(f"   Created {len(chunks)} text chunks.")

print("3. Generating embeddings & building VectorDB...")
embeddings = OllamaEmbeddings(model=MODEL_NAME)
vector_store = Chroma.from_documents(
    documents=chunks, 
    embedding=embeddings, 
    persist_directory=DB_DIR
)
retriever = vector_store.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 4}  # Retrieve top 4 most relevant chunks
)

print("4. Initializing safe Ollama instance...")
# A 4096 context window is now plenty because we only send targeted snippets
llm = OllamaLLM(model=MODEL_NAME, num_ctx=4096, num_predict=500)

# --- MODERN LCEL IMPLEMENTATION ---

# Helper function to join the retrieved text blocks into a single string
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

print("5. Assembling LCEL Pipeline...")
system_prompt = (
    "You are an expert editor and reader answering questions about the provided context files.\n"
    "If you do not know the answer based on the context, say that you do not know.\n\n"
    "Context:\n{context}"
)
prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{question}"),
])

# Build the pipeline with pipes (|) instead of using legacy langchain.chains
rag_chain = (
    {
        "context": retriever | format_docs,  # Fetch chunks and merge text
        "question": RunnablePassthrough()    # Pass user query straight through
    }

    | prompt                                 # Format into system/human wrapper
    | llm                                    # Pass string to Ollama
    | StrOutputParser()                      # Ensure clean string return values
)

# --- EXECUTION ---
print("\n--- Modern LCEL RAG Ready ---")
query = "Point out any inconsistencies or contradictions in the provided context."

start_time = time.time()
print(f"User Query: '{query}'")
print("Streaming response...\n")

# Stream chunks to the console immediately with zero startup delay
for chunk in rag_chain.stream(query):
    print(chunk, end="", flush=True)

print(f"\n\nTotal Execution Time: {time.time() - start_time:.2f} seconds")
