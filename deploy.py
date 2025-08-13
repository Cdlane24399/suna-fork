#!/usr/bin/env python3
"""
One-click deployment script for Suna/Kortix AI Platform
Supports multiple cloud platforms and deployment methods
"""

import os
import sys
import json
import subprocess
import argparse
from pathlib import Path

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_banner():
    print(f"""
{Colors.BLUE}{Colors.BOLD}
   ███████╗██╗   ██╗███╗   ██╗ █████╗     ██████╗ ███████╗██████╗ ██╗      ██████╗ ██╗   ██╗
   ██╔════╝██║   ██║████╗  ██║██╔══██╗    ██╔══██╗██╔════╝██╔══██╗██║     ██╔═══██╗╚██╗ ██╔╝
   ███████╗██║   ██║██╔██╗ ██║███████║    ██║  ██║█████╗  ██████╔╝██║     ██║   ██║ ╚████╔╝ 
   ╚════██║██║   ██║██║╚██╗██║██╔══██║    ██║  ██║██╔══╝  ██╔═══╝ ██║     ██║   ██║  ╚██╔╝  
   ███████║╚██████╔╝██║ ╚████║██║  ██║    ██████╔╝███████╗██║     ███████╗╚██████╔╝   ██║   
   ╚══════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝    ╚═════╝ ╚══════╝╚═╝     ╚══════╝ ╚═════╝    ╚═╝   
                                      
   One-Click Deployment Script
{Colors.ENDC}
""")

def check_prerequisites():
    """Check if required tools are installed"""
    print(f"{Colors.CYAN}🔍 Checking prerequisites...{Colors.ENDC}")
    
    required_tools = {
        'docker': 'Docker is required for containerization',
        'git': 'Git is required for version control'
    }
    
    missing_tools = []
    for tool, description in required_tools.items():
        try:
            subprocess.run([tool, '--version'], capture_output=True, check=True)
            print(f"  ✅ {tool} found")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print(f"  ❌ {tool} not found - {description}")
            missing_tools.append(tool)
    
    if missing_tools:
        print(f"\n{Colors.RED}❌ Missing required tools: {', '.join(missing_tools)}{Colors.ENDC}")
        return False
    
    print(f"{Colors.GREEN}✅ All prerequisites met{Colors.ENDC}")
    return True

def create_env_files():
    """Create environment files from examples"""
    print(f"\n{Colors.CYAN}📄 Setting up environment files...{Colors.ENDC}")
    
    env_files = [
        ('backend/.env.example', 'backend/.env'),
        ('frontend/.env.example', 'frontend/.env.local')
    ]
    
    for example_file, env_file in env_files:
        if not Path(env_file).exists():
            if Path(example_file).exists():
                subprocess.run(['cp', example_file, env_file])
                print(f"  📋 Created {env_file} from {example_file}")
            else:
                print(f"  ⚠️  {example_file} not found, skipping {env_file}")
        else:
            print(f"  ✅ {env_file} already exists")

def deploy_docker_local():
    """Deploy using local Docker Compose"""
    print(f"\n{Colors.CYAN}🐳 Deploying with Docker Compose...{Colors.ENDC}")
    
    try:
        # Build and start services
        print("  📦 Building images...")
        subprocess.run(['docker', 'compose', 'build'], check=True)
        
        print("  🚀 Starting services...")
        subprocess.run(['docker', 'compose', 'up', '-d'], check=True)
        
        print(f"\n{Colors.GREEN}✅ Deployment successful!{Colors.ENDC}")
        print(f"{Colors.CYAN}🌐 Frontend: http://localhost:3000{Colors.ENDC}")
        print(f"{Colors.CYAN}🔧 Backend API: http://localhost:8000{Colors.ENDC}")
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"{Colors.RED}❌ Deployment failed: {e}{Colors.ENDC}")
        return False

def deploy_docker_production():
    """Deploy using production Docker Compose"""
    print(f"\n{Colors.CYAN}🏭 Deploying with Production Docker Compose...{Colors.ENDC}")
    
    try:
        # Pull images and start services
        print("  📥 Pulling latest images...")
        subprocess.run(['docker', 'compose', '-f', 'docker-compose.prod.yaml', 'pull'], check=True)
        
        print("  🚀 Starting production services...")
        subprocess.run(['docker', 'compose', '-f', 'docker-compose.prod.yaml', 'up', '-d'], check=True)
        
        print(f"\n{Colors.GREEN}✅ Production deployment successful!{Colors.ENDC}")
        print(f"{Colors.CYAN}🌐 Frontend: http://localhost:3000{Colors.ENDC}")
        print(f"{Colors.CYAN}🔧 Backend API: http://localhost:8000{Colors.ENDC}")
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"{Colors.RED}❌ Production deployment failed: {e}{Colors.ENDC}")
        return False

def show_platform_instructions():
    """Show deployment instructions for various platforms"""
    print(f"\n{Colors.CYAN}☁️  Cloud Platform Deployment Options:{Colors.ENDC}")
    
    platforms = {
        "Railway": {
            "url": "https://railway.app",
            "instructions": [
                "1. Connect your GitHub repository to Railway",
                "2. The railway.toml file is already configured",
                "3. Set environment variables in Railway dashboard",
                "4. Deploy with one click"
            ]
        },
        "Render": {
            "url": "https://render.com",
            "instructions": [
                "1. Connect your GitHub repository to Render",
                "2. Use the render.yaml configuration file",
                "3. Set environment variables in Render dashboard",
                "4. Deploy services individually or as a blueprint"
            ]
        },
        "DigitalOcean App Platform": {
            "url": "https://cloud.digitalocean.com/apps",
            "instructions": [
                "1. Connect your GitHub repository",
                "2. Use the docker-compose.prod.yaml as reference",
                "3. Configure services manually in the dashboard",
                "4. Set environment variables and deploy"
            ]
        },
        "Vercel (Frontend Only)": {
            "url": "https://vercel.com",
            "instructions": [
                "1. Connect your GitHub repository to Vercel",
                "2. Set root directory to 'frontend'",
                "3. Configure environment variables",
                "4. Deploy backend separately on Railway/Render"
            ]
        }
    }
    
    for platform, info in platforms.items():
        print(f"\n{Colors.BOLD}{platform}:{Colors.ENDC} {info['url']}")
        for instruction in info['instructions']:
            print(f"  {instruction}")

def main():
    parser = argparse.ArgumentParser(description="Deploy Suna/Kortix AI Platform")
    parser.add_argument('--method', choices=['local', 'production', 'cloud-info'], 
                       default='local', help='Deployment method')
    parser.add_argument('--skip-checks', action='store_true', 
                       help='Skip prerequisite checks')
    
    args = parser.parse_args()
    
    print_banner()
    
    if not args.skip_checks and not check_prerequisites():
        sys.exit(1)
    
    create_env_files()
    
    if args.method == 'local':
        success = deploy_docker_local()
    elif args.method == 'production':
        success = deploy_docker_production()
    elif args.method == 'cloud-info':
        show_platform_instructions()
        return
    
    if success:
        print(f"\n{Colors.GREEN}🎉 Deployment completed successfully!{Colors.ENDC}")
        print(f"\n{Colors.YELLOW}📝 Next steps:{Colors.ENDC}")
        print("1. Configure your environment variables in the .env files")
        print("2. Set up your Supabase database")
        print("3. Add your API keys for LLM providers")
        print("4. Access the application at the URLs shown above")
    else:
        print(f"\n{Colors.RED}💥 Deployment failed. Check the error messages above.{Colors.ENDC}")
        sys.exit(1)

if __name__ == "__main__":
    main()