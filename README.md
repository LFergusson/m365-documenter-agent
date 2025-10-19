# Browser Agent - Microservices Architecture

A browser automation and analysis system built with a microservice architecture that maximizes code reuse through shared components.

## 🏗️ Architecture

This project uses a **monorepo with shared packages** approach for easy code reuse across microservices:

```
browser_agent/
├── code/                       # All application code
│   ├── shared/                # Shared components (models, utils, middleware)
│   │   ├── models/           # Common data models
│   │   └── utils/            # Utility functions
│   └── services/             # Individual microservices
│       ├── api/              # REST API service
│       ├── browser/          # Browser automation service (future)
│       └── analysis/         # Analysis service (future)
├── infra/                     # Infrastructure as Code (Bicep)
└── pyproject.toml            # Single dependency management
```

## ✨ Benefits of This Structure

### 1. **Easy Code Reuse**
- Shared code in `code/shared/` is available to all services
- Import shared components: `from shared.models import TestStatusResponse`
- No complex package management or version conflicts

### 2. **Simple Dependency Management**
- Single `pyproject.toml` file for all dependencies
- No juggling multiple Poetry projects
- Optional dependencies for specific features (`agents`, `dev`)

### 3. **Service Independence**
- Each service in `code/services/` is self-contained
- Services can be deployed independently via Docker
- Clear separation of concerns

### 4. **Easy Development**
- Install once: `pip install -e .`
- Import from anywhere in the codebase
- Standard Python package structure

## 🚀 Getting Started

### Installation

```bash
# Basic installation (API service only)
pip install -e .

# With development tools
pip install -e ".[dev]"

# With agent framework
pip install -e ".[agents]"

# Everything
pip install -e ".[dev,agents]"
```

### Running Services

#### API Service
```bash
# Development with auto-reload
uvicorn services.api.app:app --reload --host 0.0.0.0 --port 8000

# Or using Docker
cd code/services/api
docker build -t browser-agent-api -f Dockerfile ../../..
docker run -p 8000:8000 browser-agent-api
```

#### Test the API
```bash
curl http://localhost:8000/status
curl http://localhost:8000/health
```

## 📦 Shared Components

### Models (`shared/models/`)
Common data structures used across services:
- `TestStatusResponse` - Standard status response

### Utils (`shared/utils/`)
Utility functions and helpers shared across services.

## 🔧 Adding New Services

1. **Create service directory**:
   ```bash
   mkdir -p code/services/new_service
   ```

2. **Create service files**:
   ```python
   # code/services/new_service/app.py
   from shared.models import TestStatusResponse
   from fastapi import FastAPI
   
   app = FastAPI(title="New Service")
   
   @app.get("/status")
   async def status():
       return TestStatusResponse()
   ```

3. **Create Dockerfile** (optional):
   ```dockerfile
   FROM python:3.12-slim
   WORKDIR /app
   COPY pyproject.toml ./
   COPY code/ ./code/
   RUN pip install -e .
   CMD ["uvicorn", "services.new_service.app:app", "--host", "0.0.0.0"]
   ```

## 🧪 Testing

```bash
# Run tests
pytest

# Format code
black code/

# Lint code
ruff check code/
```

## 📝 Code Organization Guidelines

### What Goes in `shared/`
✅ Data models (Pydantic, dataclasses)  
✅ Common middleware (auth, logging)  
✅ Utility functions  
✅ Configuration management  
✅ Database schemas  
✅ API clients for service communication

### What Stays in `services/`
✅ Service-specific business logic  
✅ Service-specific routes/handlers  
✅ Service entry points

## 🐳 Docker Deployment

Each service can be containerized independently while sharing the same codebase:

```bash
# Build API service
docker build -t browser-agent-api -f code/services/api/Dockerfile .

# Run
docker run -p 8000:8000 browser-agent-api
```

## 🤝 Development Workflow

1. **Make changes to shared code** in `code/shared/`
2. **All services immediately have access** - no reinstall needed (editable install)
3. **Add service-specific code** in respective `code/services/` directory
4. **Test individual services** independently
5. **Deploy** services as needed

## 📚 Technology Stack

- **Python 3.12+**
- **FastAPI** - Modern web framework
- **Uvicorn** - ASGI server
- **Agent Framework** - (optional) AI agent capabilities
- **Azure** - Deployment platform

## 🔗 Related Files

- `azure.yaml` - Azure deployment configuration
- `infra/` - Bicep infrastructure templates
- `pyproject.toml` - Python project configuration

---

**Note**: This structure prioritizes simplicity and ease of development. As the project grows, you can introduce more sophisticated patterns if needed.
