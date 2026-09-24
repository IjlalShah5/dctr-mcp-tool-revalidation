#!/usr/bin/env python3
"""Controlled runtime corroboration for P02/P03 screenshot semantics.

This is not a replay of the historical MCP server package. It exercises the installed
Playwright/Chromium runtime for delegated screenshot behavior.
"""

from __future__ import annotations

from pathlib import Path
import base64
import importlib.metadata
import json
import struct
import subprocess

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "evidence" / "runtime_outputs"
OUT.mkdir(parents=True, exist_ok=True)


def png_dimensions(data: bytes) -> tuple[int, int]:
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("not a PNG")
    return struct.unpack(">II", data[16:24])


def main():
    results = {
        "experiment": "playwright_screenshot_runtime_corroboration",
        "scope_note": (
            "Current Playwright/Chromium runtime corroboration; not a historical "
            "end-to-end MCP server replay."
        ),
        "playwright_python_version": importlib.metadata.version("playwright"),
        "chromium_version": subprocess.check_output(
            ["/usr/bin/chromium", "--version"], text=True
        ).strip(),
        "cases": [],
    }

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            executable_path="/usr/bin/chromium",
            args=["--no-sandbox"],
        )
        context = browser.new_context(
            viewport={"width": 400, "height": 300},
            device_scale_factor=2,
        )
        page = context.new_page()
        page.set_content(
            '<html><body style="margin:0">'
            '<div style="width:200px;height:100px;background:#cc2222"></div>'
            '</body></html>'
        )

        scale_results = {}
        for scale in ("css", "device"):
            path = OUT / f"p02_scale_{scale}.png"
            page.screenshot(path=str(path), scale=scale)
            data = path.read_bytes()
            w, h = png_dimensions(data)
            scale_results[scale] = {
                "file": str(path.relative_to(ROOT)),
                "bytes": len(data),
                "width": w,
                "height": h,
            }

        p02_pass = (
            scale_results["css"]["width"] == 400
            and scale_results["css"]["height"] == 300
            and scale_results["device"]["width"] == 800
            and scale_results["device"]["height"] == 600
        )
        results["cases"].append({
            "case_id": "P02",
            "behavior": (
                "scale css/device changes screenshot pixel dimensions "
                "at deviceScaleFactor=2"
            ),
            "result": "PASS" if p02_pass else "FAIL",
            "observations": scale_results,
        })

        cdp = context.new_cdp_session(page)
        format_results = {}
        for fmt in ("png", "jpeg", "webp"):
            params = {"format": fmt}
            if fmt in ("jpeg", "webp"):
                params["quality"] = 80
            payload = cdp.send("Page.captureScreenshot", params)
            data = base64.b64decode(payload["data"])
            suffix = "jpg" if fmt == "jpeg" else fmt
            path = OUT / f"p03_runtime_format.{suffix}"
            path.write_bytes(data)
            if fmt == "png":
                signature_ok = data.startswith(b"\x89PNG\r\n\x1a\n")
            elif fmt == "jpeg":
                signature_ok = data.startswith(b"\xff\xd8\xff")
            else:
                signature_ok = data[:4] == b"RIFF" and data[8:12] == b"WEBP"
            format_results[fmt] = {
                "file": str(path.relative_to(ROOT)),
                "bytes": len(data),
                "signature_ok": signature_ok,
            }

        p03_pass = all(x["signature_ok"] for x in format_results.values())
        results["cases"].append({
            "case_id": "P03_BROWSER_ENCODING",
            "behavior": "Chromium screenshot runtime produces PNG/JPEG/WebP encodings",
            "result": "PASS" if p03_pass else "FAIL",
            "observations": format_results,
            "limitation": (
                "Confirms browser/runtime encoding support, not the full historical "
                "MCP response/file-registration path."
            ),
        })
        browser.close()

    (OUT / "playwright_runtime_results.json").write_text(
        json.dumps(results, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(results, indent=2))

    if any(c["result"] != "PASS" for c in results["cases"]):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
