"""MCP HTTP Streamable messaging server for client-to-client communication."""

import argparse
import asyncio
import json
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

import httpx
import uvicorn
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import JSONResponse
# Removed pydantic BaseModel - no longer needed

from .models import Message, format_relative_time
from .queue_backends import QueueBackend, InMemoryQueueBackend

# Load environment variables
load_dotenv()

# Configure logging with a more detailed format
logging.basicConfig(
    level=getattr(logging, os.getenv("LOG_LEVEL", "INFO")),
    format="%(asctime)s - %(name)s - %(levelname)s\n%(message)s\n"  # Added newline for better readability
)
logger = logging.getLogger(__name__)

# Default configuration values
DEFAULT_CONFIG = {
    "max_tokens": 4096,
    "max_iterations": 10,
    "timeouts": {
        "send_message_and_wait": 180.0,  # 3 minutes
        "get_messages": 60.0,  # 1 minute
        "message_expiration": 300.0  # 5 minutes
    }
}

# Global client tracking (in-memory)
client_activity_tracking: Dict[str, Dict] = {}

def update_client_activity(recipients_config: Dict, queue_backend: Optional[QueueBackend] = None) -> None:
    """Update client activity tracking from required recipients_config."""
    client_id = recipients_config.get("my_id")
    if not client_id:
        return
    
    # Extract client info from config
    client_info = {
        "client_id": client_id,
        "name": recipients_config.get("my_name", client_id),
        "description": recipients_config.get("my_description", ""),
        "clientType": recipients_config.get("clientType", "agent by IDE"),
        "last_seen": datetime.now().isoformat(),
        "messages_in_queue": 0  # Will be updated below
    }
    
    # Update messages in queue count
    if queue_backend and hasattr(queue_backend, 'queues'):
        queue_messages = queue_backend.queues.get(client_id, [])
        client_info["messages_in_queue"] = len(queue_messages)
    
    # Store in global tracking
    client_activity_tracking[client_id] = client_info

# Configuration management removed - now handled by clients

# File reading and callback functions removed - unified client approach means no server-side file I/O


# Callback functionality removed - unified client approach


def format_message_log(action: str, sender_id: str, recipient_id: str, message: str) -> str:
    """Format a message log entry with complete details."""
    return f"""
MESSAGE {action.upper()}
FROM: {sender_id}
TO: {recipient_id}
CONTENT:
{message}
{"=" * 80}"""

# Client type detection removed - all clients treated uniformly

# Removed format_ide_client_identity - no longer needed with unified approach

# External client formatting removed - unified approach

