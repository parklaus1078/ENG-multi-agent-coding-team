# Supported Tech Stacks

> Languages and frameworks supported by the multi-agent system, organized by project type

---

## 1. Web-Fullstack (FE + BE Separated)

### Backend

#### Python
- **FastAPI** ⭐ (Currently Supported)
  - Async, type hints, automatic documentation
  - Use cases: RESTful API, microservices
- **Flask**
  - Lightweight, flexible
  - Use cases: Small APIs, prototypes
- **Django REST Framework (DRF)**
  - Django-based REST API
  - Use cases: Enterprise APIs, when Admin needed

#### Node.js
- **Express.js**
  - Minimal, rich ecosystem
  - Use cases: RESTful API, real-time servers
- **NestJS**
  - TypeScript, Angular-style architecture
  - Use cases: Enterprise-grade backends
- **Fastify**
  - High performance, plugin architecture
  - Use cases: High-traffic APIs

#### Go
- **Gin**
  - High-performance HTTP framework
  - Use cases: Microservices, API gateways
- **Echo**
  - Middleware-centric, fast
  - Use cases: RESTful APIs
- **Fiber**
  - Express-style, zero memory allocation
  - Use cases: High-performance APIs

#### Rust
- **Axum**
  - Tokio-based, type safety
  - Use cases: High-performance APIs, systems programming
- **Actix-web**
  - Actor model, very fast
  - Use cases: Real-time services, high-traffic APIs

#### Java
- **Spring Boot (Webflux)**
  - Async reactive programming
  - Use cases: Enterprise microservices

### Frontend

#### React Ecosystem
- **Next.js** ⭐ (Currently Supported)
  - SSR, SSG, file-based routing
  - Use cases: SEO-critical web apps, large projects
- **Vite + React**
  - Fast HMR, lightweight
  - Use cases: SPAs, dashboards
- **Remix**
  - Nested routing, native forms
  - Use cases: Data-centric web apps

#### Vue Ecosystem
- **Nuxt.js**
  - SSR, file-based routing
  - Use cases: Vue-preferring teams, when SEO needed
- **Vite + Vue 3**
  - Composition API, TypeScript
  - Use cases: SPAs, admin dashboards

#### Svelte Ecosystem
- **SvelteKit**
  - Compile-time framework, lightweight
  - Use cases: When high performance needed, small bundle size

#### Other
- **Angular**
  - TypeScript native, complete framework
  - Use cases: Enterprise large-scale projects
- **Solid.js**
  - Fine-grained reactivity, React-style syntax
  - Use cases: High-performance interactive UIs

---

## 2. Web-MVC (Monolithic)

### Python
- **Django** ⭐
  - ORM, Admin, built-in template engine
  - Use cases: Content management, traditional web apps
  - Templates: Django Template Language (DTL)

### Ruby
- **Ruby on Rails**
  - Convention over Configuration
  - Use cases: Startup MVPs, CRUD web apps
  - Templates: ERB

### Java
- **Spring Boot (MVC)**
  - Thymeleaf, JSP
  - Use cases: Enterprise web applications
  - Templates: Thymeleaf, JSP

### PHP
- **Laravel**
  - Eloquent ORM, Blade templates
  - Use cases: CMS, traditional web apps
  - Templates: Blade

### C#
- **.NET (ASP.NET Core MVC)**
  - Razor Pages, Entity Framework
  - Use cases: Enterprise web apps, Windows environments
  - Templates: Razor

---

## 3. CLI Tool

### Python
- **Click** ⭐
  - Decorator-based, simple syntax
  - Use cases: General-purpose CLI tools
- **Typer**
  - Type hint-based, Click-based
  - Use cases: Modern Python CLIs
- **argparse**
  - Standard library
  - Use cases: CLI without additional dependencies

### Go
- **Cobra** ⭐
  - Used by kubectl, docker CLI
  - Use cases: Complex subcommand structures
- **urfave/cli**
  - Simple API
  - Use cases: Small to medium CLIs

### Rust
- **clap** ⭐
  - Derive macros, excellent performance
  - Use cases: High-performance CLIs, system tools
- **structopt** (merged into clap v3)
  - Struct-based argument parsing
  - Use cases: Type-safe CLIs

### Node.js
- **Commander.js**
  - Express-style API
  - Use cases: Node ecosystem CLIs
- **yargs**
  - Complex argument parsing
  - Use cases: Various option support

### Java
- **picocli**
  - Annotation-based
  - Use cases: Enterprise CLI tools

---

## 4. Desktop App

### Cross-Platform

#### Electron (JavaScript/TypeScript)
- **Electron + React** ⭐
  - Use cases: VS Code, Slack, Discord
  - Pros: Web tech utilization, rich ecosystem
  - Cons: Heavy bundle size
- **Electron + Vue**
  - Use cases: Vue-preferring teams
- **Electron + Svelte**
  - Use cases: Lightweight desktop apps

#### Tauri (Rust + Web)
- **Tauri + React/Vue/Svelte** ⭐
  - Use cases: Lightweight desktop apps (Electron alternative)
  - Pros: Small bundle size (3-5MB), fast
  - Cons: Requires Rust compilation environment

