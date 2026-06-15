"""Security defaults for the MCP-style local memory stub."""

import scripts.run_mcp_server as run_mcp_server


def test_mcp_server_default_host_is_localhost() -> None:
    """MCP stub CLI should default to local-only 127.0.0.1 binding."""
    args = run_mcp_server.build_parser().parse_args([])
    assert args.host == "127.0.0.1"
