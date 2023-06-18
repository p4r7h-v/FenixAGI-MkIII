import gensim.downloader as api
from gensim.models import Word2Vec
from nltk.tokenize import word_tokenize
import nltk

nltk.download('punkt')


def generate_word_embedding(text_data, embedding_size=100):
    """
    Generate a word embedding for given text data.

    :param text_data: List of text sentences.
    :param embedding_size: The size of the word embedding, default is 100.
    :return: Word2Vec model
    """
    # Tokenize the sentences
    tokenized_text = [word_tokenize(sentence.lower()) for sentence in text_data]

    # Train the Word2Vec model
    model = Word2Vec(tokenized_text, size=embedding_size, window=5, min_count=1, workers=4)

    # Normalize the word vectors
    model.init_sims(replace=True)

    return model


# Example usage
text_data = [
    "This is a sample sentence.",
    "Another sample sentence is here.",
    "We will generate word embeddings."
]

word_embedding_model = generate_word_embedding(text_data)

# Get the word embedding for a specific word
word_embedding = word_embedding_model.wv["sample"]
print(word_embedding)