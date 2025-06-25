# Goodday Project Management Complete - OpenWebUI Tool

This OpenWebUI tool provides integration with the Goodday project management system through the Goodday MCP server. It allows you to interact with Goodday projects, tasks, sprints, and users directly from the OpenWebUI chat interface.

## Features & Available Functions

### Project Management
- **get_goodday_projects**: Retrieve list of projects (with options for archived and root-only filtering)
- **get_goodday_project_tasks**: Retrieve tasks from a project by project name (case-insensitive, always includes subfolders)

### Sprint Management
- **get_goodday_sprint_tasks**: Get tasks from a specific sprint by project name and sprint name/number (case-insensitive, with option for closed tasks)

### User Management
- **get_goodday_user_tasks**: Get tasks assigned to a user by name or email (case-insensitive, with option for closed tasks)

### Smart Query
- **get_goodday_smart_query**: Smart query function that interprets natural language requests for Goodday data (e.g., "get tasks from sprint 233", "tasks assigned to John Doe").

## API Key Configuration

You can set the Goodday API key dynamically in code using the `Valves` class:

```python
from goodday_openwebui_complete_tool import Tools

tools = Tools()
tools.valves.api_key = "your_goodday_api_token_here"  # Set API key dynamically
```

If `valves.api_key` is not set, the tool will fall back to the `GOODDAY_API_TOKEN` environment variable.

## Usage Examples

### 1. Get All Projects
```python
result = await tools.get_goodday_projects()
```

### 2. Get Project Tasks by Name
```python
result = await tools.get_goodday_project_tasks(project_name="Astra")
```

### 3. Get Sprint Tasks
```python
result = await tools.get_goodday_sprint_tasks(project_name="Astra", sprint_name="Sprint 120")
```

### 4. Get User Tasks by Name or Email
```python
result = await tools.get_goodday_user_tasks(user="Roney Dsilva")
# or
result = await tools.get_goodday_user_tasks(user="roney@email.com")
```

### 5. Smart Query
```python
result = await tools.get_goodday_smart_query(query="get tasks from sprint 233 in Astra project")
```

## Error Handling

The tool provides informative error messages if:
- The MCP server connection fails
- API authentication fails
- Invalid parameters are provided
- Network issues occur

## Security

- API tokens are passed securely through values
- All API calls are made through the MCP server, which handles authentication
- No sensitive data is logged or exposed in error messages

## Support

For issues related to:
- **Goodday MCP Server**: Visit [goodday-mcp repository](https://github.com/cdmx1/goodday-mcp)
- **OpenWebUI**: Visit [OpenWebUI documentation](https://docs.openwebui.com/)
- **Goodday API**: Contact Goodday support or check their API documentation

## License

This tool follows the same license as the Goodday MCP server project.
