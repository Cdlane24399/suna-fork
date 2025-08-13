#!/usr/bin/env python3
"""
Deployment status checker for Suna/Kortix AI Platform
Checks the health of all services and provides deployment status
"""

import requests
import subprocess
import sys
import time
import json
from urllib.parse import urljoin

class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def check_service_health(url, service_name, timeout=10):
    """Check if a service is responding"""
    try:
        response = requests.get(url, timeout=timeout)
        if response.status_code == 200:
            print(f"  ✅ {service_name}: {Colors.GREEN}Healthy{Colors.ENDC}")
            return True
        else:
            print(f"  ❌ {service_name}: {Colors.RED}Unhealthy (HTTP {response.status_code}){Colors.ENDC}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"  ❌ {service_name}: {Colors.RED}Unreachable ({str(e)}){Colors.ENDC}")
        return False

def check_docker_services():
    """Check Docker Compose services status"""
    try:
        result = subprocess.run(
            ['docker', 'compose', 'ps', '--format', 'json'],
            capture_output=True,
            text=True,
            check=True
        )
        
        services = []
        for line in result.stdout.strip().split('\n'):
            if line.strip():
                try:
                    service = json.loads(line)
                    services.append(service)
                except json.JSONDecodeError:
                    continue
        
        print(f"\n{Colors.BLUE}{Colors.BOLD}🐳 Docker Services Status:{Colors.ENDC}")
        
        all_healthy = True
        for service in services:
            name = service.get('Name', 'Unknown')
            state = service.get('State', 'Unknown')
            status = service.get('Status', 'Unknown')
            
            if state == 'running':
                print(f"  ✅ {name}: {Colors.GREEN}Running{Colors.ENDC} ({status})")
            else:
                print(f"  ❌ {name}: {Colors.RED}{state.title()}{Colors.ENDC} ({status})")
                all_healthy = False
        
        return all_healthy, len(services)
        
    except subprocess.CalledProcessError:
        print(f"  ❌ {Colors.RED}Docker Compose not running or not found{Colors.ENDC}")
        return False, 0
    except Exception as e:
        print(f"  ❌ {Colors.RED}Error checking Docker services: {e}{Colors.ENDC}")
        return False, 0

def check_deployment_status():
    """Main function to check deployment status"""
    print(f"{Colors.BLUE}{Colors.BOLD}🔍 Checking Suna/Kortix Deployment Status{Colors.ENDC}\n")
    
    # Check Docker services
    docker_healthy, service_count = check_docker_services()
    
    if service_count == 0:
        print(f"\n{Colors.YELLOW}⚠️  No Docker services found. Run 'python start.py' or 'docker compose up -d' to start services.{Colors.ENDC}")
        return
    
    # Check web services health
    print(f"\n{Colors.BLUE}{Colors.BOLD}🌐 Web Services Health:{Colors.ENDC}")
    
    services_to_check = [
        ('http://localhost:3000', 'Frontend'),
        ('http://localhost:8000/docs', 'Backend API'),
        ('http://localhost:8000/health', 'Backend Health') if check_backend_health_endpoint() else None
    ]
    
    # Filter out None values
    services_to_check = [s for s in services_to_check if s is not None]
    
    web_healthy = True
    for url, name in services_to_check:
        if not check_service_health(url, name):
            web_healthy = False
    
    # Overall status
    print(f"\n{Colors.BLUE}{Colors.BOLD}📊 Overall Status:{Colors.ENDC}")
    
    if docker_healthy and web_healthy:
        print(f"  🎉 {Colors.GREEN}All services are healthy and running!{Colors.ENDC}")
        print(f"\n{Colors.BLUE}🌐 Access URLs:{Colors.ENDC}")
        print(f"  • Frontend: {Colors.BLUE}http://localhost:3000{Colors.ENDC}")
        print(f"  • Backend API: {Colors.BLUE}http://localhost:8000{Colors.ENDC}")
        print(f"  • API Documentation: {Colors.BLUE}http://localhost:8000/docs{Colors.ENDC}")
    elif docker_healthy and not web_healthy:
        print(f"  ⚠️  {Colors.YELLOW}Services are running but some may be starting up. Wait a moment and try again.{Colors.ENDC}")
    else:
        print(f"  ❌ {Colors.RED}Some services are not running properly. Check the logs with 'docker compose logs'.{Colors.ENDC}")

def check_backend_health_endpoint():
    """Check if backend health endpoint exists"""
    try:
        response = requests.get('http://localhost:8000/health', timeout=5)
        return True
    except:
        return False

def show_helpful_commands():
    """Show helpful commands for managing the deployment"""
    print(f"\n{Colors.BLUE}{Colors.BOLD}🛠️  Helpful Commands:{Colors.ENDC}")
    print(f"  • Start services: {Colors.BLUE}python start.py{Colors.ENDC} or {Colors.BLUE}docker compose up -d{Colors.ENDC}")
    print(f"  • Stop services: {Colors.BLUE}docker compose down{Colors.ENDC}")
    print(f"  • View logs: {Colors.BLUE}docker compose logs -f{Colors.ENDC}")
    print(f"  • Restart services: {Colors.BLUE}docker compose restart{Colors.ENDC}")
    print(f"  • Check this status: {Colors.BLUE}python status.py{Colors.ENDC}")

if __name__ == "__main__":
    try:
        check_deployment_status()
        show_helpful_commands()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Status check interrupted.{Colors.ENDC}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Colors.RED}Error during status check: {e}{Colors.ENDC}")
        sys.exit(1)