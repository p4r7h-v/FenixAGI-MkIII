from notion_client import ClientObject

class NotionBot:
  def __init__(self, token):
    self.client = ClientObject(token)

  # create data in Notion
  def create(self, database_id, properties):
    page = self.client.pages.create(
      parent={"database_id": database_id}, 
      properties=properties
    )
    return page

  # read data from Notion
  def read(self, page_id):
    page = self.client.pages.retrieve(page_id)
    return page

  # update data in Notion
  def update(self, page_id, properties):
    page = self.client.pages.update(page_id, properties=properties)
    return page

  # delete data from Notion
  def delete(self, page_id):
    page = self.client.pages.delete(page_id)
    return page