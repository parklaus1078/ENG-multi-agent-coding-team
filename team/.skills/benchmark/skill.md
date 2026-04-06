# Benchmark Skill

> **Purpose**: Performance benchmarking and regression detection
>
> **Type**: Performance Skill
>
> **Thariq's Lesson**: "Measure performance to prevent regression"

---

## 🎯 Triggers

### Auto Triggers
- Auto-pipeline: Before deployment (optional)
- Git hook: pre-push (performance-critical projects)
- CI/CD: Performance comparison in PRs
- Cron: Weekly performance reports

### Manual Triggers
```bash
# Full benchmark
bash scripts/run-skill.sh benchmark --all

# Specific module
bash scripts/run-skill.sh benchmark --module auth

# Compare against baseline
bash scripts/run-skill.sh benchmark --compare-to main

# Load testing
bash scripts/run-skill.sh benchmark --load-test --users 1000
```

---

## 🔍 Features

### 1. Performance Metrics Measurement

**Measured Metrics**:
```python
metrics = {
    # Response time
    "response_time": {
        "p50": 120,  # ms
        "p95": 250,
        "p99": 500,
        "max": 1200
    },

    # Throughput
    "throughput": {
        "requests_per_second": 1000,
        "bytes_per_second": 5000000
    },

    # Resource usage
    "resources": {
        "cpu_percent": 45,
        "memory_mb": 512,
        "disk_io_mb": 100
    },

    # Error rate
    "errors": {
        "rate": 0.001,  # 0.1%
        "total": 10,
        "by_type": {
            "timeout": 5,
            "500": 3,
            "connection": 2
        }
    },

    # Concurrency
    "concurrency": {
        "active_connections": 500,
        "max_connections": 1000
    }
}
```

### 2. Benchmark Scenarios

**API Benchmarks**:
```python
scenarios = {
    "user_login": {
        "endpoint": "/api/login",
        "method": "POST",
        "payload": {"email": "test@example.com", "password": "test123"},
        "expected_time_ms": 200,
        "concurrent_users": 100
    },

    "user_profile": {
        "endpoint": "/api/user/me",
        "method": "GET",
        "auth_required": True,
        "expected_time_ms": 100,
        "concurrent_users": 500
    },

    "search": {
        "endpoint": "/api/search",
        "method": "GET",
        "params": {"q": "test"},
        "expected_time_ms": 300,
        "concurrent_users": 200
    }
}
```

**Database Benchmarks**:
```python
db_benchmarks = {
    "simple_query": {
        "query": "SELECT * FROM users WHERE id = ?",
        "expected_time_ms": 5
    },

    "complex_join": {
        "query": """
            SELECT u.*, p.*, o.*
            FROM users u
            JOIN profiles p ON u.id = p.user_id
            JOIN orders o ON u.id = o.user_id
            WHERE u.created_at > ?
        """,
        "expected_time_ms": 50
    },

    "bulk_insert": {
        "operation": "INSERT 1000 rows",
        "expected_time_ms": 500
    }
}
```

### 3. Performance Regression Detection

**Comparison Analysis**:
```python
def detect_regression(current, baseline):
    regressions = []

    # Response time increase > 20%
    if current.p95 > baseline.p95 * 1.2:
        regressions.append({
            "metric": "response_time_p95",
            "current": current.p95,
            "baseline": baseline.p95,
            "change_percent": ((current.p95 / baseline.p95) - 1) * 100,
            "severity": "high"
        })

    # Throughput decrease > 15%
    if current.throughput < baseline.throughput * 0.85:
        regressions.append({
            "metric": "throughput",
            "current": current.throughput,
            "baseline": baseline.throughput,
            "change_percent": ((current.throughput / baseline.throughput) - 1) * 100,
            "severity": "high"
        })

    # Memory increase > 30%
    if current.memory > baseline.memory * 1.3:
        regressions.append({
            "metric": "memory",
            "current": current.memory,
            "baseline": baseline.memory,
            "change_percent": ((current.memory / baseline.memory) - 1) * 100,
            "severity": "medium"
        })

    return regressions
```

### 4. Load Testing

**Ramp-up Load Test**:
```python
def ramp_up_load_test(endpoint, max_users=1000):
    results = []

    # Gradual increase: 10 → 100 → 500 → 1000
    for users in [10, 100, 500, 1000]:
        print(f"Testing with {users} concurrent users...")

        result = run_load_test(
            endpoint=endpoint,
            concurrent_users=users,
            duration_seconds=60
        )

        results.append({
            "users": users,
            "avg_response_time": result.avg_response_time,
            "throughput": result.throughput,
            "error_rate": result.error_rate
        })

        # Stop if error rate > 5%
        if result.error_rate > 0.05:
            print(f"⚠️ Error rate exceeded at {users} users: {result.error_rate}")
            break

    return results
```

