# support 기술 스택 list

> 멀티 agent system이 support할 project type별 언어 and framework list

---

## 1. Web-Fullstack (FE + BE 분리)

### Backend

#### Python
- **FastAPI** ⭐ (currently support 중)
  - async, type 힌트, auto documentation
  - 사용 사례: RESTful API, 마이크로서비스
- **Flask**
  - 경량, 유연성
  - 사용 사례: 소규모 API, 프로토type
- **Django REST Framework (DRF)**
  - Django 기반 REST API
  - 사용 사례: 기업용 API, Admin required 시

#### Node.js
- **Express.js**
  - 미니멀, 생태계 풍부
  - 사용 사례: RESTful API, 실time 서버
- **NestJS**
  - TypeScript, Angular style 아키텍처
  - 사용 사례: 엔터프라이즈급 backend
- **Fastify**
  - 고performance, 플러그인 아키텍처
  - 사용 사례: 고트래픽 API

#### Go
- **Gin**
  - 고performance HTTP framework
  - 사용 사례: 마이크로서비스, API 게이트웨이
- **Echo**
  - 미들웨어 중심, 빠름
  - 사용 사례: RESTful API
- **Fiber**
  - Express style, 제로 메모리 할당
  - 사용 사례: 고performance API

#### Rust
- **Axum**
  - Tokio 기반, type Plan전성
  - 사용 사례: 고performance API, system 프로그래밍
- **Actix-web**
  - Actor model, 매우 빠름
  - 사용 사례: 실time 서비스, 고트래픽 API

#### Java
- **Spring Boot (Webflux)**
  - async 리액티브 프로그래밍
  - 사용 사례: 엔터프라이즈 마이크로서비스

### Frontend

#### React 생태계
- **Next.js** ⭐ (currently support 중)
  - SSR, SSG, file 기반 라우팅
  - 사용 사례: SEO important web앱, 대규모 project
- **Vite + React**
  - 빠른 HMR, 경량
  - 사용 사례: SPA, dashboard
- **Remix**
  - 중첩 라우팅, 네이티브 폼
  - 사용 사례: data 중심 web앱

#### Vue 생태계
- **Nuxt.js**
  - SSR, file 기반 라우팅
  - 사용 사례: Vue 선호 팀, SEO required 시
- **Vite + Vue 3**
  - Composition API, TypeScript
  - 사용 사례: SPA, administrator dashboard

#### Svelte 생태계
- **SvelteKit**
  - 컴file 타임 framework, 경량
  - 사용 사례: 고performance required 시, 작은 번들 size

#### other
- **Angular**
  - TypeScript 네이티브, 완전한 framework
  - 사용 사례: 엔터프라이즈 대규모 project
- **Solid.js**
  - 세밀한 반응성, React style 문법
  - 사용 사례: 고performance 인터랙티브 UI

---

## 2. Web-MVC (Monolithic)

### Python
- **Django** ⭐
  - ORM, Admin, template 엔진 내장
  - 사용 사례: 콘텐츠 관리, 전통적 web앱
  - template: Django Template Language (DTL)

### Ruby
- **Ruby on Rails**
  - Convention over Configuration
  - 사용 사례: 스타트업 MVP, CRUD web앱
  - template: ERB

### Java
- **Spring Boot (MVC)**
  - Thymeleaf, JSP
  - 사용 사례: 엔터프라이즈 web 애플리케이션
  - template: Thymeleaf, JSP

### PHP
- **Laravel**
  - Eloquent ORM, Blade template
  - 사용 사례: CMS, 전통적 web앱
  - template: Blade

### C#
- **.NET (ASP.NET Core MVC)**
  - Razor Pages, Entity Framework
  - 사용 사례: 엔터프라이즈 web앱, Windows 환경
  - template: Razor

---

## 3. CLI Tool

### Python
- **Click** ⭐
  - 데코레이터 기반, 간단한 구문
  - 사용 사례: 범용 CLI 도구
- **Typer**
  - type 힌트 기반, Click 기반
  - 사용 사례: 현대적 Python CLI
- **argparse**
  - standard library
  - 사용 사례: add 의존성 없는 CLI

### Go
- **Cobra** ⭐
  - kubectl, docker CLI에서 사용
  - 사용 사례: 복잡한 서브커맨드 Structure
- **urfave/cli**
  - 간단한 API
  - 사용 사례: 중소규모 CLI

### Rust
- **clap** ⭐
  - 파생 매크로, performance 우수
  - 사용 사례: 고performance CLI, system 도구
- **structopt** (clap v3로 통합)
  - Structure체 기반 argument 파싱
  - 사용 사례: type Plan전 CLI

### Node.js
- **Commander.js**
  - Express style API
  - 사용 사례: Node 생태계 CLI
- **yargs**
  - 복잡한 argument 파싱
  - 사용 사례: 다양한 option support

### Java
- **picocli**
  - 어노테이션 기반
  - 사용 사례: 엔터프라이즈 CLI 도구

---

## 4. Desktop App

### Cross-Platform

#### Electron (JavaScript/TypeScript)
- **Electron + React** ⭐
  - 사용 사례: VS Code, Slack, Discord
  - 장점: web 기술 활용, 풍부한 생태계
  - 단점: 무거운 번들 size
- **Electron + Vue**
  - 사용 사례: Vue 선호 팀
- **Electron + Svelte**
  - 사용 사례: 경량 desktop 앱

#### Tauri (Rust + Web)
- **Tauri + React/Vue/Svelte** ⭐
  - 사용 사례: 경량 desktop 앱 (Electron 대Plan)
  - 장점: 작은 번들 size (3-5MB), 빠름
  - 단점: Rust 컴file 환경 required

