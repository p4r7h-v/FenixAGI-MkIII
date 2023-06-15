import os
import re
import io
import contextlib
import streamlit as st
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains.router import MultiRetrievalQAChain
from langchain.llms import OpenAI
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import shutil
import uuid
import openai
import requests
from PIL import Image, ImageDraw
from io import BytesIO
import base64
import json

openai_api_key = os.getenv('OPENAI_API_KEY')
os.environ["OPENAI_API_KEY"] = openai_api_key

st.set_page_config(layout="wide")


embedding = None
text_splitter = None
retrievers_info = []
# URLs for user and chatbot images
user_image_url = "https://cdn.midjourney.com/864f655e-a2c9-4237-a989-15a9017926d7/0_0.png"
chatbot_image_url = "https://cdn.midjourney.com/bd3d7a2f-a358-4ae6-adc9-2f13a396e092/0_2.png"

def get_circular_masked_image(img_url):
    try:
        response = requests.get(img_url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        st.error(f"Error loading image: {e}")
        return

    img = Image.open(BytesIO(response.content))

    # Create circular mask
    width, height = img.size
    mask = Image.new('L', (width, height), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, width, height), fill=255)

    # Apply mask to image
    img.putalpha(mask)

    # Convert image to base64
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()

    return img_str

# Get circular masked images
user_image = get_circular_masked_image(user_image_url)
chatbot_image = get_circular_masked_image(chatbot_image_url)


# Function to get a GPT-generated response
def get_gpt_response(messages, chain):
    # Extract the user's message from the conversation
    user_message = messages[-1]['content']
    output = ""
    if chain is not None:
        try:
            # Try running the document retrieval process
            with io.StringIO() as buf, contextlib.redirect_stdout(buf):
                resp = chain.run(user_message)
                output = buf.getvalue()
                match = re.search(r"(\w+: \{'query': '.*?'\})", output)
                #st.sidebar.write(match)
                if match is None or "None" in match.group(1) : 
                    #st.sidebar.warning("No matching documents found. Generating response using GPT-3...")
                    # Make an API call to the GPT model
                    response = openai.ChatCompletion.create(
                        model="gpt-4",
                        messages=messages,
                        max_tokens=1000,
                        n=1,
                        temperature=0.5,
                    )
                    # Extract the generated text from the response
                    generated_text = response['choices'][0]['message']['content']
                    return generated_text
                else:
                    # write which index we are using 
                    #st.sidebar.write(match)
                    st.markdown(match.group(1))
                
                # If a match is found in the documents, use it as the response
                if resp:
                    st.success("Retrieving docs...")
                    return resp

        except ValueError:
            # If a ValueError is raised, fall back to GPT
            resp = None
    else:
        #st.sidebar.warning("No matching documents found. Generating response using GPT-3...")
        # Make an API call to the GPT model
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages,
            max_tokens=1000,
            n=1,
            temperature=0.5,
        )
        # Extract the generated text from the response
        generated_text = response['choices'][0]['message']['content']
        return generated_text
            
    

def main():
    
    doc = None
    # Initialize the OpenAI embeddings
    try:
        os.environ["OPENAI_API_KEY"] = openai_api_key
        embedding = OpenAIEmbeddings()
    except Exception as e:
        st.error("Error initializing OpenAI Embeddings. Please check your API key and try again.")
        raise e
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=20, length_function=len)

    # Generate a unique session ID
    session_id = uuid.uuid4().hex

    # Directories for storing indexes and uploaded files
    docs_dir = 'docs'
    # Create a unique user directory based on session ID
    user_dir = os.path.join(docs_dir, session_id)
    indexes_dir = os.path.join(user_dir, 'indexes')
               
    # Create directories if they don't exist
    os.makedirs(user_dir, exist_ok=True)
    os.makedirs(indexes_dir, exist_ok=True)
    
    # Check if session ID directory already exists
    if "retrievers_info" not in st.session_state:
        st.session_state.retrievers_info = []
        if os.path.exists(user_dir):
            existing_indexes = [filename[:-4] for filename in os.listdir(indexes_dir)]
            for filename in existing_indexes:
                index_dir_path = os.path.join(indexes_dir, filename)
                retriever = Chroma.from_disk(index_dir_path)
                retriever = retriever.as_retriever()
                st.session_state.retrievers_info.append({
                    "name": filename,
                    "description": f"Good for answering questions about {filename}",
                    "retriever": retriever
                })
                
    # Initialize the list for indexed files
    if "indexed_files" not in st.session_state:
        st.session_state.indexed_files = set()
        
    # Save uploaded files to user's directory and process them
    files = st.file_uploader('Upload files', type=['txt', 'pdf'], accept_multiple_files=True)
    if files:
        for file in files:
            filename = file.name
            if filename in st.session_state.indexed_files:
                st.success(f"{filename} is indexed. Feel free to upload another file.")
                continue
            filepath = os.path.join(user_dir, filename)
            with open(filepath, "wb") as f:
                f.write(file.getvalue())

            with st.spinner(f'Creating index for {filename}...'):
                if filename.lower().endswith('.txt'):
                    with open(filepath, 'r', encoding="utf-8", errors="ignore") as f:
                        doc = text_splitter.create_documents([f.read()])
                elif filename.lower().endswith('.pdf'):
                    with open(filepath, 'rb') as f:
                        loader = PyPDFLoader(filepath)
                        doc = loader.load_and_split()
                
                if doc is not None and filename != 'indexes':
                    if not doc:
                        st.warning(f"Document {filename} is empty after splitting.")  # Print a warning if doc is empty
                    else:
                        retriever = Chroma.from_documents(documents=doc, embedding=embedding, persist_directory=os.path.join(indexes_dir, filename[:-4]))
                        retriever.persist()
                        retriever = retriever.as_retriever()
                        # Add the retriever information as a dictionary
                        st.session_state.retrievers_info.append({
                            "name": filename[:-4],
                            "description": f"Good for answering questions about {filename[:-4]}",
                            "retriever": retriever
                        })
                        st.session_state.indexed_files.add(filename)
                        st.success(f'Index created for {filename}.')