**Spike Test**:
```python
def spike_test(endpoint):
    # Normal load
    normal = run_load_test(endpoint, users=100, duration=60)

    # Sudden spike (10x)
    spike = run_load_test(endpoint, users=1000, duration=10)

    # Recovery
    recovery = run_load_test(endpoint, users=100, duration=60)

    return {
        "normal": normal,
        "spike": spike,
        "recovery": recovery,
        "recovery_time": calculate_recovery_time(spike, recovery)
    }
```

### 5. Profiling

**Code Hotspot Detection**:
```python
import cProfile
import pstats

def profile_function(func):
    profiler = cProfile.Profile()
    profiler.enable()

    # Execute function
    result = func()

    profiler.disable()

    # Analyze results
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumulative')

    # Top 10 slowest functions
    hotspots = stats.print_stats(10)

    return {
        "result": result,
        "hotspots": hotspots
    }
```

---

## 📤 Output Format

### Benchmark Report

```markdown
# Benchmark Report

## Summary
- **Date**: 2026-03-19T13:00:00Z
- **Branch**: feature/optimize-auth
- **Comparison**: main branch
- **Status**: ⚠️ Performance Regression Detected

---

## Performance Metrics

### Response Time

| Metric | Current | Baseline | Change |
|--------|---------|----------|--------|
| p50 | 125ms | 120ms | +4.2% 🟡 |
| p95 | 310ms | 250ms | +24% 🔴 |
| p99 | 650ms | 500ms | +30% 🔴 |
| max | 1500ms | 1200ms | +25% 🔴 |

### Throughput

| Metric | Current | Baseline | Change |
|--------|---------|----------|--------|
| Requests/sec | 850 | 1000 | -15% 🔴 |
| Bytes/sec | 4.2MB | 5.0MB | -16% 🔴 |

### Resources

| Metric | Current | Baseline | Change |
|--------|---------|----------|--------|
| CPU | 52% | 45% | +15.6% 🟡 |
| Memory | 680MB | 512MB | +32.8% 🔴 |
| Disk I/O | 95MB | 100MB | -5% ✅ |

---

## Regressions Detected (4)

### 🔴 Critical: Response Time p95 (+24%)
**Impact**: High
**Affected**: /api/login, /api/user/me
**Baseline**: 250ms
**Current**: 310ms

**Root Cause Analysis**:
- Profiling shows new database query in auth middleware
- N+1 query detected

**Recommendation**:
```python
# Before
for user in users:
    user.permissions  # N+1 query

# After
users = User.includes('permissions').all()  # Eager load
```

---

### 🔴 Critical: Memory Usage (+33%)
**Impact**: High
**Baseline**: 512MB
**Current**: 680MB

**Root Cause**:
- Memory leak in session storage
- Cache not being cleared

**Recommendation**:
```python
# Add cache cleanup
def cleanup_old_sessions():
    sessions.delete_where(age > 24_hours)
```

---

### 🔴 High: Throughput (-15%)
**Impact**: High
**Baseline**: 1000 req/s
**Current**: 850 req/s

**Related to**: Response time regression

---

## Load Test Results

### Concurrent Users Test

| Users | Avg Response | Throughput | Error Rate |
|-------|--------------|------------|------------|
| 10 | 95ms | 105 req/s | 0% ✅ |
| 100 | 125ms | 850 req/s | 0.1% ✅ |
| 500 | 310ms | 1200 req/s | 1.2% 🟡 |
| 1000 | 650ms | 1100 req/s | 5.5% 🔴 |

**Max Capacity**: ~500 users (error rate < 2%)

---

## Hotspots (Top 5 Slow Functions)

| Function | Cumulative Time | Calls | Time/Call |
|----------|-----------------|-------|-----------|
| auth.check_permissions | 2.5s | 1000 | 2.5ms |
| db.query_users | 1.8s | 1500 | 1.2ms |
| cache.get | 1.2s | 5000 | 0.24ms |
| json.serialize | 0.9s | 2000 | 0.45ms |
| logging.write | 0.5s | 10000 | 0.05ms |

---

## Recommendations

1. 🔴 **Fix N+1 query** in auth middleware (High priority)
2. 🔴 **Fix memory leak** in session storage (High priority)
3. 🟡 **Optimize cache** strategy (Medium priority)
4. 🟢 **Consider CDN** for static assets (Low priority)

---

## Approval Status

❌ **Performance regression detected - Changes not recommended for merge**

Fix critical issues before merging.
```

---

## 🧠 Memory Utilization

