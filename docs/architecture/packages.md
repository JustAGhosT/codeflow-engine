# CodeFlow Package Architecture

## Overview

CodeFlow is built as a modular system with a clear separation of concerns across multiple packages,
supporting both .NET and Python runtimes. This document outlines the package structure,
responsibilities, and relationships between different components.

## Core Packages (NuGet/.NET)

### codeflow.Core

**NuGet**: `codeflow.Core`**Purpose**: Core interfaces, models, and shared utilities used throughout
the platform.

**Key Components**:

- Base interfaces for plugins and extensions
- Core domain models and DTOs
- Common utilities and helpers
- Base exception types
- Configuration models

### codeflow.Plugins

**NuGet**: `codeflow.Plugins`**Purpose**: Base interfaces and utilities for developing CodeFlow plugins.

**Key Components**:

- `IPlugin` interface
- Plugin lifecycle management
- Plugin configuration schemas
- Base classes for common plugin types
- Plugin metadata attributes

### codeflow.Extensions

**NuGet**: `codeflow.Extensions`**Purpose**: Common extensions and utilities used across the platform.

**Key Components**:

- Collection extensions
- String utilities
- Reflection helpers
- Async utilities
- Validation extensions

## Language-Specific Runtimes

### codeflow.Python

**NuGet**: `codeflow.Python`**Purpose**: Python runtime integration for codeflow.

**Features**:

- Python 3.13+ script execution
- Virtual environment management
- Dependency resolution with pip/conda
- Python code analysis and introspection
- Integration with ML/AI frameworks (PyTorch, TensorFlow)
- Template processing and generation
- Asynchronous task execution
- GIL-aware thread pooling

### codeflow.Node

**NuGet**: `codeflow.Node`**Purpose**: Node.js runtime integration for codeflow.

**Features**:

- Node.js 22+ script execution
- NPM/Yarn/PNPM package management
- Dependency resolution and auditing
- JavaScript/TypeScript code analysis
- Integration with frontend build tools

## Client Libraries

### @CodeFlow/client (npm)

**Package**: `@CodeFlow/client`**Language**: TypeScript/JavaScript**Purpose**: Official
TypeScript/JavaScript client for interacting with CodeFlow services.

**Features**:

- Type-safe API client
- Promise-based interface
- Browser and Node.js support
- Authentication helpers
- WebSocket support for real-time updates

### codeflow.Client (NuGet)

**NuGet**: `codeflow.Client`**Language**: C#**Purpose**: Official .NET client for CodeFlow services.

**Features**:

- Strongly-typed client
- Async/await support
- Dependency injection integration
- Comprehensive XML documentation
- Built-in retry policies

## Plugin Development

### Plugin Types

1. **Integration Plugins**: Connect to external services (GitHub, GitLab, etc.)
2. **Template Plugins**: Provide templates for PRs, issues, etc.
3. **Analysis Plugins**: Perform code analysis and provide insights
4. **Workflow Plugins**: Define custom workflows and automation

### Plugin Structure

```text
myplugin/
â”œâ”€â”€ src/
â”‚   â”œâ”€â”€ index.ts          # Plugin entry point
â”‚   â”œâ”€â”€ config.schema.ts  # Configuration schema
â”‚   â””â”€â”€ ...               # Plugin implementation
â”œâ”€â”€ package.json          # Plugin metadata and dependencies
â””â”€â”€ README.md             # Documentation
```

### Development Guidelines

- Follow the Plugin Development Kit (PDK) conventions
- Implement required interfaces
- Provide comprehensive documentation
- Include unit and integration tests
- Support configuration via environment variables
- Implement proper error handling and logging

## Plugin Packages

### @CodeFlow/plugin-github

**Package**: `@CodeFlow/plugin-github`**Type**: Integration Plugin**Purpose**: GitHub integration for
codeflow.

**Features**:

- Repository management
- Pull request automation
- Status checks and required contexts
- Webhook handling and validation
- GitHub Actions integration
- GitHub Apps support
- Fine-grained permissions

### @CodeFlow/plugin-azure

**Package**: `@CodeFlow/plugin-azure`**Type**: Integration Plugin**Purpose**: Azure DevOps integration
for codeflow.

**Features**:

- Azure Repos integration
- Pull request automation
- Pipeline integration and gating
- Work item linking and tracking
- Azure DevOps REST API client
- Service principal authentication

### @CodeFlow/plugin-gitlab

**Package**: `@CodeFlow/plugin-gitlab`**Type**: Integration Plugin**Purpose**: GitLab integration for
codeflow.

**Features**:

- GitLab repository integration
- Merge request automation
- CI/CD pipeline integration
- Issue and epic linking
- GitLab API client with pagination
- Group and subgroup support

### @CodeFlow/plugin-autoweave

**Package**: `@CodeFlow/plugin-autoweave`**Type**: Integration Plugin**Purpose**: AutoWeave
integration for codeflow.

**Features**:

