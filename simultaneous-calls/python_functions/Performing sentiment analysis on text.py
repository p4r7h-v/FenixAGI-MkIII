from textblob import TextBlob

def sentiment_analysis(text):
    # Create a TextBlob object
    blob = TextBlob(text)

    # Get the sentiment polarity (-1 to 1)
    polarity = blob.sentiment.polarity

    # Determine the sentiment label
    if polarity > 0:
        sentiment = "Positive"
    elif polarity < 0:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    # Return the sentiment label and polarity value
    return sentiment, polarity

# Example usage
text = "I love Python programming!"
result = sentiment_analysis(text)
print(f"Sentiment: {result[0]}, Polarity: {result[1]:.2f}")