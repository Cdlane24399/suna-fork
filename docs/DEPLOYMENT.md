# 🚀 Deployment Guide for Suna/Kortix AI Platform

This guide provides multiple deployment options for the Suna/Kortix AI agent platform, from local development to production cloud deployments.

## 📋 Table of Contents

- [Quick Start](#quick-start)
- [Local Development](#local-development)
- [Production Deployment](#production-deployment)
- [Cloud Platform Deployments](#cloud-platform-deployments)
- [Environment Configuration](#environment-configuration)
- [Troubleshooting](#troubleshooting)

## 🚀 Quick Start

### One-Click Deployment

Use the deployment script for the fastest setup:

```bash
# Clone the repository
git clone https://github.com/Cdlane24399/suna-fork.git
cd suna-fork

# Run one-click deployment
python deploy.py --method local
```

### Platform Deploy Buttons

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/your-template-id)
[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/Cdlane24399/suna-fork)

## 🏠 Local Development

### Prerequisites

- Docker and Docker Compose
- Python 3.11+
- Node.js 18+
- Git

### Setup Steps

1. **Clone and Setup**
   ```bash
   git clone https://github.com/Cdlane24399/suna-fork.git
   cd suna-fork
   python setup.py  # Interactive setup wizard
   ```

2. **Start Services**
   ```bash
   python start.py  # Start all services
   # OR manually with docker-compose
   docker compose up -d
   ```

3. **Access the Application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

## 🏭 Production Deployment

### Using Production Docker Compose

1. **Prepare Environment**
   ```bash
   cp backend/.env.example backend/.env
   cp frontend/.env.example frontend/.env.local
   # Edit .env files with production values
   ```

2. **Deploy**
   ```bash
   python deploy.py --method production
   # OR manually
   docker compose -f docker-compose.prod.yaml up -d
   ```

### Server Requirements

**Minimum:**
- 2 CPU cores
- 4GB RAM
- 20GB storage
- Docker & Docker Compose

**Recommended:**
- 4+ CPU cores
- 8GB+ RAM
- 50GB+ SSD storage
- Load balancer (nginx/Cloudflare)

## ☁️ Cloud Platform Deployments

### Railway

1. **One-Click Deploy**
   [![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/your-template-id)

2. **Manual Setup**
   - Connect GitHub repository to Railway
   - The `railway.toml` file is pre-configured
   - Set environment variables in Railway dashboard
   - Deploy automatically

### Render

1. **Blueprint Deployment**
   - Use the included `render.yaml` configuration
   - Connect your GitHub repository
   - Set environment variables in Render dashboard

2. **Manual Service Setup**
   - Create Redis service
   - Create backend web service (Docker)
   - Create frontend web service (Docker)
   - Configure environment variables

### Vercel (Frontend) + Railway/Render (Backend)

1. **Frontend on Vercel**
   ```bash
   # Set build settings in Vercel:
   # Framework: Next.js
   # Root Directory: frontend
   # Build Command: npm run build
   # Output Directory: .next
   ```

2. **Backend on Railway/Render**
   - Deploy backend and worker services separately
   - Update `NEXT_PUBLIC_BACKEND_URL` in Vercel

### DigitalOcean App Platform

1. **Create App**
   - Connect GitHub repository
   - Use `docker-compose.prod.yaml` as reference
   - Configure services:
     - Redis (managed database)
     - Backend (Docker service)
     - Frontend (Docker service)

## ⚙️ Environment Configuration

### Required Environment Variables

#### Backend (.env)
```bash
# Database
SUPABASE_URL=your_supabase_url
SUPABASE_ANON_KEY=your_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_service_key

# Redis
REDIS_HOST=redis
REDIS_PORT=6379

# LLM Provider (choose one)
ANTHROPIC_API_KEY=your_anthropic_key
OPENAI_API_KEY=your_openai_key

# Additional APIs
TAVILY_API_KEY=your_tavily_key    # Web search
FIRECRAWL_API_KEY=your_firecrawl_key  # Web scraping
```

#### Frontend (.env.local)
```bash
NEXT_PUBLIC_ENV_MODE=production
NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_anon_key
NEXT_PUBLIC_BACKEND_URL=https://your-backend-url.com/api
NEXT_PUBLIC_URL=https://your-frontend-url.com
```

### Setting Up Supabase

1. Create account at [Supabase](https://supabase.com)
2. Create new project
3. Get Project URL and API keys from Settings → API
4. Run database migrations (if any)

### Getting API Keys

- **Anthropic**: [console.anthropic.com](https://console.anthropic.com)
- **OpenAI**: [platform.openai.com](https://platform.openai.com)
- **Tavily**: [tavily.com](https://tavily.com)
- **Firecrawl**: [firecrawl.dev](https://firecrawl.dev)

## 🔧 Troubleshooting

### Common Issues

#### 1. Docker Build Failures
```bash
# Clear Docker cache
docker system prune -a
docker compose build --no-cache
```

#### 2. Environment Variables Not Loading
```bash
# Verify .env files exist and have correct syntax
ls -la backend/.env frontend/.env.local
# Check for trailing spaces or special characters
```

#### 3. Database Connection Issues
```bash
# Verify Supabase URL and keys
curl -H "apikey: YOUR_ANON_KEY" "YOUR_SUPABASE_URL/rest/v1/"
```

#### 4. Redis Connection Issues
```bash
# Check Redis is running
docker compose ps redis
# Test Redis connection
docker compose exec redis redis-cli ping
```

### Health Checks

#### Backend Health
```bash
curl http://localhost:8000/health
```

#### Frontend Health
```bash
curl http://localhost:3000
```

#### Docker Services Status
```bash
docker compose ps
docker compose logs [service_name]
```

### Performance Optimization

#### Production Optimizations
1. **Use environment-specific configs**
2. **Enable Redis persistence**
3. **Configure proper resource limits**
4. **Set up log rotation**
5. **Use a reverse proxy (nginx)**

#### Scaling Considerations
- **Backend**: Scale worker processes based on CPU cores
- **Frontend**: Use CDN for static assets
- **Database**: Consider read replicas for high traffic
- **Redis**: Use Redis Cluster for high availability

## 📊 Monitoring

### Basic Monitoring
```bash
# Service status
docker compose ps

# Resource usage
docker stats

# Logs
docker compose logs -f --tail=100
```

### Production Monitoring
- **Uptime monitoring**: UptimeRobot, Pingdom
- **Application monitoring**: Sentry, LogRocket
- **Infrastructure monitoring**: DataDog, New Relic
- **Log aggregation**: ELK stack, Fluentd

## 🔄 Updates and Maintenance

### Updating the Application
```bash
# Pull latest changes
git pull origin main

# Rebuild and restart
docker compose build
docker compose up -d
```

### Backup Strategy
1. **Database**: Use Supabase built-in backups
2. **Redis data**: Configure Redis persistence
3. **Application data**: Regular file system backups
4. **Environment configs**: Store securely in version control

## 📞 Support

- **Documentation**: [Self-Hosting Guide](./SELF-HOSTING.md)
- **Issues**: [GitHub Issues](https://github.com/Cdlane24399/suna-fork/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Cdlane24399/suna-fork/discussions)

---

**Ready to deploy?** Start with the [Quick Start](#quick-start) section above! 🚀