class MessagingServer:
    """Core stateless messaging server for client-to-client communication."""
    
    def __init__(self, queue_backend: Optional[QueueBackend] = None) -> None:
        self.queue_backend = queue_backend or InMemoryQueueBackend()
        logger.info(f"MessagingServer initialized with {type(self.queue_backend).__name__}")
    
    async def send_message(self, sender_id: str, recipient_id: str, content: str) -> str:
        """Send a message from sender to recipient."""
        
        # Cleanup expired messages before processing
        await self.queue_backend.cleanup_expired_messages()
        
        # Validate inputs
        if not sender_id.strip():
            return "❌ **Error**: Sender ID cannot be empty"
        
        if not recipient_id.strip():
            return "❌ **Error**: Recipient ID cannot be empty"
            
        if not content.strip():
            return "⚠️ **Warning**: Sending empty message"
        
        # Create message
        message = Message(
            from_client_id=sender_id,
            content=content,
            timestamp=datetime.now()
        )
        
        # Send message via queue backend
        await self.queue_backend.send_message(recipient_id, message)
        
        # Notify any blocked calls waiting for this recipient
        await self.queue_backend.notify_new_message(recipient_id)
        
        # Log complete message details
        logger.info(format_message_log("sent", sender_id, recipient_id, content))
        
        return f"✅ **Message sent successfully** to `{recipient_id}`"
    
    async def send_message_and_wait(self, sender_id: str, recipient_id: str, content: str) -> str:
        """Send a message and wait for a response (blocking call)."""
        # Use default timeout
        timeout = DEFAULT_CONFIG["timeouts"]["send_message_and_wait"]
        
        # First, send the message
        send_result = await self.send_message(sender_id, recipient_id, content)
        
        # If send failed, return the error
        if send_result.startswith("❌") or send_result.startswith("⚠️"):
            return send_result
        
        logger.info(f"Waiting for response to {sender_id} (timeout: {timeout}s)")
        
        # Wait for a response to arrive in sender's queue
        message_arrived = await self.queue_backend.wait_for_new_message(sender_id, timeout)
        
        if message_arrived:
            # Get the response messages
            messages = await self.queue_backend.get_messages(sender_id, pop=True)
            if messages:
                return self._format_messages_as_markdown(sender_id, messages)
            else:
                return "📭 **No response received** (queue was empty)"
        else:
            return f"⏰ **Timeout**: No response received within {timeout} seconds"
    
    async def send_message_without_waiting(self, sender_id: str, recipients: List[str], messages: List[str]) -> str:
        """Send messages (fire and forget) to multiple recipients and return any pending messages for sender."""
        # Validate inputs
        if not recipients:
            return "❌ **Error**: At least one recipient must be specified"
        
        if not messages:
            return "❌ **Error**: At least one message must be specified"
        
        if len(messages) != len(recipients):
            return f"❌ **Error**: Number of messages ({len(messages)}) must match number of recipients ({len(recipients)})"
        
        # Send messages to all recipients
        send_results = []
        failed_sends = []
        
        for recipient_id, content in zip(recipients, messages):
            send_result = await self.send_message(sender_id, recipient_id, content)
            
            if send_result.startswith("❌") or send_result.startswith("⚠️"):
                failed_sends.append(f"  - **{recipient_id}**: {send_result}")
            else:
                send_results.append(f"  - **{recipient_id}**: ✅ Message sent")
        
        # Format results
        total_recipients = len(recipients)
        successful_sends = len(send_results)
        
        result_parts = [
            f"📡 **Message Delivery Complete** ({successful_sends}/{total_recipients} successful)",
            ""
        ]
        
        if send_results:
            result_parts.extend(["**✅ Successful sends:**"] + send_results + [""])
        
        if failed_sends:
            result_parts.extend(["**❌ Failed sends:**"] + failed_sends + [""])
        
        # Get any pending messages for the sender (non-blocking)
        await self.queue_backend.cleanup_expired_messages()
        pending_messages_list = await self.queue_backend.get_messages(sender_id, pop=True)
        
        if pending_messages_list:
            # Format both send results and pending messages
            pending_messages = self._format_messages_as_markdown(sender_id, pending_messages_list)
            result_parts.extend(["---", "", pending_messages])
        else:
            # Just the send results
            result_parts.extend(["💡 **Tip**: Use `get_messages` to check for responses later."])
        
        return "\n".join(result_parts)
    
    async def get_messages(self, client_id: str) -> str:
        """Get and remove all messages for a client, formatted as markdown."""
        # Use default timeout
        timeout = DEFAULT_CONFIG["timeouts"]["get_messages"]
        
        # Cleanup expired messages before processing
        await self.queue_backend.cleanup_expired_messages()
        
        # Validate input
        if not client_id.strip():
            return "❌ **Error**: Client ID cannot be empty"
        
        # Get messages from queue backend
        messages = await self.queue_backend.get_messages(client_id, pop=True)
        
        if not messages:
            # No messages found - block for configured timeout
            logger.debug(f"No messages found for {client_id}, waiting {timeout} seconds...")
            
            message_arrived = await self.queue_backend.wait_for_new_message(client_id, timeout)
            
            if message_arrived:
                # Get the new messages that arrived
                messages = await self.queue_backend.get_messages(client_id, pop=True)
                if messages:
                    logger.info(f"Retrieved {len(messages)} messages for {client_id} after waiting")
                    return self._format_messages_as_markdown(client_id, messages)
                else:
                    return "📭 **No messages** for you right now."
            else:
                logger.debug(f"Timeout waiting for messages for {client_id}")
                return "📭 **No messages** for you right now.\n\n💡 **Tip:** Be sure you are using your client_id (`my_id`) from your `mcp_recipients.json` file, and try again."
        
        logger.info(f"Retrieved and popped {len(messages)} messages for {client_id}")
        
        return self._format_messages_as_markdown(client_id, messages)
    
    def _format_messages_as_markdown(self, client_id: str, messages: List[Message]) -> str:
        """Format messages as markdown."""
        message_count = len(messages)
        markdown_parts = [f"## 📨 Messages for `{client_id}` ({message_count} message{'s' if message_count != 1 else ''})", ""]
        
        for msg in messages:
            relative_time = format_relative_time(msg.timestamp)
            markdown_parts.extend([
                f"**From:** `{msg.from_client_id}`  ",
                f"**Time:** {relative_time}  ",
                f"**Message:** {msg.content}",
                "",
                "---",
                ""
            ])
        
        return "\n".join(markdown_parts)
    
    def checkin_client(self, client_id: str, name: str, capabilities: str) -> str:
        """Client checkin (for future features, currently just logs)."""
        if not client_id.strip():
            return "❌ **Error**: Client ID cannot be empty"
        
        # Create/update client info in tracking
        client_info = {
            "client_id": client_id,
            "name": name,
            "description": capabilities,
            "clientType": "checked-in client",
            "last_seen": datetime.now().isoformat(),
            "messages_in_queue": 0  # Will be updated below
        }
        
        # Update messages in queue count
        if hasattr(self.queue_backend, 'queues'):
            queue_messages = self.queue_backend.queues.get(client_id, [])
            client_info["messages_in_queue"] = len(queue_messages)
        
        # Store in global tracking
        client_activity_tracking[client_id] = client_info
        
        logger.info(f"Client checkin - ID: {client_id}, Name: {name}, Capabilities: {capabilities}")
        
        return f"👋 **Checked in successfully** as `{client_id}`  \n**Name:** {name}  \n**Capabilities:** {capabilities}"


