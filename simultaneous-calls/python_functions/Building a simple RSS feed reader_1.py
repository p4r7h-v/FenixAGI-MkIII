import feedparser

def rss_feed_reader(url):
    """
    A simple RSS feed reader that prints the feed title, published date, and summary for each entry.
    :param url: The URL of the RSS feed to read
    """
    # Parse the RSS feed
    feed = feedparser.parse(url)
    
    # Print feed title
    print(f"Feed Title: {feed.feed.title}\n")

    # Loop through each entry in the feed
    for entry in feed.entries:
        print(f"Title: {entry.title}")
        print(f"Published: {entry.published}")
        print(f"Summary: {entry.summary}\n")

# Example usage:
rss_feed_reader("https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en")