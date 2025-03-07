"""MCP server implementation for code collection."""

import logging
import os
from pathlib import Path
from typing import Any, Optional, cast

from mcp.server.fastmcp import FastMCP

from mcp_server_neurolorap.collector import CodeCollector
from mcp_server_neurolorap.terminal import JsonRpcTerminal
from mcp_server_neurolorap.types import FastMCPType

# Get module logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

__all__ = ["run_dev_mode", "create_server"]


def get_project_root() -> Path:
    """Get project root directory from environment or current directory."""
    current_dir = Path.cwd()
    project_root_str = os.environ.get("MCP_PROJECT_ROOT")
    if not project_root_str:
        os.environ["MCP_PROJECT_ROOT"] = str(current_dir)
        logger.info("Set MCP_PROJECT_ROOT to: %s", current_dir)
        return current_dir
    return Path(project_root_str)


def create_server() -> FastMCPType:
    """Create and configure a new server instance."""
    mcp = FastMCP("neurolorap", tools=True)

    @mcp.tool()  # type: ignore[misc]
    async def code_collector(
        input_path: str | list[str],
        title: str = "Code Collection",
        subproject_id: str | None = None,
    ) -> str:
        """Collect code from files into a markdown document."""
        logger.debug("Tool call: code-collector")
        logger.debug(
            "Arguments: input=%s, title=%s, subproject_id=%s",
            input_path,
            title,
            subproject_id,
        )

        try:
            root_path = get_project_root()
            collector = CodeCollector(
                project_root=root_path, subproject_id=subproject_id
            )

            logger.info("Starting code collection")
            logger.debug("Input: %s", input_path)
            logger.debug("Title: %s", title)
            logger.debug("Subproject ID: %s", subproject_id)

            output_file = collector.collect_code(input_path, title)
            if not output_file:
                msg = "No files found to process or error occurred"
                return msg

            return f"Code collection complete!\nOutput file: {output_file}"

        except (FileNotFoundError, PermissionError, OSError) as e:
            error_msg = f"File system error collecting code: {e}"
            logger.warning(error_msg)
            return error_msg
        except ValueError as e:
            error_msg = f"Invalid input: {e}"
            logger.warning(error_msg)
            return error_msg
        except TypeError as e:
            error_msg = f"Type error: {e}"
            logger.warning(error_msg)
            return error_msg
        except Exception as e:
            error_msg = f"Unexpected error collecting code: {e}"
            logger.error(error_msg, exc_info=True)
            return "An unexpected error occurred. Check server logs."

    return cast(FastMCPType, mcp)


# Initialize terminal for dev mode
terminal = JsonRpcTerminal(project_root=str(get_project_root()))


async def run_dev_mode() -> None:
    """Run the server in developer mode with JSON-RPC terminal."""
    print("Starting developer mode terminal...")
    print("Type 'help' for available commands")
    print("Type 'exit' to quit")

    while True:
        try:
            line = input("> ")
            if not line:
                continue

            request: Optional[dict[str, Any]] = terminal.parse_request(line)
            if not request:
                print("Invalid command format")
                continue

            response: dict[str, Any] = await terminal.handle_command(request)

            if "error" in response and response["error"] is not None:
                error = response["error"]
                if isinstance(error, dict) and "message" in error:
                    print(f"Error: {error['message']}")
            elif "result" in response:
                print(response["result"])

            if request.get("method") == "exit":
                break

        except (KeyboardInterrupt, EOFError):
            break
        except ValueError as e:
            print(f"Value error: {str(e)}")
        except TypeError as e:
            print(f"Type error: {str(e)}")
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            logger.error("Unexpected error in developer mode", exc_info=True)

    print("\nExiting developer mode")
