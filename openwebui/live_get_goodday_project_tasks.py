import asyncio
from openwebui.goodday_openwebui_complete_tool import Tools

async def main():
    tools = Tools()
    # Optionally set your API key here if not using env var
    # tools.valves.api_key = "your_goodday_api_token"

    # Call the function with your live parameters
    result = await tools.get_goodday_project_tasks(
        project_name="orion"  # Change to your project name
    )
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
