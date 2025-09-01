#!/bin/bash

# Galaxy Holding - Automated Installation Script
# ERPNext + n8n + AI Stack

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
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

# Check if running as root
check_root() {
    if [[ $EUID -eq 0 ]]; then
        log_error "This script should not be run as root"
        exit 1
    fi
}

# Check system prerequisites
check_prerequisites() {
    log_info "Checking system prerequisites..."
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        log_error "Docker is not installed. Installing Docker..."
        install_docker
    else
        log_success "Docker found: $(docker --version)"
    fi
    
    # Check Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        log_error "Docker Compose is not installed. Installing..."
        install_docker_compose
    else
        log_success "Docker Compose found: $(docker-compose --version)"
    fi
    
    # Check system resources
    check_system_resources
}

# Install Docker
install_docker() {
    log_info "Installing Docker..."
    
    # Update packages
    sudo apt update
    
    # Install dependencies
    sudo apt install -y apt-transport-https ca-certificates curl gnupg lsb-release
    
    # Add Docker GPG key
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
    
    # Add repository
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    
    # Install Docker
    sudo apt update
    sudo apt install -y docker-ce docker-ce-cli containerd.io
    
    # Add user to docker group
    sudo usermod -aG docker $USER
    
    # Start Docker
    sudo systemctl enable docker
    sudo systemctl start docker
    
    log_success "Docker installed successfully"
}

# Install Docker Compose
install_docker_compose() {
    log_info "Installing Docker Compose..."
    
    # Download Docker Compose
    sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    
    # Make executable
    sudo chmod +x /usr/local/bin/docker-compose
    
    # Create symlink
    sudo ln -sf /usr/local/bin/docker-compose /usr/bin/docker-compose
    
    log_success "Docker Compose installed successfully"
}

# Check system resources
check_system_resources() {
    log_info "Checking system resources..."
    
    # Check RAM
    total_ram=$(free -m | awk 'NR==2{printf "%.0f", $2/1024}')
    if [ $total_ram -lt 8 ]; then
        log_warning "Available RAM: ${total_ram}GB. Minimum 8GB recommended"
    else
        log_success "Available RAM: ${total_ram}GB"
    fi
    
    # Check disk space
    available_space=$(df -BG / | awk 'NR==2{print $4}' | sed 's/G//')
    if [ $available_space -lt 50 ]; then
        log_warning "Available space: ${available_space}GB. Minimum 50GB recommended"
    else
        log_success "Available space: ${available_space}GB"
    fi
    
    # Check CPU cores
    cpu_cores=$(nproc)
    if [ $cpu_cores -lt 4 ]; then
        log_warning "CPU cores: ${cpu_cores}. Minimum 4 cores recommended"
    else
        log_success "CPU cores: ${cpu_cores}"
    fi
}

# Create directory structure
create_directory_structure() {
    log_info "Creating directory structure..."
    
    # Main directory
    INSTALL_DIR="/opt/galaxy-holding"
    
    if [ -d "$INSTALL_DIR" ]; then
        log_warning "Directory $INSTALL_DIR already exists"
        read -p "Do you want to continue? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            log_info "Installation cancelled"
            exit 1
        fi
    fi
    
    # Create directories
    sudo mkdir -p $INSTALL_DIR/{docker,scripts,configs,templates,data,logs,backups}
    sudo chown -R $USER:$USER $INSTALL_DIR
    chmod -R 755 $INSTALL_DIR
    
    log_success "Directory structure created at $INSTALL_DIR"
    
    # Change to installation directory
    cd $INSTALL_DIR
}

# Setup environment variables
setup_environment() {
    log_info "Setting up environment variables..."
    
    # Generate encryption keys
    ENCRYPTION_KEY=$(openssl rand -base64 32)
    N8N_ENCRYPTION_KEY=$(openssl rand -base64 32)
    
    # Create .env file
    cat > docker/.env << EOF
# ==============================================
# Galaxy Holding - ERPNext + n8n + AI Stack
# Environment Variables Configuration
# ==============================================

# General Configuration
TIMEZONE=Europe/Madrid
SITE_NAME=galaxy.local
DOMAIN=galaxy.local

# ERPNext Database Configuration (MariaDB)
DB_ROOT_PASSWORD=Galaxy_Root_2025!
DB_NAME=galaxy_erpnext
DB_USER=galaxy_user
DB_PASSWORD=Galaxy_DB_2025!

# ERPNext Configuration
ADMIN_PASSWORD=Galaxy_Admin_2025!
ENCRYPTION_KEY=$ENCRYPTION_KEY
DEVELOPER_MODE=0

# n8n Database Configuration (PostgreSQL)
N8N_DB_NAME=n8n_galaxy
N8N_DB_USER=n8n_user
N8N_DB_PASSWORD=N8N_DB_2025!

# n8n Configuration
N8N_BASIC_AUTH_USER=galaxy_admin
N8N_BASIC_AUTH_PASSWORD=Galaxy_N8N_2025!
N8N_HOST=n8n.galaxy.local
N8N_PROTOCOL=http
WEBHOOK_URL=http://n8n.galaxy.local/
N8N_ENCRYPTION_KEY=$N8N_ENCRYPTION_KEY

# Microsoft 365 OAuth (configure after installation)
MICROSOFT_CLIENT_ID=your-azure-app-client-id
MICROSOFT_CLIENT_SECRET=your-azure-app-client-secret
MICROSOFT_TENANT_ID=your-azure-tenant-id

# OpenAI API (for custom GPT)
OPENAI_API_KEY=your-openai-api-key-here
EOF
    
    log_success ".env file created with generated encryption keys"
    log_warning "IMPORTANT: Edit docker/.env with your specific values before continuing"
}

