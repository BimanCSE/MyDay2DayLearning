from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langserve import add_routes
import os
load_dotenv("/Users/biman_giri/Documents/OfficeWork/MyDay2DayLearning/.env")
openai_token = os.getenv("OPENAI_API_TOKEN")
openai_base_url = os.getenv("OPENAI_API_BASE")
lanchain_endpoint = os.getenv("LANGSMITH_ENDPOINT")
lanchain_api_key = os.getenv("LANGSMITH_API_KEY")
lanchain_project = os.getenv("LANGSMITH_PROJECT")
lanchain_tracing_v2 = os.getenv("LANGSMITH_TRACING")
### defining the prompt template for the language translation
system_template = "Translate the following from English to {language}"
prompt = ChatPromptTemplate.from_messages([
    ("system", system_template),
    ("user", "{text}")
])
### defining the output parser for the language translation
parser = StrOutputParser()
### defining the language model for the language translation
llm_model = ChatOpenAI(
    model="gpt-4o",
    api_key=openai_token,
    base_url=openai_base_url,
)
### defining the chain for the language translation
chain = prompt | llm_model | parser
### defining the fastapi app
app = FastAPI(title = "langchain server", version = "1.0.0", description = "A simple langchain server for language translation")
# adding the routes to the fastapi app
add_routes(app, chain, path="/translate")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


