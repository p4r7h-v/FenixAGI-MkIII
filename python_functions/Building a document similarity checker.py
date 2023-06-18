import re
import math
from collections import Counter
from typing import List

def cosine_similarity(vector1: List[int], vector2: List[int]) -> float:
    dot_product = sum(p*q for p,q in zip(vector1, vector2))
    magnitude1 = math.sqrt(sum(p**2 for p in vector1))
    magnitude2 = math.sqrt(sum(q**2 for q in vector2))
    return dot_product / (magnitude1 * magnitude2)

def text_to_vector(text: str) -> Counter:
    words = re.findall(r'\w+', text.lower())
    return Counter(words)

def document_similarity_checker(doc1: str, doc2: str) -> float:
    vector1 = text_to_vector(doc1)
    vector2 = text_to_vector(doc2)
    
    intersection = set(vector1.keys()) & set(vector2.keys())
    numerator = sum(vector1[x] * vector2[x] for x in intersection)
    
    sum1 = sum(vector1[x]**2 for x in vector1.keys())
    sum2 = sum(vector2[x]**2 for x in vector2.keys())
    denominator = math.sqrt(sum1) * math.sqrt(sum2)
    
    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator

# Example usage:
document1 = "This is a sample text for testing the document similarity checker."
document2 = "This text is another example for testing the similarity checker method."

similarity = document_similarity_checker(document1, document2)
print(f"Similarity between document1 and doc2: {similarity:.2f}")