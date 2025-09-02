import asyncio
from goodday_openwebui_complete_tool import Tools

async def main():
    tools = Tools()
    # Set your API key and other required values here if needed
    # tools.valves.api_key = "YOUR_API_KEY"
    # tools.valves.bearer_token = "YOUR_BEARER_TOKEN"
    # tools.valves.api_base = "https://api.goodday.work/2.0"
    # tools.valves.search_url = "https://example.com/webhook/goodday-mcp/search-tasks"

    project_name = "orion"
    print(f"Fetching tasks for project: {project_name}")
    result = await tools.get_goodday_project_tasks(project_name=project_name)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
