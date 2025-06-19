# MCP IDE Bridge

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://www.docker.com/)
[![MCP Protocol](https://img.shields.io/badge/MCP-HTTP%20Streamable-green.svg)](https://spec.modelcontextprotocol.io/)

A stateless, open source MCP (Model Context Protocol) HTTP Streamable server for client-to-client messaging. This server enables secure, real-time communication between different IDE instances, development tools, or applications using the MCP protocol.

**🎯 Perfect for**: Cross-IDE collaboration, development tool integration, AI agent communication, and distributed development workflows.

## 🚀 Features

- **Stateless Architecture**: No persistent client state, maximum reliability
- **HTTP Streamable Transport**: Uses latest MCP specification (2025-03-26)
- **Security-First Design**: Client IDs act as security credentials
- **Dynamic Discovery**: Clients self-register, no pre-configuration required
- **Message Expiration**: Automatic 5-minute message cleanup
- **Real-time Messaging**: Immediate message delivery and retrieval

## 🏗️ Architecture

### Core Concepts

- **Client IDs**: Secure identifiers for clients (from `mcp_recipients.json`)
- **Message Queues**: Per-recipient queues created on-demand
- **Stateless Operations**: Each request is independent
- **Markdown Responses**: Human-readable formatted responses

### Message Flow

```
Client A → send_message → Server Queue → get_messages → Client B
```

## 📋 Available Tools

### `checkin_client`
Announce client presence to the server.
- **Parameters**: `client_id`, `name`, `capabilities`
- **Returns**: Confirmation message

### `send_message`
Send a message to another client.
- **Parameters**: `sender_id`, `recipient_id`, `message`
- **Returns**: Success confirmation

### `get_messages`
Retrieve and remove pending messages.
- **Parameters**: `client_id`
- **Returns**: Messages in markdown format (popped from queue)

### `get_my_identity`
Get instructions on client configuration.
- **Parameters**: None
- **Returns**: Information about `mcp_recipients.json`

## ⚙️ Setup

### 1. Install Dependencies

```bash
# Create Python 3.11+ virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install the package
pip install -e .
```

### 2. Configure Environment

Copy `env.example` to `.env` and adjust settings:

```bash
cp env.example .env
```

### 3. Create Client Configuration

Each client needs a `mcp_recipients.json` file:

```json
{
  "my_id": "cursor_client_1",
  "recipients": {
    "cursor_client_2": {
      "name": "Second Cursor Instance",
      "description": "Another Cursor IDE instance for testing"
    },
    "vscode_client_1": {
      "name": "VS Code Instance", 
      "description": "VS Code IDE for cross-editor communication"
    }
  },
  "server_info": {
    "url": "http://localhost:8123",
    "health_endpoint": "/api/mcp/health",
    "sse_endpoint": "/api/mcp/sse"
  }
}
```

### 4. Start the Server

**Python:**
```bash
# Default: localhost:8123
python -m mcp_messaging.server

# Custom host/port
python -m mcp_messaging.server --host 0.0.0.0 --port 9000
```

**Docker:**
```bash
# Build image
docker build -t mcp-messaging-server .

# Run container
docker run -d \
  --name mcp-messaging-server \
  -p 8123:8123 \
  -v "$(pwd)/examples:/app/examples:ro" \
  mcp-messaging-server
```

## 🔧 Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `MCP_SERVER_HOST` | `localhost` | Server bind address |
| `MCP_SERVER_PORT` | `8123` | Server port |
| `LOG_LEVEL` | `INFO` | Logging level |

### Message Settings

- **Expiration**: 5 minutes (hardcoded)
- **Cleanup**: On-demand during send/get operations
- **Format**: Markdown with relative timestamps
- **Queue**: Per-recipient, created automatically

### Transport Behavior

**Important**: MCP Streamable HTTP using FastMCP has specific transport characteristics:

- **Protocol Layer**: Uses `text/event-stream` headers for MCP protocol communication
- **Expected Behavior**: Clients should expect SSE format at the transport level
- **Implementation Note**: This is normal FastMCP behavior for Streamable HTTP transport

### Recommended Configuration

**For MCP clients that support Streamable HTTP (like Cursor, Claude Desktop):**

```python
mcp = FastMCP(
    name="your-server-name",
    stateless_http=True,     # Required for Streamable HTTP
    json_response=False      # RECOMMENDED: Enables rich streaming experience
)

mcp.run(transport="streamable-http", host=host, port=port)
```

**Why `json_response=False` is recommended:**
- ✅ **Rich streaming**: Progress updates and notifications during tool execution
- ✅ **Better UX**: Real-time feedback for long-running operations  
- ✅ **Standard MCP**: More aligned with MCP's streaming capabilities
- ✅ **Client compatibility**: Works with all MCP clients that support Streamable HTTP

**`json_response=True` vs `json_response=False`:**
- `True`: Single JSON response per tool call (simpler but less interactive)
- `False`: Streaming notifications + final result (richer experience)

**For Client Developers:**
Your MCP client should be prepared to handle:
- `content-type: text/event-stream` for protocol-level communication
- `event: message` / `data: {...}` SSE format for transport
- **Notifications**: `{"method": "notifications/message", ...}` for progress updates
- **Results**: `{"id": 1, "result": {...}}` for final tool responses
- JSON-RPC 2.0 message structure within the SSE data field

This is **correct behavior** - FastMCP implements MCP Streamable HTTP using SSE as the underlying transport mechanism while maintaining full MCP compatibility.

## 🧪 Testing

### Quick Test Flow

1. Start the server:
   ```bash
   python -m mcp_messaging.server
   ```

2. Connect MCP client and test tools:
   ```bash
   # Check in as a client
   checkin_client("client_1", "Test Client", "Testing capabilities")
   
   # Send a message
   send_message("client_1", "client_2", "Hello from client 1!")
   
   # Retrieve messages (as client_2)
   get_messages("client_2")
   
   # Get identity help
   get_my_identity()
   ```

## 📝 Development

### Project Structure

```
src/mcp_messaging/
├── __init__.py
├── server.py          # Main server implementation
├── models.py          # Data models and utilities
└── queue_backends.py  # Queue backend implementations

examples/
├── mcp_recipients.example.json  # Configuration template
└── reference/                   # Reference implementations

Dockerfile             # Container build configuration
```

### Key Design Principles

1. **Stateless**: No persistent state between requests
2. **Secure**: Client IDs as credentials
3. **Simple**: Minimal configuration required
4. **Reliable**: Automatic cleanup and error handling
5. **Standard**: Pure MCP HTTP Streamable protocol

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details on:

- Setting up the development environment
- Code style and testing guidelines
- Submitting pull requests
- Reporting issues

### Quick Start for Contributors

```bash
# Fork and clone the repository
git clone https://github.com/your-username/mcp-ide-bridge.git
cd mcp-ide-bridge

# Set up development environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e .

# Run the server
python -m mcp_messaging.server
```

## 🛣️ Roadmap

### Phase 1: ✅ Core Implementation
- [x] Stateless message queues
- [x] Basic MCP tools
- [x] Message expiration
- [x] Markdown formatting
- [x] Docker containerization

### Phase 2: 🚧 Enhancement
- [ ] Redis queue backend
- [ ] Performance tuning
- [ ] Queue size limits
- [ ] Comprehensive test suite

### Phase 3: 🔮 Advanced Features
- [ ] Token-based authentication
- [ ] Message encryption
- [ ] Rate limiting
- [ ] Audit logging

## 🔒 Security

Security is a top priority. Please see our [Security Policy](SECURITY.md) for:

- Reporting vulnerabilities responsibly
- Security best practices
- Supported versions
- Contact information

**Note**: This is early-stage software. Please review security considerations before production use.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Developed by [MVP2o.ai](https://mvp2o.ai) for the open source community
- Built with [FastMCP](https://github.com/jlowin/fastmcp) framework
- Follows [MCP Protocol](https://spec.modelcontextprotocol.io/) specifications
- Inspired by the need for seamless IDE-to-IDE communication

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/wiltshirek/mcp-ide-bridge/issues)
- **Discussions**: [GitHub Discussions](https://github.com/wiltshirek/mcp-ide-bridge/discussions)
- **Security**: See [SECURITY.md](SECURITY.md) for security-related concerns

---

**Built with MCP HTTP Streamable transport** • **Powered by FastMCP** • **Made with ❤️ by MVP2o.ai**
