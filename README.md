# MCP Streamable HTTP – Python Example

This repository provides an example implementation of an MCP (Model Context Protocol) **Streamable HTTP client and server** in Python, based on the specification:  
📄 [MCP Streamable HTTP Spec](https://modelcontextprotocol.io/specification/2025-03-26/basic/transports#streamable-http)


## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/invariantlabs-ai/mcp-streamable-http.git
cd python-example
```

### 2. Add Your Anthropic API Key

Update the `.env` file inside the `client` directory with the following content:

```env
ANTHROPIC_API_KEY=your_api_key_here
```

### 3. Set Up the Server

```bash
cd server
pip install .
python weather.py
```

By default, the server will start at `http://localhost:8123`.  
If you'd like to specify a different port, use the `--port` flag:

```bash
python weather.py --port 9000
```

### 4. Set Up the Client

```bash
cd ../client 
pip install .
```

### 5. Run the Client

```bash
python client.py
```

This will start an **interactive chat loop** using the MCP Streamable HTTP protocol.  
If you started the MCP server on a different port, specify it using the `--mcp-localhost-port` flag:

```bash
python client.py --mcp-localhost-port 9000
```

---

## 💬 Example Queries

In the client chat interface, you can ask questions like:

- “Are there any weather alerts in Sacramento?”
- “What’s the weather like in New York City?”
- “Tell me the forecast for Boston tomorrow.”

The client will forward requests to the local MCP weather server and return the results using Anthropic’s Claude language model. The transport layer used will Streamable HTTP.
