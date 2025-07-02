#!/usr/bin/env python3
"""
Live test for get_goodday_sprint_summary function
"""

import asyncio
import sys
import os
from datetime import datetime

# Add the openwebui directory to the path
import importlib.util
openwebui_path = os.path.join(os.path.dirname(__file__), 'openwebui')
tool_file_path = os.path.join(openwebui_path, 'goodday_openwebui_complete_tool.py')

if not os.path.exists(tool_file_path):
    print(f"❌ Error: Could not find goodday_openwebui_complete_tool.py")
    print(f"Expected path: {tool_file_path}")
    sys.exit(1)

# Load the module directly
spec = importlib.util.spec_from_file_location("goodday_openwebui_complete_tool", tool_file_path)
goodday_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(goodday_module)
Tools = goodday_module.Tools


async def test_sprint_summary():
    """Test the get_goodday_sprint_summary function with real data"""
    
    # Initialize the tools
    tools = Tools()
    
    # Check if API key is set in environment
    api_key = os.getenv("GOODDAY_API_TOKEN")
    if not api_key:
        print("❌ Error: GOODDAY_API_TOKEN environment variable not set")
        print("Please set your Goodday API token:")
        print("export GOODDAY_API_TOKEN='your_api_token_here'")
        return False
    
    # Set the API key in valves
    tools.valves.api_key = api_key
    
    print("🚀 Testing get_goodday_sprint_summary function")
    print("=" * 60)
    
    # Test cases with different project and sprint combinations
    test_cases = [
        {
            "project_name": "ASTRA",
            "sprint_name": "Sprint 233",
            "description": "Test with explicit 'Sprint' prefix"
        },
        {
            "project_name": "Astra", 
            "sprint_name": "233",
            "description": "Test with just sprint number"
        },
        {
            "project_name": "astra",
            "sprint_name": "sprint 102", 
            "description": "Test with different case and older sprint"
        }
    ]
    
    all_passed = True
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📋 Test Case {i}: {test_case['description']}")
        print(f"   Project: '{test_case['project_name']}'")
        print(f"   Sprint: '{test_case['sprint_name']}'")
        print("-" * 50)
        
        try:
            # Mock event emitter to track progress
            events = []
            
            async def mock_event_emitter(event):
                events.append(event)
                status_data = event.get("data", {})
                description = status_data.get("description", "")
                done = status_data.get("done", False)
                status_icon = "✅" if done else "⏳"
                print(f"   {status_icon} {description}")
            
            start_time = datetime.now()
            
            # Call the function
            result = await tools.get_goodday_sprint_summary(
                project_name=test_case["project_name"],
                sprint_name=test_case["sprint_name"],
                __event_emitter__=mock_event_emitter
            )
            
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            # Check if the result indicates success
            if result and not result.startswith("Failed to") and not result.startswith("Unable to") and not result.startswith("Project") and "not found" not in result:
                print(f"   ✅ Test passed in {duration:.2f}s")
                print(f"   📊 Summary length: {len(result)} characters")
                
                # Show a preview of the result
                preview = result[:300] + "..." if len(result) > 300 else result
                print(f"   📄 Preview:\n{preview}")
                
                # Count different sections in the summary
                sections = ["Sprint Overview:", "Status Distribution:", "Task Assignment:", "Task Details:"]
                found_sections = [section for section in sections if section in result]
                print(f"   📋 Sections found: {', '.join(found_sections)}")
                
                # Check for task descriptions
                if "Description:" in result:
                    description_count = result.count("Description:")
                    print(f"   📝 Task descriptions found: {description_count}")
                
            else:
                print(f"   ❌ Test failed in {duration:.2f}s")
                print(f"   📄 Error: {result}")
                all_passed = False
                
        except Exception as e:
            print(f"   ❌ Test failed with exception: {str(e)}")
            all_passed = False
        
        print()
    
    # Test error cases
    print("🔍 Testing Error Cases")
    print("-" * 50)
    
    error_test_cases = [
        {
            "project_name": "NonExistentProject",
            "sprint_name": "Sprint 999",
            "expected_error": "not found",
            "description": "Non-existent project"
        },
        {
            "project_name": "ASTRA",
            "sprint_name": "Sprint 99999",
            "expected_error": "not found",
            "description": "Non-existent sprint"
        }
    ]
    
    for i, test_case in enumerate(error_test_cases, 1):
        print(f"\n🚫 Error Test {i}: {test_case['description']}")
        print(f"   Project: '{test_case['project_name']}'")
        print(f"   Sprint: '{test_case['sprint_name']}'")
        
        try:
            result = await tools.get_goodday_sprint_summary(
                project_name=test_case["project_name"],
                sprint_name=test_case["sprint_name"]
            )
            
            if test_case["expected_error"] in result.lower():
                print(f"   ✅ Error handling working correctly")
                print(f"   📄 Message: {result}")
            else:
                print(f"   ❌ Unexpected result: {result}")
                all_passed = False
                
        except Exception as e:
            print(f"   ❌ Unexpected exception: {str(e)}")
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 All tests passed! get_goodday_sprint_summary is working correctly.")
    else:
        print("❌ Some tests failed. Please check the function implementation.")
    
    return all_passed


async def main():
    """Main test runner"""
    print("🧪 Goodday Sprint Summary Function Live Test")
    print(f"🕒 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    success = await test_sprint_summary()
    
    print()
    print(f"🕒 Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    # Run the test
    asyncio.run(main())
