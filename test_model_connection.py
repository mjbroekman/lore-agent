from langchain_ollama import OllamaLLM

# Initialize the local model
# Ensure the model name matches what you downloaded (e.g., "llama3")
llm = OllamaLLM(model="phi3")

# Test the connection
response = llm.invoke("Briefly describe a fantasy world where magic is powered by memories.")
print(response)
