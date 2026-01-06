import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv(
    dotenv_path="/Users/biman_giri/Documents/OfficeWork/Myday2DayLearning/llm-observability-langfuse/.langfuse-env"
)
openai_api_key = os.getenv(key="OPENAI_API_TOKEN")
openai_base_url = os.getenv(key="OPENAI_BASE_URL")
llm_client = ChatOpenAI(
    api_key=openai_api_key, base_url=openai_base_url, model="gpt-4o"
)
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_template("Tell me a joke about {topic}")
from langfuse.langchain import CallbackHandler

langfuse_handler = CallbackHandler()
chain = prompt | llm_client

response = chain.invoke(
    {"topic": "cats"}, config={"callbacks": [langfuse_handler]}
)
