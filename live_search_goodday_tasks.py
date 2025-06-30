#!/usr/bin/env python3
"""
Live test script for Goodday Search Tasks functionality
This script provides an interactive test for the search-tasks endpoint.
"""

import os
import asyncio
import httpx


async def live_search_tasks():
    """Interactive search tasks test."""
    search_endpoint_url = "https://example.com/webhook/goodday-mcp/search-tasks"
    bearer_token = os.getenv("GOODDAY_SEARCH_BEARER_TOKEN", "")
    
    print("🔍 Goodday Live Search Tasks Test")
    print("="*50)
    print(f"Search Endpoint URL: {search_endpoint_url}")
    print(f"Bearer Token: {'✅ Set' if bearer_token else '❌ Not Set'}")
    
    if not bearer_token:
        print("\n❌ ERROR: Bearer token not found!")
        print("Please set the GOODDAY_SEARCH_BEARER_TOKEN environment variable")
        print("Example: export GOODDAY_SEARCH_BEARER_TOKEN='your_token_here'")
        return
    
    print("\n📝 Enter search queries (type 'quit' to exit):")
    print("Examples: 'ASTRA task', 'S3 upload', 'security improvements'")
    print("-" * 50)
    
    headers = {
        "User-Agent": "goodday-live-search-test/1.0.0",
        "Authorization": f"Bearer {bearer_token}",
        "Content-Type": "application/json"
    }
    
    while True:
        try:
            query = input("\n🔍 Search query: ").strip()
            
            if query.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
                
            if not query:
                print("❌ Please enter a search query")
                continue
            
            print(f"🔍 Searching for: '{query}'...")
            
            url = search_endpoint_url
            params = {"query": query}
            
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=headers, params=params, timeout=30.0)
                response.raise_for_status()
                data = response.json()
            
            if not data or not isinstance(data, list) or len(data) == 0:
                print("❌ No results found")
                continue
            
            first_item = data[0]
            if not isinstance(first_item, dict) or "result" not in first_item:
                print(f"❌ Unexpected response format: {data}")
                continue
            
            results = first_item.get("result", [])
            if not results:
                print("❌ No search results found")
                continue
            
            print(f"\n✅ Found {len(results)} results:")
            print("=" * 40)
            
            seen_tasks = set()
            for i, result in enumerate(results):
                if not isinstance(result, dict):
                    continue
                
                task_id = result.get('taskId', 'N/A')
                if task_id in seen_tasks:
                    continue
                seen_tasks.add(task_id)
                
                print(f"\n📋 Result {len(seen_tasks)}:")
                print(f"   Task ID: {task_id}")
                print(f"   Title: {result.get('title', 'N/A')}")
                print(f"   Score: {result.get('score', 'N/A')}")
                print(f"   Content: {result.get('content', 'No content')[:150]}{'...' if len(result.get('content', '')) > 150 else ''}")
            
            print(f"\n📊 Summary: {len(seen_tasks)} unique tasks found")
            
        except KeyboardInterrupt:
            print("\n👋 Interrupted! Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {str(e)}")


if __name__ == "__main__":
    asyncio.run(live_search_tasks())
