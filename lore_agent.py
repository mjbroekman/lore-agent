import os
from langchain_community.document_loaders import DirectoryLoader, UnstructuredMarkdownLoader
from langchain_ollama import OllamaLLM

# 1. Target markdown files and use the markdown loader
# Change glob to "**/*.md" to capture all .md files in the folder
loader = DirectoryLoader("./lore_sync", glob="**/*.md", loader_cls=UnstructuredMarkdownLoader)
docs = loader.load()

# 2. Combine the document contents into a single string
context_text = ""
for doc in docs:
    source_name = os.path.basename(doc.metadata.get("source", "Unknown"))
    print(f"Processing file: {source_name}")
    context_text += f"\n--- Source File: {source_name} ---\n{doc.page_content}\n"
    print(f"Context size is now {len(context_text)}")

print("Creating prompt...")
# 3. Create the prompt structure
question = "Summarize the world described by the context files."
full_prompt = f"Context files:\n{context_text}\n\nTask: {question}"

# 4. Initialize and run the local model
if context_text.strip():
    llm = OllamaLLM(model="phi3")
    response = llm.invoke(full_prompt)
    print(response)
else:
    print("Error: No markdown files found in the 'lore_sync' folder.")