# Setup local hosts
setup_local_hosts() {
    log_info "Setting up local hosts..."
    
    # Add entries to hosts file
    if ! grep -q "galaxy.local" /etc/hosts; then
        echo "127.0.0.1 galaxy.local" | sudo tee -a /etc/hosts
        echo "127.0.0.1 erpnext.galaxy.local" | sudo tee -a /etc/hosts
        echo "127.0.0.1 n8n.galaxy.local" | sudo tee -a /etc/hosts
        log_success "Local hosts configured"
    else
        log_warning "Local hosts already configured"
    fi
}

# Start services
start_services() {
    log_info "Starting Docker services..."
    
    cd docker
    
    # Verify configuration
    if ! docker-compose config > /dev/null 2>&1; then
        log_error "Error in docker-compose configuration"
        docker-compose config
        exit 1
    fi
    
    # Download images
    log_info "Downloading Docker images..."
    docker-compose pull
    
    # Start services
    log_info "Starting services in background..."
    docker-compose up -d
    
    # Wait for services to be ready
    log_info "Waiting for services to be ready..."
    sleep 30
    
    # Check service status
    if docker-compose ps | grep -q "Up"; then
        log_success "Services started successfully"
    else
        log_error "Error starting services"
        docker-compose logs
        exit 1
    fi
}

# Verify services
verify_services() {
    log_info "Verifying services..."
    
    # Check ERPNext
    if curl -s -o /dev/null -w "%{http_code}" http://localhost:8080 | grep -q "200\|302"; then
        log_success "ERPNext accessible at http://localhost:8080"
    else
        log_warning "ERPNext not responding at http://localhost:8080"
    fi
    
    # Check n8n
    if curl -s -o /dev/null -w "%{http_code}" http://localhost:5678 | grep -q "200\|401"; then
        log_success "n8n accessible at http://localhost:5678"
    else
        log_warning "n8n not responding at http://localhost:5678"
    fi
}

# Show final information
show_final_info() {
    log_success "Installation completed successfully!"
    
    echo
    echo "=================================================="
    echo "         GALAXY HOLDING - ACCESS INFORMATION"
    echo "=================================================="
    echo
    echo "🌐 ERPNext:"
    echo "   URL: http://galaxy.local:8080"
    echo "   User: Administrator"
    echo "   Password: Galaxy_Admin_2025!"
    echo
    echo "🔧 n8n:"
    echo "   URL: http://n8n.galaxy.local:5678"
    echo "   User: galaxy_admin"
    echo "   Password: Galaxy_N8N_2025!"
    echo
    echo "📁 Installation directory: /opt/galaxy-holding"
    echo
    echo "=================================================="
    echo "                 NEXT STEPS"
    echo "=================================================="
    echo
    echo "1. Configure Microsoft 365 OAuth:"
    echo "   - Follow guide in docs/microsoft365_oauth_setup.md"
    echo
    echo "2. Import n8n templates:"
    echo "   - Access n8n and import files from templates/"
    echo
    echo "3. Configure custom GPT:"
    echo "   - Follow guide in docs/gpt_actions_specification.md"
    echo
    echo "4. Train users:"
    echo "   - Review documentation in docs/"
    echo
    echo "=================================================="
    echo
}

# Main function
main() {
    echo "=================================================="
    echo "    GALAXY HOLDING - AUTOMATED INSTALLATION"
    echo "         ERPNext + n8n + AI Stack"
    echo "=================================================="
    echo
    
    check_root
    check_prerequisites
    create_directory_structure
    setup_environment
    setup_local_hosts
    
    # Pause for user to configure .env
    echo
    log_warning "IMPORTANT: Configure docker/.env file with your specific values"
    log_warning "Especially: MICROSOFT_CLIENT_ID, MICROSOFT_CLIENT_SECRET, OPENAI_API_KEY"
    echo
    read -p "Press Enter when you have configured the .env file..."
    echo
    
    start_services
    verify_services
    show_final_info
}

# Execute main function
main "$@"