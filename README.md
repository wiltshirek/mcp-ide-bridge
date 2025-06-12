# MCP Messaging Server

A stateless MCP (Model Context Protocol) HTTP Streamable server for client-to-client messaging. This server enables secure, real-time communication between different IDE instances, development tools, or applications using the MCP protocol.

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

```bash
# Default: localhost:8123
python -m mcp_messaging.server

# Custom host/port
python -m mcp_messaging.server --host 0.0.0.0 --port 9000
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
└── server.py          # Main server implementation

examples/
└── reference/          # Original weather.py example

tests/                  # Future test suite
```

### Key Design Principles

1. **Stateless**: No persistent state between requests
2. **Secure**: Client IDs as credentials
3. **Simple**: Minimal configuration required
4. **Reliable**: Automatic cleanup and error handling
5. **Standard**: Pure MCP HTTP Streamable protocol

## 🛣️ Roadmap

### Phase 1: ✅ Core Implementation
- [x] Stateless message queues
- [x] Basic MCP tools
- [x] Message expiration
- [x] Markdown formatting

### Phase 2: 🚧 Optimization
- [ ] Performance tuning
- [ ] Queue size limits
- [ ] Concurrent access protection
- [ ] Memory optimization

### Phase 3: 🔮 Security Enhancement
- [ ] Public/private key authentication
- [ ] Message encryption
- [ ] Key rotation
- [ ] Audit logging

## 🔒 Security Considerations

- **Client IDs**: Treat as secure tokens, don't expose in logs
- **Network**: Bind to localhost for local development
- **Messages**: Currently unencrypted (future enhancement)
- **Access**: No authentication beyond client ID knowledge

## 📄 License

[Your License Here]

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

---

**Built with MCP HTTP Streamable transport** • **Powered by FastMCP**
