import os
import time
import ollama
from langchain_community.document_loaders import DirectoryLoader, UnstructuredMarkdownLoader
from langchain_ollama import OllamaLLM

MAX_TOKENS = 1500
MAX_SECONDS = 600

# 1. Target markdown files and use the markdown loader
# Change glob to "**/*.md" to capture all .md files in the folder
loader = DirectoryLoader("./lore_sync", glob="**/*.md", loader_cls=UnstructuredMarkdownLoader)
docs = loader.load()

# 2. Combine the document contents into a single string
context_text = ""
total_tokens = 0
for doc in docs:
    source_name = os.path.basename(doc.metadata.get("source", "Unknown"))
    print(f"Processing file: {source_name}")
    context_text += f"\n--- Source File: {source_name} ---\n{doc.page_content}\n"
    file_tokens = len(doc.page_content.split())
    total_tokens += file_tokens
    print(f"Tokens in {source_name}: {file_tokens}")
    print(f"Context size is now {len(context_text)}")

print(f"Total tokens: {total_tokens}")

print("Creating prompt...")
# 3. Create the prompt structure
question = "Summarize the world described by the context files."
full_prompt = f"Context files:\n{context_text}\n\nTask: {question}"

# 4. Initialize and run the local model
if context_text.strip():
    start_time = time.time()
    try:
        stream = ollama.chat(
            model="phi3",
            messages=[{'role': 'user', 'content': full_prompt}],
            stream=True,
            options={
                'num_predict': (total_tokens * 2),
                'temperature': 0.7
            }
        )

        print("=== Generation Progress ===")
        token_count = 0
        for chunk in stream:
            # Print the tokens in real-time as progress info
            text_chunk = chunk['message']['content']
            print(text_chunk, end='', flush=True)

            token_count += 1

            elapsed_time = time.time() - start_time

            if elapsed_time > MAX_SECONDS:
                print(f"\n\nMaximum time exceeded ({MAX_SECONDS} seconds).")
                break

        # llm = OllamaLLM(
        #     model="phi3",
        #     num_predict=(total_tokens*2),
        #     temperature=0.7
        #     )
        # response = llm.invoke(full_prompt)
        # print(response)
    except Exception as e:
        print(f"Error occurred while invoking the model: {e}")
else:
    print("Error: No markdown files found in the 'lore_sync' folder.")
