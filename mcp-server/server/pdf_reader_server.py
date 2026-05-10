# server/pdf_reader_server.py

from mcp.server.fastmcp import FastMCP

from tools.get_working_directory.tool import get_working_directory
from tools.list_pdfs_in_directory.tool import list_pdfs_in_directory
from tools.read_pdf_content.tool import read_pdf_content


mcp = FastMCP("pdf-reader-server")

mcp.add_tool(get_working_directory)
mcp.add_tool(list_pdfs_in_directory)
mcp.add_tool(read_pdf_content)