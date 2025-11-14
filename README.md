This is a demo weather MCP server that I wrote as a part of a [linkedin course](https://www.linkedin.com/learning/model-context-protocol-mcp-hands-on-with-agentic-ai/articles/creating-an-mcp-server-using-python).

For development with MCP inspector, run:

```
uv run mcp dev main.py
```

For use with an MCP client (eg [5ire](https://5ire.app/)), run:
```
uv run main.py
```
... and connect the client to a "remote" endpoint, `http://127.0.0.1:8000/mcp`.
