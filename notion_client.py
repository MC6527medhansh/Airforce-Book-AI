import os
from notion_client import Client

notion = Client(auth=os.getenv("NOTION_TOKEN"))
DATABASE_ID = os.getenv("NOTION_DATABASE_ID")


def push_to_notion(title, section, subsection, content):
    """
    Creates a new page in your Notion database with the given fields.
    """
    notion.pages.create(
        parent={"database_id": DATABASE_ID},
        properties={
            "Title": {"title": [{"text": {"content": title}}]},
            "Section": {"select": {"name": section}},
            "Subsection": {"rich_text": [{"text": {"content": subsection}}]}
        },
        children=[{
            "object": "block",
            "type": "paragraph",
            "paragraph": {"rich_text": [{"text": {"content": content}}]}
        }]
    )
