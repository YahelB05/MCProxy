import requests

BASE_URL = "http://localhost/mcp/"
HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json, text/event-stream"
}


def send_request(payload, session_id=None):
    headers = HEADERS.copy()
    if session_id:
        headers["Mcp-Session-Id"] = session_id
    response = requests.post(BASE_URL, headers=headers, json=payload)
    try:
        response_json = response.json()
    except ValueError:
        response_json = response.text
    print(f"➡ Sent method: {payload.get('method', 'unknown')}")
    print(f"⬅ Response: {response_json}\n")
    return response


# 1. Initialize
init_payload = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "initialize",
    "params": {
        "protocolVersion": "2025-06-18",
        "capabilities": {
            "elicitation": {}
        },
        "clientInfo": {
            "name": "example-client",
            "version": "1.0.0"
        }
    }
}

resp = send_request(init_payload)

# 2. Extract Mcp-Session-Id
session_id = resp.headers.get("Mcp-Session-Id")
if not session_id:
    raise RuntimeError("Mcp-Session-Id not found in response headers!")
print(f"✅ Using session ID: {session_id}\n")

# 3. notifications/initialized
notif_payload = {
    "jsonrpc": "2.0",
    "method": "notifications/initialized"
}
send_request(notif_payload, session_id=session_id)

# 4. tools/list
tools_payload = {
    "jsonrpc": "2.0",
    "id": 4,
    "method": "tools/list"
}
send_request(tools_payload, session_id=session_id)

# 5. tools/call
tools_payload = {
  "jsonrpc": "2.0",
  "id": 5,
  "method": "tools/call",
  "params": {
    "name": "get_user_data"
  }
}
send_request(tools_payload, session_id=session_id)
