# MCProxy - MCP Proxy for RESTful APIs

MCProxy easley and almost seamlessly generates and deploys a proxy between your <b>existing</b> API and the clients.
<br />
It won't replace the existing interface with the existing API, but it will extend the functionality of your system
with <b>MCP</b>.
<br />

---

## What's MCP?

MCP (Model Context Protocol) is a standardized communication protocol that enables AI tools and services to interact
seamlessly,
where servers expose operations (“tools”) with defined input/output schemas and clients can discover, invoke, and use
them dynamically.
<br />
In this ecosystem, an MCP Server acts as a gateway, exposing AI capabilities, workflows, or APIs—often with streaming
outputs—while an MCP Client, typically an AI agent or application, discovers and calls these tools to perform tasks.
<br />
<br />
<b>MCProxy</b> acts as an MCP Server proxy layer that wraps your existing REST API, enabling AI clients to interact with
your services using the MCP protocol without changing your underlying API.

---

## Deployment

Deploying **MCProxy** is straightforward:

1. **Build the Docker image:**  
   `docker build -t mcp-proxy:<version> .`

2. **Prepare the configuration file**  
   Define the endpoints you want to expose to MCP clients. By default, MCProxy will look for `config.json`.

3. **Mount the configuration file**  
   Mount it into your Docker container, Kubernetes pod, or deployment.

4. **Expose MCProxy**  
   Make the service accessible via your preferred routing or ingress method.

💡 You can check the examples in `./dev/` for inspiration on configuration and setup.

Once deployed, MCP clients can connect to MCProxy and access exactly the data you’ve allowed — **no extra coding
required**.

---

## Environment Variables

| Variable      | Description                          | Default         |
|---------------|--------------------------------------|-----------------|
| `CONFIG_FILE` | Full path to the configuration file. | `./config.json` |

---

## Configuration JSON Schema:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "API Endpoints Schema",
  "type": "object",
  "required": [
    "version",
    "endpoints"
  ],
  "properties": {
    "version": {
      "type": "string",
      "description": "Version of the schema or API definition"
    },
    "endpoints": {
      "type": "array",
      "description": "List of API endpoints",
      "items": {
        "type": "object",
        "required": [
          "name",
          "description",
          "url",
          "method"
        ],
        "properties": {
          "name": {
            "type": "string",
            "description": "Unique name of the endpoint"
          },
          "description": {
            "type": "string",
            "description": "A short description of the endpoint"
          },
          "url": {
            "type": "string",
            "format": "uri",
            "description": "Base URL of the endpoint"
          },
          "method": {
            "type": "string",
            "enum": [
              "GET",
              "POST",
              "PUT",
              "DELETE",
              "PATCH"
            ],
            "description": "HTTP method to use"
          },
          "path_params": {
            "type": "array",
            "description": "List of path parameters",
            "items": {
              "type": "object",
              "additionalProperties": {
                "type": "string"
              }
            }
          },
          "query_params": {
            "type": "array",
            "description": "List of query parameters",
            "items": {
              "type": "object",
              "additionalProperties": {
                "type": "string"
              }
            }
          }
        },
        "additionalProperties": false
      }
    }
  },
  "additionalProperties": false
}
```

**Example for a configuration file: `./dev/deployment/docker/endpoints.json`**

---

## Testing

Set up the environment, including:

- **Nginx** as the reverse proxy (BSD 2-Clause License)
- **mendhak/http-https-echo** as the RESTful API (MIT License)
- The **MCProxy** server

```commandline
cd ./dev/deployment/docker
docker compose up -d
```

To test the default configuration, you can use the available scripts, for example:

```commandline
cd ./dev/scripts
python3 test_list_tools.py
```

<b>Note:</b> Both Nginx and http-https-echo are used only in the example Docker Compose setup and are not bundled with
this project.

---

## ⚠️ Disclaimer:

The creators of MCProxy are not responsible for any unintended exposure of data through the endpoints you configure. It
is your responsibility to ensure that the endpoints you expose do not leak sensitive or unwanted information.
