import asyncio
from goodday_openwebui_complete_tool import Tools


async def fetch_sprint_tasks(project_name, sprint_name, closed=False):
    tools = Tools()
    # Optionally set your API key here if not using env var
    # tools.valves.api_key = "your_goodday_api_token"
    return await tools.get_goodday_sprint_tasks(
        project_name=project_name, sprint_name=sprint_name, closed=closed
    )


async def main():
    result = await fetch_sprint_tasks(
        project_name="Astra", sprint_name="Sprint 121", closed=False
    )
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
