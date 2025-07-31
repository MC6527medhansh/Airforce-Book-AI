# main.py

from agents import writer_agent, research_agent, editor_agent
from notion_api import push_to_notion
from book_outline import BOOK_INDEX

def run_book(book_index: dict[str, list[str]]) -> None:
    """
    For each chapter and subsection:
      1. Draft via WriterAgent
      2. Research facts via ResearchAgent
      3. Polish via EditorAgent
      4. Push final text to Notion
    """
    for chapter_title, subsections in book_index.items():
        print(f"\n▶️ Chapter: {chapter_title}")
        for subsection in subsections:
            print(f"  ✍️ Drafting: {subsection}")
            draft = writer_agent(subsection, subsections)

            print(f"  🔍 Researching: {subsection}")
            facts = research_agent(subsection)

            combined = f"{draft}\n\n**Research facts:**\n{facts}"

            print(f"  🛠 Polishing: {subsection}")
            polished = editor_agent(combined)

            print(f"  📤 Pushing to Notion: {subsection}")
            push_to_notion(
                title=chapter_title,
                section=chapter_title,
                subsection=subsection,
                content=polished
            )
            print(f"  ✅ Done: {subsection}")
    print("\n🎉 All chapters processed!")

if __name__ == "__main__":
    run_book(BOOK_INDEX)
