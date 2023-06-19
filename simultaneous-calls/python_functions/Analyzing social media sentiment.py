from textblob import TextBlob

def analyze_social_media_sentiment(text):
    """
    Function to analyze the sentiment of given text.

    :param text: The text to be analyzed
    :return: A tuple containing the polarity, subjectivity and sentiment status of the text
    """
    # Create a TextBlob object
    sentiment_blob = TextBlob(text)

    # Extract polarity and subjectivity
    polarity = sentiment_blob.sentiment.polarity
    subjectivity = sentiment_blob.sentiment.subjectivity

    # Classify sentiment status based on polarity
    if polarity > 0:
        sentiment_status = "Positive"
    elif polarity < 0:
        sentiment_status = "Negative"
    else:
        sentiment_status = "Neutral"

    return polarity, subjectivity, sentiment_status

# Example usage:
text = "I love Python programming!"
polarity, subjectivity, sentiment_status = analyze_social_media_sentiment(text)
print(f"Polarity: {polarity}, Subjectivity: {subjectivity}, Sentiment: {sentiment_status}")