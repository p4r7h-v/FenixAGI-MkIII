import gensim.summarization

def text_summarizer(text, summary_ratio=0.2, word_count=None):
    """
    Summarizes the input text using Gensim's summarize function.
    
    Args:
        text (str): The input text to be summarized.
        summary_ratio (float, optional): A ratio determining the size of the summary.
                                          Default is 0.2, meaning the summary would be 20% of the original text.
        word_count (int, optional): The desired word count of the summary. If both summary_ratio and
                                     word_count are provided, word_count will be used.

    Returns:
        str: The summarized text.
    """
    if not text:
        return "Empty text provided. Please provide a valid text."
    
    try:
        summary = gensim.summarization.summarize(text, ratio=summary_ratio, word_count=word_count)
        if not summary:
            return "Gensim could not generate a summary for the given text."
        return summary
    except ValueError as e:
        return str(e)