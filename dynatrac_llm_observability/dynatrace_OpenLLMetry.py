from dotenv import load_dotenv

load_dotenv(dotenv_path="/Users/biman_giri/Documents/officework/MyDay2DayLearning/.env")
import os

from langchain_openai import ChatOpenAI
from traceloop.sdk.decorators import workflow
from traceloop.sdk import Traceloop

Traceloop.init(app_name="Dynatrace-demo-observability", disable_batch=True)
openai_client = ChatOpenAI(
    api_key=os.getenv(key="OPENAI_API_TOKEN"),
    base_url=os.getenv(key="OPENAI_API_BASE"),
    model="gpt-4o",
)


@workflow("generate llm response")
def generate_llm_response(question: str) -> str:
    return openai_client.invoke(input=question)
