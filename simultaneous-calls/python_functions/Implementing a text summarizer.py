import heapq
import nltk
from collections import defaultdict
from nltk.cluster.util import cosine_distance
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize

nltk.download('punkt')
nltk.download('stopwords')

def text_summarizer(text, num_sentences=3):
    def sentence_similarity(sent1, sent2, stopwords=None):
        if stopwords is None:
            stopwords = []
    
        sent1 = [w.lower() for w in sent1 if w.lower() not in stopwords]
        sent2 = [w.lower() for w in sent2 if w.lower() not in stopwords]
    
        all_words = list(set(sent1 + sent2))
    
        vector1 = [0] * len(all_words)
        vector2 = [0] * len(all_words)
    
        for w in sent1:
            vector1[all_words.index(w)] += 1
    
        for w in sent2:
            vector2[all_words.index(w)] += 1
    
        return 1 - cosine_distance(vector1, vector2)
    
    def build_similarity_matrix(sentences, stop_words):
        similarity_matrix = defaultdict(list)
        
        for idx1, sent1 in enumerate(sentences):
            for idx2, sent2 in enumerate(sentences):
                if idx1 != idx2:
                    sim = sentence_similarity(sent1, sent2, stop_words)
                    similarity_matrix[idx1].append((idx2, sim))
    
        return similarity_matrix
    
    stop_words = stopwords.words('english')
    sentences = sent_tokenize(text)
    tokenized_sentences = [word_tokenize(s) for s in sentences]

    similarity_matrix = build_similarity_matrix(tokenized_sentences, stop_words)
    
    scores = defaultdict(int)
    for idx1, sim_list in enumerate(similarity_matrix.values()):
        for idx2, sim in sim_list:
            sim_val = sim_list[idx2][1]
            scores[idx1] += sim_val
            scores[idx2] += sim_val
    
    top_sentence_indices = heapq.nlargest(num_sentences, scores, key=scores.get)
    top_sentence_indices.sort()
    summary = [sentences[idx] for idx in top_sentence_indices]

    return ' '.join(summary)

example_text = """This is a sample text for our text summarization function. The function is based on the TextRank algorithm, which is an unsupervised extractive summarization method. Extractive summarization methods select a subset of existing words, phrases, or sentences from the original text to form the summary. TextRank works by constructing a similarity matrix for the input sentences, and ranking sentences based on the similarity to each other. The highest-ranked sentences are selected to make up the final summary. This similarity is calculated using cosine similarity, which measures the angle between two non-zero vectors."""

print(text_summarizer(example_text, num_sentences=2))