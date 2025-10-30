#!/usr/bin/env python3
"""
使用 HTTP SSE 流式测试 MCP 服务器的工具列表
"""

import json

import requests


def parse_sse_response(text):
    """解析 SSE 格式的响应"""
    # SSE 格式: event: message\ndata: {...}\n\n
    lines = text.strip().split("\n")
    for line in lines:
        if line.startswith("data: "):
            data = line[6:]  # 去掉 "data: " 前缀
            try:
                return json.loads(data)
            except (json.JSONDecodeError, ValueError):
                pass
    return None


def test_mcp_http():
    """通过 HTTP SSE 流式请求测试 MCP 服务器"""
    base_url = "http://127.0.0.1:8080/mcp"

    print("\n" + "=" * 60)
    print(f"Testing MCP Server (HTTP SSE): {base_url}")
    print("=" * 60)

    # 第1步: 初始化会话
    print("\n📡 Step 1: Initialize session...")
    init_payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "test-client", "version": "1.0.0"},
        },
    }

    try:
        response = requests.post(
            base_url,
            json=init_payload,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json, text/event-stream",
            },
        )

        print(f"   Status: {response.status_code}")
        print(f"   Content-Type: {response.headers.get('Content-Type')}")

        if response.status_code == 200:
            # 解析 SSE 响应
            result = parse_sse_response(response.text)
            if result and "result" in result:
                server_info = result["result"].get("serverInfo", {})
                print(f"   ✅ Server: {server_info.get('name')}")
                print(f"   Version: {server_info.get('version')}")
        else:
            print(f"   ❌ Error: {response.text}")
            return

        # 获取 session ID（如果有）
        session_id = None
        # 检查多种可能的 header 名称
        session_headers = [
            "x-mcp-session-id",
            "mcp-session-id",
            "x-session-id",
            "session-id",
            "x-mcp-session",
        ]
        for header in session_headers:
            if header in response.headers:
                session_id = response.headers[header]
                print(f"   Session ID ({header}): {session_id}")
                break

        if not session_id:
            print("   ⚠️  No session ID in response headers")
            print(f"   Available headers: {list(response.headers.keys())}")

        # 第2步: 请求工具列表
        print("\n📋 Step 2: List tools...")
        tools_payload = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list",
            "params": {},
        }

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
        }
        if session_id:
            # 尝试所有可能的 session header 名称
            headers["x-mcp-session-id"] = session_id
            headers["mcp-session-id"] = session_id
            headers["x-session-id"] = session_id

        tools_response = requests.post(base_url, json=tools_payload, headers=headers)

        print(f"   Status: {tools_response.status_code}")

        if tools_response.status_code == 200:
            # 解析 SSE 响应
            tools_result = parse_sse_response(tools_response.text)

            if (
                tools_result
                and "result" in tools_result
                and "tools" in tools_result["result"]
            ):
                tools = tools_result["result"]["tools"]
                print(f"\n✅ Discovered {len(tools)} tools:\n")

                # 列出所有工具
                for i, tool in enumerate(tools, 1):
                    marker = (
                        "🆕" if tool.get("name") == "get_candles_snapshot" else "  "
                    )
                    print(f"{marker} {i:2d}. {tool.get('name')}")

                # 检查 get_candles_snapshot
                print("\n" + "=" * 60)
                tool_names = [t.get("name") for t in tools]

                if "get_candles_snapshot" in tool_names:
                    print("✅✅✅ get_candles_snapshot IS AVAILABLE via HTTP!")

                    # 显示详细信息
                    snapshot_tool = next(
                        t for t in tools if t.get("name") == "get_candles_snapshot"
                    )
                    print("\n📝 Tool Details:")
                    print(f"   Name: {snapshot_tool.get('name')}")

                    if "description" in snapshot_tool:
                        desc = snapshot_tool["description"]
                        # 只显示前150个字符
                        print(f"   Description: {desc[:150]}...")

                    if "inputSchema" in snapshot_tool:
                        schema = snapshot_tool["inputSchema"]
                        if "required" in schema:
                            print(f"   Required: {schema['required']}")
                        if "properties" in schema:
                            print(f"   Parameters: {list(schema['properties'].keys())}")
                else:
                    print("❌ get_candles_snapshot NOT FOUND in HTTP response")
                    print(f"\nFirst 5 tools: {', '.join(tool_names[:5])}")

                print("=" * 60 + "\n")
            else:
                print("\n⚠️  Unexpected response format:")
                print(json.dumps(tools_result, indent=2)[:500])
        else:
            print(f"   ❌ Error: {tools_response.text}")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        print(f"   Type: {type(e).__name__}")
        import traceback

        traceback.print_exc()
        print("\n⚠️  Make sure server is running:")
        print("   uv run start")


if __name__ == "__main__":
    test_mcp_http()
