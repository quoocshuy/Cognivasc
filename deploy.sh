#!/bin/bash

# =============================================================================
# Deploy Script cho Cognivasc Application
# =============================================================================

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_NAME="cognivasc"
BACKEND_PORT=8000
FRONTEND_PORT=3000
NGINX_PORT=80

# Functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is installed
check_docker() {
    log_info "Checking Docker installation..."
    if ! command -v docker &> /dev/null; then
        log_error "Docker is not installed. Please install Docker first."
        exit 1
    fi

    if ! command -v docker-compose &> /dev/null; then
        log_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi

    log_success "Docker and Docker Compose are installed"
}

# Check if required files exist
check_files() {
    log_info "Checking required files..."

    local required_files=(
        "backend/Dockerfile"
        "frontend/Dockerfile"
        "docker-compose.yml"
        "backend/anemia_model.keras"
        "backend/requirements.txt"
        "frontend/package.json"
    )

    for file in "${required_files[@]}"; do
        if [ ! -f "$file" ]; then
            log_error "Required file not found: $file"
            exit 1
        fi
    done

    log_success "All required files found"
}

# Create necessary directories
create_directories() {
    log_info "Creating necessary directories..."

    mkdir -p backend/logs
    mkdir -p backend/cache
    mkdir -p nginx/ssl

    log_success "Directories created"
}

# Build and start services
deploy_services() {
    log_info "Building and starting services..."

    # Stop existing containers
    log_info "Stopping existing containers..."
    docker-compose down --remove-orphans

    # Build and start services
    log_info "Building Docker images..."
    docker-compose build --no-cache

    log_info "Starting services..."
    docker-compose up -d

    log_success "Services started successfully"
}

# Wait for services to be healthy
wait_for_services() {
    log_info "Waiting for services to be healthy..."

    # Wait for backend
    log_info "Waiting for backend service..."
    timeout=60
    while [ $timeout -gt 0 ]; do
        if curl -f http://localhost:$BACKEND_PORT/health &> /dev/null; then
            log_success "Backend service is healthy"
            break
        fi
        sleep 2
        timeout=$((timeout-2))
    done

    if [ $timeout -le 0 ]; then
        log_error "Backend service failed to start within 60 seconds"
        exit 1
    fi

    # Wait for frontend
    log_info "Waiting for frontend service..."
    timeout=30
    while [ $timeout -gt 0 ]; do
        if curl -f http://localhost:$FRONTEND_PORT/ &> /dev/null; then
            log_success "Frontend service is healthy"
            break
        fi
        sleep 2
        timeout=$((timeout-2))
    done

    if [ $timeout -le 0 ]; then
        log_error "Frontend service failed to start within 30 seconds"
        exit 1
    fi
}

# Show deployment status
show_status() {
    log_info "Deployment Status:"
    echo ""
    echo "Services:"
    docker-compose ps
    echo ""
    echo "Application URLs:"
    echo "  Frontend: http://localhost:$FRONTEND_PORT"
    echo "  Backend API: http://localhost:$BACKEND_PORT"
    echo "  API Docs: http://localhost:$BACKEND_PORT/docs"
    echo "  Health Check: http://localhost:$BACKEND_PORT/health"
    echo ""
    echo "Logs:"
    echo "  View all logs: docker-compose logs -f"
    echo "  Backend logs: docker-compose logs -f backend"
    echo "  Frontend logs: docker-compose logs -f frontend"
}

# Main deployment function
main() {
    echo "=========================================="
    echo "Cognivasc Application Deployment"
    echo "=========================================="
    echo ""

    check_docker
    check_files
    create_directories
    deploy_services
    wait_for_services
    show_status

    echo ""
    log_success "Deployment completed successfully!"
    echo ""
    log_info "You can now access the application at:"
    echo "  Frontend: http://localhost:$FRONTEND_PORT"
    echo "  Backend: http://localhost:$BACKEND_PORT"
}

# Handle script arguments
case "${1:-deploy}" in
    "deploy")
        main
        ;;
    "stop")
        log_info "Stopping services..."
        docker-compose down
        log_success "Services stopped"
        ;;
    "restart")
        log_info "Restarting services..."
        docker-compose restart
        log_success "Services restarted"
        ;;
    "logs")
        docker-compose logs -f
        ;;
    "status")
        docker-compose ps
        ;;
    "clean")
        log_warning "This will remove all containers, images, and volumes. Are you sure? (y/N)"
        read -r response
        if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
            docker-compose down --volumes --rmi all
            log_success "Cleanup completed"
        else
            log_info "Cleanup cancelled"
        fi
        ;;
    *)
        echo "Usage: $0 {deploy|stop|restart|logs|status|clean}"
        echo ""
        echo "Commands:"
        echo "  deploy  - Deploy the application (default)"
        echo "  stop    - Stop all services"
        echo "  restart - Restart all services"
        echo "  logs    - Show logs from all services"
        echo "  status  - Show status of all services"
        echo "  clean   - Remove all containers, images, and volumes"
        exit 1
        ;;
esac
