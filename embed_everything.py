import os
import sys
import traceback
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains.router import MultiRetrievalQAChain
from langchain.llms import OpenAI
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

def main():
    doc = None
    indexed_files = set()

    # Initialize the OpenAI embeddings
    try:
        os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
        embedding = OpenAIEmbeddings()
    except Exception as e:
        print("Error initializing OpenAI Embeddings. Please check your API key and try again.")
        traceback.print_exc()
        sys.exit(1)
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=20, length_function=len)

    # Directories for storing indexes and uploaded files
    docs_dir = 'docs'
    user_dir = os.path.join(docs_dir)
    indexes_dir = os.path.join(user_dir, 'indexes')
               
    # Create directories if they don't exist
    os.makedirs(user_dir, exist_ok=True)
    os.makedirs(indexes_dir, exist_ok=True)
    
    # Save uploaded files to user's directory and process them
    root_directory = '.'  # Set the root directory here
    files = [f for f in os.listdir(root_directory) if os.path.isfile(os.path.join(root_directory, f))]
    
    if files:
        for filename in files:
            if filename in indexed_files or not filename.lower().endswith(('.txt', '.pdf')):
                continue

            filepath = os.path.join(root_directory, filename)
            print(f'Creating index for {filename}...')
            try:
                if filename.lower().endswith('.txt'):
                    with open(filepath, 'r', encoding="utf-8", errors="ignore") as f:
                        doc = text_splitter.create_documents([f.read()])
                elif filename.lower().endswith('.pdf'):
                    loader = PyPDFLoader(filepath)
                    doc = loader.load_and_split()
                
                if doc is not None and filename != 'indexes':
                    if not doc:
                        print(f"Document {filename} is empty after splitting.")  # Print a warning if doc is empty
                    else:
                        retriever = Chroma.from_documents(documents=doc, embedding=embedding, persist_directory=os.path.join(indexes_dir, filename[:-4]))
                        retriever.persist()
                        retriever = retriever.as_retriever()
                        indexed_files.add(filename)
                        print(f'Index created for {filename}.')
            except Exception as e:
                print(f'Error creating index for {filename}.')
                traceback.print_exc()

if __name__ == "__main__":
    main()
