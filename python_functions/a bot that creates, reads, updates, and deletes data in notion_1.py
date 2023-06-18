from notion.client import NotionClient

class NotionBot:
    def __init__(self, token):
        self.client = NotionClient(token_v2=token)
    
    def create_data(self, page_url, title):
        page = self.client.get_block(page_url)
        new_child = page.children.add_new(Heading1Block, title=title)
        print("Data created successfully!!")
        return new_child.id

    def read_data(self, page_url):
        page = self.client.get_block(page_url)
        for block in page.children:
            print(block.title)
            
    def update_data(self, block_id, new_title):
        block = self.client.get_block(block_id)
        block.title = new_title
        print("Data updated successfully!!")
        
    def delete_data(self, block_id):
        block = self.client.get_block(block_id)
        block.remove()
        print("Data deleted successfully!!")


# Instantiate the bot
bot = NotionBot("your_notion_token")

# Create data
new_block_id = bot.create_data("page_url", "New Title")

# Read data
bot.read_data("page_url")

# Update data
bot.update_data(new_block_id, "Updated Title")

# Delete data
bot.delete_data(new_block_id)