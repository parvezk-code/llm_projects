# services/mcp/exceptions.py


class MCPConnectionError(Exception):
    pass


class MCPToolExecutionError(Exception):
    pass


class MCPParseError(Exception):
    pass
