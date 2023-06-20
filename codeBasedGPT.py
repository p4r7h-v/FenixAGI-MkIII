import os
import io
import re
import contextlib
import traceback
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains.router import MultiRetrievalQAChain
from langchain.llms import OpenAI
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import openai


os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# Function to get a GPT-generated response
def get_gpt_response(messages, chain):
    user_message = messages[-1]['content']
    output = ""
    if chain is not None:
        try:
            with io.StringIO() as buf, contextlib.redirect_stdout(buf):
                resp = chain.run(user_message)
                print("Response: ", resp)
                output = buf.getvalue()
                print("Output: ", output)
                match = re.search(r"(\w+: \{'query': '.*?'\})", output)
                print("Match: ", match)
                if match is None or "None" in match.group(1) :
                    response = openai.ChatCompletion.create(
                        model="gpt-4-0613",
                        messages=messages,
                        max_tokens=1000,
                        n=1,
                        temperature=0.5,
                    )
                    generated_text = response['choices'][0]['message']['content']
                    return generated_text
                else:
                    print(match.group(1))
                
                if resp:
                    print("Retrieving docs...")
                    return resp
        except ValueError:
            resp = None
    else:
        response = openai.ChatCompletion.create(
            model="gpt-4-0613",
            messages=messages,
            max_tokens=1000,
            n=1,
            temperature=0.5,
        )
        generated_text = response['choices'][0]['message']['content']
        return generated_text


def main():

    try:
        embedding = OpenAIEmbeddings()
    except Exception as e:
        print("Error initializing OpenAI Embeddings. Please check your API key and try again.")
        traceback.print_exc()
        exit(1)

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=20, length_function=len)

    indexed_files = set()
    docs_dir = 'docs'
    indexes_dir = os.path.join(docs_dir, 'indexes')

    os.makedirs(indexes_dir, exist_ok=True)
    retrievers_info = []

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
                        print(f"Document {filename} is empty after splitting.")
                    else:
                        retriever = Chroma.from_documents(documents=doc, embedding=embedding, persist_directory=os.path.join(indexes_dir, filename[:-4]))
                        retriever.persist()
                        retriever = retriever.as_retriever()
                        retrievers_info.append({
                            "name": filename[:-4],
                            "description": f"Good for answering questions about {filename[:-4]}",
                            "retriever": retriever
                        })
                        indexed_files.add(filename)
                        print(f'Index created for {filename}.')
            except Exception as e:
                print(f'Error creating index for {filename}.')
                traceback.print_exc()

    print("Creating chain...")
    print("Retrievers: ", retrievers_info)
    chain = MultiRetrievalQAChain.from_retrievers(OpenAI(), retrievers_info, verbose=True)
    print("Chain created.")
    print(chain)
    conversation = []

    while True:
        user_input = input("Your Input: ")
        conversation.append({"role": "user", "content": user_input})

        # Generate response using GPT
        response = get_gpt_response(conversation, chain)

        if not response:
            response = openai.ChatCompletion.create(
                model="gpt-4-0613",
                messages=conversation,
                max_tokens=1000,
                n=1,
                temperature=0.5,
            )

            generated_text = response['choices'][0]['message']['content']
            print(f"Chatbot: {generated_text}")
        else:
            print(f"Chatbot: {response}")

        conversation.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()