# Initialize the messaging server and FastMCP
messaging_server = MessagingServer(
    queue_backend=InMemoryQueueBackend(
        message_expiration_seconds=DEFAULT_CONFIG["timeouts"]["message_expiration"]
    )
)

# Initialize FastMCP with HTTP Streamable transport
mcp = FastMCP(
    name="messaging-server",
    description="MCP server for client-to-client messaging using HTTP Streamable transport. Messaging capabilities are determined by each client's mcp_recipients list, which defines available recipients and client identity. All messaging tools require recipients_config parameter for client activity tracking and proper message routing.",
    stateless_http=True,  # Use stateless HTTP for Streamable HTTP transport
    json_response=False   # Use SSE streaming format for richer client experience
)


@mcp.tool()
async def checkin_client(client_id: str, name: str, capabilities: str = "Generic project description") -> str:
    """Check in as a client to announce your presence.
    
    Args:
        client_id: Your unique client ID. **This should be the `my_id` field from your local `mcp_recipients.json` file. Do not use an arbitrary value.**
        name: Display name for this client instance. **This should match the `my_name` field from your local `mcp_recipients.json` file.**
        capabilities: Description of client capabilities (default: Generic project description)
        
    Returns:
        Confirmation of successful checkin
    
    **Note:** For correct identity and attribution, always use the values from your configured `mcp_recipients.json` file. If you are unsure, ask your project lead for the correct configuration.
    """
    result = messaging_server.checkin_client(client_id, name, capabilities)
    return result


