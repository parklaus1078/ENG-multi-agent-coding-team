# General Coding Principles

> Foundational principles applied across all project types

---

## 1. Code Quality Principles

### DRY (Don't Repeat Yourself)
- Extract duplicate code into functions/classes
- Refactor if the same logic repeats 3+ times
- Separate configuration values into constants/environment variables

### KISS (Keep It Simple, Stupid)
- Try simple solutions first
- Avoid unnecessary abstraction
- Use clear variable names (minimize abbreviations)

### YAGNI (You Aren't Gonna Need It)
- Implement only what's currently needed
- Don't write speculative code for the future
- Add features when they become necessary

### SOLID Principles

#### S - Single Responsibility Principle
- Functions/classes should do one thing only
- Should have only one reason to change

#### O - Open/Closed Principle
- Open for extension, closed for modification
- Utilize interfaces/abstract classes

#### L - Liskov Substitution Principle
- Subtypes must be substitutable for their base types

#### I - Interface Segregation Principle
- Don't depend on methods you don't use
- Prefer small, specific interfaces

#### D - Dependency Inversion Principle
- Depend on abstractions, not concretions
- Utilize dependency injection (DI)

---

## 2. Naming Conventions

### General Principles
- **Meaningful names**: `data` ❌ → `userData` ✅
- **Pronounceable names**: `yyyymmdd` ❌ → `currentDate` ✅
- **Searchable names**: `7` ❌ → `MAX_RETRY_COUNT` ✅
- **Remove unnecessary context**: `UserClass` ❌ → `User` ✅

### Language-Specific Conventions

#### Python
- Variables/functions: `snake_case`
- Classes: `PascalCase`
- Constants: `UPPER_SNAKE_CASE`
- Private: `_leading_underscore`

#### JavaScript/TypeScript
- Variables/functions: `camelCase`
- Classes: `PascalCase`
- Constants: `UPPER_SNAKE_CASE`
- Private (TypeScript): `#field` or `private field`

#### Go
- Variables/functions: `camelCase` (exported: `PascalCase`)
- Interfaces: `PascalCase`
- Constants: `PascalCase` or `camelCase`

#### Rust
- Variables/functions: `snake_case`
- Types/traits: `PascalCase`
- Constants: `UPPER_SNAKE_CASE`

#### Java
- Variables/functions: `camelCase`
- Classes: `PascalCase`
- Constants: `UPPER_SNAKE_CASE`
- Packages: `lowercase`

---

## 3. Security Fundamentals

### Input Validation
- **Never trust user input**
- Validate type, length limits, allowed characters
- Prefer whitelist approach (avoid blacklists)

### Secrets Management
- **Never hardcode secrets in code**
  - API keys, passwords, tokens, etc.
- Use environment variables (`.env` file, never commit to Git)
- Provide `.env.example` template
- Production: Use secret management tools (AWS Secrets Manager, HashiCorp Vault, etc.)

### SQL Injection Prevention
- Use ORM or parameterized queries
- Never build SQL with string concatenation

