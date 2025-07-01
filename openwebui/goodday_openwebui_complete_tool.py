"""
title: Goodday Project Management
author: Roney Dsilva
author_url: https://github.com/cdmx1/goodday-mcp
funding_url: https://github.com/cdmx1/goodday-mcp
version: 1.1.0
required_open_webui_version: 0.5.3
"""

import os
import httpx
from typing import Callable
from fastapi import Request
from pydantic import BaseModel, Field


class Tools:
    class Valves(BaseModel):
        api_key: str = Field("", description="Your Goodday API key")
        api_base: str = Field("https://api.goodday.work/2.0", description="Goodday API base URL")
        search_url: str = Field("https://example.com/webhook/goodday-mcp/search-tasks", description="Full VectorDB Search API endpoint URL")
        bearer_token: str = Field("", description="Bearer token for search API authentication")

    def __init__(self):
        self.valves = self.Valves()
        self.user_agent = "goodday-openwebui-complete/1.1.0"

    async def _make_goodday_request(self, endpoint: str, method: str = "GET", data: dict = None) -> dict:
        """Make a direct request to the Goodday API."""
        api_token = self.valves.api_key or os.getenv("GOODDAY_API_TOKEN", "")
        if not api_token:
            raise ValueError("GOODDAY_API_TOKEN environment variable or Valves.api_key is required")
        
        headers = {
            "User-Agent": self.user_agent,
            "gd-api-token": api_token,
            "Content-Type": "application/json"
        }
        
        url = f"{self.valves.api_base}/{endpoint.lstrip('/')}"
        
        async with httpx.AsyncClient() as client:
            try:
                if method.upper() == "POST":
                    response = await client.post(url, headers=headers, json=data, timeout=30.0)
                elif method.upper() == "PUT":
                    response = await client.put(url, headers=headers, json=data, timeout=30.0)
                elif method.upper() == "DELETE":
                    response = await client.delete(url, headers=headers, timeout=30.0)
                else:
                    response = await client.get(url, headers=headers, timeout=30.0)

                response.raise_for_status()
                return response.json()

            except httpx.HTTPStatusError as e:
                raise Exception(f"HTTP error {e.response.status_code}: {e.response.text}")
            except httpx.RequestError as e:
                raise Exception(f"Request error: {str(e)}")
            except Exception as e:
                raise Exception(f"Unexpected error: {str(e)}")

    async def _make_search_request(self, method: str = "GET", params: dict = None) -> dict:
        """Make a request to the search API with bearer token authentication."""
        bearer_token = self.valves.bearer_token or os.getenv("GOODDAY_SEARCH_BEARER_TOKEN", "")
        if not bearer_token:
            raise ValueError("Bearer token is required for search API. Set it in Valves.bearer_token or GOODDAY_SEARCH_BEARER_TOKEN environment variable")
        
        headers = {
            "User-Agent": self.user_agent,
            "Authorization": f"Bearer {bearer_token}",
            "Content-Type": "application/json"
        }
        
        # Use the full URL directly from search_url
        url = str(self.valves.search_url).strip()
        
        async with httpx.AsyncClient() as client:
            try:
                if method.upper() == "GET":
                    response = await client.get(url, headers=headers, params=params, timeout=30.0)
                else:
                    response = await client.request(method.upper(), url, headers=headers, params=params, timeout=30.0)

                response.raise_for_status()
                return response.json()

            except httpx.HTTPStatusError as e:
                raise Exception(f"Search API HTTP error {e.response.status_code}: {e.response.text}")
            except httpx.RequestError as e:
                raise Exception(f"Search API request error: {str(e)}")
            except Exception as e:
                raise Exception(f"Search API unexpected error: {str(e)}")

    def _format_task(self, task: dict) -> str:
        """Format a task into a readable string with safe checks."""
        if not isinstance(task, dict):
            return f"Invalid task data: {repr(task)}"

        # Defensive defaults in case nested keys are not dicts
        status = task.get('status') if isinstance(task.get('status'), dict) else {}
        project = task.get('project') if isinstance(task.get('project'), dict) else {}
        
        return f"""
**Task ID:** {task.get('shortId', 'N/A')}
**Title:** {task.get('name', 'N/A')}
**Status:** {status.get('name', 'N/A')}
**Project:** {project.get('name', 'N/A')}
**Assigned To:** {task.get('assignedToUserId', 'N/A')}
**Priority:** {task.get('priority', 'N/A')}
**Start Date:** {task.get('startDate', 'N/A')}
**End Date:** {task.get('endDate', 'N/A')}
**Description:** {task.get('message', 'No description')}
""".strip()

    def _format_project(self, project: dict) -> str:
        """Format a project into a readable string with safe checks."""
        if not isinstance(project, dict):
            return f"Invalid project data: {repr(project)}"

        # Defensive defaults in case nested keys are not dicts
        status = project.get('status') if isinstance(project.get('status'), dict) else {}
        owner = project.get('owner') if isinstance(project.get('owner'), dict) else {}

        return f"""
**Project ID:** {project.get('id', 'N/A')}
**Name:** {project.get('name', 'N/A')}
**Health:** {project.get('health', 'N/A')}
**Status:** {status.get('name', 'N/A')}
**Start Date:** {project.get('startDate', 'N/A')}
**End Date:** {project.get('endDate', 'N/A')}
**Progress:** {project.get('progress', 0)}%
**Owner:** {owner.get('name', 'N/A')}
""".strip()

    def _format_user(self, user: dict) -> str:
        """Format a user into a readable string with safe checks."""
        if not isinstance(user, dict):
            return f"Invalid user data: {repr(user)}"

        # Defensive defaults in case nested keys are not dicts
        role = user.get('role') if isinstance(user.get('role'), dict) else {}

        return f"""
**User ID:** {user.get('id', 'N/A')}
**Name:** {user.get('name', 'N/A')}
**Email:** {user.get('email', 'N/A')}
**Role:** {role.get('name', 'N/A')}
**Status:** {user.get('status', 'N/A')}
""".strip()

    def _format_search_result(self, result: dict) -> str:
        """Format a search result into a readable string with safe checks."""
        if not isinstance(result, dict):
            return f"Invalid search result data: {repr(result)}"

        # Safely get values and handle None cases
        task_id = result.get('taskId') or 'N/A'
        title = result.get('title') or 'N/A'
        content = result.get('content') or 'No content'

        return f"""
**Task ID:** {task_id}
**Title:** {title}
**Content:** {content}
""".strip()

    # Project Management Tools
    async def get_goodday_projects(
        self, 
        archived: bool = True,  # Always True
        root_only: bool = False,
        __request__: Request = None, 
        __user__: dict = None, 
        __event_emitter__: Callable = None
    ) -> str:
        """
        Get list of projects from Goodday project management system

        :param archived: Set to true to retrieve archived/closed projects
        :param root_only: Set to true to return only root projects
        """
        archived = True  # Force always true
        if __event_emitter__:
            await __event_emitter__({
                "type": "status",
                "data": {"description": "Fetching Goodday projects...", "done": False},
            })

        try:
            params = []
            if archived:
                params.append("archived=true")
            if root_only:
                params.append("rootOnly=true")
            
            endpoint = "projects"
            if params:
                endpoint += "?" + "&".join(params)
            
            data = await self._make_goodday_request(endpoint)
            
            if not data:
                return "No projects found."
                
            if isinstance(data, dict):
                if "error" in data:
                    return f"Unable to fetch projects: {data.get('error', 'Unknown error')}"
            elif not isinstance(data, list):
                return f"Unexpected response format: {type(data).__name__} - {str(data)}"
            
            projects = [self._format_project(project) for project in data]
            result = "\n---\n".join(projects)

            if __event_emitter__:
                await __event_emitter__({
                    "type": "status",
                    "data": {"description": "Successfully retrieved projects", "done": True},
                })

            return f"**Goodday Projects:**\n\n{result}"

        except Exception as e:
            error_msg = f"Failed to retrieve projects: {str(e)}"
            if __event_emitter__:
                await __event_emitter__({
                    "type": "status",
                    "data": {"description": error_msg, "done": True},
                })
            return error_msg

    # Task Management Tools
    async def get_goodday_project_tasks(
        self, 
        project_name: str,
        __request__: Request = None, 
        __user__: dict = None, 
        __event_emitter__: Callable = None
    ) -> str:
        """
        Get tasks from a specific Goodday project by project name (case-insensitive)

        :param project_name: The name of the project (required, case-insensitive)
        """
        if __event_emitter__:
            await __event_emitter__({
                "type": "status",
                "data": {"description": f"Finding project '{project_name}'...", "done": False},
            })

        try:
            # Get all projects and find the one matching project_name (case-insensitive)
            projects_data = await self._make_goodday_request("projects")
            if not projects_data or not isinstance(projects_data, list):
                return "Unable to fetch projects."
            project_name_lower = project_name.lower().strip()
            matched_project = None
            for proj in projects_data:
                if not isinstance(proj, dict):
                    continue
                current_project_name = proj.get('name', '').lower().strip()
                if current_project_name == project_name_lower:
                    matched_project = proj
                    break
                if project_name_lower in current_project_name or current_project_name in project_name_lower:
                    matched_project = proj
                    break
            if not matched_project:
                available_projects = [p.get('name', 'Unknown') for p in projects_data if isinstance(p, dict)]
                return f"Project '{project_name}' not found. Available projects: {', '.join(available_projects[:10])}{'...' if len(available_projects) > 10 else ''}"
            project_id = matched_project.get('id')
            actual_project_name = matched_project.get('name')

            if __event_emitter__:
                await __event_emitter__({
                    "type": "status",
                    "data": {"description": f"Fetching tasks for project '{actual_project_name}' (ID: {project_id})...", "done": False},
                })

            params = []
            params.append("subfolders=true")  # Always include subfolders
            endpoint = f"project/{project_id}/tasks"
            if params:
                endpoint += "?" + "&".join(params)
            data = await self._make_goodday_request(endpoint)
            if not data:
                return f"No tasks found in project '{actual_project_name}'."
            if isinstance(data, dict) and "error" in data:
                return f"Unable to fetch tasks: {data.get('error', 'Unknown error')}"
            if not isinstance(data, list):
                return f"Unexpected response format: {str(data)}"
            tasks = [self._format_task(task) for task in data]
            result = "\n---\n".join(tasks)

            if __event_emitter__:
                await __event_emitter__({
                    "type": "status",
                    "data": {"description": f"Successfully retrieved project tasks for '{actual_project_name}'", "done": True},
                })

            return f"**Project '{actual_project_name}' Tasks:**\n\n{result}"

        except Exception as e:
            error_msg = f"Failed to retrieve project tasks: {str(e)}"
            if __event_emitter__:
                await __event_emitter__({
                    "type": "status",
                    "data": {"description": error_msg, "done": True},
                })
            return error_msg

    async def get_goodday_sprint_tasks(
        self, 
        project_name: str,
        sprint_name: str,
        closed: bool = True,  # Always True
        __request__: Request = None, 
        __user__: dict = None, 
        __event_emitter__: Callable = None
    ) -> str:
        """
        Get tasks from a specific sprint by project name and sprint name

        :param project_name: The name of the project (e.g., "ASTRA", "Astra")
        :param sprint_name: The name of the sprint (e.g., "Sprint 233", "233")
        :param closed: Set to true to retrieve all open and closed tasks
        """
        closed = True  # Force always true
        if __event_emitter__:
            await __event_emitter__({
                "type": "status",
                "data": {"description": f"Finding project '{project_name}' and sprint '{sprint_name}'...", "done": False},
            })

        def _find_main_project(projects_data, project_name):
            project_name_lower = project_name.lower().strip()
            for proj in projects_data:
                if not isinstance(proj, dict):
                    continue
                current_project_name = proj.get('name', '').lower().strip()
                if current_project_name == project_name_lower:
                    return proj
                if project_name_lower in current_project_name or current_project_name in project_name_lower:
                    return proj
            return None

        def _find_sprint_project(projects_data, _unused_parent_project_id, sprint_name):
            import re
            normalized_sprint_name = sprint_name.lower().strip()
            if not normalized_sprint_name.startswith("sprint"):
                normalized_sprint_name = f"sprint {normalized_sprint_name}"
            available_sprints = []
            search_number = re.search(r'(\d+)', normalized_sprint_name)
            exact_match = None
            substring_match = None
            for proj in projects_data:
                if (isinstance(proj, dict) and 
                    proj.get('systemType') == 'PROJECT'):
                    sprint_proj_name = proj.get('name', '').lower().strip()
                    if sprint_proj_name.startswith('sprint'):
                        available_sprints.append(proj.get('name', ''))
                        project_number = re.search(r'(\d+)', sprint_proj_name)
                        # Prefer exact number match
                        if search_number and project_number and search_number.group(1) == project_number.group(1):
                            exact_match = proj
                        # Fallback: search number as substring anywhere in the sprint name
                        elif search_number and search_number.group(1) in sprint_proj_name:
                            if not substring_match:
                                substring_match = proj
                        elif normalized_sprint_name == sprint_proj_name:
                            if not exact_match:
                                exact_match = proj
                        elif normalized_sprint_name in sprint_proj_name or sprint_proj_name in normalized_sprint_name:
                            if not substring_match:
                                substring_match = proj
            if exact_match:
                return exact_match, available_sprints
            if substring_match:
                return substring_match, available_sprints
            return None, available_sprints

        try:
            # Get all projects to find the main project
            projects_data = await self._make_goodday_request("projects")
            if not projects_data or not isinstance(projects_data, list):
                return "Unable to fetch projects."
            main_project = _find_main_project(projects_data, project_name)
            if not main_project:
                available_projects = [p.get('name', 'Unknown') for p in projects_data if isinstance(p, dict)]
                return f"Project '{project_name}' not found. Available projects: {', '.join(available_projects[:10])}{'...' if len(available_projects) > 10 else ''}"
            project_id = main_project.get('id')
            actual_project_name = main_project.get('name')

            # Print all sprint projects under the main project
            sprint_projects = [
                p for p in projects_data
                if isinstance(p, dict)
                and p.get('name', '').lower().startswith('sprint')
                and p.get('parentProjectId') == project_id
            ]
            if sprint_projects:
                sprint_list = '\n'.join([
                    f"- {p.get('name', 'Unknown')} (ID: {p.get('id', 'N/A')})" for p in sprint_projects
                ])
                if __event_emitter__:
                    await __event_emitter__({
                        "type": "status",
                        "data": {"description": f"Sprints under project '{actual_project_name}':\n{sprint_list}", "done": False},
                    })
            else:
                if __event_emitter__:
                    await __event_emitter__({
                        "type": "status",
                        "data": {"description": f"No sprints found under project '{actual_project_name}'.", "done": False},
                    })

            # Get all projects again to find the sprint
            projects_data = await self._make_goodday_request("projects")
            if not projects_data or not isinstance(projects_data, list):
                return "Unable to fetch projects to find sprint."
            sprint_project, available_sprints = _find_sprint_project(projects_data, project_id, sprint_name)
            if not sprint_project:
                if available_sprints:
                    return f"Sprint '{sprint_name}' not found in project {project_id}. Available sprints: {', '.join(available_sprints)}"
                else:
                    return f"No sprints found in project {project_id}. Make sure the project ID is correct and contains sprint sub-projects."
            sprint_id = sprint_project.get('id')
            actual_sprint_name = sprint_project.get('name')

            if __event_emitter__:
                await __event_emitter__({
                    "type": "status",
                    "data": {"description": f"Found sprint '{actual_sprint_name}', fetching tasks...", "done": False},
                })

            params = []
            if closed:
                params.append("closed=true")
            params.append("subfolders=true")
            endpoint = f"project/{sprint_id}/tasks"
            if params:
                endpoint += "?" + "&".join(params)
            data = await self._make_goodday_request(endpoint)
            if not data:
                return f"No tasks found in sprint '{actual_sprint_name}'."
            if isinstance(data, dict) and "error" in data:
                return f"Unable to fetch sprint tasks: {data.get('error', 'Unknown error')}"
            if not isinstance(data, list):
                return f"Unexpected response format: {str(data)}"
            if len(data) == 0:
                return f"Sprint '{actual_sprint_name}' exists but contains no tasks."
            tasks = [self._format_task(task) for task in data]
            result = "\n---\n".join(tasks)
            if __event_emitter__:
                await __event_emitter__({
                    "type": "status",
                    "data": {"description": f"Successfully retrieved {len(data)} tasks from sprint '{actual_sprint_name}'", "done": True},
                })
            return f"**Sprint '{actual_sprint_name}' Tasks ({len(data)} tasks):**\n\n{result}"

        except Exception as e:
            error_msg = f"Failed to retrieve sprint tasks: {str(e)}"
            if __event_emitter__:
                await __event_emitter__({
                    "type": "status",
                    "data": {"description": error_msg, "done": True},
                })
            return error_msg

    async def get_goodday_smart_query(
        self, 
        query: str,
        __request__: Request = None, 
        __user__: dict = None, 
        __event_emitter__: Callable = None
    ) -> str:
        """
        Smart query function that interprets natural language requests for Goodday data

        :param query: Natural language query (e.g., "get tasks from sprint 233", "tasks assigned to Roney Dsilva", "Sprint 102 tasks from ASTRA project")
        """
        if __event_emitter__:
            await __event_emitter__({
                "type": "status",
                "data": {"description": f"Processing query: '{query}'...", "done": False},
            })

        try:
            query_lower = query.lower().strip()
            
            # Pattern: "get tasks in sprint X in PROJECT" or "sprint X tasks from PROJECT"
            if "sprint" in query_lower and ("tasks" in query_lower or "task" in query_lower):
                # Extract sprint number/name and project name
                import re
                
                # More flexible regex patterns
                sprint_patterns = [
                    r'sprint\s+(\w+)',
                    r'spring\s+(\w+)',  # Handle typos like "spring" instead of "sprint"
                ]
                
                project_patterns = [
                    r'(?:from|in|project)\s+(\w+)',
                    r'(\w+)\s+project',
                ]
                
                sprint_name = None
                project_name = None
                
                # Try to find sprint name
                for pattern in sprint_patterns:
                    sprint_match = re.search(pattern, query_lower)
                    if sprint_match:
                        sprint_name = sprint_match.group(1)
                        break
                
                # Try to find project name
                for pattern in project_patterns:
                    project_match = re.search(pattern, query_lower)
                    if project_match:
                        project_name = project_match.group(1)
                        break
                
                if sprint_name:
                    if project_name:
                        return await self.get_goodday_sprint_tasks(
                            project_name=project_name,
                            sprint_name=sprint_name,
                            __request__=__request__,
                            __user__=__user__,
                            __event_emitter__=__event_emitter__
                        )
                    return f"Please specify the project name. Example: 'get tasks from sprint {sprint_name} in ASTRA project'"
            
            # Pattern: "tasks assigned to USER" or "USER tasks"
            if ("assigned to" in query_lower or "tasks for" in query_lower) and "task" in query_lower:
                # Extract user name or email
                if "assigned to" in query_lower:
                    user_part = query_lower.split("assigned to")[1].strip()
                elif "tasks for" in query_lower:
                    user_part = query_lower.split("tasks for")[1].strip()
                else:
                    user_part = ""
                user_value = user_part.replace("user", "").replace("tasks", "").strip()
                if user_value:
                    return await self.get_goodday_user_tasks(
                        user=user_value,
                        __request__=__request__,
                        __user__=__user__,
                        __event_emitter__=__event_emitter__
                    )
            # Pattern: "get messages from TASK-ID" or "messages for TASK-ID"
            if ("message" in query_lower or "messages" in query_lower) and ("from" in query_lower or "for" in query_lower):
                # Extract task ID and project name
                import re
                task_id_pattern = r'(?:from|for)\s+([A-Z]+-\d+)'
                task_match = re.search(task_id_pattern, query_lower)
                
                # Try to extract project name
                project_patterns = [
                    r'(?:from|in|project)\s+(\w+)',
                    r'(\w+)\s+project',
                ]
                project_name = None
                for pattern in project_patterns:
                    project_match = re.search(pattern, query_lower)
                    if project_match:
                        project_name = project_match.group(1)
                        break
                
                if task_match:
                    task_short_id = task_match.group(1).upper()
                    if project_name:
                        return await self.get_goodday_task_messages(
                            task_short_id=task_short_id,
                            project_name=project_name,
                            __request__=__request__,
                            __user__=__user__,
                            __event_emitter__=__event_emitter__
                        )
                    else:
                        return f"Please specify the project name. Example: 'get messages from {task_short_id} in ASTRA project'"

            # Pattern: "get task TASK-ID" or "task details for TASK-ID" or "details for TASK-ID"
            if (("task" in query_lower and "detail" in query_lower) or 
                ("details" in query_lower and ("for" in query_lower or "of" in query_lower)) or
                ("get task" in query_lower)) and not ("tasks" in query_lower or "message" in query_lower):
                # Extract task ID and project name
                import re
                task_id_patterns = [
                    r'(?:task|for|of)\s+([A-Z]+-\d+)',
                    r'([A-Z]+-\d+)',  # Just the task ID pattern
                ]
                
                # Try to extract project name
                project_patterns = [
                    r'(?:from|in|project)\s+(\w+)',
                    r'(\w+)\s+project',
                ]
                project_name = None
                for pattern in project_patterns:
                    project_match = re.search(pattern, query_lower)
                    if project_match:
                        project_name = project_match.group(1)
                        break
                
                task_short_id = None
                for pattern in task_id_patterns:
                    task_match = re.search(pattern, query_lower)
                    if task_match:
                        task_short_id = task_match.group(1).upper()
                        break
                
                if task_short_id:
                    if project_name:
                        return await self.get_goodday_task_details(
                            task_short_id=task_short_id,
                            project_name=project_name,
                            __request__=__request__,
                            __user__=__user__,
                            __event_emitter__=__event_emitter__
                        )
                    else:
                        return f"Please specify the project name. Example: 'get task {task_short_id} in ASTRA project'"

            # Pattern: "USER tasks" (e.g., "Roney Dsilva tasks")
            if "task" in query_lower and not any(keyword in query_lower for keyword in ["sprint", "spring", "project", "assigned", "message", "detail"]):
                user_value = query_lower.replace("tasks", "").replace("task", "").replace("get", "").strip()
                if user_value:
                    return await self.get_goodday_user_tasks(
                        user=user_value,
                        __request__=__request__,
                        __user__=__user__,
                        __event_emitter__=__event_emitter__
                    )
            # Pattern: "search for QUERY" or "find tasks QUERY"
            if ("search" in query_lower or "find" in query_lower) and "task" in query_lower:
                # Extract search query
                search_terms = query_lower
                # Remove common words
                for word in ["search", "for", "find", "tasks", "task", "get"]:
                    search_terms = search_terms.replace(word, "").strip()
                
                if search_terms:
                    return await self.search_goodday_tasks(
                        query=search_terms,
                        __request__=__request__,
                        __user__=__user__,
                        __event_emitter__=__event_emitter__
                    )

            # If no pattern matches, provide suggestions
            return """I couldn't understand your query. Here are some examples of what I can help with:

**Search Tasks:**
- "search for Security tasks"
- "find tasks S3 upload"
- "search tasks security improvements"

**Sprint Tasks:**
- "get tasks from sprint 233 in ASTRA project"
- "get tasks in sprint 122 in Astra project"
- "sprint 102 tasks from PROJECT_NAME"
- "tasks from sprint 233"

**User Tasks:**
- "tasks assigned to Roney Dsilva"
- "Roney Dsilva tasks"
- "tasks for John Smith"

**Task Messages:**
- "get messages from RAD-434 in ASTRA project"
- "messages for ABC-123 in PROJECT_NAME"
- "get all messages from TASK-456 in Astra"

**Task Details:**
- "get task RAD-434 in ASTRA project"
- "task details for ABC-123 in PROJECT_NAME" 
- "details for TASK-456 in Astra"
- "get details of RAD-434 in ASTRA"

**Other Options:**
- Use specific function names like `get_goodday_projects()` for projects
- Use `get_goodday_users()` to see available users
- Use `get_goodday_project_tasks()` for project tasks
- Use `search_goodday_tasks()` for semantic search

Please try rephrasing your query with one of these patterns."""

        except Exception as e:
            error_msg = f"Failed to process query: {str(e)}"
            if __event_emitter__:
                await __event_emitter__({
                    "type": "status",
                    "data": {"description": error_msg, "done": True},
                })
            return error_msg

    async def get_goodday_user_tasks(
        self,
        user: str,
        closed: bool = True,  # Always True
        __request__: Request = None,
        __user__: dict = None,
        __event_emitter__: Callable = None
    ) -> str:
        """
        Get tasks assigned to a user by name or email (case-insensitive).
        :param user: User name or email (case-insensitive)
        :param closed: Set to true to retrieve all open and closed tasks
        """
        closed = True  # Force always true
        if __event_emitter__:
            await __event_emitter__({
                "type": "status",
                "data": {"description": f"Finding user '{user}'...", "done": False},
            })
        try:
            users_data = await self._make_goodday_request("users")
            if not users_data or not isinstance(users_data, list):
                return "Unable to fetch users."
            user_lower = user.lower().strip()
            matched_user = None
            for u in users_data:
                if not isinstance(u, dict):
                    continue
                name = u.get('name', '').lower().strip()
                email = u.get('email', '').lower().strip()
                if user_lower == name or user_lower == email:
                    matched_user = u
                    break
                if user_lower in name or user_lower in email:
                    matched_user = u
                    break
            if not matched_user:
                available_users = [u.get('name', 'Unknown') for u in users_data if isinstance(u, dict)]
                return f"User '{user}' not found. Available users: {', '.join(available_users[:10])}{'...' if len(available_users) > 10 else ''}"
            user_id = matched_user.get('id')
            actual_user_name = matched_user.get('name')
            if __event_emitter__:
                await __event_emitter__({
                    "type": "status",
                    "data": {"description": f"Fetching tasks assigned to '{actual_user_name}' (ID: {user_id})...", "done": False},
                })
            params = []
            if closed:
                params.append("closed=true")
            endpoint = f"user/{user_id}/assigned-tasks"
            if params:
                endpoint += "?" + "&".join(params)
            data = await self._make_goodday_request(endpoint)
            if not data:
                return f"No tasks found assigned to '{actual_user_name}'."
            if isinstance(data, dict) and "error" in data:
                return f"Unable to fetch user tasks: {data.get('error', 'Unknown error')}"
            if not isinstance(data, list):
                return f"Unexpected response format: {str(data)}"
            tasks = [self._format_task(task) for task in data]
            result = "\n---\n".join(tasks)
            if __event_emitter__:
                await __event_emitter__({
                    "type": "status",
                    "data": {"description": f"Successfully retrieved tasks for '{actual_user_name}'", "done": True},
                })
            return f"**Tasks assigned to '{actual_user_name}':**\n\n{result}"
        except Exception as e:
            error_msg = f"Failed to retrieve user tasks: {str(e)}"
            if __event_emitter__:
                await __event_emitter__({
                    "type": "status",
                    "data": {"description": error_msg, "done": True},
                })
            return error_msg

    async def get_goodday_task_messages(
        self,
        task_short_id: str,
        project_name: str,
        __request__: Request = None,
        __user__: dict = None,
        __event_emitter__: Callable = None
    ) -> str:
        """
        Get messages from a specific task by its short ID (e.g., RAD-434) within a specified project.

        :param task_short_id: The short ID of the task (e.g., RAD-434)
        :param project_name: The name of the project containing the task (required, case-insensitive)
        """
        if __event_emitter__:
            await __event_emitter__({
                "type": "status",
                "data": {"description": f"Finding project '{project_name}'...", "done": False},
            })

        try:
            # Get all projects and find the one matching project_name (case-insensitive)
            projects_data = await self._make_goodday_request("projects")
            if not projects_data or not isinstance(projects_data, list):
                return "Unable to fetch projects to search for task."
            project_name_lower = project_name.lower().strip()
            matched_project = None
            for proj in projects_data:
                if not isinstance(proj, dict):
                    continue
                current_project_name = proj.get('name', '').lower().strip()
                if current_project_name == project_name_lower:
                    matched_project = proj
                    break
                if project_name_lower in current_project_name or current_project_name in project_name_lower:
                    matched_project = proj
                    break
            if not matched_project:
                available_projects = [p.get('name', 'Unknown') for p in projects_data if isinstance(p, dict)]
                return f"Project '{project_name}' not found. Available projects: {', '.join(available_projects[:10])}{'...' if len(available_projects) > 10 else ''}"
            project_id = matched_project.get('id')
            found_in_project = matched_project.get('name')

            if __event_emitter__:
                await __event_emitter__({
                    "type": "status",
                    "data": {"description": f"Searching for task '{task_short_id}' in project '{found_in_project}'...", "done": False},
                })

            # Search for the task in the specified project
            endpoint = f"project/{project_id}/tasks?subfolders=true"
            tasks_data = await self._make_goodday_request(endpoint)
            if not tasks_data or not isinstance(tasks_data, list):
                return f"Unable to fetch tasks for project '{found_in_project}'."
            task_id = None
            task_name = None
            for task in tasks_data:
                if isinstance(task, dict) and task.get('shortId') == task_short_id:
                    task_id = task.get('id')
                    task_name = task.get('name')
                    break
            if not task_id:
                return f"Task with short ID '{task_short_id}' not found in project '{found_in_project}'. Please verify the task ID and project name are correct."

            if __event_emitter__:
                await __event_emitter__({
                    "type": "status",
                    "data": {"description": f"Found task '{task_name}' in project '{found_in_project}', fetching messages...", "done": False},
                })

            # Now get the messages for this task
            endpoint = f"task/{task_id}/messages"
            messages_data = await self._make_goodday_request(endpoint)

            if not messages_data:
                return f"No messages found for task '{task_short_id}' ({task_name})."

            if isinstance(messages_data, dict) and "error" in messages_data:
                return f"Unable to fetch task messages: {messages_data.get('error', 'Unknown error')}"

            if not isinstance(messages_data, list):
                return f"Unexpected response format: {str(messages_data)}"

            if len(messages_data) == 0:
                return f"Task '{task_short_id}' ({task_name}) has no messages."

            # Get all users for name lookup
            users_data = await self._make_goodday_request("users")
            user_id_to_name = {}
            if isinstance(users_data, list):
                for u in users_data:
                    if isinstance(u, dict):
                        user_id_to_name[u.get("id")] = u.get("name", "Unknown")

            def user_display(user_id):
                if not user_id:
                    return "N/A"
                name = user_id_to_name.get(user_id)
                return f"{name} ({user_id})" if name else user_id

            # Format the messages
            formatted_messages = []
            for msg in messages_data:
                if not isinstance(msg, dict):
                    continue

                formatted_msg = f"""
**Message ID:** {msg.get('id', 'N/A')}
**Date Created:** {msg.get('dateCreated', 'N/A')}
**From User:** {user_display(msg.get('fromUserId'))}
**To User:** {user_display(msg.get('toUserId'))}
**Message:** {msg.get('message', 'No message content')}
**Task Status ID:** {msg.get('taskStatusId', 'N/A')}
**Time Report ID:** {msg.get('timeReportId', 'N/A')}
**Edit By User:** {user_display(msg.get('editByUserId'))}
**Edit Date:** {msg.get('editDate', 'N/A')}
""".strip()
                formatted_messages.append(formatted_msg)

            result = "\n---\n".join(formatted_messages)

            if __event_emitter__:
                await __event_emitter__({
                    "type": "status",
                    "data": {"description": f"Successfully retrieved {len(messages_data)} messages for task '{task_short_id}'", "done": True},
                })

            return f"**Messages for Task '{task_short_id}' ({task_name}) in project '{found_in_project}' - {len(messages_data)} messages:**\n\n{result}"

        except Exception as e:
            error_msg = f"Failed to retrieve task messages: {str(e)}"
            if __event_emitter__:
                await __event_emitter__({
                    "type": "status",
                    "data": {"description": error_msg, "done": True},
                })
            return error_msg

    async def get_goodday_task_details(
        self,
        task_short_id: str,
        project_name: str,
        __request__: Request = None,
        __user__: dict = None,
        __event_emitter__: Callable = None
    ) -> str:
        """
        Get detailed information about a specific task by its short ID (e.g., RAD-434) within a specified project.

        :param task_short_id: The short ID of the task (e.g., RAD-434)
        :param project_name: The name of the project containing the task (required, case-insensitive)
        """
        if __event_emitter__:
            await __event_emitter__({
                "type": "status",
                "data": {"description": f"Finding project '{project_name}'...", "done": False},
            })

        try:
            # Get all projects and find the one matching project_name (case-insensitive)
            projects_data = await self._make_goodday_request("projects")
            if not projects_data or not isinstance(projects_data, list):
                return "Unable to fetch projects to search for task."
            project_name_lower = project_name.lower().strip()
            matched_project = None
            for proj in projects_data:
                if not isinstance(proj, dict):
                    continue
                current_project_name = proj.get('name', '').lower().strip()
                if current_project_name == project_name_lower:
                    matched_project = proj
                    break
                if project_name_lower in current_project_name or current_project_name in project_name_lower:
                    matched_project = proj
                    break
            if not matched_project:
                available_projects = [p.get('name', 'Unknown') for p in projects_data if isinstance(p, dict)]
                return f"Project '{project_name}' not found. Available projects: {', '.join(available_projects[:10])}{'...' if len(available_projects) > 10 else ''}"
            project_id = matched_project.get('id')
            found_in_project = matched_project.get('name')

            if __event_emitter__:
                await __event_emitter__({
                    "type": "status",
                    "data": {"description": f"Searching for task '{task_short_id}' in project '{found_in_project}'...", "done": False},
                })

            # Search for the task in the specified project
            endpoint = f"project/{project_id}/tasks?subfolders=true"
            tasks_data = await self._make_goodday_request(endpoint)
            if not tasks_data or not isinstance(tasks_data, list):
                return f"Unable to fetch tasks for project '{found_in_project}'."
            task_id = None
            for task in tasks_data:
                if isinstance(task, dict) and task.get('shortId') == task_short_id:
                    task_id = task.get('id')
                    break
            if not task_id:
                return f"Task with short ID '{task_short_id}' not found in project '{found_in_project}'. Please verify the task ID and project name are correct."

            if __event_emitter__:
                await __event_emitter__({
                    "type": "status",
                    "data": {"description": f"Found task in project '{found_in_project}', fetching detailed information...", "done": False},
                })

            # Now get the detailed task information
            endpoint = f"task/{task_id}"
            task_data = await self._make_goodday_request(endpoint)

            if not task_data:
                return f"No details found for task '{task_short_id}'."

            if isinstance(task_data, dict) and "error" in task_data:
                return f"Unable to fetch task details: {task_data.get('error', 'Unknown error')}"

            if not isinstance(task_data, dict):
                return f"Unexpected response format: {str(task_data)}"

            # Get all users for name lookup
            users_data = await self._make_goodday_request("users")
            user_id_to_name = {}
            if isinstance(users_data, list):
                for u in users_data:
                    if isinstance(u, dict):
                        user_id_to_name[u.get("id")] = u.get("name", "Unknown")

            def user_display(user_id):
                if not user_id:
                    return "N/A"
                name = user_id_to_name.get(user_id)
                return f"{name} ({user_id})" if name else user_id

            # Format the task details
            status = task_data.get('status', {}) if isinstance(task_data.get('status'), dict) else {}
            task_type = task_data.get('taskType', {}) if isinstance(task_data.get('taskType'), dict) else {}
            custom_fields = task_data.get('customFieldsData', {}) if isinstance(task_data.get('customFieldsData'), dict) else {}
            subtasks = task_data.get('subtasks', []) if isinstance(task_data.get('subtasks'), list) else []
            users = task_data.get('users', []) if isinstance(task_data.get('users'), list) else []

            formatted_details = f"""
**Task ID:** {task_data.get('shortId', 'N/A')}
**Name:** {task_data.get('name', 'N/A')}
**Project:** {found_in_project}
**Status:** {status.get('name', 'N/A')})
**Task Type:** {task_type.get('name', 'N/A')})
**System Status:** {task_data.get('systemStatus', 'N/A')}
**System Type:** {task_data.get('systemType', 'N/A')}
**Priority:** {task_data.get('priority', 'N/A')}
**Assigned To:** {user_display(task_data.get('assignedToUserId'))}
**Action Required:** {user_display(task_data.get('actionRequiredUserId'))}
**Created By:** {user_display(task_data.get('createdByUserId'))}
**Start Date:** {task_data.get('startDate', 'N/A')}
**End Date:** {task_data.get('endDate', 'N/A')}
**Deadline:** {task_data.get('deadline', 'N/A')}
**Schedule Date:** {task_data.get('scheduleDate', 'N/A')}
**Schedule Status:** {task_data.get('scheduleStatus', 'N/A')}
**Estimate:** {task_data.get('estimate', 'N/A')}
**Reported Time:** {task_data.get('reportedTime', 'N/A')}
**Moment Created:** {task_data.get('momentCreated', 'N/A')}
**Moment Closed:** {task_data.get('momentClosed', 'N/A')}
**Recent Activity:** {task_data.get('recentActivityMoment', 'N/A')}
**Parent Task ID:** {task_data.get('parentTaskId', 'N/A')}
**Users:** {', '.join([user_display(uid) for uid in users]) if users else 'N/A'}
**Subtasks Count:** {len(subtasks)}
""".strip()

            # Add custom fields if they exist
            if custom_fields:
                formatted_details += "\n\n**Custom Fields:**"
                for field_id, field_value in custom_fields.items():
                    formatted_details += f"\n- {field_id}: {field_value}"

            # Add subtasks if they exist
            if subtasks:
                formatted_details += f"\n\n**Subtasks ({len(subtasks)}):**"
                for i, subtask in enumerate(subtasks[:10]):  # Limit to first 10 subtasks
                    if isinstance(subtask, dict):
                        formatted_details += f"\n- {subtask.get('shortId', 'N/A')}: {subtask.get('name', 'N/A')}"
                    else:
                        formatted_details += f"\n- Subtask {i+1}: {subtask}"
                if len(subtasks) > 10:
                    formatted_details += f"\n... and {len(subtasks) - 10} more subtasks"

            if __event_emitter__:
                await __event_emitter__({
                    "type": "status",
                    "data": {"description": f"Successfully retrieved details for task '{task_short_id}'", "done": True},
                })

            return f"**Task Details for '{task_short_id}' in project '{found_in_project}':**\n\n{formatted_details}"

        except Exception as e:
            error_msg = f"Failed to retrieve task details: {str(e)}"
            if __event_emitter__:
                await __event_emitter__({
                    "type": "status",
                    "data": {"description": error_msg, "done": True},
                })
            return error_msg

    # Search Tools
    async def search_goodday_tasks(
        self,
        query: str,
        __request__: Request = None,
        __user__: dict = None,
        __event_emitter__: Callable = None
    ) -> str:
        """
        Search for tasks in Goodday using semantic search

        :param query: Search query to find relevant tasks (e.g., "security task", "UI improvements")
        """
        # Validate and sanitize the query parameter
        if not query or not isinstance(query, str):
            return "Error: Search query must be a non-empty string"
        
        query = query.strip()
        if not query:
            return "Error: Search query cannot be empty"
            
        if __event_emitter__:
            await __event_emitter__({
                "type": "status",
                "data": {"description": f"Searching for tasks with query: '{query}'...", "done": False},
            })

        try:
            # Make the search request
            params = {"query": query}
            data = await self._make_search_request(params=params)

            if not data:
                return f"No search results found for query: '{query}'"

            if isinstance(data, dict) and "error" in data:
                return f"Search error: {data.get('error', 'Unknown error')}"

            # Handle the response format - expecting a list with result objects
            if not isinstance(data, list) or len(data) == 0:
                return f"No search results found for query: '{query}'"

            # Extract results from the first item in the list
            first_item = data[0]
            if not isinstance(first_item, dict) or "result" not in first_item:
                return f"Unexpected search response format: {str(data)}"

            results = first_item.get("result", [])
            if not isinstance(results, list) or len(results) == 0:
                return f"No search results found for query: '{query}'"

            # Format the search results
            formatted_results = []
            seen_task_ids = set()
            
            for result in results:
                if not isinstance(result, dict):
                    continue
                
                task_id = result.get('taskId') or 'N/A'
                
                # Group by task ID to avoid duplicates
                if task_id not in seen_task_ids:
                    seen_task_ids.add(task_id)
                    formatted_results.append(self._format_search_result(result))
                else:
                    # For duplicate task IDs, append additional content if different
                    existing_result = None
                    for i, existing in enumerate(formatted_results):
                        if task_id in existing:
                            existing_result = i
                            break
                    
                    if existing_result is not None:
                        current_content = result.get('content') or ''
                        if current_content and current_content not in formatted_results[existing_result]:
                            formatted_results[existing_result] += f"\n**Additional Content:** {current_content}"

            result_text = "\n---\n".join(formatted_results)

            if __event_emitter__:
                await __event_emitter__({
                    "type": "status",
                    "data": {"description": f"Found {len(formatted_results)} unique tasks matching '{query}'", "done": True},
                })

            return f"**Search Results for '{query}' ({len(formatted_results)} unique tasks found):**\n\n{result_text}"

        except Exception as e:
            error_msg = f"Failed to search tasks: {str(e)}"
            if __event_emitter__:
                await __event_emitter__({
                    "type": "status",
                    "data": {"description": error_msg, "done": True},
                })
            return error_msg
