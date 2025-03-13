"""
This file simply contains all the Pinecone codes where we first get the extracted data, then split into chunks then get the downloaded embedding model and create the index in Pinecone and then convert those into vector embeddings and push / store to the Pinecone database.

So in future if lets say we want to add more PDF, or modify the data or something then we would have to split it again, embed it and push it to the Pinecone index, here we can simply run this file

NOTE: BEFORE LAUNCHING THE APP, ENSURE TO EXECUTE THIS FILE AS THIS IS WHERE WE GET THE EXTRACTED DATA FROM PDF, SPLIT INTO CHUNKS, DOWNLOAD EMBEDDINGS, CREATE PINECONE INDEX, EMBED THOSE CHUNKS AND STORE TO PINCONE.
ALSO EXECUTE ONLY 1 TIME, UNLESS YOU DID SOME CHANGES TO THE DATA OR ADDED MORE PDF, ETC
"""

from src.helper import load_pdf_file, text_split, download_hugging_face_embeddings
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from dotenv import load_dotenv
import os


load_dotenv()

PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY


extracted_data = load_pdf_file(data="Data/")
text_chunks = text_split(extracted_data)
embeddings = download_hugging_face_embeddings()


pc = Pinecone(api_key=PINECONE_API_KEY)

index_name = "medbot"

pc.create_index(
    name=index_name,
    dimension=384,  # Vector size (matches embedding model output)
    metric="cosine",  # Similarity metric
    spec=ServerlessSpec(  # Configures a serverless index:
        cloud="aws",  # Runs on AWS servers.
        region="us-east-1",  # Stores data in AWS's us-east-1 region.
    ),
)


# Embed each chunk and upsert the embeddings into your Pinecone index.
docsearch = PineconeVectorStore.from_documents(
    documents=text_chunks,
    index_name=index_name,
    embedding=embeddings,
)
