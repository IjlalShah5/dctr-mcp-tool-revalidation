#!/usr/bin/env python3
"""Controlled MCP server running through the official MCP Python SDK (v1.30.0).

The fixture reads an immutable-for-this-process contract description at startup.
Tests simulate maintainer deployment of a changed Tool definition by restarting
the separate SDK server subprocess with a changed fixture configuration.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from mcp.server.fastmcp import FastMCP

CONFIG = Path(os.environ["DCTR_ROUND3_SDK_CONTRACT_FILE"])
CALL_COUNT = Path(os.environ["DCTR_ROUND3_SDK_CALL_COUNTER"])
config = json.loads(CONFIG.read_text(encoding="utf-8"))
description = config["description"]
if not isinstance(description, str) or not description:
    raise ValueError("fixture description must be non-empty")

mcp = FastMCP("round3-synthetic-stdio-server")

@mcp.tool(name="round3_echo", description=description)
def round3_echo(message: str) -> str:
    """Fixture-only side effect: persist a Tool invocation count to disk."""
    # Count writes demonstrate that a denied request never crossed tools/call.
    current = int(CALL_COUNT.read_text(encoding="ascii")) if CALL_COUNT.exists() else 0
    CALL_COUNT.write_text(str(current + 1), encoding="ascii")
    return message

if __name__ == "__main__":
    mcp.run(transport="stdio")