async def send_message_and_wait(sender_id: str, recipient_id: str, message: str, expectation: str = "response_expected") -> str:
    """Send message and wait for immediate response. **Use only when you need to block and wait.**
    
    **🚨 IMPORTANT**: This blocks for 3 minutes waiting for response! 
    **💡 For most cases, use send_message_without_waiting instead.**
    
    **When to use:**
    - ✅ Need to wait for immediate response before continuing
    - ✅ Urgent situations requiring immediate reply
    - ❌ DO NOT make rapid multiple calls (use fire-and-forget instead)
    
    Args:
        sender_id: Your client ID
        recipient_id: The recipient's client ID
        message: The message content to send
        expectation: Response expectation - one of:
            - "response_expected": I expect a response via send_message_and_wait
            - "no_response": I do not expect a response
            - "end_conversation": End of conversation
        
    Returns:
        The response message(s) in markdown format, or timeout message (3 minute timeout)
    """
    # Append expectation to message with emphasis
    expectation_text = {
        "response_expected": "**📬 I expect a response via send_message_and_wait**",
        "no_response": "**📭 I do not expect a response**", 
        "end_conversation": "**🔚 End of conversation**"
    }
    
    formatted_message = f"{message}\n\n---\n{expectation_text.get(expectation, expectation_text['response_expected'])}"
    
    # Fire and forget for no_response - don't block
    if expectation == "no_response":
        result = await messaging_server.send_message(sender_id, recipient_id, formatted_message)
        return f"📭 **Message sent** (no response expected)\n\n{result}"
    
    # Block and wait for response (original behavior)
    return await messaging_server.send_message_and_wait(sender_id, recipient_id, formatted_message)


@mcp.tool()
async def send_message_without_waiting(sender_id: str, recipients: List[Dict[str, str]], recipients_config: Dict) -> str:
    """Send messages to one or more recipients instantly (fire & forget).
    
    **🔄 WORKFLOW**: Send messages → then call get_messages to check for replies.
    
    **Features:**
    - ✅ **INSTANT** - No blocking, immediate return
    - ✅ **SCALABLE** - Send to one or more recipients in single call
    - ✅ **EFFICIENT** - Fast messaging for all use cases
    
    **Next Step:** Call get_messages to check for responses from recipients.
    
    Args:
        sender_id: Your client ID
        recipients: List of recipient-message mappings, where each item is {"id": recipient_id, "message": message_content}
        recipients_config: Configuration for the sender
        
    Returns:
        Send results showing success/failure for each recipient, plus any pending messages for you
        
    Examples:
        - Multiple recipients: recipients=[{"id": "alice", "message": "Review code"}, {"id": "bob", "message": "Check UI"}]
        - Single recipient: recipients=[{"id": "alice", "message": "Quick question about the API"}]
    """
    # Update client activity tracking
    update_client_activity(recipients_config, messaging_server.queue_backend)
    
    # Extract recipient IDs and messages from the mappings
    recipient_ids = [r["id"] for r in recipients]
    messages = [r["message"] for r in recipients]
    
    result = await messaging_server.send_message_without_waiting(sender_id, recipient_ids, messages)
    return result


@mcp.tool()
async def get_messages(client_id: str, recipients_config: Dict) -> str:
    """📬 **ESSENTIAL WORKFLOW STEP** - Check for replies after using send_message_without_waiting.
    
    **🔄 RECOMMENDED WORKFLOW**: 
    1. Use send_message_without_waiting to send messages
    2. Call get_messages to check for replies
    3. Repeat as needed for ongoing conversations
    
    **Behavior**: 
    - ⏰ Waits up to 60 seconds for new messages if queue is empty
    - 🗑️ Messages are removed from queue after retrieval
    - 📥 Returns all pending messages in one call
    
    Args:
        client_id: Your client ID
        
    Returns:
        Your messages formatted in markdown (blocks up to 60 seconds waiting for new messages)
    """
    # Update client activity tracking
    update_client_activity(recipients_config, messaging_server.queue_backend)
    
    result = await messaging_server.get_messages(client_id)
    return result


@mcp.tool()
async def get_my_identity(recipients_config: Dict) -> str:
    """Get information about your client identity and available recipients.
    
    Returns:
        Instructions for finding your client configuration
    """
    # Update client activity tracking
    update_client_activity(recipients_config, messaging_server.queue_backend)
    
    return """## 🆔 Client Identity & Recipients

## Your Client Configuration
Please check your local `mcp_recipients.json` file in your project root folder for:
- **Your client ID** (my_id field)  
- **Available recipients** (recipients section)

## Local File Location
Look for `mcp_recipients.json` in your project directory.

## Usage
Use your client ID for `sender_id` and recipient IDs for `recipient_id` parameters in other messaging tools."""



