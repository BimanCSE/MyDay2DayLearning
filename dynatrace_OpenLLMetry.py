import os
import openai 
from langchain_openai import ChatOpenAI
from langchain.messages import HumanMessage, AIMessage
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from traceloop.sdk import Traceloop
from traceloop.sdk.decorators import workflow,task
load_dotenv(dotenv_path = ".env")
api_key = os.getenv("OPENAI_API_TOKEN")
base_url = os.getenv("OPENAI_API_BASE")
llm_model = ChatOpenAI(api_key = api_key, base_url = base_url,model = "gpt-4o")
dynatrace_api_token = os.getenv("DYNATRACE_API_TOKEN")
headers = { "Authorization": f"Api-Token {dynatrace_api_token}" }
Traceloop.init(
    app_name="demo-dynatrace-observability",
    api_endpoint="https://xpj24234.live.dynatrace.com/api/v2/otlp",
    headers=headers,
    disable_batch=True
)
@task(name="add_prompt_context")
def add_prompt_context():
    prompt = ChatPromptTemplate.from_template("explain the business of company {company} in a max of {length} words")
    chain = prompt | llm_model
    return chain

@task(name="prep_prompt_chain")
def prep_prompt_chain():
    return add_prompt_context()

@workflow(name="ask_question")
def prompt_question():
    chain = prep_prompt_chain()
    return chain.invoke({"company": "dynatrace", "length" : 50})

if  __name__ == "__main__":
    print(prompt_question())

