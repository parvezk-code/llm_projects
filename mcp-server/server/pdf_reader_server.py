# server/pdf_reader_server.py

from mcp.server.fastmcp import FastMCP

from conf.settings import settings
from tools.extract_pdf_text_tool import extract_pdf_text


mcp = FastMCP(settings.SERVER_NAME)

mcp.add_tool(extract_pdf_text)