async def _get_active_sessions_internal() -> str:
    """Internal function to get information about active messaging clients.
    
    Returns:
        JSON information about recently active messaging clients including last seen times
    """
    try:
        # Get queue statistics
        if hasattr(messaging_server.queue_backend, 'get_queue_stats'):
            queue_stats = messaging_server.queue_backend.get_queue_stats()
        else:
            queue_stats = {
                "total_queues": len(getattr(messaging_server.queue_backend, 'queues', {})),
                "total_messages": sum(len(msgs) for msgs in getattr(messaging_server.queue_backend, 'queues', {}).values()),
                "active_waiters": len(getattr(messaging_server.queue_backend, 'notification_events', {}))
            }
        
        # Update message counts for all queues, even if client isn't tracked
        messaging_clients = []
        for client_id, queue in messaging_server.queue_backend.queues.items():
            client_info = client_activity_tracking.get(client_id, {
                "client_id": client_id,
                "name": client_id,
                "description": "Client with messages in queue",
                "clientType": "untracked client",
                "last_seen": datetime.now().isoformat()
            })
            client_info["messages_in_queue"] = len(queue)
            messaging_clients.append(client_info)
        
        # Add tracked clients that don't have queues
        for client_id, client_info in client_activity_tracking.items():
            if client_id not in messaging_server.queue_backend.queues:
                client_info["messages_in_queue"] = 0
                messaging_clients.append(client_info)
        
        # Create the response structure with total_messages at root level for frontend compatibility
        response = {
            "messagingClients": messaging_clients,
            "queueStats": queue_stats,
            "total_messages": queue_stats["total_messages"]  # Add total_messages at root level
        }
        
        return json.dumps(response, indent=2)
        
    except Exception as e:
        logger.error(f"Error getting session info: {e}")
        error_msg = f"❌ **Error**: Could not retrieve session information: {str(e)}"
        return error_msg


@mcp.custom_route("/api/sessions", methods=["GET", "OPTIONS"])
async def get_sessions_json(request):
    """REST endpoint for session statistics - returns pure JSON for normal REST clients."""
    # Handle CORS preflight requests
    if request.method == "OPTIONS":
        headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type, Authorization"
        }
        return JSONResponse(content={}, headers=headers)
    
    try:
        # Call our internal get_active_sessions function
        result = await _get_active_sessions_internal()
        
        # Parse the JSON result and return as JSONResponse with CORS headers
        data = json.loads(result)
        headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type, Authorization"
        }
        return JSONResponse(content=data, headers=headers)
        
    except Exception as e:
        logger.error(f"Error getting session JSON: {e}")
        error_data = {"error": f"Could not retrieve session information: {str(e)}"}
        headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type, Authorization"
        }
        return JSONResponse(content=error_data, status_code=500, headers=headers)


# REST endpoints for client registration removed - now handled by client-side parameter injection


def main() -> None:
    """Main entry point for the messaging server."""
    parser = argparse.ArgumentParser(description="MCP HTTP Streamable messaging server")
    parser.add_argument(
        "--port", 
        type=int, 
        default=int(os.getenv("MCP_SERVER_PORT", "8123")),
        help="Port to listen on"
    )
    parser.add_argument(
        "--host",
        type=str,
        default=os.getenv("MCP_SERVER_HOST", "localhost"),
        help="Host to bind to"
    )
    parser.add_argument(
        "--queue-backend",
        type=str,
        default=os.getenv("QUEUE_BACKEND", "memory"),
        choices=["memory"],  # Future: add "redis"
        help="Queue backend to use"
    )
    args = parser.parse_args()
    
    logger.info(f"Starting MCP messaging server on {args.host}:{args.port}")
    logger.info(f"Queue backend: {type(messaging_server.queue_backend).__name__}")
    logger.info("Tools available: checkin_client, send_message_without_waiting, get_messages, get_my_identity")
    
    # Start the server with HTTP Streamable transport
    # Configure host and port via FastMCP settings
    mcp.settings.host = args.host
    mcp.settings.port = args.port
    
    print(f"🚀 Starting MCP messaging server at http://{args.host}:{args.port}")
    logger.info("MCP messaging server starting", extra={"host": args.host, "port": args.port})
    
    mcp.run(transport="streamable-http")


if __name__ == "__main__":
    main()