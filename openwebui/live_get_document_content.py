import asyncio
from goodday_openwebui_complete_tool import Tools

async def main():
    tools = Tools()
    # Optionally set your API key here if not using env var
    # tools.valves.api_key = "your_goodday_api_token"

    # First, search for documents to get a document ID
    print("=== Searching for documents ===")
    search_result = await tools.search_project_documents(
        project_name="ASTRA",
        document_name="postgres"
    )
    print(search_result)

    # Then, get content of a specific document (replace with actual document ID from search results)
    print("\n=== Getting document content ===")
    # Replace 'YOUR_DOCUMENT_ID_HERE' with an actual document ID from the search results above
    result = await tools.get_document_content(
        document_id="YOUR_DOCUMENT_ID_HERE"  # Replace with actual document ID
    )
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
