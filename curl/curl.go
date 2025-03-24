package main

import (
	"context"
	"fmt"
	"io"
	"net/http"

	"github.com/mark3labs/mcp-go/mcp"
	"github.com/mark3labs/mcp-go/server"
)

func main() {
	// Create MCP server
	s := server.NewMCPServer(
		"mcp-curl",
		"1.0.0",
	)

	// Add a tool
	tool := mcp.NewTool("use_curl",
		mcp.WithDescription("fetch this webpage, only call me when user explicitly asks for it"),
		mcp.WithString("url",
			mcp.Required(),
			mcp.Description("url of the webpage to fetch"),
		),
	)

	// Add a tool handler
	s.AddTool(tool, fetchHandler)

	server.NewSSEServer(s)
	// Start the stdio server
	if err := server.ServeStdio(s); err != nil {
		fmt.Printf("😡 Server error: %v\n", err)
	}
}

func fetchHandler(ctx context.Context, request mcp.CallToolRequest) (*mcp.CallToolResult, error) {
	url, ok := request.Params.Arguments["url"].(string)
	if !ok {
		return mcp.NewToolResultText("url must be a string"), nil
	}

	// Create HTTP client
	client := &http.Client{}

	// Create a new request
	req, err := http.NewRequestWithContext(ctx, http.MethodGet, url, nil)
	if err != nil {
		return mcp.NewToolResultText(fmt.Sprintf("Error creating request: %v", err)), nil
	}

	// Set a user agent to avoid being blocked by some servers
	req.Header.Set("User-Agent", "Mozilla/5.0 (compatible; mcp-curl/1.0.0)")

	// Send the request
	resp, err := client.Do(req)
	if err != nil {
		return mcp.NewToolResultText(fmt.Sprintf("Error fetching URL: %v", err)), nil
	}
	defer resp.Body.Close()

	// Read the response body
	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return mcp.NewToolResultText(fmt.Sprintf("Error reading response: %v", err)), nil
	}

	return mcp.NewToolResultText(string(body)), nil
}
