import ollama

client = ollama.Client()

model = "llama3.2:3b"
prompt = "What is python"

response = client.generate(model=model, prompt=prompt)
print(response.response)

