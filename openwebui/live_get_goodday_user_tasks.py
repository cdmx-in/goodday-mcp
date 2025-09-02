import asyncio
from goodday_openwebui_complete_tool import Tools

async def main():
    tools = Tools()
    # Optionally set your API key here if not using env var
    # tools.valves.api_key = "your_goodday_api_token"

    # Call the function with your live parameters
    result = await tools.get_goodday_user_tasks(
        user="Roney Dsilva",  # You can also use an email here
        closed=False
    )
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
