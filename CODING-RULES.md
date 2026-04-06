# Coding Rules - Multi-Agent Coding Team

> This document consolidates all coding rules that agents (Coding Agent, QA Agent) must follow when developing the Multi-Agent Coding Team system itself.
>
> For project-specific rules, see `team/.rules/` directory.

---

## Table of Contents

1. [General Coding Principles](#1-general-coding-principles)
2. [Backend (FastAPI / Python / PostgreSQL)](#2-backend-fastapi--python--postgresql)
3. [Frontend (Next.js / React / TypeScript)](#3-frontend-nextjs--react--typescript)

---

## 1. General Coding Principles

### 1.1. DRY (Don't Repeat Yourself)

**Principle**: Avoid code duplication. Extract repeated logic into functions, classes, or modules.

```python
# ❌ Bad
def calculate_user_total(user):
    return user.amount * 1.1

def calculate_admin_total(admin):
    return admin.amount * 1.1

# ✅ Good
def calculate_total_with_tax(entity):
    return entity.amount * 1.1
```

### 1.2. KISS (Keep It Simple, Stupid)

**Principle**: Favor simple solutions over complex ones. Don't over-engineer.

```python
# ❌ Overly complex
def is_valid(user):
    return all([
        hasattr(user, 'email') and bool(user.email),
        hasattr(user, 'name') and bool(user.name),
        hasattr(user, 'age') and isinstance(user.age, int) and user.age > 0
    ])

# ✅ Simple and readable
def is_valid(user):
    return user.email and user.name and user.age > 0
```

### 1.3. YAGNI (You Aren't Gonna Need It)

**Principle**: Don't add functionality until it's actually needed.

```python
# ❌ Pre-optimizing for future needs
class User:
    def __init__(self):
        self.cache = {}
        self.backup_cache = {}
        self.tertiary_cache = {}  # Will we ever need 3 caches?

# ✅ Implement only what's needed now
class User:
    def __init__(self):
        self.cache = {}
```

### 1.4. SOLID Principles

#### Single Responsibility Principle (SRP)
A class/function should have one, and only one, reason to change.

```python
# ❌ Multiple responsibilities
class UserManager:
    def create_user(self, data): ...
    def send_welcome_email(self, user): ...
    def log_to_file(self, message): ...

# ✅ Single responsibility
class UserService:
    def create_user(self, data): ...

class EmailService:
    def send_welcome_email(self, user): ...

class Logger:
    def log(self, message): ...
```

#### Open/Closed Principle (OCP)
Open for extension, closed for modification.

```python
# ✅ Use Protocol for extensibility
from typing import Protocol

class PaymentProcessor(Protocol):
    def process(self, amount: float) -> bool: ...

class CreditCardProcessor:
    def process(self, amount: float) -> bool:
        # Credit card logic
        return True

class PayPalProcessor:
    def process(self, amount: float) -> bool:
        # PayPal logic
        return True
```

### 1.5. Function Size Limit

**Rule**: Functions exceeding 50 lines must be split into smaller functions.

```python
# ❌ Too long
def process_order(order):
    # 100 lines of code...
    pass

# ✅ Split into smaller functions
def validate_order(order): ...
def calculate_total(order): ...
def apply_discount(order): ...
def process_payment(order): ...

def process_order(order):
    validate_order(order)
    total = calculate_total(order)
    total = apply_discount(order)
    process_payment(order)
```

### 1.6. Error Handling

**Rule**: All exceptions must be explicitly handled. No silent failures.

```python
# ❌ Silent failure
try:
    result = risky_operation()
except:
    pass

# ✅ Explicit handling
try:
    result = risky_operation()
except ValueError as e:
    logger.error(f"Invalid value: {e}")
    raise
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    raise
```

### 1.7. Logging

**Rule**: Use logger, never `print()`.

```python
# ❌ Never use print
print("User created")

# ✅ Use logger
import logging
logger = logging.getLogger(__name__)
logger.info("User created: user_id=%s", user.id)
```

**Logging Levels**:
- `DEBUG`: Detailed diagnostic information
- `INFO`: General informational messages
- `WARNING`: Warning messages
- `ERROR`: Error messages
- `CRITICAL`: Critical errors

**Never log sensitive information** (passwords, tokens, API keys).

### 1.8. Security Basics

#### Never Hardcode Secrets
```python
# ❌ Never hardcode
API_KEY = "sk-1234567890abcdef"

# ✅ Use environment variables
import os
API_KEY = os.getenv("API_KEY")
```

#### Validate All Inputs
```python
# ✅ Always validate
def create_user(email: str, age: int):
    if not email or "@" not in email:
        raise ValueError("Invalid email")
    if age < 0 or age > 150:
        raise ValueError("Invalid age")
    # proceed...
```

### 1.9. Testing Strategy

#### Unit Tests
Test individual functions/methods in isolation.

```python
# tests/test_user_service.py
async def test_create_user():
    mock_repo = AsyncMock()
    service = UserService(mock_repo)

    user = await service.create_user({"email": "test@example.com"})

    assert user.email == "test@example.com"
    mock_repo.create.assert_called_once()
```

#### Integration Tests
Test interactions between components.

```python
# tests/api/test_users.py
async def test_create_user_endpoint(client):
    response = await client.post("/api/users", json={"email": "test@example.com"})

    assert response.status_code == 201
    assert response.json()["data"]["email"] == "test@example.com"
```

### 1.10. Git Commit Conventions

**Format**: `<type>: <description>`

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `refactor`: Code refactoring
- `docs`: Documentation changes
- `test`: Test additions/changes
- `chore`: Build/tooling changes

**Examples**:
```bash
feat: add user profile endpoint
fix: resolve null pointer in payment processing
refactor: extract email validation to utility
docs: update API documentation for /users endpoint
test: add integration tests for authentication
chore: update dependencies
```

### 1.11. Code Review Checklist

Before submitting code:

- [ ] All tests pass
- [ ] No `print()` statements
- [ ] No hardcoded secrets
- [ ] Error handling added
- [ ] Logging added
- [ ] Type hints added (Python)
- [ ] Docstrings added
- [ ] No code duplication
- [ ] Function size < 50 lines
- [ ] Security considerations addressed

---

## 2. Backend (FastAPI / Python / PostgreSQL)

### 2.1. Project Structure

```
be-project/
├── src/
│   ├── main.py                   # FastAPI app entrypoint
│   ├── core/
│   │   ├── config.py             # pydantic-settings based env loading
│   │   ├── database.py           # Engine, session factory, get_async_db()
│   │   └── exceptions.py         # BaseCustomException + handler
│   ├── api/
│   │   └── v1/
│   │       ├── router.py         # Router integration
│   │       ├── swaggers/         # Swagger response definitions
│   │       └── endpoints/        # Endpoint files (users.py, items.py)
│   ├── models/                   # SQLAlchemy ORM models
│   ├── schemas/                  # Pydantic schemas (Request/Response)
│   ├── services/                 # Business logic
│   │   └── exceptions/           # Domain-specific exceptions
│   ├── repositories/             # DB query layer
│   │   └── protocols/            # Repository interfaces (Protocol)
│   ├── dependencies/             # DI factory functions
│   ├── constants/                # Domain constants/Enums
│   ├── middleware/               # Cross-cutting concerns
│   └── utils/                    # Reusable utilities
│       └── logger.py
├── tests/
│   ├── conftest.py               # pytest fixtures
│   ├── api/v1/
│   ├── services/
│   └── repositories/
├── alembic/                      # DB migrations
├── ruff.toml                     # Linter configuration
└── .envrc.example                # direnv environment variables
```

### 2.2. Layer Responsibilities

| Layer | Responsibility | Forbidden |
|-------|---------------|-----------|
| `endpoints/` | HTTP request/response handling | Business logic |
| `services/` | Business logic | Direct DB queries |
| `repositories/` | DB queries (AsyncSession) | Business logic |
| `schemas/` | Input/output validation | Exposing ORM models |
| `dependencies/` | DI factory functions | Business/query logic |
| `core/` | Infrastructure setup | Domain logic |

### 2.3. Database Configuration

#### Driver Stack
| Purpose | Library |
|---------|---------|
| Async driver | `asyncpg` |
| ORM | `sqlalchemy[asyncio]` (`AsyncSession`, `async_sessionmaker`) |
| Migrations | `alembic` (runs with sync connection) |

#### Engine and Session Factory (`src/core/database.py`)

```python
# src/core/database.py
from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from src.core.config import settings

engine = create_async_engine(
    settings.DATABASE_URL,           # postgresql+asyncpg://...
    pool_size=settings.DATABASE_POOL_SIZE,
    max_overflow=settings.DATABASE_MAX_OVERFLOW,
    pool_pre_ping=True,              # Auto-detect broken connections
    echo=settings.DEBUG,
)

AsyncSessionFactory = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,          # Prevent lazy-load issues after await
    autoflush=False,
    autocommit=False,
)

async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Provides AsyncSession per request.
    Commits on success, rolls back on exception.
    DO NOT import directly - inject via dependencies/.
    """
    async with AsyncSessionFactory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
```

#### ORM Model Base

```python
# src/models/base.py
from datetime import datetime
from sqlalchemy import DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class TimestampMixin:
    """Auto-manage created_at/updated_at. Recommended for all tables."""
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
```

#### ORM Model Rules

```python
# src/models/user.py
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from src.models.base import Base, TimestampMixin

class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
```

**Rules**:
- Use `Mapped[T]` + `mapped_column()` (SQLAlchemy 2.x style)
- **NEVER** use `Column()` syntax (legacy)
- Explicitly specify `nullable` for all columns
- Add `index=True` for frequently queried fields

### 2.4. Repository Pattern with Protocol

#### Protocol Definition (Interface)

**ALWAYS define Protocol BEFORE implementation**.
Services depend on Protocol types, NOT concrete classes.
This ensures OCP (Open/Closed) and LSP (Liskov Substitution) at the type level.

```python
# src/repositories/protocols/user_repository.py
from typing import Protocol
from src.models.user import User

class UserRepositoryProtocol(Protocol):
    async def find_by_id(self, user_id: int) -> User | None: ...
    async def find_all_active(self, *, offset: int, limit: int) -> list[User]: ...
    async def count_active(self) -> int: ...
    async def create(self, user: User) -> User: ...
    async def update(self, user: User) -> User: ...
    async def delete(self, user_id: int) -> None: ...
```

#### Repository Implementation

```python
# src/repositories/user_repository.py
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.user import User

class UserRepository:
    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def find_by_id(self, user_id: int) -> User | None:
        result = await self._db.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()

    async def find_all_active(self, *, offset: int, limit: int) -> list[User]:
        result = await self._db.execute(
            select(User)
            .where(User.is_active == True)
            .order_by(User.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def count_active(self) -> int:
        result = await self._db.execute(
            select(func.count()).where(User.is_active == True)
        )
        return result.scalar_one()

    async def create(self, user: User) -> User:
        self._db.add(user)
        await self._db.flush()     # Get ID (commit handled by get_async_db)
        await self._db.refresh(user)
        return user
```

**Rules**:
- **NEVER** call `self._db.commit()` — commit is handled by `get_async_db()`
- `flush()` is allowed when ID is needed before commit
- Use `selectinload`/`joinedload` for N+1 prevention

### 2.5. Multi-Repository Transactions (Unit of Work)

**When using multiple Repositories in one business logic, they MUST share the same `AsyncSession`.**
The DI factory injects the same `db` instance to each Repository.

```python
# dependencies/order.py — Same session to both Repositories
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import get_async_db
from src.repositories.order_repository import OrderRepository
from src.repositories.inventory_repository import InventoryRepository
from src.services.order_service import OrderService

def get_order_service(
    db: AsyncSession = Depends(get_async_db),
) -> OrderService:
    # Same db session → Wrapped in one transaction
    return OrderService(
        order_repo=OrderRepository(db),
        inventory_repo=InventoryRepository(db),
    )
```

```python
# src/services/order_service.py — Transaction atomicity guaranteed
class OrderService:
    def __init__(
        self,
        order_repo: OrderRepositoryProtocol,
        inventory_repo: InventoryRepositoryProtocol,
    ) -> None:
        self._order_repo = order_repo
        self._inventory_repo = inventory_repo

    async def place_order(self, user_id: int, item_id: int, quantity: int) -> Order:
        # Both queries in same session → If one fails, get_async_db() rolls back all
        await self._inventory_repo.decrease(item_id, quantity)
        return await self._order_repo.create(user_id, item_id, quantity)
```

**Rules**:
- Service constructor parameters are Protocol types (NO direct references to concrete classes)
- Transaction boundaries are ALWAYS managed by `get_async_db()` — Services must NOT commit/rollback

### 2.6. FastAPI Writing Rules

#### Router

```python
# ✅ Use APIRouter with prefix and tags
router = APIRouter(prefix="/users", tags=["users"])

@router.get(
    "/{user_id}",
    response_model=BaseResponse[UserResponse],
    status_code=200,
    responses=GET_USER_RESPONSES,   # From swaggers/
)
async def get_user(
    user_id: int,
    service: UserService = Depends(get_user_service),
) -> BaseResponse[UserResponse]:
    return await service.get_user(user_id)
```

#### Dependency Injection Rules

- Services MUST be injected via `Depends(get_{domain}_service)`
- DB session (`get_async_db`) is defined in `core/database.py`, imported in `dependencies/`
- **NEVER** inject `AsyncSession` directly in endpoints
- **NEVER** inject Repository directly in endpoints

```
Endpoint → get_{domain}_service → get_{domain}_repository → get_async_db
(Endpoint only knows Service, DI chain handles the rest)
```

#### Response Format Standardization

All API responses use `BaseResponse[T]`:

```python
# Success
{"success": true, "data": {...}, "error": null}

# Failure
{"success": false, "data": null, "error": {"code": "USER_NOT_FOUND", "message": "..."}}
```

#### Exception Structure

**`core/exceptions.py`**: Base class and handler ONLY.
**`services/exceptions/`**: Domain-specific exception files.

```python
# src/core/exceptions.py — Base class + handler only
from fastapi import Request
from fastapi.responses import JSONResponse

class BaseCustomException(Exception):
    status_code: int = 500
    code: str = "INTERNAL_SERVER_ERROR"
    message: str = "Server error occurred"

    def __init__(self, message: str | None = None) -> None:
        self.message = message or self.__class__.message

async def custom_exception_handler(
    request: Request, exc: BaseCustomException
) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "data": None,
            "error": {"code": exc.code, "message": exc.message},
        },
    )
```

```python
# src/services/exceptions/user_exceptions.py — Domain exceptions in domain files
from src.core.exceptions import BaseCustomException

class UserNotFoundException(BaseCustomException):
    status_code = 404
    code = "USER_NOT_FOUND"
    message = "User not found"

class UserAlreadyExistsException(BaseCustomException):
    status_code = 409
    code = "USER_ALREADY_EXISTS"
    message = "User already exists"
```

```python
# src/main.py — Handler registration REQUIRED
from src.core.exceptions import BaseCustomException, custom_exception_handler

app = FastAPI()
app.add_exception_handler(BaseCustomException, custom_exception_handler)
```

**Rules**:
- **NEVER** use `HTTPException` directly
- New domains create `services/exceptions/{domain}_exceptions.py`

### 2.7. Pydantic Schema Rules

#### BaseResponse (Required for all responses)

```python
# src/schemas/base.py
from typing import Generic, TypeVar
from pydantic import BaseModel

T = TypeVar("T")

class ErrorDetail(BaseModel):
    code: str
    message: str

class BaseResponse(BaseModel, Generic[T]):
    success: bool
    data: T | None = None
    error: ErrorDetail | None = None

    @classmethod
    def ok(cls, data: T) -> "BaseResponse[T]":
        return cls(success=True, data=data, error=None)

    @classmethod
    def fail(cls, code: str, message: str) -> "BaseResponse[None]":
        return cls(success=False, data=None, error=ErrorDetail(code=code, message=message))
```

#### Domain Schema Pattern

```python
# src/schemas/user.py — Base → Create/Update → Response pattern
from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr

class UserBase(BaseModel):
    email: EmailStr
    name: str

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):           # All fields Optional
    name: str | None = None

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
```

**Rules**:
- **NEVER** use `orm_mode` → Use `ConfigDict(from_attributes=True)` (Pydantic v2)
- NEVER expose sensitive info (password) in Response schemas
- All Update schema fields are `Optional`

### 2.8. Environment Variables (direnv + pydantic-settings)

#### How It Works

direnv reads `.envrc` and loads variables into **shell environment (`os.environ`)**.
pydantic-settings reads from `os.environ` automatically when instantiated,
so **NO `env_file` configuration needed**.

Why NOT to use `env_file=".env"`:
- `.envrc` uses `export KEY="value"` format, `.env` uses `KEY=value` format — format conflict
- `.env` may overwrite variables already set by direnv → priority confusion
- Maintaining two files increases maintenance burden

```
Priority (High → Low)
1. os.environ   ← direnv loads .envrc here  ✅ Use this only
2. env_file     ← .env file direct parsing   ❌ DO NOT USE
3. field default
```

#### config.py

```python
# src/core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # DB
    DATABASE_URL: str                 # postgresql+asyncpg://user:pass@host:5432/dbname
    DATABASE_POOL_SIZE: int = 10
    DATABASE_MAX_OVERFLOW: int = 20

    # App
    SECRET_KEY: str
    DEBUG: bool = False
    ALLOWED_ORIGINS: list[str] = []

    model_config = SettingsConfigDict(
        # env_file NOT set — reads from os.environ populated by direnv
        case_sensitive=True,
    )

settings = Settings()
```

#### .envrc.example

```bash
# .envrc.example — Keys only, no values. Only commit this file
# Usage: cp .envrc.example .envrc → Fill values → direnv allow

export DATABASE_URL="postgresql+asyncpg://user:password@localhost:5432/dbname"
export DATABASE_POOL_SIZE="10"
export DATABASE_MAX_OVERFLOW="20"
export SECRET_KEY=""
export DEBUG="false"
export ALLOWED_ORIGINS=""
```

**Rules**:
- NEVER hardcode secrets/URLs
- `.envrc` in `.gitignore`, only `.envrc.example` committed
- NEVER create `.env` file or use `env_file` setting (DO NOT mix with direnv)
- When adding new env vars, update both `Settings` class and `.envrc.example`

### 2.9. Declarative Coding First

Use declarative style for SQLAlchemy queries, list processing.
If declarative code exceeds 50 lines, extract parts into separate functions.

```python
# ❌ Imperative
async def get_recent_active_emails(db: AsyncSession) -> list[str]:
    emails = []
    rows = await db.execute(select(User))
    for user in rows.scalars():
        if user.is_active and user.created_at > cutoff:
            emails.append(user.email)
    return emails

# ✅ Declarative
async def get_recent_active_emails(db: AsyncSession) -> list[str]:
    result = await db.execute(
        select(User.email)
        .where(User.is_active == True, User.created_at > cutoff)
        .order_by(User.created_at.desc())
    )
    return list(result.scalars().all())
```

### 2.10. Readability

Combine modularity and explicit coding so endpoint code "reads like English".
Reveal intent through variable names.

```python
# ❌
if user and user.is_active and not user.is_deleted and user.role in ("admin", "member"):
    ...

# ✅
is_valid_user = user and user.is_active and not user.is_deleted
has_required_role = user.role in (UserRole.ADMIN, UserRole.MEMBER)
if is_valid_user and has_required_role:
    ...
```

### 2.11. Utilities (`utils/`)

#### logger

```python
# src/utils/logger.py
import logging
import sys

def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(
            logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
        )
        logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    return logger

# Usage
logger = get_logger(__name__)
logger.info("User created: user_id=%s", user.id)
```

**Rules**:
- **NEVER** use `print()`, always use `logger`
- NEVER log sensitive info (passwords, tokens)

### 2.12. Linter Configuration (`ruff.toml`)

```toml
[tool.ruff]
target-version = "py312"
line-length = 100

[tool.ruff.lint]
select = [
    "E",    # pycodestyle errors
    "W",    # pycodestyle warnings
    "F",    # pyflakes
    "I",    # isort
    "B",    # flake8-bugbear
    "C4",   # flake8-comprehensions
    "UP",   # pyupgrade
    "N",    # pep8-naming
    "ASYNC",# flake8-async (detects blocking calls in async functions)
]
ignore = ["E501"]   # line-length delegated to formatter

[tool.ruff.lint.isort]
known-first-party = ["src"]
```

### 2.13. Testing DI Override Pattern

QA-BE Agent overrides DB session with this pattern.

```python
# tests/conftest.py
import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from src.main import app
from src.core.database import get_async_db
from src.models.base import Base

TEST_DATABASE_URL = "postgresql+asyncpg://postgres:password@localhost:5432/test_db"

@pytest.fixture(scope="session")
async def engine():
    _engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    async with _engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield _engine
    async with _engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await _engine.dispose()

@pytest.fixture
async def db_session(engine):
    SessionFactory = async_sessionmaker(bind=engine, expire_on_commit=False)
    async with SessionFactory() as session:
        yield session
        await session.rollback()   # Test isolation: rollback after each test

@pytest.fixture
async def client(db_session: AsyncSession):
    async def override_get_async_db():
        yield db_session

    app.dependency_overrides[get_async_db] = override_get_async_db
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()
```

**Service Unit Tests** — Replace Repository with `AsyncMock`:

```python
# tests/services/test_user_service.py
from unittest.mock import AsyncMock
from src.services.user_service import UserService
from src.services.exceptions.user_exceptions import UserNotFoundException

async def test_get_user_raises_when_not_found():
    # Given
    mock_repo = AsyncMock()
    mock_repo.find_by_id.return_value = None
    service = UserService(mock_repo)

    # When / Then
    with pytest.raises(UserNotFoundException):
        await service.get_user(user_id=999)
```

**Rules**:
- `app.dependency_overrides[get_async_db]` replaces real session with test session
- Each test is isolated via transaction rollback (`scope="function"`)
- Service unit tests must be executable with `AsyncMock` only, no real DB

### 2.14. Backend Naming Conventions

| Target | Convention | Example |
|--------|-----------|---------|
| File names | snake_case | `user_service.py` |
| Class names | PascalCase | `UserService` |
| Functions/variables | snake_case | `get_user_by_id` |
| Constants | UPPER_SNAKE_CASE | `MAX_RETRY_COUNT` |
| API routes | kebab-case | `/api/v1/user-profiles` |
| DB table names | snake_case plural | `users`, `user_profiles` |
| DB column names | snake_case | `created_at`, `is_active` |
| Protocol files | `{domain}_repository.py` | `user_repository.py` |
| Exception files | `{domain}_exceptions.py` | `user_exceptions.py` |

### 2.15. Backend Forbidden Actions

| Forbidden | Alternative |
|-----------|------------|
| `print()` | `logger.info()` |
| `from module import *` | Explicit imports |
| Directly raise `HTTPException` | Inherit from `BaseCustomException` |
| `requests` library | `httpx.AsyncClient` |
| Sync `Session` | `AsyncSession` |
| `Column()` syntax (SQLAlchemy legacy) | `Mapped[T]` + `mapped_column()` |
| `commit()` in Repository | Handled by `get_async_db()` |
| Inject `AsyncSession` directly in endpoints | Inject via `get_{domain}_service` |
| Define domain exceptions in `core/exceptions.py` | `services/exceptions/{domain}_exceptions.py` |
| Define `get_async_db` in `dependencies/` | Define in `core/database.py`, import in `dependencies/` |
| Service directly references Repository concrete type | Declare as Protocol type |
| Abuse of `any` type | Explicit types + comment explaining reason if necessary |
| Single function > 50 lines | Split with meaningful names |
| Hardcoded secrets/URLs | Reference `settings` object |
| `.env` file + `env_file` setting | Unify with direnv + `.envrc` |

---

## 3. Frontend (Next.js / React / TypeScript)

### 3.1. Project Structure

```
fe-project/
├── src/
│   ├── app/                        # Next.js App Router
│   │   ├── layout.tsx              # Root layout (fonts, global providers)
│   │   ├── page.tsx
│   │   ├── loading.tsx             # Root Suspense fallback
│   │   ├── not-found.tsx           # 404 page
│   │   ├── error.tsx               # Root error boundary (Client Component)
│   │   ├── global-error.tsx        # Crash-level error boundary
│   │   ├── providers.tsx           # Global Client Providers ('use client')
│   │   └── (routes)/               # Route groups — domain folders
│   │       └── {domain}/
│   │           ├── page.tsx
│   │           ├── loading.tsx
│   │           ├── error.tsx
│   │           └── _components/    # Route-local components (not shareable)
│   ├── components/
│   │   ├── ui/                     # Reusable atomic components (Button, Input)
│   │   └── features/               # Domain composite components
│   ├── hooks/                      # Custom hooks
│   ├── lib/
│   │   ├── api/
│   │   │   ├── client.ts           # Base fetch wrapper
│   │   │   └── {domain}.ts         # Domain API functions
│   │   └── utils/                  # Pure utility functions
│   ├── stores/                     # Zustand stores (client global state only)
│   ├── types/
│   │   └── api/                    # API response types (mirroring BE schemas)
│   ├── constants/                  # App-wide constants and Enums
│   ├── styles/                     # Global styles
│   └── middleware.ts               # Edge middleware (auth, redirect)
├── public/
├── tests/
│   ├── components/
│   └── hooks/
├── next.config.ts
├── tsconfig.json
└── .env.example                    # Required env var keys only (no values)
```

### 3.2. TanStack Query Setup

#### QueryClient Provider (Required Initial Setup)

`layout.tsx` is a Server Component, so `QueryClientProvider` cannot be placed directly.
MUST create separate `providers.tsx`.

```tsx
// src/app/providers.tsx
'use client';

import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';
import { useState } from 'react';

export function AppProviders({ children }: { children: React.ReactNode }) {
  // Wrap with useState to create instance only once per component
  // Direct `new QueryClient()` creates new instance every render
  const [queryClient] = useState(
    () =>
      new QueryClient({
        defaultOptions: {
          queries: {
            staleTime: 1000 * 60,       // Global default staleTime: 1 minute
            retry: 1,
            refetchOnWindowFocus: false,
          },
        },
      }),
  );

  return (
    <QueryClientProvider client={queryClient}>
      {children}
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  );
}
```

```tsx
// src/app/layout.tsx — Keep as Server Component
import { AppProviders } from './providers';

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <AppProviders>{children}</AppProviders>
      </body>
    </html>
  );
}
```

#### Data Fetching Strategy Selection Criteria

Performance and accuracy depend on this decision. Choose pattern based on data characteristics.

| Data Type | Pattern | Location |
|-----------|---------|----------|
| Rarely changes, SEO important | `fetch` + `cache: 'force-cache'` (SSG) | Server Component |
| Changes periodically (minutes~hours) | `fetch` + `next: { revalidate: N }` (ISR) | Server Component |
| Changes every request, auth-dependent | `fetch` + `cache: 'no-store'` (SSR) | Server Component |
| Real-time, user-triggered, post-navigation refresh | TanStack Query | Client Component |

#### Server Component Data Fetching

```typescript
// app/(routes)/products/page.tsx
// ✅ Fetch directly at component level — no prop drilling
export default async function ProductsPage() {
  const products = await getProducts();
  return <ProductList products={products} />;
}

// src/lib/api/products.ts
export async function getProducts(): Promise<Product[]> {
  const res = await fetch(`${process.env.API_URL}/products`, {
    next: { revalidate: 60 },           // ISR: revalidate every 60 seconds
    headers: { 'Content-Type': 'application/json' },
  });

  if (!res.ok) throw new Error('Failed to fetch products');
  const data: ApiResponse<Product[]> = await res.json();
  return data.data ?? [];
}
```

#### Prefetch + HydrationBoundary (SSR + Client Cache Connection)

Prefetch data in Server Component and hydrate to Client Component.
Without this pattern, Client Component starts fetch from scratch after mount, causing loading flicker.

```tsx
// app/(routes)/users/page.tsx — Server Component
import { dehydrate, HydrationBoundary, QueryClient } from '@tanstack/react-query';
import { UserList } from './_components/UserList';

export default async function UsersPage() {
  const queryClient = new QueryClient();

  // Prefetch on server — queryKey MUST be identical to Client
  await queryClient.prefetchQuery({
    queryKey: ['users'],
    queryFn: getUsers,
  });

  return (
    // Pass dehydrated cache to client
    <HydrationBoundary state={dehydrate(queryClient)}>
      <UserList />   {/* Renders immediately with cache, no loading */}
    </HydrationBoundary>
  );
}
```

```tsx
// app/(routes)/users/_components/UserList.tsx — Client Component
'use client';

export function UserList() {
  // Prefetched data in cache, so isLoading starts as false
  const { data: users } = useQuery({
    queryKey: ['users'],              // MUST match prefetchQuery key
    queryFn: getUsers,
  });

  return (
    <ul>
      {users?.map((user) => <UserCard key={user.id} user={user} />)}
    </ul>
  );
}
```

> ⚠️ If `prefetchQuery` `queryKey` differs from Client `useQuery` `queryKey`, hydration won't connect and server fetch result is discarded.

#### useQuery — Client Component Data Fetching

```typescript
// src/hooks/useUser.ts
import { useQuery } from '@tanstack/react-query';
import { getUser } from '@/lib/api/users';

export function useUser(userId: number) {
  return useQuery({
    queryKey: ['users', userId],
    queryFn: () => getUser(userId),   // src/lib/api/users.ts function
    staleTime: 1000 * 60 * 5,        // 5 minutes (overrides global default)
  });
}
```

**Rules**:
- **NEVER** `fetch()` or direct `apiClient` call inside `useEffect` — MUST use TanStack Query
- NEVER store server state (API responses) in Zustand

#### useMutation — Server Data Modification

All operations creating/updating/deleting data use `useMutation`.
**FORBIDDEN** to manage `isPending`, `onSuccess`, `onError` manually with `useState`.

```typescript
// src/hooks/useCreateUser.ts
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { userApi } from '@/lib/api/users';

export function useCreateUser() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: CreateUserRequest) => userApi.create(data),
    onSuccess: () => {
      // Invalidate related cache on success — list auto-refreshes
      queryClient.invalidateQueries({ queryKey: ['users'] });
      toast.success('User created');
    },
    onError: (error: ApiError) => {
      toast.error(error.message);
    },
  });
}
```

```tsx
// React Hook Form + useMutation integration pattern
'use client';

export function CreateUserForm() {
  const { register, handleSubmit, formState: { errors } } = useForm<CreateUserRequest>({
    resolver: zodResolver(createUserSchema),
  });

  const { mutate: createUser, isPending } = useCreateUser();

  return (
    // handleSubmit validates then calls mutate
    <form onSubmit={handleSubmit((values) => createUser(values))}>
      <input {...register('email')} />
      {errors.email && <p role="alert">{errors.email.message}</p>}
      <button type="submit" disabled={isPending}>
        {isPending ? 'Creating...' : 'Create User'}
      </button>
    </form>
  );
}
```

**Rules**:
- `mutationFn` MUST use functions from `src/lib/api/{domain}.ts`
- `onSuccess` MUST invalidate related cache with `invalidateQueries`
- **NEVER** manage `isPending` state with separate `useState` — Use `useMutation`'s `isPending`

### 3.3. Component Writing Rules

#### Basic Format

```tsx
// ✅ named export + Props interface separation
// Uses Client Hook (useUser) so MUST declare 'use client'
'use client';

interface UserCardProps {
  userId: number;
  variant?: 'compact' | 'full';
}

export function UserCard({ userId, variant = 'full' }: UserCardProps) {
  const { data: user, isLoading } = useUser(userId);

  if (isLoading) return <UserCardSkeleton />;
  if (!user) return null;

  return <div className={cn(userCardVariants({ variant }))}>{user.name}</div>;
}
```

#### Server Component vs Client Component

- Default is **Server Component** — only use `'use client'` when necessary
- `'use client'` needed for: event handlers, `useState`, `useEffect`, browser APIs, TanStack Query hooks
- Push `'use client'` to tree's lowest level — keep parents as Server Components

```
✅ Correct structure:              ❌ Wrong structure:
ServerPage                        'use client' Page
  └─ ServerSection                  └─ ServerSection
       └─ 'use client' Button            └─ 'use client' Button
                                              (whole page loses RSC benefits)
```

#### Streaming with Suspense

Async Server Components MUST be wrapped in `<Suspense>` to enable streaming.
DO NOT await all fetches at top level — this blocks entire initial render.

```tsx
// ✅ Each section streams independently — sent as ready
export default function DashboardPage() {
  return (
    <div>
      <h1>Dashboard</h1>
      <Suspense fallback={<StatsSkeleton />}>
        <StatsSection />          {/* Async Server Component */}
      </Suspense>
      <Suspense fallback={<FeedSkeleton />}>
        <ActivityFeed />          {/* Async Server Component */}
      </Suspense>
    </div>
  );
}
```

#### Memoization Criteria

DO NOT memoize by default — only use when performance issues are measured.

| API | When to Use |
|-----|------------|
| `React.memo` | Frequently re-renders with same props AND render cost is high |
| `useMemo` | Truly expensive computation (e.g., large list sort/filter) |
| `useCallback` | Passing function as prop to memoized child component |

#### Component Size

- If > 100 lines, split into sub-components
- One component, one responsibility

### 3.4. API Integration Rules

#### API Client (Client-side)

```typescript
// src/lib/api/client.ts
export class ApiError extends Error {
  constructor(
    public readonly code: string,
    message: string,
    public readonly status: number,
  ) {
    super(message);
    this.name = 'ApiError';
  }
}

export async function apiClient<T>(
  endpoint: string,
  options?: RequestInit,
): Promise<ApiResponse<T>> {
  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}${endpoint}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  });

  if (!res.ok) {
    const error = await res.json();
    throw new ApiError(error.error.code, error.error.message, res.status);
  }

  return res.json();
}
```

#### API Function Location

- Client-side functions: `src/lib/api/{domain}.ts`
- **NEVER** call `fetch()` directly inside components or hooks

#### Response Type Definition

Mirror BE schemas in `src/types/api/{domain}.ts`.

```typescript
// src/types/api/user.ts
export interface ApiResponse<T> {
  success: boolean;
  data: T | null;
  error: { code: string; message: string } | null;
}

export interface User {
  id: number;
  email: string;
  name: string;
  isActive: boolean;
  createdAt: string;
}
```

### 3.5. Form Handling

All forms use **React Hook Form + Zod + useMutation** combination.
**FORBIDDEN** to manage form state or loading state with `useState`.

```tsx
// src/hooks/useLogin.ts — useMutation MUST be in custom hook
// Hook file doesn't need 'use client' — component using it needs 'use client'
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { useRouter } from 'next/navigation';

export function useLogin() {
  const queryClient = useQueryClient();
  const router = useRouter();

  return useMutation({
    mutationFn: (values: LoginFormValues) => authApi.login(values),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['me'] });
      router.push('/dashboard');
    },
    onError: (error: ApiError) => {
      toast.error(error.message);
    },
  });
}
```

```tsx
// src/components/features/auth/LoginForm.tsx
'use client';

import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

const loginSchema = z.object({
  email: z.string().email('Invalid email format'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
});

type LoginFormValues = z.infer<typeof loginSchema>;

export function LoginForm() {
  const { register, handleSubmit, formState: { errors } } = useForm<LoginFormValues>({
    resolver: zodResolver(loginSchema),
  });

  // useMutation extracted to custom hook — queryClient/router declared inside hook
  const { mutate: login, isPending } = useLogin();

  return (
    <form onSubmit={handleSubmit((values) => login(values))}>
      <input {...register('email')} />
      {errors.email && <p role="alert">{errors.email.message}</p>}
      <input type="password" {...register('password')} />
      {errors.password && <p role="alert">{errors.password.message}</p>}
      <button type="submit" disabled={isPending}>
        {isPending ? 'Logging in...' : 'Login'}
      </button>
    </form>
  );
}
```

### 3.6. State Management Rules

| State Type | Tool | Example |
|-----------|------|---------|
| Server state (API responses) | TanStack Query | User profile, product list |
| Shareable UI state (filters, tabs, pages) | URL state (`useSearchParams` / `nuqs`) | `?page=2&sort=asc` |
| Client global state (auth, theme) | Zustand | Login session |
| Local UI state | `useState` | Modal open/close |

**Rules**:
- NEVER store server state in Zustand — that's TanStack Query's role
- UI state that needs bookmarking/sharing MUST be stored in URL

#### Zustand Store Pattern

```typescript
// src/stores/authStore.ts
import { create } from 'zustand';

interface AuthState {
  user: User | null;
  setUser: (user: User | null) => void;
  clearUser: () => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  setUser: (user) => set({ user }),
  clearUser: () => set({ user: null }),
}));

// ✅ Use selector to prevent unnecessary re-renders
export const useCurrentUser = () => useAuthStore((state) => state.user);
```

### 3.7. Declarative Coding First

Write in declarative (what) style rather than imperative (how) for readability and maintainability.

#### Conditional Rendering

```tsx
// ❌ Imperative — harder to read as conditions grow
function UserStatus({ user }: { user: User }) {
  let badge;
  if (user.role === 'admin') {
    badge = <AdminBadge />;
  } else if (user.isActive) {
    badge = <ActiveBadge />;
  } else {
    badge = <InactiveBadge />;
  }
  return <div>{badge}</div>;
}

// ✅ Declarative — intent clear at a glance
// Map component itself, not JSX instance — safely extensible with props
const statusBadgeMap: Record<string, React.ComponentType> = {
  admin: AdminBadge,
  active: ActiveBadge,
  inactive: InactiveBadge,
};

function UserStatus({ user }: { user: User }) {
  const key = user.role === 'admin' ? 'admin' : user.isActive ? 'active' : 'inactive';
  const Badge = statusBadgeMap[key];
  return <div><Badge /></div>;
}
```

#### List Processing

```tsx
// ❌ Imperative
function ActiveUserList({ users }: { users: User[] }) {
  const result = [];
  for (const user of users) {
    if (user.isActive) {
      result.push(<UserCard key={user.id} user={user} />);
    }
  }
  return <ul>{result}</ul>;
}

// ✅ Declarative
function ActiveUserList({ users }: { users: User[] }) {
  const activeUsers = users.filter((user) => user.isActive);

  return (
    <ul>
      {activeUsers.map((user) => (
        <UserCard key={user.id} user={user} />
      ))}
    </ul>
  );
}
```

#### Loading/Error/Empty State Branching

```tsx
// ❌ Inline branching — JSX gets complex
function UserProfile({ userId }: { userId: number }) {
  const { data, isLoading, isError } = useUser(userId);
  return (
    <div>
      {isLoading ? <Spinner /> : isError ? <ErrorMessage /> : !data ? <EmptyState /> : <ProfileCard user={data} />}
    </div>
  );
}
```

```tsx
// ✅ Declarative early return — each state clearly separated
// 'use client' MUST be at file top
'use client';

function UserProfile({ userId }: { userId: number }) {
  const { data: user, isLoading, isError } = useUser(userId);

  if (isLoading) return <Spinner />;
  if (isError) return <ErrorMessage />;
  if (!user) return <EmptyState />;

  return <ProfileCard user={user} />;
}
```

### 3.8. TypeScript Rules

- `tsconfig.json` MUST have `strict: true`
- **NEVER** use `any` type (if unavoidable: `// eslint-disable-next-line @typescript-eslint/no-explicit-any` + reason comment)
- **NEVER** use `// @ts-ignore` — `// @ts-expect-error` + reason comment allowed
- `interface` vs `type` usage:
  - Object shape → `interface`
  - Union / Intersection / Primitive alias / Function signature → `type`
- All component Props MUST have explicit types
- Form and API validation types use Zod schema as single source of truth

```typescript
// ✅ Derive TypeScript type from Zod schema — NO duplicate definitions
const userSchema = z.object({ id: z.number(), name: z.string() });
type User = z.infer<typeof userSchema>;
```

### 3.9. Performance

#### Images

MUST use `next/image`. Regular `<img>` tag **FORBIDDEN**.

```tsx
import Image from 'next/image';

// ✅ Fixed size image
<Image src="/hero.png" alt="Hero image" width={1200} height={600} priority />

// ✅ Unknown size — use fill mode
<div className="relative h-64 w-full">
  <Image src={user.avatar} alt={user.name} fill className="object-cover" />
</div>
```

**Rules**:
- Add `priority` to above-the-fold images (LCP element)
- Always provide meaningful `alt` text

#### Fonts

MUST use `next/font`. Loading fonts via `<link>` or `@import` **FORBIDDEN**.

```typescript
// src/app/layout.tsx — Final version with AppProviders and fonts
import { Inter } from 'next/font/google';
import { AppProviders } from './providers';

const inter = Inter({
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-inter',
});

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    // MUST apply inter.variable for font to be used
    <html lang="en" className={inter.variable}>
      <body>
        <AppProviders>{children}</AppProviders>
      </body>
    </html>
  );
}
```

### 3.10. SEO and Metadata

All pages MUST export metadata. DO NOT leave `<title>` or OG tags empty.

```typescript
// Static metadata
export const metadata: Metadata = {
  title: 'Page Title',
  description: 'Page description',
  openGraph: { title: 'Page Title', description: 'Page description' },
};

// Dynamic metadata
export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const product = await getProduct(params.id);
  return {
    title: product.name,
    openGraph: { images: [product.imageUrl] },
  };
}
```

### 3.11. Environment Variables

| Prefix | Accessible Where | Usage |
|--------|----------------|-------|
| `NEXT_PUBLIC_` | Browser + Server | Public API URL, feature flags |
| (no prefix) | Server only | Secret keys, internal API URLs |

```bash
# .env.example — Keys only, no values. Only commit this file
NEXT_PUBLIC_API_URL=
NEXT_PUBLIC_GA_ID=
API_SECRET_KEY=
```

**Rules**:
- **NEVER** use `NEXT_PUBLIC_` prefix for secrets
- `.env*.local` in `.gitignore`, only `.env.example` committed
- Access env vars through type constant file — detect missing vars at startup

```typescript
// src/constants/env.ts
export const env = {
  apiUrl: process.env.NEXT_PUBLIC_API_URL!,
  gaId: process.env.NEXT_PUBLIC_GA_ID,
} as const;
```

### 3.12. Frontend Naming Conventions

| Target | Convention | Example |
|--------|-----------|---------|
| Component files | PascalCase | `UserCard.tsx` |
| Hook files | camelCase, `use` prefix | `useUserProfile.ts` |
| Utility files | camelCase | `formatDate.ts` |
| Store files | camelCase, `Store` suffix | `authStore.ts` |
| Types/Interfaces | PascalCase | `UserProfile` |
| Constants | UPPER_SNAKE_CASE | `MAX_PAGE_SIZE` |
| Route-local components | `_components/` prefix folder | `_components/HeroSection.tsx` |
| Path alias | `@/` maps to `src/` | `import { Button } from '@/components/ui/Button'` |

### 3.13. Styling

- **Tailwind CSS only** — inline `style` attribute **FORBIDDEN** (except dynamic values impossible with Tailwind)
- Conditional classes use `clsx` or `cn()` — string concatenation **FORBIDDEN**
- CSS Modules allowed only for complex animations
- Color hex values hardcoding **FORBIDDEN** — always use Tailwind tokens

```tsx
// ❌
<div style={{ color: '#3b82f6' }} className={'card' + (active ? ' active' : '')} />

// ✅
<div className={cn('rounded-lg bg-white', { 'ring-2 ring-blue-500': active })} />
```

### 3.14. Error Handling

```tsx
// Page level: error.tsx (Next.js App Router)
'use client';
export default function Error({ error, reset }: { error: Error; reset: () => void }) {
  return (
    <div role="alert">
      <p>An error occurred</p>
      <button onClick={reset}>Try again</button>
    </div>
  );
}

// Component level: conditional rendering or ErrorBoundary
// API error: catch ApiError and show toast
try {
  await createUser(data);
} catch (error) {
  if (error instanceof ApiError) toast.error(error.message);
  else throw error;               // MUST re-throw unexpected errors
}
```

### 3.15. Accessibility (a11y)

- All images MUST have `alt` (decorative images: `alt=""`)
- All interactive elements (`button`, `a`) MUST have text content or `aria-label` for accessible label
- DO NOT indicate state with color only — accompany with icon or text
- Form error messages MUST have `role="alert"` for screen reader notification
- Verify keyboard navigation works without mouse — test with Tab key
- Modal open/close MUST manage focus (`focus-trap`, `autoFocus`)
- Minimum touch target size: 44×44px

### 3.16. Frontend Forbidden Actions

| Forbidden | Alternative |
|-----------|------------|
| `console.log()` in committed code | Remove before commit or use logger utility |
| `// @ts-ignore` | `// @ts-expect-error` + reason comment |
| `any` type | Explicit type; if unavoidable `// eslint-disable` + reason |
| `default export` | named export (except Next.js page/layout files) |
| API calls in `useEffect` | TanStack Query (`useQuery` / `useMutation`) |
| Hardcoded API URLs | `env` constants from environment variables |
| `<img>` tag | `next/image` |
| `<link>` / `@import` font loading | `next/font` |
| `style={{ ... }}` | Tailwind classes |
| String class concatenation | `cn()` / `clsx()` |
| Store server state in Zustand | TanStack Query |
| Manage shareable UI state with `useState` | URL state (`useSearchParams` / `nuqs`) |
| Manage form/loading state with `useState` | React Hook Form + Zod + `useMutation` |
| No cache invalidation after mutation success | Call `invalidateQueries` in `onSuccess` |
| `QueryClientProvider` directly in `layout.tsx` | Separate into `providers.tsx` |
| `new QueryClient()` directly at component top | `useState(() => new QueryClient())` pattern |
| `prefetchQuery` and `useQuery` `queryKey` mismatch | MUST use identical keys |
| Inline complex logic in JSX | Extract to meaningful handler/variable names |
| Await all fetches before render | Suspense + streaming |
| Import entire library | named / path import |
| `NEXT_PUBLIC_` prefix for secrets | Server-only env vars without prefix |
| `export *` in barrel files (cross-domain) | Explicit named re-exports |

---

## Summary

This document consolidates:
1. **General Coding Principles** — DRY, KISS, YAGNI, SOLID, error handling, logging, security, testing
2. **Backend Rules** — FastAPI, Python, PostgreSQL, SQLAlchemy, Repository Pattern, DI, Pydantic
3. **Frontend Rules** — Next.js, React, TypeScript, TanStack Query, Server/Client Components, forms

**For project-specific rules, refer to:**
- `team/.rules/general-coding-rules.md`
- `team/.rules/_verified/web-fullstack/backend-fastapi-python.md`
- `team/.rules/_verified/web-fullstack/frontend-nextjs-typescript.md`

**Follow these rules rigorously to maintain code quality, consistency, and system stability.**
