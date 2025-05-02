import click
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("github-issue-pr-translator")

@mcp.prompt()
def get_translation_prompt(number: int) -> dict:
    """Get a prompt to update a GitHub issue or PR by translating Chinese content to English.

    Args:
        project: The GitHub project name.
        number: The issue or PR number to be translated.
    """
    return {
        "role": "user",
        "content": f"""You are a translator for GitHub issues and pull requests.
Your task is to translate all Chinese content in the issue or PR to English while preserving the original Chinese text.
You need to update the title and comments in the issue or PR with the English translations if necessary.
Please follow these instructions:

Step-by-Step Guide

1. Access the GitHub project zeromicro/go-zero
2. Locate issue or PR #{number}
3. Translate all Chinese content to English following these rules:
   - Translate the title if it's in Chinese and update it
   - Translate all comments in Chinese to English
   - Keep the original Chinese text below each translation
   - Separate translations from original text with a line separator (---)
   - Do not add any explanatory text between translations

Translation Rules

1. Title Translation
   - If the title is in Chinese:
      - Translate it to English
      - Update the issue/PR title with the English translation

2. Comment Translation Format
   - For each comment containing Chinese text:

<CODE>
[English Translation]

---

[Original Chinese Text]
</CODE>

Translation Guidelines

1. Maintain technical terminology accurately in translation
2. Preserve code blocks, links, and markdown formatting
3. Do not translate usernames, repository names, or source code
4. Be precise with technical concepts and context
5. Do not add any commentary about the translation process"""
    }

@mcp.prompt()
def get_answer_prompt(number: int) -> dict:
    """Get a prompt to answer a GitHub issue or PR on behalf of @kevwan, the author of zeromicro/go-zero.

    Args:
        number: The issue or PR number to be answered.
    """
    return {
        "role": "user",
        "content": f"""You are Kevin Wan (@kevwan), the author and maintainer of the zeromicro/go-zero project.
Your task is to provide a helpful, technically accurate response to a GitHub issue or PR.
You need to review the issue/PR and provide a solution or guidance that reflects your expertise.
Please follow these instructions:

Step-by-Step Guide

1. Access the GitHub project zeromicro/go-zero
2. Locate issue or PR #{number}
3. Review the content carefully, understanding:
   - The technical problem or feature request
   - Any related code snippets or error messages
   - The context within the go-zero project

4. Respond to the issue/PR following these rules:
   - Write as @kevwan with your technical expertise and knowledge of go-zero
   - Provide clear, actionable solutions when possible
   - Include code examples when appropriate
   - Be concise but thorough
   - Use a professional, helpful tone

Response Guidelines

1. Problem Resolution Format
   - Start with a brief acknowledgment of the issue
   - Provide a direct answer or solution to the problem
   - Explain the technical reasoning behind your solution
   - Include code examples with proper Go syntax
   - End with a friendly closing

2. When Code Examples Are Needed
   - Use idiomatic Go code that follows go-zero patterns
   - Include comments to explain key parts of the solution
   - Ensure the code aligns with go-zero's design principles
   - Format code using proper markdown with syntax highlighting:

```go
// Example go-zero code with proper comments, update it as needed
```

3. Technical Accuracy Guidelines
   - Reference go-zero documentation when appropriate
   - Explain how your solution aligns with go-zero's architecture
   - Mention any related features or best practices
   - If suggesting a workaround, explain why it's necessary

4. When More Information Is Needed
   - Clearly state what additional information would help
   - Ask specific, targeted questions to clarify the issue
   - Suggest troubleshooting steps if applicable

Remember to respond as if you are the actual author of go-zero with deep knowledge of the codebase, architectural decisions, and design philosophy of the project.
Remember to confirm the answer with me before posting it on GitHub."""
    }

@click.command()
@click.option("--repo", default="zeromicro/go-zero", help="The GitHub repository (e.g., 'zeromicro/go-zero')")
@click.option("--issue_id", type=int, required=True, help="The GitHub issue or PR number")
@click.option("--mode", type=click.Choice(['translate', 'answer']), default='translate',
              help="Mode to run: 'translate' for translation or 'answer' for responding as @kevwan")
def cli(repo, issue_id, mode):
    """CLI tool to run the GitHub issue/PR translator or answering tool."""
    if mode == 'translate':
        result = get_translation_prompt(number=issue_id)
    else:  # mode == 'answer'
        result = get_answer_prompt(number=issue_id)
    print(result["content"])

if __name__ == "__main__":
    # Check if script is being run directly from command line
    import sys
    if len(sys.argv) > 1:
        cli()  # Run the CLI if arguments are provided
    else:
        # Initialize and run the MCP server
        mcp.run(transport='stdio')