from langchain.schema import HumanMessage, SystemMessage
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

#Load environment variables from .env file
load_dotenv()

# Set up OpenAI API key
openai_api_key = os.getenv("OPEN_API_KEY")

# Initialize the ChatOpenAI model
agent = ChatOpenAI(model="gpt-5-nano", temperature=0, api_key= openai_api_key)

messages = [ SystemMessage(content="You are a helpful assistant who is excellent computer programmer. Your name is Codey."),
             HumanMessage(content="What is a bit and tell me who you are?") ]

res= agent.invoke(messages)
print(res)