#### Flutter (Dart)
- **Flutter Desktop**
  - 사용 사례: 크로스 플랫폼 (mobile + desktop)
  - 장점: 네이티브 performance, 일관된 UI
  - 단점: 상대적으로 작은 desktop 생태계

#### Qt
- **Qt (C++/Python)** ⭐
  - PyQt, PySide6
  - 사용 사례: professional 도구 (Autodesk, Adobe partial 툴)
  - 장점: 진정한 네이티브 UI, performance
  - 단점: learning 곡선

### Platform-Specific

#### macOS
- **SwiftUI** ⭐
  - Swift 네이티브
  - 사용 사례: macOS 전용 앱
  - 장점: 최고의 macOS 통합
- **AppKit (Objective-C/Swift)**
  - 레거시 macOS 앱
  - 사용 사례: 복잡한 macOS 전용 feature

#### Windows
- **WPF (C#/.NET)** ⭐
  - XAML 기반
  - 사용 사례: Windows 엔터프라이즈 앱
- **WinUI 3 (C#/.NET)**
  - 현대적 Windows UI
  - 사용 사례: Windows 11 네이티브 앱
- **Windows Forms (C#/.NET)**
  - 레거시, 빠른 프로토타이핑
  - 사용 사례: 내부 도구

---

## 5. Mobile App

### Cross-Platform
- **React Native**
  - JavaScript/TypeScript
  - 사용 사례: iOS + Android concurrent development
- **Flutter**
  - Dart
  - 사용 사례: 네이티브 performance required 시
- **Expo (React Native 기반)**
  - 사용 사례: 빠른 프로토타이핑

### Native
- **SwiftUI (iOS)**
  - Swift
  - 사용 사례: iOS 전용 앱
- **Jetpack Compose (Android)**
  - Kotlin
  - 사용 사례: Android 전용 앱

---

## 6. Library / SDK

### JavaScript/TypeScript
- **npm package**
  - 번들러: Rollup, tsup, Vite
  - 사용 사례: React 컴포넌트 library, 유틸리티

### Python
- **pip package**
  - 빌드 도구: setuptools, poetry, hatch
  - 사용 사례: data analytics library, API 클라이언트

### Rust
- **crates.io**
  - Cargo
  - 사용 사례: system library, WASM module

### Go
- **Go module**
  - go mod
  - 사용 사례: CLI library, 네트워크 유틸리티

### Java
- **Maven/Gradle package**
  - 사용 사례: 엔터프라이즈 유틸리티, Android library

---

## 7. Data Pipeline / ETL

### Python
- **Apache Airflow** ⭐
  - DAG 기반 워크플로우
  - 사용 사례: data pipeline 오케스트레이션
- **Prefect**
  - 현대적 워크플로우 엔진
  - 사용 사례: data 엔지니어링
- **Luigi**
  - Spotify development
  - 사용 사례: 배치 task pipeline

### Scala
- **Apache Spark**
  - 대규모 data process
  - 사용 사례: 빅data analytics

### SQL-based
- **dbt (Data Build Tool)**
  - SQL 기반 변환
  - 사용 사례: data 웨어하우스 model링

---

## 8. other

### Game Development
- **Unity (C#)**
  - 크로스 플랫폼 게임
- **Unreal Engine (C++)**
  - AAA 게임

### WebAssembly
- **Rust (wasm-pack)**
  - 브라우저 고performance 연산
- **AssemblyScript**
  - TypeScript style WASM

### Embedded / IoT
- **Rust (embedded-hal)**
  - 임베디드 system
- **C/C++ (Arduino, ESP32)**
  - IoT 디바이스

---

## 우선ranking (1차 support Goal)

현실적으로 모든 스택을 support하기는 어려우므로, 사용 frequency와 수요를 고려한 우선ranking:

### Tier 1 (immediately support)
1. **Web-Fullstack**
   - BE: FastAPI (Python) ✅ 기존 support
   - FE: Next.js (React) ✅ 기존 support
   - BE: Express.js (Node.js) 🆕
   - BE: NestJS (Node.js) 🆕

2. **Web-MVC**
   - Django (Python) 🆕
   - Spring Boot MVC (Java) 🆕

3. **CLI Tool**
   - Click (Python) 🆕
   - Cobra (Go) 🆕

### Tier 2 (next stage)
4. **Desktop App**
   - Tauri + React 🆕
   - Electron + React 🆕

5. **Library**
   - npm package (TypeScript) 🆕
   - pip package (Python) 🆕

### Tier 3 (수요 confirmation 후)
6. **Mobile App**
   - React Native 🆕
   - Flutter 🆕

7. **Data Pipeline**
   - Airflow 🆕

---

## next stage

각 기술 스택별로 must 작성 할 documentation:

1. **코딩 룰** (`.rules/{카테고리}/{스택}.md`)
   - directory Structure
   - 아키텍처 pattern
   - 네이밍 컨벤션
   - 보Plan guide
   - 테스팅 전략

2. **PM template** (`.agents/pm/templates/{타입}.md`)
   - 산출물 형식
   - specification template

3. **코딩 agent template** (`.agents/coding/templates/{타입}.md`)
   - task 순서
   - file create 순서
   - 의존성 관리

4. **QA template** (`.agents/qa/templates/{타입}.md`)
   - test framework
   - test Structure
   - coverage Goal

---

**작성 일시**: 2026-03-12
**version**: v0.0.1-draft
