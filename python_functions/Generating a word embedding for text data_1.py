import gensim.downloader as api
from gensim.models import Word2Vec
from gensim.utils import simple_preprocess

def generate_word_embedding(text):
    # Tokenize and preprocess the text
    tokenized_text = simple_preprocess(text)
    
    # Load a pre-trained Word2Vec model (you can replace 'glove-wiki-gigaword-100' with another model if needed)
    model = api.load('word2vec-google-news-300')
    
    # Generate the word embedding for each word in the tokenized text
    word_embeddings = []
    for word in tokenized_text:
        if word in model.wv:
            word_embeddings.append(model.wv[word])
        else:
            print(f"Warning: '{word}' not in vocabulary, skipping.")
    
    return word_embeddings

# Example usage:
text = "This is an example of generating word embeddings for text data."
word_embeddings = generate_word_embedding(text)
print(word_embeddings)