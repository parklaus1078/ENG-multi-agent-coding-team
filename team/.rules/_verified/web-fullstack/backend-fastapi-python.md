# Backend Coding Rules (FastAPI / Python / PostgreSQL)

> This file contains coding rules that Coding Agent and QA Agent must follow when working on web-fullstack project backends.

---

## 1. Project Structure

```
be-project/
├── src/
│   ├── main.py                   # FastAPI app entrypoint, register routers/middleware/exception handlers
│   ├── core/
│   │   ├── config.py             # pydantic-settings based environment variable loader
│   │   ├── database.py           # Engine, session factory, get_async_db() — infrastructure setup only
│   │   └── exceptions.py         # Define BaseCustomException + custom_exception_handler only
│   ├── api/
│   │   └── v1/
│   │       ├── router.py         # Integrate all routers (include_router)
│   │       ├── swaggers/         # Define Swagger documentation response objects
│   │       │                     # (Composed by referencing Pydantic models from schemas/)
│   │       └── endpoints/        # Files per endpoint (e.g., users.py, items.py)
│   ├── models/                   # SQLAlchemy ORM models (inherit DeclarativeBase)
│   ├── schemas/                  # Pydantic schemas (Request / Response / Base)
│   ├── services/                 # Business logic
│   │   └── exceptions/           # Domain-specific exception classes (e.g., user_exceptions.py)
│   ├── repositories/             # DB query layer (direct AsyncSession usage)
│   │   └── protocols/            # Repository interfaces (Protocol definitions)
│   ├── dependencies/             # DI dependency injection functions (separated by domain)
│   │   └── user.py               # get_user_repository(), get_user_service()
│   ├── constants/                # Domain-specific constants / Enum / environment-specific values
│   ├── middleware/               # Cross-cutting concern middleware (Request ID, logging, etc.)
│   └── utils/                    # Reusable utilities (HTTP client wrapper, logger, etc.)
│       └── logger.py
│
├── tests/
│   ├── conftest.py               # pytest fixtures (TestClient, DB override, etc.)
│   ├── api/v1/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   ├── repositories/
│   └── dependencies/
│
├── alembic/                      # DB migrations
│   └── versions/
├── ruff.toml                     # Linter configuration (see section below)
└── .envrc.example                # direnv-based environment variable example
```

---

## 2. Layer Responsibility Separation (Mandatory)

| Layer | Role | Prohibited Actions |
|-------|------|-------------------|
| `endpoints/` | HTTP request/response handling, routing | No direct business logic |
| `services/` | Business logic | No direct DB queries |
| `repositories/` | DB queries (direct `AsyncSession` usage) | No business logic |
| `schemas/` | Input/output data validation | No direct ORM model exposure |
| `dependencies/` | DI factory functions | No business/query logic |
| `core/` | Infrastructure setup (DB, env vars, base exceptions) | No domain logic |

---

## 3. DB Setup (PostgreSQL + Async SQLAlchemy)

### 3-1. Drivers

| Purpose | Library |
|---------|---------|
| Async driver | `asyncpg` |
| ORM | `sqlalchemy[asyncio]` (`AsyncSession`, `async_sessionmaker`) |
| Migration | `alembic` (runs with sync connection separately) |

### 3-2. Engine and Session Factory (`src/core/database.py`)

DB infrastructure setup must be defined **only in `src/core/database.py`**.
`dependencies/` imports `get_async_db` from this file.

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
    expire_on_commit=False,          # Prevent lazy-load after await
    autoflush=False,
    autocommit=False,
)

