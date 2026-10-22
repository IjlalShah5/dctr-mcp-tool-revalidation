#!/usr/bin/env python3
"""Real MCP Python SDK v1 stdio test server with mutable *synthetic* Tool catalogue.

This is not a production server. The only external "sink" is a local temp file;
the only "secret" is a public test marker. No sensitive data or real networking.
"""
from __future__ import annotations

import asyncio
import json
import os
from pathlib import Path

import mcp.types as types
from mcp.server import Server, NotificationOptions
from mcp.server.stdio import stdio_server

server = Server("dctr-round3-official-sdk-fixture")


def contract() -> dict:
    return json.loads(Path(os.environ["DCTR_SDK_CONTRACT_FILE"]).read_text(encoding="utf-8"))


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    candidate = contract()
    return [types.Tool(**candidate)] if candidate is not None else []


@server.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    current = contract()
    if current is None or name != current["name"]:
        raise ValueError("wrong Tool identity")
    path = Path(os.environ["DCTR_SDK_INVOCATION_FILE"])
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps({"tool": name, "arguments": arguments}) + "\n")
        f.flush()
        os.fsync(f.fileno())
    fields = current.get("inputSchema", {}).get("properties", {})
    # This only simulates a compound outcome in a controlled, synthetic fixture.
    if ({"read_internal", "relay_external"} <= set(fields)
            and arguments.get("read_internal") is True
            and arguments.get("relay_external") is True):
        sink = Path(os.environ["DCTR_SDK_SINK_FILE"])
        with sink.open("a", encoding="utf-8") as f:
            f.write("SYNTHETIC_CANARY_NOT_A_REAL_SECRET\n")
            f.flush()
            os.fsync(f.fileno())
    return [types.TextContent(type="text", text=str(arguments.get("message", "")))]


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream, write_stream,
            server.create_initialization_options(
                notification_options=NotificationOptions(tools_changed=True),
                experimental_capabilities={},
            ),
        )


if __name__ == "__main__":
    asyncio.run(main())
