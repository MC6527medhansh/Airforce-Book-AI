from agents import writer_agent
from notion_api import push_to_notion
from book_outline import BOOK_INDEX

def run_book(book_index: dict[str, list[str]]) -> None:
    """
    Iterates over every chapter and its subsections,
    generates text, and pushes it to Notion.
    """
    for chapter_title, subsections in book_index.items():
        print(f"\n Starting Chapter: {chapter_title}")
        for subsection in subsections:
            print(f" Writing: {subsection}")
            # Generate content
            content = writer_agent(subsection, subsections)
            # Push to Notion
            push_to_notion(
                title=chapter_title,
                section=chapter_title,
                subsection=subsection,
                content=content
            )
            print(f" Pushed '{subsection}'")
    print("\n All chapters complete!")

if __name__ == "__main__":
    run_book(BOOK_INDEX)
