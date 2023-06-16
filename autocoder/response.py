import os
import re
import io
import contextlib
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains.router import MultiRetrievalQAChain
from langchain.llms import OpenAI
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import openai
import shutil
import uuid

# Setup OpenAI API key
openai_api_key = os.getenv('OPENAI_API_KEY')
os.environ["OPENAI_API_KEY"] = openai_api_key

BASE_DIR = os.getcwd()
TEXT_DIR = os.path.join(BASE_DIR, 'text')
PDF_DIR = os.path.join(BASE_DIR, 'pdf')
INDEXES_DIR = os.path.join(BASE_DIR, 'indexes')

# Initialize the OpenAI embeddings
embedding = OpenAIEmbeddings()

# Initialize the text splitter
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=20, length_function=len)

def process_text_files(directory_path):
    retrievers_info = []
    for file_name in os.listdir(directory_path):
        file_path = os.path.join(directory_path, file_name)
        if os.path.isfile(file_path) and file_name.endswith('.txt'):
            with open(file_path, 'r', encoding="utf-8", errors="ignore") as f:
                doc = text_splitter.create_documents([f.read()])
            if doc:
                retriever = Chroma.from_documents(documents=doc, embedding=embedding, persist_directory=os.path.join(INDEXES_DIR, file_name[:-4]))
                retriever.persist()
                retriever = retriever.as_retriever()
                retrievers_info.append({
                    "name": file_name[:-4],
                    "description": f"Good for answering questions about {file_name[:-4]}",
                    "retriever": retriever
                })
    return retrievers_info

def process_pdf_files(directory_path):
    retrievers_info = []
    for file_name in os.listdir(directory_path):
        file_path = os.path.join(directory_path, file_name)
        if os.path.isfile(file_path) and file_name.endswith('.pdf'):
            loader = PyPDFLoader(file_path)
            doc = loader.load_and_split()
            if doc:
                retriever = Chroma.from_documents(documents=doc, embedding=embedding, persist_directory=os.path.join(INDEXES_DIR, file_name[:-4]))
                retriever.persist()
                retriever = retriever.as_retriever()
                retrievers_info.append({
                    "name": file_name[:-4],
                    "description": f"Good for answering questions about {file_name[:-4]}",
                    "retriever": retriever
                })
    return retrievers_info

def process_python_files(directory_path):
    retrievers_info = []
    for file_name in os.listdir(directory_path):
        file_path = os.path.join(directory_path, file_name)
        if os.path.isfile(file_path) and file_name.endswith('.py'):
            with open(file_path, 'r', encoding="utf-8", errors="ignore") as f:
                doc = text_splitter.create_documents([f.read()])
            if doc:
                retriever = Chroma.from_documents(documents=doc, embedding=embedding, persist_directory=os.path.join(INDEXES_DIR, file_name[:-3]))
                retriever.persist()
                retriever = retriever.as_retriever()
                retrievers_info.append({
                    "name": file_name[:-3],
                    "description": f"Good for answering questions about {file_name[:-3]}",
                    "retriever": retriever
                })
    return retrievers_info

# Initialize the language model
llm = OpenAI()

# Initialize the multi-retrieval question-answering chain
chain = MultiRetrievalQAChain(llm)

# Process files from respective directories and add to the chain
retrievers_info = process_text_files(TEXT_DIR)
retrievers_info.extend(process_pdf_files(PDF_DIR))
retrievers_info.extend(process_python_files(BASE_DIR))  # Let's process Python files from base directory

# Add all retrievers to the chain
for retriever_info in retrievers_info:
    chain.add_retriever(retriever_info['name'], retriever_info['retriever'], retriever_info['description'])

# Finalize the chain
chain.finalize()

# Start terminal application
while True:
    print("Ask your question (type 'exit' to quit): ")
    question = input()
    if question.lower() == 'exit':
        break
    answer = chain.ask(question)
    print("Answer: ", answer)