#!/usr/bin/env python3
"""Simple test script to verify the MCP server can be imported and initialized."""

import sys
import os
import asyncio

# Add the current directory to the path so we can import main
sys.path.insert(0, os.path.dirname(__file__))

async def test_tools():
    """Test that tools are properly registered."""
    import main
    
    try:
        # List all available tools
        tools = await main.mcp.list_tools()
        print(f"✓ Found {len(tools)} tools registered")
        
        print("\nAvailable tools:")
        for tool in tools:
            print(f"  - {tool.name}: {tool.description}")
        
        # Test some expected tools exist
        tool_names = [tool.name for tool in tools]
        expected_tools = [
            'get_projects', 'get_project', 'create_project',
            'get_project_tasks', 'get_task', 'create_task',
            'get_users', 'get_user'
        ]
        
        missing_tools = []
        for expected in expected_tools:
            if expected not in tool_names:
                missing_tools.append(expected)
        
        if missing_tools:
            print(f"✗ Missing expected tools: {missing_tools}")
            return False
        else:
            print("✓ All expected tools are registered")
        
        return True
        
    except Exception as e:
        print(f"✗ Error testing tools: {e}")
        return False

def test_import():
    """Test that we can import the main module without errors."""
    try:
        print("Testing import of main module...")
        import main
        print("✓ Successfully imported main module")
        
        # Test that the MCP server is properly initialized
        print("Testing MCP server initialization...")
        assert hasattr(main, 'mcp'), "MCP server not found"
        print("✓ MCP server is properly initialized")
        
        # Test helper functions
        print("Testing helper functions...")
        test_task = {
            'id': 'test_id',
            'title': 'Test Task',
            'status': {'name': 'Open'},
            'project': {'name': 'Test Project'}
        }
        formatted = main.format_task(test_task)
        assert 'Test Task' in formatted
        print("✓ Helper functions work correctly")
        
        return True
        
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main_test():
    """Run all tests."""
    print("=" * 50)
    print("Testing Goodday MCP Server")
    print("=" * 50)
    
    # Test basic import
    if not test_import():
        return False
    
    print()
    
    # Test tools
    if not await test_tools():
        return False
    
    print("\n" + "=" * 50)
    print("✓ All tests passed! Server is ready to use.")
    print("=" * 50)
    
    print("\nTo use the server:")
    print("1. Set your GOODDAY_API_TOKEN environment variable")
    print("2. Run: uv run main.py")
    print("3. Or configure it in Claude Desktop as shown in README.md")
    
    return True

if __name__ == "__main__":
    # Set a dummy API token for testing
    os.environ['GOODDAY_API_TOKEN'] = 'test_token_for_import_test'
    
    success = asyncio.run(main_test())
    sys.exit(0 if success else 1)
