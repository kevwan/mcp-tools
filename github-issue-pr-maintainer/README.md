# MCP Tools: GitHub Issue Translator

A Model Context Protocol (MCP) tool for translating GitHub issues and PRs from Chinese to English.

## Table of Contents

- [Overview](#overview)
- [Installation](#installation)
- [Usage](#usage)
- [Tutorial: Building MCP Tools with FastMCP](#tutorial-building-mcp-tools-with-fastmcp)
  - [1. Developing an MCP Tool with Python and FastMCP](#1-developing-an-mcp-tool-with-python-and-fastmcp)
  - [2. Building the Project with uv](#2-building-the-project-with-uv)
  - [3. Adding the Tool to Claude and VS Code](#3-adding-the-tool-to-claude-and-vs-code)

## Overview

This tool integrates with AI assistants to translate GitHub issues and PRs from Chinese to English. It uses the Model Context Protocol (MCP) to provide structured data to LLMs like Claude.

## Installation

### Prerequisites

- Python 3.10 or later
- [uv](https://github.com/astral-sh/uv) package manager

### Installing with uv

```bash
# Clone the repository
git clone https://github.com/yourusername/mcp-tools.git
cd mcp-tools

# Create a virtual environment and install dependencies
uv venv
uv pip install -e .
```

## Usage

### As a Command-Line Tool

```bash
# Direct usage
python main.py --repo zeromicro/go-zero --issue_id 4814

# Using uv
uv --directory /path/to/mcp-tools run main.py --repo zeromicro/go-zero --issue_id 4814

# Using the installed entry point
github-translate --repo zeromicro/go-zero --issue_id 4814
```

### As an MCP Server

When integrated with Claude or another LLM:

1. The LLM will call your tool with the required parameters
2. Your tool processes the request and returns a formatted prompt
3. The LLM uses this prompt to perform the translation task

## Tutorial: Building MCP Tools with FastMCP

This tutorial explains how to create, build, and integrate MCP tools like this one.

### 1. Developing an MCP Tool with Python and FastMCP

#### Step 1: Set Up Your Project Structure

Create a directory with the following structure:
```
mcp-tools/
├── main.py           # Main script with MCP integration
├── pyproject.toml    # Project configuration
└── README.md         # Documentation
```

#### Step 2: Configure Your Project with pyproject.toml

Create a `pyproject.toml` file to define your project's metadata and dependencies:

```toml
[project]
name = "mcp-tools"
version = "0.1.0"
description = "MCP tools for GitHub issue translation prompts"
readme = "README.md"
requires-python = ">=3.10"
dependencies = [
    "click",
    "mcp",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["."]

[project.scripts]
github-translate = "main:cli"
```

#### Step 3: Create Your MCP Tool (main.py)

Implement your MCP tool in `main.py`:

```python
import click
from mcp.server.fastmcp import FastMCP

# Create a FastMCP instance with a unique identifier
mcp = FastMCP("github-issue-pr-translator")

# Define a prompt function decorated with @mcp.prompt()
@mcp.prompt()
def get_prompt(project: str, number: int) -> dict:
    """Get a prompt to update a GitHub issue or PR by translating Chinese content to English.

    Args:
        project: The GitHub project name.
        number: The issue or PR number to be translated.
    """
    return {
        "role": "user",
        "content": f"""Translation Instructions for GitHub Issues/PRs

# Your detailed prompt template here with {project} and {number} injected
"""
    }

# Define a CLI interface using Click
@click.command()
@click.option("--repo", required=True, help="The GitHub repository (e.g., 'zeromicro/go-zero')")
@click.option("--issue_id", type=int, required=True, help="The GitHub issue or PR number")
def cli(repo, issue_id):
    """CLI tool to run the GitHub issue/PR translator."""
    # Maps CLI parameters to the prompt function parameters
    result = get_prompt(project=repo, number=issue_id)
    print(result["content"])

if __name__ == "__main__":
    # Check if script is being run directly from command line
    import sys
    if len(sys.argv) > 1:
        cli()  # Run the CLI if arguments are provided
    else:
        # Initialize and run the MCP server
        mcp.run(transport='stdio')
```

#### Key Components Explained:

1. **FastMCP Instance**:
   ```python
   mcp = FastMCP("github-issue-pr-translator")
   ```
   - Creates an MCP server with a unique identifier

2. **Prompt Function**:
   ```python
   @mcp.prompt()
   def get_prompt(project: str, number: int) -> dict:
   ```
   - Decorated with `@mcp.prompt()` to register it with the MCP server
   - Takes parameters that will be supplied by the user or client
   - Returns a dictionary with `role` and `content` keys

3. **CLI Interface**:
   ```python
   @click.command()
   @click.option("--repo", required=True, help="...")
   @click.option("--issue_id", type=int, required=True, help="...")
   def cli(repo, issue_id):
   ```
   - Uses Click to create a user-friendly command-line interface
   - Maps CLI options to your prompt function parameters

4. **Dual-Mode Execution**:
   ```python
   if __name__ == "__main__":
       import sys
       if len(sys.argv) > 1:
           cli()
       else:
           mcp.run(transport='stdio')
   ```
   - Runs as CLI tool when arguments are provided
   - Runs as MCP server when no arguments are provided

### 2. Building the Project with uv

[uv](https://github.com/astral-sh/uv) is a fast Python package manager and resolver. Here's how to use it with your MCP tool:

#### Step 1: Install uv

If you haven't installed uv yet:

```bash
curl -sSf https://github.com/astral-sh/uv/releases/latest/download/install.sh | sh
```

#### Step 2: Create a Virtual Environment and Install Dependencies

Navigate to your project directory and run:

```bash
uv venv
uv pip install -e .
```

This installs your package in development mode with all dependencies.

#### Step 3: Build Your Project

Build a distribution package:

```bash
uv pip install build
python -m build
```

This creates distributable packages in the `dist/` directory.

#### Step 4: Run Your Tool

You can run your tool directly using uv:

```bash
uv run main.py --repo zeromicro/go-zero --issue_id 4814
```

Or use the directory option to specify your project path:

```bash
uv --directory /path/to/mcp-tools run main.py --repo zeromicro/go-zero --issue_id 4814
```

### 3. Adding the Tool to Claude and VS Code

#### Adding to Claude's Configuration

To integrate your MCP tool with Claude:

1. **Create a JSON Configuration File**:

Create a file named `claude-mcp-config.json`:

```json
{
  "tools": [
    {
      "name": "github-issue-pr-translator",
      "description": "Translates Chinese GitHub issues/PRs to English",
      "inputSchema": {
        "type": "object",
        "properties": {
          "project": {
            "type": "string",
            "description": "GitHub project name (e.g., 'zeromicro/go-zero')"
          },
          "number": {
            "type": "integer",
            "description": "Issue or PR number"
          }
        },
        "required": ["project", "number"]
      }
    }
  ],
  "toolConfig": {
    "github-issue-pr-translator": {
      "command": ["python", "-m", "main"],
      "env": {
        "PYTHONPATH": "/path/to/your/mcp-tools"
      }
    }
  }
}
```

2. **Configure Claude to Use Your Tool**:

In the Claude web interface:
- Go to Settings
- Navigate to the Developer or Tools section
- Upload or paste your configuration file
- Authenticate and authorize the tool when prompted

#### Adding to VS Code

1. **Install the Claude VS Code Extension**:
   - Open VS Code
   - Go to Extensions (Ctrl+Shift+X)
   - Search for "Claude AI Assistant"
   - Install the extension

2. **Configure the Extension**:
   - Open Settings (Ctrl+,)
   - Search for "Claude"
   - Find the "Custom Tools" or "MCP Tools" section
   - Add your tool configuration:

```json
{
  "claude.tools": [
    {
      "name": "github-issue-pr-translator",
      "description": "Translates Chinese GitHub issues/PRs to English",
      "command": "python -m main",
      "workingDir": "/path/to/your/mcp-tools",
      "schema": {
        "type": "object",
        "properties": {
          "project": {
            "type": "string",
            "description": "GitHub project name"
          },
          "number": {
            "type": "integer",
            "description": "Issue or PR number"
          }
        },
        "required": ["project", "number"]
      }
    }
  ]
}
```

3. **Restart VS Code**:
   - Restart VS Code to apply the changes
   - The tool should now be available in the Claude sidebar

## Using Your MCP Tool

Once integrated, you can use your tool with Claude or in VS Code by:

1. **In Claude's Web Interface**:
   - Type: "Use the github-issue-pr-translator tool to translate issue #4814 in zeromicro/go-zero"
   - Claude will call your tool with the appropriate parameters

2. **In VS Code**:
   - Open the Claude panel
   - Type a similar request or use the tools panel to select and configure your tool
   - View the translated content directly in the VS Code interface

## Advanced Features

You can enhance your MCP tool with additional features:

1. **Add Error Handling**:
   - Implement proper error handling for HTTP requests, parsing failures, etc.
   - Return structured error messages that Claude can understand

2. **Support Multiple Functions**:
   - Add more `@mcp.prompt()` decorated functions for different tasks
   - Create a comprehensive suite of translation or GitHub interaction tools

3. **Add Authentication**:
   - Implement GitHub API token support for accessing private repositories
   - Store credentials securely using environment variables

4. **Add Caching**:
   - Cache previous translations to improve performance
   - Implement a simple database for persistent storage