- Bidirectional synchronization
- Template and asset management
- Configuration synchronization
- Status reporting
- Webhook support

## Template System

### Core Template Packages

#### @autoweave/template-engine

**Package**: `@autoweave/template-engine`**Purpose**: Core template processing engine.

**Features**:

- Multi-template language support (Liquid, Handlebars, etc.)
- Template inheritance and composition
- Built-in template functions and filters
- Caching and incremental rendering
- Dependency tracking

#### @autoweave/template-sdk

**Package**: `@autoweave/template-sdk`**Purpose**: Development kit for creating custom templates.

**Features**:

- TypeScript/JavaScript API
- Template validation and linting
- Testing utilities
- Debugging tools
- Documentation generation

#### @autoweave/template-registry

**Package**: `@autoweave/template-registry`**Purpose**: Central template repository and management.

**Features**:

- Template discovery and resolution
- Versioning and semantic version support
- Access control and permissions
- Template metadata and documentation
- Dependency management

### Standard Template Packages

#### @autoweave/templates-standard

**Package**: `@autoweave/templates-standard`**Type**: Template Package**Purpose**: Standard Pull
Request templates for common scenarios.

**Included Templates**:

- Feature PR template
- Bugfix PR template
- Documentation PR template
- Chore/refactor PR template
- Release PR template
- Hotfix template
- Experimental feature template

#### @autoweave/templates-security

**Package**: `@autoweave/templates-security`**Type**: Template Package**Purpose**: Security-focused
PR templates and workflows.

**Included Templates**:

- Security vulnerability fix template
- Dependency update template
- Security policy update template
- Security review checklist
- CVE mitigation template
- Secret rotation template
- Compliance documentation template

#### @autoweave/templates-ai

**Package**: `@autoweave/templates-ai`**Type**: Template Package**Purpose**: AI/ML focused
templates.

**Included Templates**:

- Model training PR
- Dataset update
- Feature engineering
- Hyperparameter tuning
- Model evaluation report

## Package Relationships

```mermaid
graph TD
    %% Core Packages
    A[codeflow.Core] --> B[codeflow.Plugins]
    A --> C[codeflow.Extensions]

    %% Language Runtimes
    B --> D[codeflow.Python]
    B --> E[codeflow.Node]

    %% Client Libraries
    A --> F[@CodeFlow/client]
    A --> G[codeflow.Client]

    %% Plugin Packages
    B --> H[@CodeFlow/plugin-github]
    B --> I[@CodeFlow/plugin-azure]
    B --> J[@CodeFlow/plugin-gitlab]
    B --> K[@CodeFlow/plugin-autoweave]

    %% Template System
    A --> L[@autoweave/template-engine]
    L --> M[@autoweave/template-sdk]
    L --> N[@autoweave/template-registry]

    %% Template Packages
    N --> O[@autoweave/templates-standard]
    N --> P[@autoweave/templates-security]
    N --> Q[@autoweave/templates-ai]

    %% Python Services
    D --> R[codeflow-python]
    R --> S[codeflow.ai]
    R --> T[codeflow.templates]
    R --> U[codeflow.analysis]

    %% Styling
    classDef core fill:#f9f,stroke:#333
    classDef plugin fill:#9cf,stroke:#333
    classDef template fill:#9f9,stroke:#333
    classDef python fill:#f99,stroke:#333

    class A,B,C core
    class H,I,J,K plugin
    class L,M,N,O,P,Q template
    class R,S,T,U python

    linkStyle 0,1,2,3 stroke:#333,stroke-width:2px
    linkStyle 4,5,6,7,8,9,10,11,12,13 stroke:#999,stroke-width:1px,stroke-dasharray: 5 5

## Versioning and Compatibility

### Package Versioning
All packages follow [Semantic Versioning](https://semver.org/) (SemVer):
- **MAJOR** version for incompatible API changes
- **MINOR** version for backward-compatible functionality
- **PATCH** version for backward-compatible bug fixes

### Template Versioning
Templates use a modified semantic versioning scheme:
- **MAJOR**: Breaking changes to template structure or required context
- **MINOR**: New features or non-breaking changes
- **PATCH**: Bug fixes and improvements
- **PRERELEASE**: Optional pre-release identifiers for development versions

### Compatibility Matrix
| Component             | Min .NET Version | Min Python Version | Node.js Version |
| --------------------- | ---------------- | ------------------ | --------------- |
| Core                  | .NET 9.0         | 3.13               | N/A             |
| Python Services       | N/A              | 3.13+              | N/A             |
| Node.js Plugins       | N/A              | N/A                | 18.x+           |
| Template Engine       | .NET 9.0         | 3.13+              | N/A             |
| AutoWeave Integration | .NET 9.0         | 3.13+              | N/A             |

## Contributing

To contribute to any of the packages:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Update documentation
5. Add/update tests
6. Submit a pull request

## License

All packages are licensed under the MIT License unless otherwise specified.
```
