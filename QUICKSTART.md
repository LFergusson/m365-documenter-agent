# Quick Start Guide

## What You Have Now

A **microservice architecture** with:
- ✅ All code under `/code` folder
- ✅ Single `pyproject.toml` (no Poetry complexity)
- ✅ Shared code automatically available to all services
- ✅ Working API service

## Quick Commands

```bash
# Install everything
pip install -e .

# Run API service
uvicorn services.api.app:app --reload --port 8000

# Test it
curl http://localhost:8000/status
# Response: {"status":"ok"}

# Add new shared model
cat > code/shared/models/user.py << 'EOF'
from dataclasses import dataclass

@dataclass
class User:
    id: int
    name: str
    email: str
EOF

# Use in any service immediately
# code/services/api/app.py
from shared.models.user import User  # ✅ Works!
```

## Structure
```
code/
├── shared/              # Shared code (models, utils)
│   ├── models/         
│   │   └── responses.py
│   └── utils/
└── services/           # Microservices
    ├── api/
    │   ├── app.py      # FastAPI application
    │   └── Dockerfile
    └── browser/
        └── app.py      # Example second service
```

## No Poetry Complexity!

Instead of managing:
- ❌ Multiple `pyproject.toml` files
- ❌ Multiple Poetry environments  
- ❌ Complex package publishing
- ❌ Version conflicts between services

You have:
- ✅ One `pip install -e .`
- ✅ Direct imports: `from shared.models import X`
- ✅ Simple, fast development

## Questions?

**Q: How do I share code between services?**
A: Put it in `code/shared/` and import: `from shared.models import MyModel`

**Q: How do I add a new service?**
A: Create `code/services/new_service/app.py` and import shared code

**Q: Do I need to reinstall after changing shared code?**
A: No! Editable install (`-e`) means changes are immediate

**Q: How do I deploy services separately?**
A: Each service has its own Dockerfile that copies shared code

**Q: What if services need different dependencies?**
A: Add them to the main `pyproject.toml` or use optional dependencies

## See Also

- `README.md` - Full documentation
- `docs/ARCHITECTURE.md` - Detailed architecture explanation
- `pyproject.toml` - Project configuration
