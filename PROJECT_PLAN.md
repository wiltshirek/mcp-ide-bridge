# MCP HTTP Streamable Messaging Server - Project Plan

## Phase 1: Project Restructuring & Setup ✅
- [x] Create standard Python project structure
- [x] Set up Python 3.11 virtual environment support
- [x] Create proper pyproject.toml with MCP dependencies
- [x] Move weather.py to examples/reference directory
- [x] Create main server module structure
- [x] Set up .env configuration
- [x] Create .gitignore for Python project

## Phase 2: MCP HTTP Streamable Server Foundation ✅
- [x] Implement base MCP server using FastMCP
- [x] Configure HTTP Streamable transport properly
- [x] Set up proper session management
- [x] Implement basic server lifecycle (initialize, etc.)
- [x] Add proper logging and error handling
- [x] Test basic MCP connection with simple client

## Phase 3: Client-to-Client Messaging Core (Stateless Architecture) ✅
- [x] Design stateless message queue system (queues named by recipient_id)
- [x] Implement dynamic client discovery (no pre-registration needed)
- [x] Create pure MCP HTTP Streamable messaging (no separate SSE)
- [x] Design tools for:
  - [x] `checkin_client` - Parameters: client_id, name, capabilities (static project description placeholder)
  - [x] `send_message` - Parameters: sender_id (read from 'my_id' in local mcp_recipients.json), recipient_id (from 'recipients' section), message
  - [x] `get_messages` - Parameters: client_id (returns formatted markdown, pops messages immediately)
  - [x] `get_my_identity` - Return static message: "Check your local mcp_recipients.json file for your client ID and available recipients"
- [x] Implement in-memory message queues by recipient_id
- [x] Add 5-minute message expiration (cleanup on send/get message calls)
- [x] Messages popped immediately when retrieved (no persistence)
- [x] Add basic logging for message flow and errors
- [x] No duplicate detection - accept all messages as-is
- [x] Future: Leverage MCP heartbeat events for advanced cleanup

## Phase 4: Queue Abstraction & Blocking Implementation ✅
- [x] Design abstract QueueBackend interface (Redis-compatible design)
- [x] Implement InMemoryQueueBackend with asyncio.Event wake-up
- [x] Refactor MessagingServer to use pluggable queue backend
- [x] Implement `send_message_and_wait` tool with blocking support
- [x] Add 60-second timeout with graceful error handling
- [x] Support concurrent blocked calls per client
- [x] Test end-to-end conversational flow
- [x] Validate architecture is Redis-ready for future implementation

## Phase 4.5: Redis Queue Backend (Future)
- [ ] Implement RedisQueueBackend with pub/sub notifications
- [ ] Add Redis connection configuration via environment variables
- [ ] Test blocking behavior with Redis backend
- [ ] Performance comparison: in-memory vs Redis
- [ ] Documentation for Redis deployment scenarios

## Phase 5: Performance Optimization
- [ ] Optimize message queue performance for high throughput
- [ ] Implement queue size limits and overflow handling (drop oldest)
- [ ] Add concurrent access protection for message queues
- [ ] Memory optimization for high-frequency messaging
- [ ] Performance testing with multiple concurrent clients and blocked calls

## Phase 6: Testing & Refinement
- [ ] Create test client for validation
- [ ] Test multi-client conversation scenarios
- [ ] Test timeout and error handling
- [ ] Performance testing with multiple connections
- [ ] Documentation and examples

## Key Technical Considerations

### Stateless Architecture Benefits:
- **Security Through Obscurity**: Client IDs act as secure tokens
- **Dynamic Discovery**: No pre-configuration required
- **Simple Scaling**: Stateless design allows horizontal scaling
- **Fault Tolerance**: No persistent state to corrupt or lose

### Architecture Notes:
- **Message Queues**: Named by recipient_id, created on-demand
- **Queue Backends**: Pluggable interface (in-memory, Redis, Memcache)
- **Message Lifecycle**: 5-minute expiration, immediate pop on retrieval
- **Message Cleanup**: Triggered on send_message/get_messages calls (not background tasks)
- **Client Discovery**: Optional checkin with client_id, name, static capabilities description
- **Security Model**: Client IDs are treated as security credentials
- **Pure MCP HTTP**: No separate SSE endpoints (SSE deprecated)
- **Stateless Design**: No client tracking, no duplicate detection, no conversation IDs
- **Parameter Descriptions**: Guide LLM to read mcp_recipients.json locally
- **Message Format**: Markdown formatted with sender, timestamp, content
- **Blocking Responses**: send_message_and_wait blocks until response appears in sender's queue
- **Wake-up Mechanism**: Compatible with external pub/sub systems (Redis) or polling

### Future Security Enhancements:
- **Phase 7: Cryptographic Security**
  - [ ] Implement private/public key pairs for message signing
  - [ ] Server verifies message authenticity using sender's public key
  - [ ] Add message encryption for sensitive communications
  - [ ] Implement key rotation and revocation mechanisms

## Current Status
🎉 **Phase 4 Complete!** - Blocking response mechanism implemented and tested

**Core Features Implemented ✅:**
- **Stateless MCP HTTP Streamable messaging server**
- **5 MCP tools**: checkin_client, send_message, send_message_and_wait, get_messages, get_my_identity  
- **Pluggable queue backend architecture** (Redis-ready)
- **Blocking conversation support** with 60-second timeout
- **asyncio.Event-based wake-up mechanism** for real-time responses
- **5-minute message expiration** with on-demand cleanup
- **Markdown formatted responses** with relative timestamps
- **Complete Python 3.11+ environment** with proper packaging

**Key Architectural Achievement:**
- **True conversational flow**: Client A can send a message and block until Client B responds
- **Stateless design**: No conversation tracking, just queue-based wake-up
- **Future-ready**: Abstract QueueBackend interface ready for Redis implementation

**Ready for Production Testing:**
- Server running on localhost:8123
- All tools functional and tested
- Environment properly configured

**Next steps:** 
- Test with real MCP clients (Cursor)
- Implement Redis backend when needed (Phase 4.5)
- Performance optimization (Phase 5) 