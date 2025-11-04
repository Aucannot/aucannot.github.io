#!/bin/bash

# Jekyll Local Development Server Script
# This script sets up and runs the Jekyll site locally for development

set -e  # Exit on any error

# Color codes for output formatting
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if bundle command is available
check_bundle() {
    if ! command -v bundle &> /dev/null; then
        print_error "bundle command not found!"
        print_info "Please install Ruby and Bundler:"
        print_info "  - Install Ruby: https://www.ruby-lang.org/en/documentation/installation/"
        print_info "  - Install Bundler: gem install bundler"
        exit 1
    fi
    print_success "Bundler is installed"
}

# Check if Gemfile exists
check_gemfile() {
    if [ ! -f "Gemfile" ]; then
        print_error "Gemfile not found in current directory!"
        print_info "Please run this script from the Jekyll project root"
        exit 1
    fi
    print_success "Gemfile found"
}

# Install dependencies
install_dependencies() {
    print_info "Installing dependencies..."
    bundle install
    print_success "Dependencies installed successfully"
}

# Clean previous builds (optional)
clean_build() {
    read -p "Do you want to clean previous builds? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_info "Cleaning previous builds..."
        rm -rf _site
        rm -rf .jekyll-cache
        print_success "Build directory cleaned"
    fi
}

# Start Jekyll development server
start_server() {
    print_info "Starting Jekyll development server..."
    print_info "Server will be available at: http://localhost:4000"
    print_info "Press Ctrl+C to stop the server"
    echo

    # Start Jekyll with live reload
    bundle exec jekyll serve --watch --livereload
}

# Main execution
main() {
    echo "========================================="
    echo "  Jekyll Local Development Server"
    echo "========================================="
    echo

    # Run checks and setup
    check_bundle
    check_gemfile
    install_dependencies
    clean_build

    echo
    print_info "Starting server..."
    echo

    # Start the server
    start_server
}

# Run main function
main