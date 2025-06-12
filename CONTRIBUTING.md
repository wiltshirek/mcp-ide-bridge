# Contributing to MCP IDE Bridge

Thank you for your interest in contributing to the MCP IDE Bridge project! This document provides guidelines for contributing to this open source MCP (Model Context Protocol) messaging server.

## 🚀 Getting Started

### Prerequisites
- Python 3.11 or higher
- Docker and Docker Compose (for containerized development)
- Git

### Development Setup

1. **Fork and Clone**
   ```bash
   git clone https://github.com/your-username/mcp-ide-bridge.git
   cd mcp-ide-bridge
   ```

2. **Set up Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -e .
   ```

4. **Run the Server**
   ```bash
   python -m mcp_messaging.server
   ```

## 🛠️ Development Guidelines

### Code Style
- Follow PEP 8 Python style guidelines
- Use type hints where appropriate
- Write descriptive docstrings for functions and classes
- Keep functions focused and modular

### Testing
- Write tests for new features
- Ensure existing tests pass before submitting PRs
- Test both success and error cases
- Include integration tests for MCP protocol compliance

### Documentation
- Update README.md for user-facing changes
- Document new configuration options
- Include examples for new features
- Update API documentation

## 📋 How to Contribute

### Reporting Issues
- Use GitHub Issues to report bugs or request features
- Include detailed reproduction steps for bugs
- Provide system information (OS, Python version, etc.)
- Check existing issues before creating new ones

### Submitting Changes

1. **Create a Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make Your Changes**
   - Write clean, well-documented code
   - Follow the existing code style
   - Add tests for new functionality

3. **Test Your Changes**
   ```bash
   # Run tests (when test suite is available)
   python -m pytest
   
   # Test Docker build
   docker-compose build
   docker-compose up -d
   ```

4. **Commit Your Changes**
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```

5. **Push and Create PR**
   ```bash
   git push origin feature/your-feature-name
   ```
   Then create a Pull Request on GitHub.

### Commit Message Format
Use conventional commits format:
- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation changes
- `refactor:` for code refactoring
- `test:` for adding tests
- `chore:` for maintenance tasks

## 🏗️ Architecture Guidelines

### Core Principles
- **Stateless Design**: Server should not maintain persistent client state
- **MCP Compliance**: Follow MCP protocol specifications
- **Security First**: Validate inputs, use secure defaults
- **Extensibility**: Design for pluggable backends and transports

### Adding New Features

#### Queue Backends
To add a new queue backend (e.g., Redis):
1. Implement the `QueueBackend` abstract class
2. Add configuration options
3. Update Docker compose with new services
4. Document setup and configuration

#### Transport Protocols
For new transport protocols:
1. Follow MCP specification requirements
2. Maintain backward compatibility
3. Add comprehensive tests
4. Update documentation

## 🔒 Security Considerations

### Input Validation
- Validate all client inputs
- Sanitize message content
- Implement rate limiting
- Check message size limits

### Authentication
- Client IDs serve as basic authentication
- Consider implementing token-based auth for production
- Document security best practices

### Docker Security
- Use non-root users in containers
- Minimize attack surface
- Keep dependencies updated
- Follow container security best practices

## 📚 Resources

- [MCP Specification](https://spec.modelcontextprotocol.io/)
- [FastMCP Documentation](https://github.com/jlowin/fastmcp)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)

## 🤝 Community

- Be respectful and inclusive
- Help newcomers get started
- Share knowledge and best practices
- Follow the project's code of conduct

## 📄 License

By contributing to this project, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to MCP IDE Bridge! 🎉 