### XSS (Cross-Site Scripting) Prevention
- Escape user input when inserting into HTML
- Utilize framework built-in protections (React's auto-escaping, etc.)

### CSRF (Cross-Site Request Forgery) Prevention
- Use CSRF tokens
- Set SameSite cookie attribute

### Authentication/Authorization
- Passwords: Use strong hashing algorithms (bcrypt, argon2, etc.)
- JWT: Don't include sensitive data, set short expiration times
- Use HTTPS (mandatory in production)

### Error Messages
- Don't expose stack traces in production
- Generic error messages for users
- Log detailed errors only

---

## 4. Error Handling

### General Principles
- **Never ignore errors**
- Handle expected errors explicitly
- Fail fast for unrecoverable errors

### Logging
- Use appropriate log levels:
  - `DEBUG`: Debug information during development
  - `INFO`: General information (request processing, start/stop)
  - `WARNING`: Potential issues
  - `ERROR`: Recoverable errors
  - `CRITICAL`: System-critical errors

- Don't log sensitive information (passwords, tokens, etc.)
- Prefer structured logging (JSON format)

### Language-Specific Patterns

#### Python
```python
# ✅ Good example
try:
    result = risky_operation()
except SpecificError as e:
    logger.error(f"Operation failed: {e}")
    raise
```

#### JavaScript/TypeScript
```typescript
// ✅ Good example
try {
  const result = await riskyOperation();
} catch (error) {
  logger.error('Operation failed', { error });
  throw error;
}
```

#### Go
```go
// ✅ Good example
result, err := riskyOperation()
if err != nil {
    log.Printf("operation failed: %v", err)
    return err
}
```

---

## 5. Testing

### Test Pyramid
1. **Unit Tests (70%)**: Individual functions/methods
2. **Integration Tests (20%)**: Multiple modules working together
3. **E2E Tests (10%)**: Entire system flows

### Test Writing Principles
- **F.I.R.S.T Principles**:
  - **Fast**: Execute quickly
  - **Independent**: Can run independently
  - **Repeatable**: Repeatable results
  - **Self-Validating**: Automatic verification
  - **Timely**: Write in timely manner (with implementation)

### AAA Pattern
```python
def test_user_creation():
    # Arrange (setup)
    user_data = {"email": "test@example.com", "password": "secret"}

    # Act (execute)
    user = create_user(user_data)

    # Assert (verify)
    assert user.email == "test@example.com"
    assert user.id is not None
```

### Coverage Goals
- Unit tests: 80% or higher
- Integration tests: Cover major flows
- E2E tests: Critical user flows

---

## 6. Git Commit Messages

### Conventional Commits

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Type
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code formatting (no functionality change)
- `refactor`: Refactoring
- `test`: Add/modify tests
- `chore`: Build, packages, etc.

### Example
```
feat(auth): implement JWT token-based authentication

- Issue JWT token on login
- Add token verification middleware
- Set expiration time to 1 hour

Closes #123
```

---

## 7. Code Review

### Reviewer Checklist
- [ ] Does code meet requirements?
- [ ] Are tests included?
- [ ] Any security vulnerabilities?
- [ ] Any performance issues?
- [ ] Is naming clear?
- [ ] No unnecessary duplication?
- [ ] Is error handling appropriate?

### Author Checklist
- [ ] Self-review complete
- [ ] Tests pass
- [ ] Linter/formatter run
- [ ] Commit message rules followed
- [ ] Changes documented

---

## 8. Documentation

### Code Comments
- **Explain why (Why)**, express what (What) in code
- Complex algorithms need comments
- Use TODO, FIXME, HACK tags

### README.md Required Sections
1. **Project Description**
2. **Installation**
3. **Usage**
4. **Environment Variable Setup**
5. **Running Tests**
6. **License**

### API Documentation (Backend)
- Use OpenAPI/Swagger auto-generation
- Add descriptions to all endpoints
- Include Request/Response examples

---

## 9. Dependency Management

### Version Pinning
- Production dependencies: Pin exact versions
- Development dependencies: Ranges acceptable

### Security Updates
- Regularly scan dependencies for security issues
- Use automation tools (Dependabot, Snyk, etc.)

### Minimal Dependencies
- Add only necessary libraries
- Prefer small utilities over giant libraries

---

## 10. Performance

### General Principles
- **Measure before optimizing** (no guessing)
- Profile bottlenecks
- Avoid premature optimization

### Database
- Prevent N+1 query problems
- Use appropriate indexes
- Implement pagination (for large datasets)

### Caching
- Cache infrequently changed data
- Set cache expiration strategy
- Follow cache key naming conventions

---

## 11. Prohibited Actions

### Absolutely Forbidden
- ❌ Hardcoded secrets
- ❌ SQL injection-vulnerable queries
- ❌ Direct execution of user input (eval, etc.)
- ❌ Committing `.env` files to Git
- ❌ Debug mode enabled in production
- ❌ Logging sensitive information

### Discouraged
- ⚠️ Excessive global variables
- ⚠️ Deep nesting (3+ levels)
- ⚠️ Long functions (50+ lines)
- ⚠️ Magic numbers (unexplained constants)
- ⚠️ Commented-out code (use Git history)

---

## 12. References

### Books
- Clean Code (Robert C. Martin)
- The Pragmatic Programmer (David Thomas, Andrew Hunt)
- Refactoring (Martin Fowler)

### Web Resources
- OWASP Top 10: https://owasp.org/www-project-top-ten/
- 12 Factor App: https://12factor.net/
- Semantic Versioning: https://semver.org/

---

**Version**: v1.0.0
**Last Updated**: 2026-03-12
