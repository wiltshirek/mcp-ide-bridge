"""Simple MCP connection test - no Anthropic API required"""

import argparse
import asyncio
from contextlib import AsyncExitStack

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client


class MCPConnectionTest:
    """Simple test to verify MCP connection and tool listing"""

    def __init__(self):
        self.session: ClientSession = None
        self.exit_stack = AsyncExitStack()

    async def connect_to_streamable_http_server(self, server_url: str):
        """Connect to an MCP server running with HTTP Streamable transport"""
        print(f"🔌 Connecting to MCP server at: {server_url}")
        
        self._streams_context = streamablehttp_client(
            url=server_url,
            headers={},
        )
        read_stream, write_stream, _ = await self._streams_context.__aenter__()

        self._session_context = ClientSession(read_stream, write_stream)
        self.session: ClientSession = await self._session_context.__aenter__()

        print("📡 Initializing MCP session...")
        await self.session.initialize()
        print("✅ MCP session initialized successfully!")

    async def test_list_tools(self):
        """Test listing available tools"""
        print("\n🔧 Testing tool listing...")
        
        try:
            response = await self.session.list_tools()
            print(f"✅ Successfully listed {len(response.tools)} tools:")
            
            for i, tool in enumerate(response.tools, 1):
                print(f"  {i}. {tool.name}")
                print(f"     Description: {tool.description}")
                print()
            
            return True
            
        except Exception as e:
            print(f"❌ Error listing tools: {str(e)}")
            return False

    async def cleanup(self):
        """Properly clean up the session and streams"""
        print("\n🧹 Cleaning up connection...")
        if self._session_context:
            await self._session_context.__aexit__(None, None, None)
        if self._streams_context:
            await self._streams_context.__aexit__(None, None, None)
        print("✅ Cleanup completed!")


async def main():
    """Main function to run the connection test"""
    parser = argparse.ArgumentParser(description="Test MCP Streamable HTTP connection")
    parser.add_argument(
        "--mcp-localhost-port", type=int, default=8111, help="Localhost port to connect to"
    )
    args = parser.parse_args()

    client = MCPConnectionTest()

    try:
        await client.connect_to_streamable_http_server(
            f"http://localhost:{args.mcp_localhost_port}/mcp"
        )
        
        success = await client.test_list_tools()
        
        if success:
            print("\n🎉 SUCCESS: MCP client can connect and list tools!")
            print("   The messaging server is working correctly.")
        else:
            print("\n💥 FAILED: Could not list tools from the server.")
            
    except Exception as e:
        print(f"\n❌ Connection failed: {str(e)}")
    finally:
        await client.cleanup()


if __name__ == "__main__":
    asyncio.run(main()) 