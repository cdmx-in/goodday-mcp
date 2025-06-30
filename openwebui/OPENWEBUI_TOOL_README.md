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

### Search & Task Details
- **search_goodday_tasks**: Search for tasks using semantic search with a VectorDB backend
- **get_goodday_task_messages**: Get messages from a specific task by its short ID (e.g., RAD-434) within a project
- **get_goodday_task_details**: Get detailed information about a specific task by its short ID within a project

## Configuration

### API Key Configuration

You can set the Goodday API key dynamically in code using the `Valves` class:

```python
from goodday_openwebui_complete_tool import Tools

tools = Tools()
tools.valves.api_key = "your_goodday_api_token_here"  # Set API key dynamically
tools.valves.search_url = "https://your-server.com/webhook/goodday-mcp/search-tasks"  # Set full search endpoint URL
tools.valves.bearer_token = "your_search_bearer_token"  # Set search bearer token
```

### Available Valves Configuration

- **api_key**: Your Goodday API token (can also use `GOODDAY_API_TOKEN` environment variable)
- **api_base**: Goodday API base URL (default: "https://api.goodday.work/2.0")  
- **search_url**: Full VectorDB Search API endpoint URL (default: "https://tbp-mng.c-dev.in/webhook/goodday-mcp/search-tasks") - **Specify the complete endpoint URL**
- **bearer_token**: Bearer token for search API authentication (can also use `GOODDAY_SEARCH_BEARER_TOKEN` environment variable)

**Note**: If `valves.api_key` is not set, the tool will fall back to the `GOODDAY_API_TOKEN` environment variable. Similarly for `bearer_token` and `GOODDAY_SEARCH_BEARER_TOKEN`.

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

### 6. Search Tasks
```python
result = await tools.search_goodday_tasks(query="security improvements")
```

### 7. Get Task Messages
```python
result = await tools.get_goodday_task_messages(task_short_id="RAD-434", project_name="Astra")
```

### 8. Get Task Details
```python
result = await tools.get_goodday_task_details(task_short_id="RAD-434", project_name="Astra")
```

## Search API Setup

To use the search functionality, you need to configure a VectorDB backend:

1. **Set the full search endpoint URL** in valves:
   ```python
   tools.valves.search_url = "https://tbp-mng.c-dev.in/webhook/goodday-mcp/search-tasks"
   ```

2. **Set the bearer token** for authentication:
   ```python
   tools.valves.bearer_token = "your_bearer_token_here"
   ```
   Or set the environment variable:
   ```bash
   export GOODDAY_SEARCH_BEARER_TOKEN="your_bearer_token_here"
   ```

### Creating the Vector Database with n8n

You can create the VectorDB using the provided n8n workflow. This workflow:

1. **Fetches all projects** from Goodday API
2. **Retrieves tasks** for each project (including subfolders)
3. **Gets task messages** for each task
4. **Chunks the data** into manageable pieces with task context
5. **Creates embeddings** using Ollama (mxbai-embed-large model)
6. **Stores in Qdrant** vector database
7. **Provides search endpoint** for semantic search

**Key Features:**
- Automatically clears and rebuilds the vector database
- Chunks task messages with task ID and name as context
- Provides webhook endpoint for search queries
- Returns structured results with task ID, title, content, and relevance score

**Setup Requirements:**
- n8n instance with Langchain nodes
- Ollama server with mxbai-embed-large model
- Qdrant vector database instance
- Goodday API credentials
- Bearer token for webhook authentication

**Webhook Endpoint:** The workflow creates a webhook at `/goodday-mcp/search-tasks` that accepts:
- Query parameter: `query` (the search term)
- Authentication: Bearer token in header
- Response: JSON array with search results including task ID, title, content, and score

To use the provided workflow, import the JSON workflow into your n8n instance and configure your credentials accordingly.

**Workflow File:** The complete n8n workflow is available in `n8n-workflow-goodday-vectordb.json` in this directory. Import this file into your n8n instance to get started quickly.

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
