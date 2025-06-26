"""Simple tests to verify basic functionality."""

import asyncio
from datetime import datetime

from mcp_messaging.server import MessagingServer
from mcp_messaging.models import Message


async def test_basic_messaging():
    """Test basic message sending and receiving."""
    server = MessagingServer()
    
    # Send a message
    result = await server.send_message("sender1", "recipient1", "Hello world!")
    assert "✅ Message sent successfully" in result
    
    # Get the message
    messages = await server.get_messages("recipient1")
    assert "Hello world!" in messages
    assert "sender1" in messages


async def test_client_checkin():
    """Test client checkin functionality."""
    server = MessagingServer()
    
    result = server.checkin_client("client1", "Test Client", "Test capabilities")
    assert "✅ Successfully checked in" in result
    assert "client1" in result


def test_message_model():
    """Test Message model creation."""
    timestamp = datetime.now()
    message = Message(
        from_client_id="sender1",
        content="Test content",
        timestamp=timestamp
    )
    
    assert message.from_client_id == "sender1"
    assert message.content == "Test content"
    assert message.timestamp == timestamp


if __name__ == "__main__":
    # Run the async tests
    asyncio.run(test_basic_messaging())
    asyncio.run(test_client_checkin())
    test_message_model()
    print("✅ All basic tests passed!") 