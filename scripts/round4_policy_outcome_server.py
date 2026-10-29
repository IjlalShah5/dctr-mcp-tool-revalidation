#!/usr/bin/env python3
"""Round4 controlled outcome-oracle server using official MCP SDK stdio.

The "event" is a line in a TEMPORARY LOCAL FILE and uses PUBLIC synthetic
markers. Scenarios are author-designed; there is no attacker, secret, network
transfer, independent severity ground truth or natural Tool mutation.
"""
from __future__ import annotations

import asyncio
import json
import os
from pathlib import Path

import mcp.types as types
from mcp.server import NotificationOptions, Server
from mcp.server.stdio import stdio_server

server = Server("dctr-round4-controlled-oracle")


def load_fixture():
    data = json.loads(Path(os.environ["DCTR_R4_ORACLE_CONFIG"]).read_text(encoding="utf-8"))
    tool = data["tool"]
    assert tool["name"] == "round3_echo"
    assert isinstance(data["trigger"], dict)
    assert data["scenario_id"]
    return data


@server.list_tools()
async def list_tools() -> list[types.Tool]:
    return [types.Tool(**load_fixture()["tool"])]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    fixture = load_fixture()
    if name != fixture["tool"]["name"]:
        raise ValueError("Unrecognized Tool")
    counts = Path(os.environ["DCTR_R4_CALLS"])
    with counts.open("a", encoding="utf-8") as f:
        f.write(json.dumps({"scenario": fixture["scenario_id"], "arguments": arguments}, sort_keys=True) + "\n")
        f.flush()
        os.fsync(f.fileno())
    trigger = fixture["trigger"]
    if trigger and all(arguments.get(key) == expected for key, expected in trigger.items()):
        output = Path(os.environ["DCTR_R4_EVENT_LOG"])
        with output.open("a", encoding="utf-8") as f:
            f.write(json.dumps({"scenario": fixture["scenario_id"], "oracle": "PUBLIC_LOCAL_MARKER"}) + "\n")
            f.flush()
            os.fsync(f.fileno())
    return [types.TextContent(type="text", text=str(arguments.get("message", "")))]


async def run():
    async with stdio_server() as (reader, writer):
        await server.run(
            reader, writer,
            server.create_initialization_options(
                notification_options=NotificationOptions(tools_changed=True),
                experimental_capabilities={},
            ),
        )


if __name__ == "__main__":
    asyncio.run(run())
