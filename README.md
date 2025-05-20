# MCP Streamable HTTP – Python and Typescript Examples

This repository provides example implementations of MCP (Model Context Protocol) **Streamable HTTP client and server** in Python and Typescript, based on the specification:  
📄 [MCP Streamable HTTP Spec](https://modelcontextprotocol.io/specification/2025-03-26/basic/transports#streamable-http).

You can set up a client and server using either Python or TypeScript. This example also demonstrates cross-language compatibility, allowing a Python client to communicate with a TypeScript server, and vice-versa.

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/invariantlabs-ai/mcp-streamable-http.git
cd python-example
```

### 2. Python Example

#### 1. Add Your Anthropic API Key

Update the `.env` file inside the `python-example/client` directory with the following content:

```env
ANTHROPIC_API_KEY=your_api_key_here
```

#### 2. Set Up the Server

```bash
cd python-example/server
pip install .
python weather.py
```

By default, the server will start at `http://localhost:8123`.  
If you'd like to specify a different port, use the `--port` flag:

```bash
python weather.py --port=9000
```

#### 3. Set Up the Client

```bash
cd ../client
pip install .
```

#### 4. Run the Client

```bash
python client.py
```

This will start an **interactive chat loop** using the MCP Streamable HTTP protocol.  
If you started the MCP server on a different port, specify it using the `--mcp-localhost-port` flag:

```bash
python client.py --mcp-localhost-port=9000
```

### 3. Typescript Example

#### 1. Add Your Anthropic API Key

Update the `.env` file inside the `typescript-example/client` directory with the following content:

```env
ANTHROPIC_API_KEY=your_api_key_here
```

#### 2. Set Up the Server

```bash
cd typescript-example/server
npm install && npm run build
node build/index.js
```

By default, the server will start at `http://localhost:8123`.  
If you'd like to specify a different port, use the `--port` flag:

```bash
node build/index.js --port=9000
```

#### 3. Set Up the Client

```bash
cd ../client
npm install && npm run build
```

#### 4. Run the Client

```bash
node build/index.js
```

This will start an **interactive chat loop** using the MCP Streamable HTTP protocol.  
If you started the MCP server on a different port, specify it using the `--mcp-localhost-port` flag:

```bash
node build/index.js --mcp-localhost-port=9000
```

---

## 💬 Example Queries

In the client chat interface, you can ask questions like:

- “Are there any weather alerts in Sacramento?”
- “What’s the weather like in New York City?”
- “Tell me the forecast for Boston tomorrow.”

The client will forward requests to the local MCP weather server and return the results using Anthropic’s Claude language model. The transport layer used will Streamable HTTP.
