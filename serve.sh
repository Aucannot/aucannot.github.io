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
MIN_RUBY_VERSION='3.1.0'
RECOMMENDED_RUBY_SERIES='3.3'

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

# Compare semantic versions using RubyGems' version parser.
version_gte() {
    ruby -e 'exit(Gem::Version.new(ARGV[0]) >= Gem::Version.new(ARGV[1]) ? 0 : 1)' "$1" "$2"
}

check_ruby() {
    if ! command -v ruby &> /dev/null; then
        print_error "ruby command not found!"
        print_info "This site requires Ruby ${MIN_RUBY_VERSION}+"
        exit 1
    fi

    local current_ruby_version
    current_ruby_version="$(ruby -e 'print RUBY_VERSION')"

    if version_gte "$current_ruby_version" "$MIN_RUBY_VERSION"; then
        print_success "Ruby ${current_ruby_version} is compatible"
        return
    fi

    local candidate
    for candidate in \
        /opt/homebrew/opt/ruby@3.4/bin \
        /opt/homebrew/opt/ruby@3.3/bin \
        /opt/homebrew/opt/ruby@3.2/bin \
        /opt/homebrew/opt/ruby@3.1/bin; do
        if [ -x "${candidate}/ruby" ]; then
            export PATH="${candidate}:$PATH"
            current_ruby_version="$(ruby -e 'print RUBY_VERSION')"
            break
        fi
    done

    if version_gte "$current_ruby_version" "$MIN_RUBY_VERSION"; then
        print_success "Using compatible Ruby ${current_ruby_version}"
        return
    fi

    print_error "Ruby ${current_ruby_version} is too old for jekyll-theme-chirpy 7.2.x"
    print_info "GitHub Actions builds this site with Ruby ${RECOMMENDED_RUBY_SERIES}"
    print_info "On macOS with Homebrew, install a newer Ruby with:"
    print_info "  brew install ruby@${RECOMMENDED_RUBY_SERIES}"
    print_info "  export PATH=\"/opt/homebrew/opt/ruby@${RECOMMENDED_RUBY_SERIES}/bin:\$PATH\""
    exit 1
}

# Check if bundle command is available
check_bundle() {
    if ! command -v bundle &> /dev/null; then
        print_error "bundle command not found!"
        print_info "Please install Bundler for the active Ruby:"
        print_info "  gem install bundler"
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
    bundle config set --local path 'vendor/bundle'
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
    check_ruby
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