### benchmark-history.json

```json
{
  "version": "0.0.1",
  "project": "multi-agent-coding-team",

  "baseline": {
    "branch": "main",
    "commit": "abc123",
    "timestamp": "2026-03-15T10:00:00Z",
    "metrics": {
      "response_time_p95": 250,
      "throughput": 1000,
      "memory_mb": 512
    }
  },

  "benchmark_runs": [
    {
      "branch": "feature/optimize-auth",
      "commit": "def456",
      "timestamp": "2026-03-19T13:00:00Z",
      "metrics": {
        "response_time_p95": 310,
        "throughput": 850,
        "memory_mb": 680
      },
      "regressions": [
        {
          "metric": "response_time_p95",
          "change_percent": 24,
          "severity": "critical"
        }
      ]
    }
  ],

  "performance_trend": [
    {"date": "2026-03-01", "p95": 280},
    {"date": "2026-03-08", "p95": 265},
    {"date": "2026-03-15", "p95": 250},
    {"date": "2026-03-19", "p95": 310}
  ],

  "known_bottlenecks": [
    {
      "name": "auth.check_permissions",
      "avg_time_ms": 2.5,
      "frequency": "high",
      "optimization_attempted": false
    }
  ]
}
```

---

## ⚠️ Gotchas

### 1. Regression Threshold Configuration

**Principles**:
- Response time: +20% → 🔴 Block
- Throughput: -15% → 🔴 Block
- Memory: +30% → 🟡 Warning
- CPU: +20% → 🟡 Warning

### 2. Simulate Real Environment

**Validation**:
```python
# ❌ Wrong: Test only on local
run_benchmark(env="local")

# ✅ Correct: Similar data to production
run_benchmark(
    env="staging",
    data_volume=production_data_volume,
    concurrent_users=production_avg_users
)
```

### 3. Cache Warmup

**Principle**:
```python
# Warmup cache before benchmarking
def warmup_cache():
    # Pre-execute common queries
    for query in common_queries:
        execute(query)

    # Allow sufficient wait time
    time.sleep(5)

# Measure after warmup
warmup_cache()
run_benchmark()
```

### 4. Control External Dependencies

**Principles**:
- Mock external APIs
- Use dedicated database instance
- Simulate network latency

---

## 📊 Expected Benefits

### Before (Manual Benchmarking)

```
Deploy → Detect slowness in production (hours to days later)
   → Rollback
   → Analyze root cause
   → Fix
```

**Problems**:
- ❌ Late detection (after deployment)
- ❌ User impact
- ❌ Difficult root cause analysis

### After (Automated Benchmarking)

```
Create PR → benchmark skill (automatic)
         → Detect regression (2 minutes)
         → Block PR
         → Fix and retest
```

**Improvements**:
- ✅ Immediate detection (before deployment)
- ✅ No user impact
- ✅ Automatic root cause analysis

### Numeric Goals

| Item | Goal |
|------|------|
| **Performance Regression Detection** | **100%** (before deployment) |
| **User Impact** | **0%** |
| **Analysis Time** | **-80%** (automated) |
| **Production Rollbacks** | **-90%** |

---

## 🔗 Integration

### Auto-pipeline Integration

```python
# auto_pipeline.py

# Benchmark before deployment (optional)
if env == "production":
    print("🔬 Running performance benchmark...")

    benchmark_result = self.run_skill("benchmark", {
        "compare_to": "main"
    })

    if benchmark_result["regressions"]:
        critical = [r for r in benchmark_result["regressions"] if r["severity"] == "critical"]

        if critical:
            print(f"❌ Performance regression detected: {len(critical)} issue(s)")
            print("   Deployment blocked")
            raise Exception("Performance regression - fix required")

        print(f"⚠️  Warning: {len(benchmark_result['regressions'])} regression(s)")
    else:
        print("✅ No performance regressions")
```

### GitHub Actions Integration

```yaml
# .github/workflows/benchmark.yml
name: Performance Benchmark

on: [pull_request]

jobs:
  benchmark:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Checkout base branch
        run: git fetch origin ${{ github.base_ref }}

      - name: Run benchmark
        run: |
          bash scripts/run-skill.sh benchmark --compare-to origin/${{ github.base_ref }}

      - name: Comment PR
        uses: actions/github-script@v6
        with:
          script: |
            const fs = require('fs');
            const report = fs.readFileSync('benchmark-report.md', 'utf8');
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: report
            });
```

---

**Related Documentation**:
- [benchmark.py](benchmark.py) - Implementation
- [benchmark-history.json](../../.memory/benchmark-history.json) - Benchmark history
- [benchmark-config.json](benchmark-config.json) - Benchmark configuration
