# Microsoft 365 Documenter - Agent

![](/docs/img/DocoAgent.png)

This repository provides a series of Agents built on Agent-Framework to document a Microsoft 365 Tenancy in As Built As Configured documentation. It also allows for the development of Maester Tests.



## 🤖 Agents
The agents in this include:
[x] Graph Documenter
[] Graph Retriever 
[] Document Writer
[] Maester Author

Each agent has a specific purpose and prompts that are used to 

## 🏗️ Architecture
This project is a series of serverless components built on Azure PaaS. The code is architected as a series of microservices including the: 
[X] Agent API (A2A Support)
[X] Agent UI (User Interface)
[X] Admin UI

### Infrastructure:
The application is intended to be hosted on Azure App Services running docker containers.

### Code
This project uses a **monorepo with shared packages** approach for easy code reuse across microservices:

```
browser_agent/
├── src/                      # All application code
│   ├── shared/               # Shared components (models, utils, middleware)
│   │   ├── models/           # Common data models
│   │   └── utils/            # Utility functions
│   └── services/             # Individual microservices
│       ├── api/              # REST API service
│       ├── web-app/          # Browser automation service (future)
│       └── admin-app/        # Analysis service (future)
├── infra/                    # Infrastructure as Code (Bicep)
└── pyproject.toml            # Single dependency management
```