import asyncio
from goodday_openwebui_complete_tool import Tools

async def main():
    tools = Tools()
    # Optionally set your API key here if not using env var
    # tools.valves.api_key = "your_goodday_api_token"

    print(f"Searching for project: ASTRA")
    
    # First, let's find the project details
    try:
        projects_data = await tools._make_goodday_request("projects?archived=true")
        
        # Filter to only PROJECT and FOLDER type projects
        project_type_projects = [p for p in projects_data if isinstance(p, dict) and p.get('systemType') in ['PROJECT', 'FOLDER']]
        print(f"Found {len(projects_data) if projects_data else 0} total items (including tags/system projects)")
        print(f"Found {len(project_type_projects)} PROJECT/FOLDER type projects")
        
                # Find projects containing ASTRA in their name (case-insensitive)
        astra_projects = []
        for project in project_type_projects:
            if isinstance(project, dict) and 'astra' in project.get('name', '').lower():
                astra_projects.append(project)
        
        if astra_projects:
            print(f"Found {len(astra_projects)} project(s) containing 'ASTRA':")
            for i, proj in enumerate(astra_projects):
                print(f"  {i+1}. {proj.get('name')} (ID: {proj.get('id')}, Type: {proj.get('systemType')})")
            
            # Use the first match
            astra_project = astra_projects[0]
            print(f"\nUsing first match: {astra_project.get('name')}")
        else:
            print("No projects found containing 'ASTRA' in their name")
            print("Available PROJECT/FOLDER type projects (first 10):")
            for i, proj in enumerate(project_type_projects[:10]):
                print(f"  {i+1}. {proj.get('name')} (ID: {proj.get('id')}, Type: {proj.get('systemType')})")
            return
            
    except Exception as e:
        print(f"Error during debugging: {e}")
        return

    # Call the function with your live parameters
    result = await tools.search_project_documents(
        project_name="ASTRA",  # Change to your project name
        document_name="database",  # Optional: filter by document name
        include_content=True  # Set to True to include document content
    )
    print("Final result:")
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
