# MCP Server Neurolorap

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://github.com/aindreyway/mcp-server-neurolorap/actions/workflows/tests.yml/badge.svg)](https://github.com/aindreyway/mcp-server-neurolorap/actions/workflows/tests.yml)
[![codecov](https://codecov.io/gh/aindreyway/mcp-server-neurolorap/branch/main/graph/badge.svg)](https://codecov.io/gh/aindreyway/mcp-server-neurolorap)

MCP server for collecting code from files and directories into a single markdown document.

## Features

- Collect code from entire project
- Collect code from specific directories or files
- Collect code from multiple paths
- Customizable ignore patterns via .neuroloraignore
- Markdown output with syntax highlighting
- Table of contents generation
- Support for multiple programming languages
- Developer mode with JSON-RPC terminal interface
- Robust file system synchronization
- Comprehensive error handling and logging

## Quick Overview

```sh
# Using uvx (recommended)
uvx mcp-server-neurolorap

# Or using pip (not recommended)
pip install mcp-server-neurolorap
```

You don't need to install or configure any dependencies manually. The tool will set up everything you need to collect and document code.

## Installation

**You'll need to have [UV](https://docs.astral.sh/uv/) >= 0.4.10 installed on your machine.**

To install and run the server:

```sh
# Install using uvx (recommended)
uvx mcp-server-neurolorap

# Or install using pip (not recommended)
pip install mcp-server-neurolorap
```

This will automatically:

- Install all required dependencies
- Configure Cline integration
- Set up the server for immediate use

The server will be available through the MCP protocol in Cline. You can use it to collect and document code from any project.

## Usage

### Developer Mode

The server includes a developer mode with JSON-RPC terminal interface for direct interaction:

```bash
# Start the server in developer mode
python -m mcp_server_neurolorap --dev
```

Available commands:

- `help`: Show available commands
- `list_tools`: List available MCP tools
- `collect <path>`: Collect code from specified path
- `exit`: Exit developer mode

Example session:

```
> help
Available commands:
- help: Show this help message
- list_tools: List available MCP tools
- collect <path>: Collect code from specified path
- exit: Exit the terminal

> list_tools
["code-collector"]

> collect src
Code collection complete!
Output file: code_collection.md

> exit
Goodbye!
```

### Through MCP Tools

```python
from modelcontextprotocol import use_mcp_tool

# Collect code from entire project
result = use_mcp_tool(
    "code-collector",
    {
        "input": ".",
        "title": "My Project"
    }
)

# Collect code from specific directory
result = use_mcp_tool(
    "code-collector",
    {
        "input": "./src",
        "title": "Source Code"
    }
)

# Collect code from multiple paths
result = use_mcp_tool(
    "code-collector",
    {
        "input": ["./src", "./tests"],
        "title": "Project Files"
    }
)
```

### File Storage

The server uses a structured approach to file storage:

1. All generated files are stored in `~/.mcp-docs/<project-name>/`
2. A `.neurolora` symlink is created in your project root pointing to this directory

This ensures:

- Clean project structure
- Consistent file organization
- Easy access to generated files
- Support for multiple projects
- Reliable file synchronization across different OS environments
- Fast file visibility in IDEs and file explorers

### Customizing Ignore Patterns

Create a `.neuroloraignore` file in your project root to customize which files are ignored:

```gitignore
# Dependencies
node_modules/
venv/

# Build
dist/
build/

# Cache
__pycache__/
*.pyc

# IDE
.vscode/
.idea/

# Generated files
.neurolora/
```

If no `.neuroloraignore` file exists, a default one will be created with common ignore patterns.

## Development

1. Clone the repository
2. Create and activate virtual environment:

```sh
python -m venv .venv
source .venv/bin/activate  # On Unix
# or
.venv\Scripts\activate  # On Windows
```

3. Install development dependencies:

```sh
pip install -e ".[dev]"
```

4. Run the server:

```sh
# Normal mode (MCP server with stdio transport)
python -m mcp_server_neurolorap

# Developer mode (JSON-RPC terminal interface)
python -m mcp_server_neurolorap --dev
```

### Testing

The project maintains high quality standards through automated testing and continuous integration:

- Comprehensive test suite with over 80% code coverage
- Automated testing on Python 3.10, 3.11, and 3.12
- Continuous integration through GitHub Actions
- Regular security scans and dependency checks

For development and testing details, see PROJECT_SUMMARY.md.

### Code Quality

The project maintains high code quality standards through various tools:

```sh
# Format code
black .

# Sort imports
isort .

# Lint code
flake8 .

# Type check
mypy src tests

# Security check
bandit -r src/
safety check
```

All these checks are run automatically on pull requests through GitHub Actions.

### CI/CD Pipeline

The project uses GitHub Actions for continuous integration and deployment:

- Runs tests on Python 3.10, 3.11, and 3.12
- Checks code formatting and style
- Performs type checking
- Runs security scans
- Generates coverage reports
- Builds and validates package
- Uploads test artifacts

The pipeline must pass before merging any changes.

## License

MIT License. See LICENSE file for details.
