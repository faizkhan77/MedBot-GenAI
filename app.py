from flask import Flask, render_template, jsonify, request
from src.helper import download_hugging_face_embeddings
from langchain_pinecone import PineconeVectorStore
from langchain_google_genai import GoogleGenerativeAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from src.prompt import *
import os

#### *NEW FOR RETAINING PAST MEMORY ####
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain


app = Flask(__name__)

load_dotenv()

PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
os.environ["GEMINI_API_KEY"] = GEMINI_API_KEY

embeddings = download_hugging_face_embeddings()

index_name = "medbot"

# Embed each chunk and upsert the embeddings into your Pinecone index.
docsearch = PineconeVectorStore.from_existing_index(
    index_name=index_name, embedding=embeddings
)

retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={"k": 3})

# ✅ Create Memory for Conversational Context
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

model = GoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=GEMINI_API_KEY)
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)

# question_answer_chain = create_stuff_documents_chain(model, prompt)
# rag_chain = create_retrieval_chain(retriever, question_answer_chain)

rag_chain = ConversationalRetrievalChain.from_llm(
    llm=model, retriever=retriever, memory=memory
)


@app.route("/")
def index():
    return render_template("chat.html")


# @app.route("/get", methods=["GET", "POST"])
# def chat():
#     msg = request.form["msg"]
#     input = msg
#     print(input)
#     response = rag_chain.invoke({"input": msg})
#     print("Response : ", response["answer"])
#     return str(response["answer"])


@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    response = rag_chain.invoke(
        {
            "question": msg,
            "chat_history": memory.load_memory_variables({})[
                "chat_history"
            ],  # Pass chat history
        }
    )

    print("Response : ", response["answer"])
    return str(response["answer"])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
