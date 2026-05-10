from pathlib import Path
import sys

# Add project root to Python path
ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))


from services.mcp.mcp_client_controller import MCPClientController


def main() -> None:
    server_url = "http://localhost:8000/mcp"
    pdf_path = "zz_test/test_doc.pdf"

    mcp_controller = MCPClientController(server_url)

    result = mcp_controller.call_tool_sync(
        tool_name="extract_pdf_text",
        arguments={"pdf_path": pdf_path},
    )

    if result.success:
        print("SUCCESS")
        print(result.data)
    else:
        print("FAILED")
        print(result.error)


if __name__ == "__main__":
    main()