async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Provide request-scoped AsyncSession.
    Commit on normal exit, rollback and re-raise on exception.
    Do not import directly — must be injected through dependencies/.
    """
    async with AsyncSessionFactory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
```

### 3-3. ORM Model Base

```python
# src/models/base.py
from datetime import datetime
from sqlalchemy import DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class TimestampMixin:
    """Automatically manage creation/update timestamps. Recommended for all tables."""
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

### 3-4. ORM Model Writing Rules

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

- Must use `Mapped[T]` + `mapped_column()` (SQLAlchemy 2.x style)
- Prohibit `Column()` syntax (legacy)
- Specify `nullable` for all columns
- Add `index=True` to frequently queried fields

### 3-5. Repository Protocol (Interface Definition)

**Define Protocol first** before writing implementation.
Service depends only on Protocol type and never directly references concrete class.
This ensures OCP (closed to implementation changes) and LSP (implementation substitutability) at the type level.

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

### 3-6. Repository Implementation

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
        await self._db.flush()     # Secure ID (commit handled in get_async_db)
        await self._db.refresh(user)
        return user
```

- Prohibit direct `self._db.commit()` calls — commit handled in `get_async_db()`
- Allow `flush()` when needed (e.g., to secure ID)
- Explicitly use `selectinload` / `joinedload` for relationships that may cause N+1 problems

### 3-7. Multi-Repository Transactions (Unit of Work)

**When using multiple Repositories in one business logic, they must share the same `AsyncSession`.**
Handle this by injecting the same `db` instance to each Repository in the DI factory.

```python
# dependencies/order.py — Inject same session to two Repositories
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import get_async_db
from src.repositories.order_repository import OrderRepository
from src.repositories.inventory_repository import InventoryRepository
from src.services.order_service import OrderService

def get_order_service(
    db: AsyncSession = Depends(get_async_db),
) -> OrderService:
    # Same db session → bound in one transaction
    return OrderService(
        order_repo=OrderRepository(db),
        inventory_repo=InventoryRepository(db),
    )
```

```python
# src/services/order_service.py — Transaction atomicity automatically guaranteed
class OrderService:
    def __init__(
        self,
        order_repo: OrderRepositoryProtocol,
        inventory_repo: InventoryRepositoryProtocol,
    ) -> None:
        self._order_repo = order_repo
        self._inventory_repo = inventory_repo

    async def place_order(self, user_id: int, item_id: int, quantity: int) -> Order:
        # Two queries in same session → if either raises exception, get_async_db() rolls back all
        await self._inventory_repo.decrease(item_id, quantity)
        return await self._order_repo.create(user_id, item_id, quantity)
```

- Service constructor declares Protocol types (prohibit direct concrete class references)
- Transaction boundary always managed by `get_async_db()` — prohibit commit/rollback in Service

### 3-8. Alembic Migrations

- Migrations use sync connection (`psycopg2` or `pg8000`) (Alembic requirement)
- Always review generated files after `alembic revision --autogenerate`
- Explicitly use `op.rename_table()` when changing `__tablename__` (otherwise autogenerate incorrectly creates drop/create)

---

## 4. FastAPI Writing Rules

### 4-1. Routers

```python
# ✅ Use APIRouter, specify prefix and tags
router = APIRouter(prefix="/users", tags=["users"])

@router.get(
    "/{user_id}",
    response_model=BaseResponse[UserResponse],
    status_code=200,
    responses=GET_USER_RESPONSES,   # Swagger spec from swaggers/
)
async def get_user(
    user_id: int,
    service: UserService = Depends(get_user_service),
) -> BaseResponse[UserResponse]:
    return await service.get_user(user_id)
```

### 4-2. Dependency Injection Rules

- Services must be injected via `Depends(get_{domain}_service)`
- DB session (`get_async_db`) defined in `core/database.py`, imported and used in `dependencies/`
- Prohibit direct `AsyncSession` injection in endpoints
- Prohibit direct Repository injection in endpoints

```
Endpoint → get_{domain}_service → get_{domain}_repository → get_async_db
(Endpoint only knows service, DI resolves the chain below)
```

### 4-3. Unified Response Format

All API responses use `BaseResponse[T]` (see Section 5):

```python
# Success
{"success": true, "data": {...}, "error": null}

# Failure
{"success": false, "data": null, "error": {"code": "USER_NOT_FOUND", "message": "..."}}
```

### 4-4. Exception Structure

**`core/exceptions.py`**: Base class and handler only.
**`services/exceptions/`**: Separate domain-specific exception files.

```python
# src/core/exceptions.py — Define base class + handler only
from fastapi import Request
from fastapi.responses import JSONResponse

class BaseCustomException(Exception):
    status_code: int = 500
    code: str = "INTERNAL_SERVER_ERROR"
    message: str = "Server error occurred."

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
# src/services/exceptions/user_exceptions.py — Domain exceptions in domain file
from src.core.exceptions import BaseCustomException

class UserNotFoundException(BaseCustomException):
    status_code = 404
    code = "USER_NOT_FOUND"
    message = "User not found."

class UserAlreadyExistsException(BaseCustomException):
    status_code = 409
    code = "USER_ALREADY_EXISTS"
    message = "User already exists."
```

```python
# src/main.py — Handler registration mandatory (otherwise all custom exceptions return 500)
from src.core.exceptions import BaseCustomException, custom_exception_handler

app = FastAPI()
app.add_exception_handler(BaseCustomException, custom_exception_handler)
```

- Prohibit direct `HTTPException` usage
- Create new `services/exceptions/{domain}_exceptions.py` file when adding new domain

### 4-5. Middleware (`middleware/`)

Handle cross-cutting concerns with middleware. Register with `add_middleware()` in `main.py`.

```python
# src/middleware/request_id.py — Assign unique ID to all requests
import uuid
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response
```

```python
# src/middleware/logging.py — Common request/response logging
import time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from src.utils.logger import get_logger

logger = get_logger(__name__)

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start = time.perf_counter()
        response = await call_next(request)
        duration_ms = (time.perf_counter() - start) * 1000
        logger.info(
            "method=%s path=%s status=%s duration=%.1fms request_id=%s",
            request.method,
            request.url.path,
            response.status_code,
            duration_ms,
            getattr(request.state, "request_id", "-"),
        )
        return response
```

```python
# src/main.py
from src.middleware.request_id import RequestIDMiddleware
from src.middleware.logging import LoggingMiddleware

app.add_middleware(RequestIDMiddleware)
app.add_middleware(LoggingMiddleware)
```

### 4-6. `swaggers/` Directory Usage

Define Swagger spec objects passed to endpoint `responses=` parameter, separated by domain.
Maximize reuse of Pydantic models from `schemas/`.

```python
# src/api/v1/swaggers/user.py
from src.schemas.user import UserResponse
from src.schemas.base import BaseResponse

GET_USER_RESPONSES: dict = {
    200: {"model": BaseResponse[UserResponse], "description": "User retrieval success"},
    404: {
        "description": "User not found",
        "content": {
            "application/json": {
                "example": {
                    "success": False,
                    "data": None,
                    "error": {"code": "USER_NOT_FOUND", "message": "User not found."},
                }
            }
        },
    },
}
```

### 4-7. `constants/` Directory Usage

Separate domain-specific constants, Enums, and environment-specific branch values into files.

```python
# src/constants/user.py
from enum import StrEnum

class UserRole(StrEnum):
    ADMIN = "admin"
    MEMBER = "member"
    GUEST = "guest"

MAX_LOGIN_ATTEMPT = 5
DEFAULT_PAGE_SIZE = 20
```

---

## 5. Pydantic Schema Rules

### 5-1. BaseResponse (Mandatory for all responses)

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

### 5-2. Pagination Schema (Common for list APIs)

All list APIs requiring pagination use the schema below.
Default to offset-based pagination; define cursor-based separately if infinite scroll needed.

```python
# src/schemas/pagination.py
from typing import Generic, TypeVar
from pydantic import BaseModel, Field

T = TypeVar("T")

class PaginationQuery(BaseModel):
    """Common pagination query parameters"""
    page: int = Field(default=1, ge=1, description="Page number (starts from 1)")
    size: int = Field(default=20, ge=1, le=100, description="Page size")

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.size

    @property
    def limit(self) -> int:
        return self.size

class PaginatedData(BaseModel, Generic[T]):
    """Common pagination response structure"""
    items: list[T]
    total: int
    page: int
    size: int
    total_pages: int

    @classmethod
    def of(cls, items: list[T], total: int, query: PaginationQuery) -> "PaginatedData[T]":
        return cls(
            items=items,
            total=total,
            page=query.page,
            size=query.size,
            total_pages=-(-total // query.size),  # ceiling division
        )
```

```python
# Endpoint usage example
@router.get("/", response_model=BaseResponse[PaginatedData[UserResponse]])
async def list_users(
    query: Annotated[PaginationQuery, Query()],
    service: UserService = Depends(get_user_service),
) -> BaseResponse[PaginatedData[UserResponse]]:
    result = await service.list_users(query)
    return BaseResponse.ok(result)
```

### 5-3. Domain Schema Pattern

```python
# src/schemas/user.py — Base → Create/Update → Response pattern
from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr

class UserBase(BaseModel):
    email: EmailStr
    name: str

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):           # Update: all fields Optional
    name: str | None = None

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
```

- Prohibit `orm_mode` → Use `ConfigDict(from_attributes=True)` (Pydantic v2)
- Don't expose sensitive info like `password` in Response schemas
- All Update schema fields must be `Optional`

---

## 6. Inversion of Control & Dependency Injection

Define entire DI chain from DB session → Repository → Service in `dependencies/{domain}.py`.

```python
# src/dependencies/user.py
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import get_async_db          # Import from core
from src.repositories.user_repository import UserRepository
from src.repositories.protocols.user_repository import UserRepositoryProtocol
from src.services.user_service import UserService

def get_user_repository(
    db: AsyncSession = Depends(get_async_db),
) -> UserRepositoryProtocol:                        # Return as Protocol type
    return UserRepository(db)

def get_user_service(
    user_repository: UserRepositoryProtocol = Depends(get_user_repository),
) -> UserService:
    return UserService(user_repository)
```

- Always get `get_async_db` from `src/core/database.py`
- Declare return type as Protocol to ensure implementation substitutability at type level
- Service/Repository classes receive dependencies only through constructor parameters (no global state)

---

## 7. Async Processing

- DB I/O: `AsyncSession` + `async/await` mandatory (prohibit sync `Session`)
- External HTTP calls: Use `httpx.AsyncClient` (prohibit `requests`)
- CPU-bound tasks: Use `asyncio.run_in_executor()`
- Prohibit blocking sleep other than `asyncio.sleep()`

---

## 8. Environment Variable Management (direnv + pydantic-settings)

### How It Works

direnv reads `.envrc` and **loads variables into shell environment (`os.environ`)**.
pydantic-settings automatically reads `os.environ` on instance creation,
so **it correctly retrieves all environment variables without `env_file` setting.**

Why you shouldn't use `env_file=".env"` together:
- `.envrc` uses `export KEY="value"` format, `.env` uses `KEY=value` format — format mismatch when mixed
- `.env` may overwrite values direnv already loaded into `os.environ`, causing priority confusion
- Maintaining two files doubles maintenance burden

```
Priority (high → low)
1. os.environ   ← direnv loads .envrc here  ✅ Use only this
2. env_file     ← Direct .env file parsing  ❌ Prohibited
3. field default
```

### config.py

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
        # No env_file — reads values direnv loaded into os.environ
        case_sensitive=True,
    )

settings = Settings()
```

### .envrc.example

```bash
# .envrc.example — List keys only without actual values, commit only this file to git
# Usage: cp .envrc.example .envrc → fill values then direnv allow

export DATABASE_URL="postgresql+asyncpg://user:password@localhost:5432/dbname"
export DATABASE_POOL_SIZE="10"
export DATABASE_MAX_OVERFLOW="20"
export SECRET_KEY=""
export DEBUG="false"
export ALLOWED_ORIGINS=""
```

### Rules

- Absolutely prohibit hardcoded secrets/URLs
- Add `.envrc` to `.gitignore`, commit only `.envrc.example`
- Prohibit creating `.env` file and `env_file` setting (don't mix with direnv)
- When adding new environment variable, update both `Settings` class and `.envrc.example`
- Handle environment-specific branch values by referencing `settings` in `constants/` files

---

## 9. Declarative Coding First

Prefer declarative style in SQLAlchemy queries, list processing, etc.
If declarative code exceeds 50 lines, extract separable parts into separate functions.

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

---

## 10. Readability

Combine modularization and explicit coding so endpoint code "reads like English sentences."
Reveal intent through variable names for complex conditions.

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

---

## 11. Utils (`utils/`)

### logger

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

- Prohibit `print()`, always use `logger`
- Don't log sensitive info (passwords, tokens)

### HTTP Client

```python
# src/utils/http_client.py
import httpx

class AsyncHTTPClient:
    def __init__(self, base_url: str, timeout: float = 10.0) -> None:
        self._client = httpx.AsyncClient(base_url=base_url, timeout=timeout)

    async def get(self, path: str, **kwargs) -> httpx.Response:
        response = await self._client.get(path, **kwargs)
        response.raise_for_status()
        return response

    async def aclose(self) -> None:
        await self._client.aclose()
```

---

## 12. Linter Configuration (`ruff.toml`)

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
    "ASYNC",# flake8-async (detect blocking calls in async functions)
]
ignore = ["E501"]   # Delegate line-length to formatter

[tool.ruff.lint.isort]
known-first-party = ["src"]
```

---

## 13. Test DI Override Pattern

QA-BE Agent overrides DB session with this pattern.

```python
# tests/conftest.py
import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from src.main import app
from src.core.database import get_async_db          # Import from core
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

**Service unit tests** — Replace Repository with `AsyncMock`:

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

- Replace real session with test session via `app.dependency_overrides[get_async_db]`
- Isolate each test with transaction rollback (`scope="function"`)
- Service unit tests should be executable with only `AsyncMock` without real DB

---

## 14. Naming Conventions

| Target | Rule | Example |
|--------|------|---------|
| File names | snake_case | `user_service.py` |
| Class names | PascalCase | `UserService` |
| Functions/variables | snake_case | `get_user_by_id` |
| Constants | UPPER_SNAKE_CASE | `MAX_RETRY_COUNT` |
| API paths | kebab-case | `/api/v1/user-profiles` |
| DB table names | snake_case plural | `users`, `user_profiles` |
| DB column names | snake_case | `created_at`, `is_active` |
| Protocol files | `{domain}_repository.py` | `user_repository.py` |
| Exception files | `{domain}_exceptions.py` | `user_exceptions.py` |

---

## 15. Prohibited Actions (Complete Summary)

| Prohibited Item | Alternative |
|-----------------|-------------|
| `print()` | `logger.info()` |
| `from module import *` | Explicit imports |
| Directly raise `HTTPException` | Inherit from `BaseCustomException` |
| `requests` library | `httpx.AsyncClient` |
| Sync `Session` | `AsyncSession` |
| `Column()` syntax (SQLAlchemy legacy) | `Mapped[T]` + `mapped_column()` |
| `commit()` in Repository | Handled in `get_async_db()` |
| Direct `AsyncSession` injection in endpoints | Inject via `get_{domain}_service` |
| Define domain exceptions in `core/exceptions.py` | `services/exceptions/{domain}_exceptions.py` |
| Define `get_async_db` in `dependencies/` | Define in `core/database.py`, import in `dependencies/` |
| Service directly references Repository implementation type | Declare as Protocol type |
| Abuse of `any` type | Explicit types + comment reason if necessary |
| Single functions over 50 lines | Separate and give meaningful names |
| Hardcoded secrets/URLs | Reference `settings` object |
| `.env` file + `env_file` setting | Unify with direnv + `.envrc` |
