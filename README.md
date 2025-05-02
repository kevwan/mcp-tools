# MCP Tools

A collection of useful tools built with the Model Context Protocol (MCP) framework.

## Overview

This repository contains a set of tools designed to interface with AI models using the Model Context Protocol. Each tool is designed to extend the capabilities of AI assistants by providing additional functionality through standardized interfaces.

## Tools Included

### 1. MCP Curl

A Go-based MCP server that provides a tool for fetching web content. The curl tool allows AI assistants to retrieve content from URLs when explicitly requested by users.

**Features:**
- Fetches web content via HTTP GET requests
- Sets appropriate user agent headers to avoid blocking
- Returns the full content of webpages as text
- Implements the MCP standard for seamless integration with AI assistants

### 2. GitHub Issue/PR Maintainer

A Python-based MCP server that helps with maintaining GitHub issues and pull requests, specifically for the zeromicro/go-zero project. It provides two main functionalities:

**Features:**
- **Translation Mode**: Translates Chinese content in issues/PRs to English while preserving the original text
- **Answer Mode**: Generates responses to issues/PRs on behalf of the repository maintainer, with technically accurate and helpful content
- Command-line interface for direct usage
- Implements the MCP standard for integration with AI assistants

## Usage

### MCP Curl

```bash
# Navigate to the curl directory
cd curl

# Build and run the curl tool
go build
./curl
```

### GitHub Issue/PR Maintainer

```bash
# Navigate to the github-issue-pr-maintainer directory
cd github-issue-pr-maintainer

# Run in translation mode
python main.py --issue_id 123 --mode translate

# Run in answer mode
python main.py --issue_id 123 --mode answer

# Run as an MCP server
python main.py
```

## Requirements

### MCP Curl
- Go 1.24+
- github.com/mark3labs/mcp-go v0.15.0

### GitHub Issue/PR Maintainer
- Python 3.11+
- MCP Python library
- Click package

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/kevwan/mcp-tools.git
   cd mcp-tools
   ```

2. For the Go tool:
   ```bash
   cd curl
   go build
   ```

3. For the Python tool:
   ```bash
   cd github-issue-pr-maintainer
   pip install -e .
   ```

## License

See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

## Acknowledgments

- This project uses the Model Context Protocol (MCP), a standard for AI tool interfaces.
- Special thanks to the creators of the MCP standard and its implementations.