# Storing the chat
if 'conversation' not in st.session_state:
    st.session_state['conversation'] = []

# Set page title
st.title(':blue[DocumentChat]')
st.header(':blue[Talk to your documents]')
# Initial chatbot message
welcome_message = "Hi! I'm an assistant that can answer questions about your documents. Upload some documents and ask me a question! 🤖 (please refrain from uploading sensitive/personal data as I get the hang of things around here.)"
st.markdown(welcome_message)

# Initialize the retrievers_info
if "retrievers_info" not in st.session_state:
    st.session_state.retrievers_info = []

# Only create the chain if retrievers_info is not empty
if st.session_state.retrievers_info:
    chain = MultiRetrievalQAChain.from_retrievers(OpenAI(), st.session_state.retrievers_info, verbose=True)
else:
    chain = None

if 'user_input' not in st.session_state:
    st.session_state['user_input'] = None

if 'submit_button' not in st.session_state:
    st.session_state['submit_button'] = False

# Get user's input
st.session_state['user_input'] = st.text_input("Your Input", "", key="input", label_visibility="hidden")
st.session_state['submit_button'] = st.button("Submit")

# Get the answer
if st.session_state['submit_button'] and st.session_state['user_input'] and (not st.session_state['conversation'] or st.session_state['user_input'] != st.session_state['conversation'][-1]['content']):
   # Prepare the conversation history
    st.session_state['conversation'].append({"role": "user", "content": st.session_state['user_input']})

    # Display the user's message
    st.markdown(
        f'<img src="data:image/png;base64,{user_image}" style="border-radius: 50%; width: 50px; height: 50px; margin-bottom: 20px; margin-right:10px"> {st.session_state["user_input"]}',
        unsafe_allow_html=True
    )

    if st.session_state['submit_button']:
        # Generate response using GPT
        response = get_gpt_response(st.session_state['conversation'], chain)

        # Append chatbot's message to the conversation history
        st.session_state['conversation'].append({"role": "assistant", "content": response})
        #st.sidebar.write(st.session_state['conversation'])

        # Display the assistant's message
        st.markdown(
            f'<img src="data:image/png;base64,{chatbot_image}" style="border-radius: 50%; width: 50px; height: 50px; margin-bottom: 20px; margin-right:10px"><p style="color:#FFFFFF">{response}</p>',
            unsafe_allow_html=True
        )

    # Generate three possible next questions
    prompt = "\n".join([message['content'] for message in st.session_state['conversation'][-5:]]) + "\nWhat are three good follow up questions the user can ask?"
    questions_response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=100,
        n=1,
        temperature=0.7,
    )
    questions = questions_response['choices'][0]['message']['content'].split("\n")

    # Display the three possible next questions
    st.markdown("Here are things you might want to know:")
    for i, question in enumerate(questions, 1):
        st.markdown(
            f'<img src="data:image/png;base64,{user_image}" style="border-radius: 50%; width: 50px; height: 50px; margin-bottom: 20px; margin-right:10px"> {question}',
            unsafe_allow_html=True
        )        # Append the question to the conversation history
        st.session_state['conversation'].append({"role": "user", "content": question})
        # Generate response using GPT
        response = get_gpt_response(st.session_state['conversation'], chain)
        # Append chatbot's message to the conversation history
        st.session_state['conversation'].append({"role": "assistant", "content": response})
        # Display the assistant's message
        st.markdown(
            f'<img src="data:image/png;base64,{chatbot_image}" style="border-radius: 50%; width: 50px; height: 50px; margin-bottom: 20px; margin-right:10px"><p style="color:#FFFFFF">{response}</p>',
            unsafe_allow_html=True
        )
    
    # Reset the conversation history after displaying the follow-up questions
    st.session_state['conversation'] = []

if __name__ == '__main__':
    main()