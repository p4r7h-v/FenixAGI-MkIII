def simple_search_engine(keyword, documents):
    results = []
    lower_keyword = keyword.lower()

    for index, doc in enumerate(documents):
        lower_doc = doc.lower()
        if lower_keyword in lower_doc:
            results.append({"index": index, "document": doc})

    return results

# Example usage:
documents = [
    "The quick brown fox jumps over the lazy dog",
    "I love Python programming",
    "Simple search engines are fun to build",
    "Python is a versatile programming language",
]

keyword = "python"

print(simple_search_engine(keyword, documents))