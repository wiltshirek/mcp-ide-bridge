#!/bin/bash

# MCP Messaging Server Docker Deployment Script

set -e

echo "🐳 MCP Messaging Server Docker Deployment"
echo "=========================================="

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

# Check if docker-compose is available
if ! command -v docker-compose > /dev/null 2>&1; then
    echo "❌ docker-compose is not installed. Please install docker-compose and try again."
    exit 1
fi

# Parse command line arguments
ACTION=${1:-"up"}

case $ACTION in
    "build")
        echo "🔨 Building Docker image..."
        docker-compose build --no-cache
        ;;
    "up")
        echo "🚀 Starting MCP Messaging Server..."
        docker-compose up -d
        echo "✅ Server started successfully!"
        echo "📡 Server available at: http://localhost:8123"
        echo "🔍 Check logs with: docker-compose logs -f"
        ;;
    "down")
        echo "🛑 Stopping MCP Messaging Server..."
        docker-compose down
        echo "✅ Server stopped successfully!"
        ;;
    "restart")
        echo "🔄 Restarting MCP Messaging Server..."
        docker-compose down
        docker-compose up -d
        echo "✅ Server restarted successfully!"
        ;;
    "logs")
        echo "📋 Showing server logs..."
        docker-compose logs -f
        ;;
    "status")
        echo "📊 Server status:"
        docker-compose ps
        ;;
    "clean")
        echo "🧹 Cleaning up Docker resources..."
        docker-compose down -v
        docker system prune -f
        echo "✅ Cleanup completed!"
        ;;
    *)
        echo "Usage: $0 {build|up|down|restart|logs|status|clean}"
        echo ""
        echo "Commands:"
        echo "  build   - Build the Docker image"
        echo "  up      - Start the server (default)"
        echo "  down    - Stop the server"
        echo "  restart - Restart the server"
        echo "  logs    - Show server logs"
        echo "  status  - Show server status"
        echo "  clean   - Stop server and clean up resources"
        exit 1
        ;;
esac 