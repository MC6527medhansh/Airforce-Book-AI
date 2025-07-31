import os
from dotenv import load_dotenv
from notion_client import Client

load_dotenv()

notion = Client(auth=os.getenv("NOTION_TOKEN"))
DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

def push_to_notion(title: str, section: str, subsection: str, content: str) -> None:
    """
    Pushes a single subsection as a new page in the Notion database.
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
            "paragraph": {"rich_text": [{"type":"text", "text": {"content": content}}]}
        }]
    )
