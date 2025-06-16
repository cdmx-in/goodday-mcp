# GoodDay MCP Server

[![PyPI version](https://badge.fury.io/py/goodday-mcp.svg)](https://badge.fury.io/py/goodday-mcp)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Model Context Protocol (MCP) server that integrates with GoodDay work management platform, providing AI assistants with comprehensive project and task management capabilities through GoodDay's API v2.

## 🚀 Features

- **8 comprehensive tools** for complete GoodDay integration
- **Project Management**: List, view, and create projects
- **Task Management**: Create, update, and track tasks
- **User Management**: Assign tasks and track user workloads
- **Natural Language Interface**: Use with Claude Desktop and other MCP clients
- **Async/Await Support**: Efficient API calls with proper error handling
- **Type Safety**: Full type hints for better development experience

## 📦 Installation

### Option 1: Install from PyPI (Recommended)
```bash
pip install goodday-mcp
```

### Option 2: Install with uv
```bash
uv add goodday-mcp
```

### Option 3: From Source
```bash
git clone https://github.com/goodday-mcp/goodday-mcp
cd goodday-mcp
pip install -e .
```

## ⚙️ Configuration

### 1. Get Your GoodDay API Token

1. Go to your GoodDay organization
2. Navigate to **Organization → Settings → API**
3. Click **"Generate"** to create an API token

### 2. Set Environment Variable

```bash
export GOODDAY_API_TOKEN="your-api-token-here"
```

### 3. Configure Your MCP Client

#### Claude Desktop

Add to your `claude_desktop_config.json`:

**Option 1: Using pip installed package**
```json
{
  "mcpServers": {
    "goodday": {
      "command": "goodday-mcp",
      "env": {
        "GOODDAY_API_TOKEN": "your-api-token-here"
      }
    }
  }
}
```

**Option 2: Using uv**
```json
{
  "mcpServers": {
    "goodday": {
      "command": "uv",
      "args": ["run", "goodday-mcp"],
      "env": {
        "GOODDAY_API_TOKEN": "your-api-token-here"
      }
    }
  }
}
```

#### Other MCP Clients

For other MCP clients, run the server directly:

```bash
goodday-mcp
```

## 🛠️ Available Tools

### Project Management
- **`list_projects`** - List all projects with filtering options (archived, root-only)
- **`get_project`** - Get detailed information about a specific project  
- **`create_project`** - Create new projects with full configuration

### Task Management
- **`list_project_tasks`** - List all tasks in a project with filtering
- **`get_task`** - Get detailed information about a specific task
- **`create_task`** - Create new tasks with comprehensive options
- **`update_task_status`** - Update task status with optional comments
- **`get_user_assigned_tasks`** - Get tasks assigned to a specific user

## 💬 Usage Examples

Once configured with your MCP client, you can use natural language commands:

### Project Queries
- *"Show me all my active projects"*
- *"List archived projects only"*
- *"Get details for project ABC123"*

### Task Management
- *"Create a new task called 'Review quarterly reports' in the Marketing project"*
- *"List all tasks in project XYZ456"*
- *"Show me all overdue tasks"*
- *"Update task TASK789 status to completed"*

### User Management
- *"What tasks are assigned to John Doe?"*
- *"Show me all my assigned tasks"*
- *"List tasks that need my attention"*

## 🔧 Development

### Prerequisites

- Python 3.10 or higher
- Valid GoodDay API token
- Internet connection for API access

### Local Development

1. Clone the repository:
   ```bash
   git clone https://github.com/goodday-mcp/goodday-mcp
   cd goodday-mcp
   ```

2. Install with uv (recommended):
   ```bash
   uv sync
   ```

3. Set your API token:
   ```bash
   export GOODDAY_API_TOKEN="your-token"
   ```

4. Run the server:
   ```bash
   uv run goodday-mcp
   ```

### Testing

```bash
# Test the installation
goodday-mcp --help

# Test with your API token
export GOODDAY_API_TOKEN="your-token"
echo '{"jsonrpc": "2.0", "id": 1, "method": "tools/list"}' | goodday-mcp
```

## 📋 API Reference

### Tool Parameters

All tools support the standard MCP protocol. Here are the key parameters:

#### Projects
- `list_projects(archived: bool = False, root_only: bool = False)`
- `get_project(project_id: str)`
- `create_project(name: str, created_by_user_id: str, project_template_id: str, ...)`

#### Tasks
- `list_project_tasks(project_id: str, include_closed: bool = False, include_subfolders: bool = False)`
- `get_task(task_id: str)`
- `create_task(project_id: str, title: str, from_user_id: str, ...)`
- `update_task_status(task_id: str, user_id: str, status_id: str, message: str = None)`
- `get_user_assigned_tasks(user_id: str, include_closed: bool = False)`

## 🛡️ Security

- All API communications use HTTPS
- API tokens are handled securely via environment variables
- No sensitive data is logged or cached
- Comprehensive input validation on all parameters

See [SECURITY.md](SECURITY.md) for more details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Links

- **GoodDay API Documentation**: https://www.goodday.work/developers/api-v2
- **Model Context Protocol**: https://modelcontextprotocol.io/
- **Claude Desktop**: https://claude.ai/download

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/goodday-mcp/goodday-mcp/issues)
- **Documentation**: [README.md](https://github.com/goodday-mcp/goodday-mcp#readme)
- **Changelog**: [CHANGELOG.md](CHANGELOG.md)

---

**Built with ❤️ for the GoodDay and MCP communities**
