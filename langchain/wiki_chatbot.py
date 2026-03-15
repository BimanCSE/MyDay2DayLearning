## all import statement
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.messages import HumanMessage
import shutil
from langchain_core.messages import trim_messages
from langchain_core.runnables.passthrough import RunnablePassthrough
from operator import itemgetter
from langchain_core.runnables import Runnable
# loading the environment variables
load_dotenv("/Users/biman_giri/Documents/OfficeWork/MyDay2DayLearning/.env")
openai_token = os.getenv("OPENAI_API_TOKEN")
openai_base_url = os.getenv("OPENAI_API_BASE")
lanchain_endpoint = os.getenv("LANGSMITH_ENDPOINT")
lanchain_api_key = os.getenv("LANGSMITH_API_KEY")
lanchain_project = os.getenv("LANGSMITH_PROJECT")
lanchain_tracing_v2 = os.getenv("LANGSMITH_TRACING")

# defining the llm mode
llm_model = ChatOpenAI(model="gpt-4o", api_key=openai_token, base_url=openai_base_url)
# defining the embedding model
embedding_model = OpenAIEmbeddings(
    model="text-embedding-3-large", api_key=openai_token, base_url=openai_base_url
)
in_memeory_chat_history = dict()
trimmer = trim_messages(
    max_tokens=1000,
    strategy="last",
    token_counter=llm_model,
    include_system=True,
    allow_partial=False,
    start_on="human",
)
print("Defining the text splitter...")
text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
    "cl100k_base", chunk_size=1000, chunk_overlap=200
)
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant, answer the question based on the given context.",
        ),
        ("user", "Here is the context: {context} Here is the question: {question}"),
    ]
)

chain = (
    RunnablePassthrough.assign(question=itemgetter("question") | trimmer)
    | prompt
    | llm_model
    | StrOutputParser()
)


def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in in_memeory_chat_history:
        in_memeory_chat_history[session_id] = InMemoryChatMessageHistory()
    return in_memeory_chat_history[session_id]


while True:
    if len(in_memeory_chat_history) == 0:
        print("No users found")
    else:
        list_of_users = "\n".join(
            [
                f"{index}: {user}"
                for index, user in enumerate(list(in_memeory_chat_history.keys()))
            ]
        )
        print(f"List of users: {list_of_users}")
    print("--------------------------------")
    print("1 . Select the user\n")
    print("2 . Create a new user\n")
    print("3. Delete the user\n")
    print("5 . Exit\n")
    print("--------------------------------")
    user_choice = input("Enter your choice: ")
    if user_choice == "2":
        user_name = input("Enter the user name: ")
        session_id = f"{user_name}_chat"
        url_input = input("Enter the ULR on which you wanted to build the chatbot: ")

        loader = WebBaseLoader(url_input)
        document = loader.load()
        chunks = text_splitter.split_documents(document)
        faiss_db = FAISS.from_documents(chunks, embedding_model)
        if os.path.exists(f"faiss_db_{session_id}"):
            shutil.rmtree(f"faiss_db_{session_id}")
        faiss_db.save_local(f"faiss_db_{session_id}")
        in_memeory_chat_history[session_id] = InMemoryChatMessageHistory()
        with_message_history = RunnableWithMessageHistory(
            chain, get_session_history, input_messages_key="question"
        )
        config = {"configurable": {"session_id": session_id}}
        while True:
            user_input = input("Enter the question: ")
            if user_input == "exit":
                break
            context = faiss_db.similarity_search(user_input, k=3)
            context = "\n".join([doc.page_content for doc in context])
            response = with_message_history.invoke(
                {"question": [HumanMessage(content=user_input)], "context": context},
                config=config,
            )
            print(response)
    elif user_choice == "1":
        selected_user = input(
            f"Select the Uers between 0 and {len(in_memeory_chat_history)-1}: ",
        )
        id_to_user = {
            index: user for index, user in enumerate(in_memeory_chat_history.keys())
        }
        selected_user = id_to_user[int(selected_user)]
        session_id = selected_user
        faiss_db = FAISS.load_local(
            f"faiss_db_{session_id}",
            embedding_model,
            allow_dangerous_deserialization=True,
        )
        with_message_history = RunnableWithMessageHistory(
            chain, get_session_history, input_messages_key="question"
        )
        config = {"configurable": {"session_id": session_id}}
        while True:
            user_input = input("Enter the question: ")
            if user_input == "exit":
                break
            context = faiss_db.similarity_search(user_input, k=3)
            context = "\n".join([doc.page_content for doc in context])
            response = with_message_history.invoke(
                {"question": [HumanMessage(content=user_input)], "context": context},
                config=config,
            )
            print(response)
    elif user_choice == "3":
        user_name = input("Enter the user name: ")
        session_id = f"{user_name}_chat"
        shutil.rmtree(f"faiss_db_{session_id}")
        in_memeory_chat_history.remove(session_id)
        print(f"User {user_name} deleted successfully")
    elif user_choice == "5":
        exit()