#### Flutter (Dart)
- **Flutter Desktop**
  - Use cases: Cross-platform (mobile + desktop)
  - Pros: Native performance, consistent UI
  - Cons: Relatively small desktop ecosystem

#### Qt
- **Qt (C++/Python)** ⭐
  - PyQt, PySide6
  - Use cases: Professional tools (Autodesk, some Adobe tools)
  - Pros: True native UI, performance
  - Cons: Learning curve

### Platform-Specific

#### macOS
- **SwiftUI** ⭐
  - Swift native
  - Use cases: macOS-only apps
  - Pros: Best macOS integration
- **AppKit (Objective-C/Swift)**
  - Legacy macOS apps
  - Use cases: Complex macOS-specific features

#### Windows
- **WPF (C#/.NET)** ⭐
  - XAML-based
  - Use cases: Windows enterprise apps
- **WinUI 3 (C#/.NET)**
  - Modern Windows UI
  - Use cases: Windows 11 native apps
- **Windows Forms (C#/.NET)**
  - Legacy, rapid prototyping
  - Use cases: Internal tools

---

## 5. Mobile App

### Cross-Platform
- **React Native**
  - JavaScript/TypeScript
  - Use cases: iOS + Android simultaneous development
- **Flutter**
  - Dart
  - Use cases: When native performance needed
- **Expo (React Native-based)**
  - Use cases: Rapid prototyping

### Native
- **SwiftUI (iOS)**
  - Swift
  - Use cases: iOS-only apps
- **Jetpack Compose (Android)**
  - Kotlin
  - Use cases: Android-only apps

---

## 6. Library / SDK

### JavaScript/TypeScript
- **npm package**
  - Bundlers: Rollup, tsup, Vite
  - Use cases: React component libraries, utilities

### Python
- **pip package**
  - Build tools: setuptools, poetry, hatch
  - Use cases: Data analysis libraries, API clients

### Rust
- **crates.io**
  - Cargo
  - Use cases: System libraries, WASM modules

### Go
- **Go module**
  - go mod
  - Use cases: CLI libraries, network utilities

### Java
- **Maven/Gradle package**
  - Use cases: Enterprise utilities, Android libraries

---

## 7. Data Pipeline / ETL

### Python
- **Apache Airflow** ⭐
  - DAG-based workflow
  - Use cases: Data pipeline orchestration
- **Prefect**
  - Modern workflow engine
  - Use cases: Data engineering
- **Luigi**
  - Developed by Spotify
  - Use cases: Batch job pipelines

### Scala
- **Apache Spark**
  - Large-scale data processing
  - Use cases: Big data analytics

### SQL-based
- **dbt (Data Build Tool)**
  - SQL-based transformations
  - Use cases: Data warehouse modeling

---

## 8. Other

### Game Development
- **Unity (C#)**
  - Cross-platform games
- **Unreal Engine (C++)**
  - AAA games

### WebAssembly
- **Rust (wasm-pack)**
  - Browser high-performance computing
- **AssemblyScript**
  - TypeScript-style WASM

### Embedded / IoT
- **Rust (embedded-hal)**
  - Embedded systems
- **C/C++ (Arduino, ESP32)**
  - IoT devices

---

## Priority (Phase 1 Support Goals)

Realistically, supporting all stacks is difficult, so priorities based on usage frequency and demand:

### Tier 1 (Immediate Support)
1. **Web-Fullstack**
   - BE: FastAPI (Python) ✅ Already supported
   - FE: Next.js (React) ✅ Already supported
   - BE: Express.js (Node.js) 🆕
   - BE: NestJS (Node.js) 🆕

2. **Web-MVC**
   - Django (Python) 🆕
   - Spring Boot MVC (Java) 🆕

3. **CLI Tool**
   - Click (Python) 🆕
   - Cobra (Go) 🆕

### Tier 2 (Next Phase)
4. **Desktop App**
   - Tauri + React 🆕
   - Electron + React 🆕

5. **Library**
   - npm package (TypeScript) 🆕
   - pip package (Python) 🆕

### Tier 3 (After Demand Confirmation)
6. **Mobile App**
   - React Native 🆕
   - Flutter 🆕

7. **Data Pipeline**
   - Airflow 🆕

---

## Next Steps

Documents to write for each tech stack:

1. **Coding Rules** (`.rules/{category}/{stack}.md`)
   - Directory structure
   - Architecture patterns
   - Naming conventions
   - Security guidelines
   - Testing strategies

2. **PM Templates** (`.agents/pm/templates/{type}.md`)
   - Deliverable format
   - Specification templates

3. **Coding Agent Templates** (`.agents/coding/templates/{type}.md`)
   - Work order
   - File creation order
   - Dependency management

4. **QA Templates** (`.agents/qa/templates/{type}.md`)
   - Testing frameworks
   - Test structure
   - Coverage goals

---

**Written**: 2026-03-12
**Version**: v0.0.1-draft
