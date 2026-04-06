# Library Workflow

> **Project Type**: library (e.g., npm package, Python package, Rust crate)
>
> **Applicable When**: `project_type` in `.project-meta.json` is `"library"`

---

## 📂 Deliverable Structure

```
projects/{current_project}/planning/specs/
├── api/
│   └── PLAN-{number}-{slug}.md          # Public API spec
├── examples/
│   └── PLAN-{number}-{slug}.md          # Usage examples
└── test-cases/
    ├── PLAN-{number}-api.md             # API test cases
    └── PLAN-{number}-examples.md        # Example code validation tests
```

---

## 🔨 Work Process

### Step 1: Ticket Analysis

Extract the following from ticket:
- [ ] Function/Class/Method names
- [ ] Parameters and types
- [ ] Return values
- [ ] Exceptions/Errors
- [ ] Usage scenarios

---

### Step 2: Present Deliverable List

```
Project: {current_project} (library)
Ticket: PLAN-{number}-{slug}

Files to be created:
- specs/api/PLAN-{number}-{slug}.md
- specs/examples/PLAN-{number}-{slug}.md
- specs/test-cases/PLAN-{number}-api.md
- specs/test-cases/PLAN-{number}-examples.md

Main APIs: parse(), validate(), transform()
Examples: Basic usage, Option usage, Error handling

Continue? (yes/no)
```

---

### Step 3-1: Public API Spec

**File**: `specs/api/PLAN-{number}-{slug}.md`

```markdown
# {Function/Class Name} API Spec

## Function Signature

\`\`\`typescript
function parse(input: string, options?: ParseOptions): ParseResult
\`\`\`

## Parameters

| Name | Type | Required | Description | Default |
|------|------|------|------|--------|
| input | string | Y | Input string to parse | - |
| options | ParseOptions | N | Parsing options | {} |
| options.strict | boolean | N | Strict mode | false |
| options.encoding | string | N | Encoding | 'utf-8' |

## Return Value

| Type | Description |
|------|------|
| ParseResult | Parse result object |

**ParseResult Structure**:
\`\`\`typescript
interface ParseResult {
  success: boolean;
  data: any;
  errors: ParseError[];
}
\`\`\`

## Exceptions

| Exception Type | Trigger Condition | Example |
|----------|----------|------|
| ParseError | Invalid input format | `throw new ParseError("Invalid format at line 5")` |
| TypeError | Wrong type passed | `parse(123)` → TypeError |

## Behavior Description

1. Validate input string
2. Merge options (defaults + user-provided)
3. Perform parsing
4. Return result or throw exception

## Performance Characteristics

- **Time Complexity**: O(n), n = input string length
- **Space Complexity**: O(n)
- **Throughput**: ~10MB/s (average)

## Side Effects

- None (pure function)

## Thread Safety

- Safe (does not modify state)
```

---

### Step 3-2: Usage Examples

**File**: `specs/examples/PLAN-{number}-{slug}.md`

```markdown
# {Function Name} Usage Examples

## Basic Usage

\`\`\`typescript
import { parse } from 'my-library';

const input = "name: John\\nage: 30";
const result = parse(input);

console.log(result.data);
// { name: "John", age: 30 }
\`\`\`

## Using Options

### Strict Mode

\`\`\`typescript
const result = parse(input, { strict: true });

// In strict mode, error on undefined fields
\`\`\`

### Custom Encoding

\`\`\`typescript
const result = parse(input, { encoding: 'latin1' });
\`\`\`

## Error Handling

\`\`\`typescript
try {
  const result = parse("invalid input");
  if (!result.success) {
    console.error(result.errors);
  }
} catch (error) {
  if (error instanceof ParseError) {
    console.error('Parse failed:', error.message);
  }
}
\`\`\`

## Advanced Usage

### Pipeline Chaining

\`\`\`typescript
const result = parse(input)
  .transform(data => data.filter(x => x.age > 18))
  .validate(schema);
\`\`\`

### Stream Processing

\`\`\`typescript
const stream = fs.createReadStream('large-file.txt');
const results = await parseStream(stream);
\`\`\`

## Real-World Use Cases

### Parse Config File

\`\`\`typescript
const configFile = fs.readFileSync('config.txt', 'utf-8');
const config = parse(configFile);
app.configure(config.data);
\`\`\`

### Process API Response

\`\`\`typescript
const response = await fetch('/api/data');
const text = await response.text();
const parsed = parse(text);
\`\`\`
```

---

### Step 3-3: Test Cases

#### API Tests

**File**: `specs/test-cases/PLAN-{number}-api.md`

```markdown
# {Function Name} API Test Cases

## Normal Cases

| ID | Scenario | Input | Expected Return |
|----|---------|------|-----------|
| TC-API-001 | Basic usage | `parse("name: John")` | `{ success: true, data: { name: "John" } }` |
| TC-API-002 | Using options | `parse(input, { strict: true })` | Strict mode applied |

## Exception Cases

| ID | Scenario | Input | Expected Exception |
|----|---------|------|----------|
| TC-API-101 | Empty string | `parse("")` | `ParseError: "Empty input"` |
| TC-API-102 | Null input | `parse(null)` | `TypeError` |
| TC-API-103 | Invalid format | `parse("invalid:::")` | `ParseError: "Invalid format"` |

## Edge Cases

| ID | Scenario | Input | Expected Result |
|----|---------|------|----------|
| TC-API-201 | Very long string | 10MB string | Process without performance degradation |
| TC-API-202 | Special characters | `parse("emoji 😀")` | Parse correctly |
| TC-API-203 | Unicode | `parse("한글 테스트")` | Parse correctly |
```

#### Example Validation Tests

**File**: `specs/test-cases/PLAN-{number}-examples.md`

```markdown
# {Function Name} Example Code Validation Tests

## README Example Execution Tests

| ID | Example | Expected Result |
|----|------|----------|
| TC-EX-001 | Basic usage example in README | Executes without error |
| TC-EX-002 | Advanced usage example in README | Matches documented result |

## Documentation Example Validation

| ID | Example Location | Test Method |
|----|----------|----------|
| TC-EX-101 | All code snippets in API docs | Executable via copy-paste |
| TC-EX-102 | Blog post examples | Matches actual behavior |
```

---

## ✅ Completion Checklist

- [ ] Public API spec created (function signature, parameters, return value)
- [ ] Usage examples created (basic, options, error handling, advanced)
- [ ] API test cases (normal, exception, edge)
- [ ] Example validation test cases
- [ ] Performance characteristics documented
- [ ] Exception types clearly defined
- [ ] Log file created

---

## 🔍 Library Special Checks

### API Design Principles
- **Simplicity**: Only required parameters, options are optional
- **Consistency**: Unified naming conventions
- **Predictability**: Intuitive behavior
- **Extensibility**: Extend features via options

### Documentation Requirements
- [ ] Function signature (with types)
- [ ] Parameter description (required/optional, default values)
- [ ] Return value structure
- [ ] Exception list
- [ ] Usage examples (minimum 3)

### Version Compatibility
- Indicate breaking changes
- Mark deprecated APIs
- Migration guide (if needed)

---

**Related Documents**:
- [gotchas.md](../gotchas.md)
- [CLAUDE.md](../CLAUDE.md)
