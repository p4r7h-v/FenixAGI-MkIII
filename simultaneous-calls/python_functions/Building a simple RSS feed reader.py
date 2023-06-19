import feedparser

def read_rss_feed(url):
    rss_feed = feedparser.parse(url)

    if rss_feed.bozo:  # To check if the feed is well-formed
        print("The given URL does not seem to be a valid RSS feed")
        return

    print("Feed Title:", rss_feed.feed.title)
    print("Feed Link:", rss_feed.feed.link)

    for entry in rss_feed.entries:
        print("\nEntry Title:", entry.title)
        print("Entry Link:", entry.link)
        print("Entry Description:", entry.description)

if __name__ == '__main__':
    feed_url = "https://example.com/rss_feed_url"
    read_rss_feed(feed_url)