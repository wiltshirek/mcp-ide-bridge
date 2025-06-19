# Security Policy

## Supported Versions

We actively support the following versions of MCP IDE Bridge:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

We take security vulnerabilities seriously. If you discover a security vulnerability in MCP IDE Bridge, please report it responsibly.

### How to Report

**Please do NOT report security vulnerabilities through public GitHub issues.**

Instead, please report security vulnerabilities by:

1. **Email**: Send details to security@mvp2o.ai
2. **GitHub Security Advisories**: Use GitHub's private vulnerability reporting feature
3. **Direct Contact**: Contact the maintainer directly through secure channels

### What to Include

When reporting a vulnerability, please include:

- **Description**: Clear description of the vulnerability
- **Impact**: Potential impact and attack scenarios
- **Reproduction**: Step-by-step instructions to reproduce the issue
- **Environment**: Version, OS, configuration details
- **Proof of Concept**: If applicable, include PoC code (responsibly)

### Response Timeline

- **Acknowledgment**: Within 48 hours of report
- **Initial Assessment**: Within 5 business days
- **Status Updates**: Weekly updates on progress
- **Resolution**: Target resolution within 30 days for critical issues

## Security Best Practices

### For Users

#### Production Deployment
- **Network Security**: Deploy behind a firewall or VPN
- **Authentication**: Use strong client IDs as authentication tokens
- **TLS/SSL**: Always use HTTPS in production environments
- **Rate Limiting**: Implement rate limiting at the network level
- **Monitoring**: Monitor for unusual traffic patterns

#### Configuration Security
- **Client IDs**: Use cryptographically secure random client IDs
- **Environment Variables**: Store sensitive config in environment variables
- **File Permissions**: Restrict access to configuration files
- **Container Security**: Run containers as non-root users

#### Message Security
- **Input Validation**: Validate all message content
- **Size Limits**: Configure appropriate message size limits
- **Content Filtering**: Implement content filtering if needed
- **Logging**: Be careful not to log sensitive information

### For Developers

#### Code Security
- **Input Sanitization**: Always sanitize user inputs
- **SQL Injection**: Use parameterized queries (when database backends are added)
- **XSS Prevention**: Escape output when rendering user content
- **Dependency Management**: Keep dependencies updated

#### Docker Security
- **Base Images**: Use official, minimal base images
- **Non-root Users**: Always run as non-root user
- **Secrets Management**: Never include secrets in images
- **Image Scanning**: Regularly scan images for vulnerabilities

## Known Security Considerations

### Current Architecture
- **Client Authentication**: Currently uses client IDs as basic authentication
- **Message Persistence**: Messages are stored in memory (not encrypted at rest)
- **Transport Security**: Relies on HTTP transport (recommend HTTPS)
- **Rate Limiting**: Not implemented at application level

### Planned Security Enhancements
- Token-based authentication system
- Message encryption at rest
- Built-in rate limiting
- Audit logging
- Role-based access control

## Security Updates

Security updates will be:
- **Prioritized**: Security fixes take priority over feature development
- **Documented**: All security updates will be documented in release notes
- **Communicated**: Security advisories will be published for significant issues
- **Backward Compatible**: Security fixes will maintain backward compatibility when possible

## Vulnerability Disclosure Policy

### Coordinated Disclosure
We follow responsible disclosure practices:

1. **Private Reporting**: Vulnerabilities reported privately first
2. **Investigation**: We investigate and develop fixes
3. **Coordination**: We coordinate with reporters on disclosure timeline
4. **Public Disclosure**: Public disclosure after fixes are available
5. **Credit**: We provide credit to security researchers (with permission)

### Disclosure Timeline
- **Critical Vulnerabilities**: 7-14 days after fix is available
- **High Severity**: 30 days after fix is available
- **Medium/Low Severity**: 60-90 days after fix is available

## Security Resources

### External Resources
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Docker Security Best Practices](https://docs.docker.com/engine/security/)
- [Python Security Guidelines](https://python-security.readthedocs.io/)
- [MCP Security Considerations](https://spec.modelcontextprotocol.io/security)

### Security Tools
- **Static Analysis**: Use tools like `bandit` for Python security analysis
- **Dependency Scanning**: Use `safety` to check for vulnerable dependencies
- **Container Scanning**: Use `docker scan` or similar tools
- **Network Testing**: Use tools like `nmap` for network security testing

## Contact

For security-related questions or concerns:
- **Security Email**: security@mvp2o.ai
- **Company**: MVP2o.ai
- **GitHub**: [@wiltshirek](https://github.com/wiltshirek)

---

Thank you for helping keep MCP IDE Bridge secure! 🔒 