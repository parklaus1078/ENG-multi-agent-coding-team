# Deploy Skill

> **Purpose**: Deployment automation and safety verification
>
> **Type**: Deployment Skill
>
> **Thariq's Lesson**: "Automate deployment with safety checks"

---

## 🎯 Triggers

### Automatic Triggers
- Auto-pipeline: After PR merge (optional)
- GitHub Actions: Push to main branch
- Cron: Scheduled deployment (e.g., every Friday)

### Manual Triggers
```bash
# Deploy to dev environment
bash scripts/run-skill.sh deploy --env dev

# Deploy to staging
bash scripts/run-skill.sh deploy --env staging

# Deploy to production (with safety checks)
bash scripts/run-skill.sh deploy --env production

# Dry-run (preview)
bash scripts/run-skill.sh deploy --env production --dry-run

# Rollback
bash scripts/run-skill.sh deploy --rollback --env production
```

---

## 🔍 Features

### 1. Environment-Specific Deployment Strategy

**Environment Configuration**:
```json
{
  "dev": {
    "auto_deploy": true,
    "tests_required": false,
    "approval_required": false,
    "url": "https://dev.example.com"
  },
  "staging": {
    "auto_deploy": true,
    "tests_required": true,
    "approval_required": false,
    "url": "https://staging.example.com"
  },
  "production": {
    "auto_deploy": false,
    "tests_required": true,
    "approval_required": true,
    "smoke_tests": true,
    "canary": true,
    "rollback_enabled": true,
    "url": "https://example.com"
  }
}
```

### 2. Pre-Deployment Verification

**Checklist**:
```python
def pre_deploy_checks(env):
    checks = []

    # 1. Tests passed
    if env.tests_required:
        test_result = run_tests()
        if not test_result.all_passed:
            return {"status": "blocked", "reason": "Tests failed"}

    # 2. Branch verification
    if env == "production":
        current_branch = get_current_branch()
        if current_branch != "main":
            return {"status": "blocked", "reason": "Only main branch can deploy to production"}

    # 3. Check uncommitted changes
    if has_uncommitted_changes():
        return {"status": "blocked", "reason": "Uncommitted changes detected"}

    # 4. Environment variables verification
    required_vars = get_required_env_vars(env)
    missing_vars = [v for v in required_vars if not os.getenv(v)]
    if missing_vars:
        return {"status": "blocked", "reason": f"Missing environment variables: {missing_vars}"}

    # 5. Dependency verification
    if has_dependency_conflicts():
        return {"status": "warning", "reason": "Potential dependency conflicts"}

    return {"status": "ready"}
```

### 3. Deployment Strategies

#### Blue-Green Deployment
```python
def blue_green_deploy(env):
    # 1. Deploy new version to Green environment
    deploy_to_green(env)

    # 2. Smoke test
    if not run_smoke_tests(green_url):
        rollback_to_blue()
        return {"status": "failed", "reason": "Smoke test failed"}

    # 3. Switch traffic
    switch_traffic_to_green()

    # 4. Keep Blue environment (for rollback)
    keep_blue_for_rollback(hours=24)
```

#### Canary Deployment
```python
def canary_deploy(env):
    # 1. Route only 10% traffic to new version
    deploy_canary(traffic_percent=10)

    # 2. Monitor (10 minutes)
    metrics = monitor_canary(duration_minutes=10)

    # 3. Check error rate
    if metrics.error_rate > 1%:
        rollback_canary()
        return {"status": "failed", "reason": "Error rate exceeded"}

    # 4. Gradually increase (50% → 100%)
    increase_canary_traffic(50)
    monitor_canary(duration_minutes=10)

    increase_canary_traffic(100)
```

#### Rolling Deployment
```python
def rolling_deploy(env):
    instances = get_instances(env)

    for instance in instances:
        # 1. Remove instance from load balancer
        remove_from_load_balancer(instance)

        # 2. Deploy new version
        deploy_to_instance(instance)

        # 3. Health check
        if not health_check(instance):
            rollback_instance(instance)
            return {"status": "failed", "reason": f"{instance} deployment failed"}

        # 4. Add back to load balancer
        add_to_load_balancer(instance)

        # 5. Wait before next instance
        wait(seconds=30)
```

### 4. Smoke Tests

**Automatic Post-Deployment Verification**:
```python
def run_smoke_tests(url):
    tests = [
        # 1. Health check
        {"name": "Health", "endpoint": "/health", "expected": 200},

        # 2. Main API functionality
        {"name": "Login", "endpoint": "/api/login", "method": "POST"},
        {"name": "User Profile", "endpoint": "/api/user/me", "method": "GET"},

        # 3. Database connection
        {"name": "DB Connection", "check": lambda: db.ping()}
    ]

    for test in tests:
        result = run_test(test, url)
        if not result.passed:
            return {"status": "failed", "test": test.name}

    return {"status": "passed"}
```

### 5. Rollback

**Automatic Rollback Conditions**:
```python
def should_auto_rollback(metrics):
    # 1. Error rate > 5%
    if metrics.error_rate > 0.05:
        return True

    # 2. Response time > 2x previous
    if metrics.response_time > previous_metrics.response_time * 2:
        return True

    # 3. 5xx errors > 10 per minute
    if metrics.server_errors_per_min > 10:
        return True

    return False
```

**Rollback Execution**:
```bash
# Immediate rollback to previous version
bash scripts/run-skill.sh deploy --rollback --env production

# Rollback to specific version
bash scripts/run-skill.sh deploy --rollback --version v1.2.3 --env production
```

---

## 📤 Output Format

### Deployment Report

```markdown
# Deployment Report: Production

## Summary
- **Environment**: Production
- **Version**: v1.3.0
- **Strategy**: Canary (10% → 50% → 100%)
- **Status**: ✅ Success
- **Duration**: 15 minutes
- **Deployed At**: 2026-03-19T12:00:00Z

---

## Pre-Deploy Checks

✅ All tests passed (150/150)
✅ Coverage: 85%
✅ Branch: main
✅ No uncommitted changes
✅ Environment variables: OK
✅ Dependencies: OK

---

## Deployment Steps

### 1. Canary Deploy (10%)
- **Started**: 12:00:00
- **Traffic**: 10%
- **Monitoring**: 10 minutes
- **Error Rate**: 0.05% ✅
- **Response Time**: 120ms ✅

### 2. Increase to 50%
- **Started**: 12:10:00
- **Traffic**: 50%
- **Monitoring**: 10 minutes
- **Error Rate**: 0.03% ✅
- **Response Time**: 118ms ✅

### 3. Full Deployment (100%)
- **Started**: 12:20:00
- **Traffic**: 100%
- **Status**: ✅ Complete

---

## Smoke Tests

✅ Health check: /health → 200 OK
✅ Login API: /api/login → 200 OK
✅ User Profile: /api/user/me → 200 OK
✅ Database: Connection OK

---

## Metrics

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| Response Time | 125ms | 118ms | -5.6% ✅ |
| Error Rate | 0.02% | 0.03% | +0.01% ✅ |
| Throughput | 1000 req/s | 1050 req/s | +5% ✅ |
| Memory | 1.2GB | 1.1GB | -8% ✅ |

---

## Rollback Plan

Previous version: v1.2.9
Rollback command:
```bash
bash scripts/run-skill.sh deploy --rollback --version v1.2.9 --env production
```

Rollback available for: 24 hours

---

## Next Steps

1. ✅ Monitor metrics for 24 hours
2. ✅ Keep v1.2.9 for rollback
3. ⬜ Remove old version after 24h
```

---

## 🧠 Memory Utilization

### deploy-history.json

```json
{
  "version": "0.0.1",
  "project": "multi-agent-coding-team",

  "deployments": [
    {
      "version": "v1.3.0",
      "env": "production",
      "timestamp": "2026-03-19T12:00:00Z",
      "strategy": "canary",
      "duration_minutes": 15,
      "status": "success",
      "metrics": {
        "error_rate_before": 0.02,
        "error_rate_after": 0.03,
        "response_time_before": 125,
        "response_time_after": 118
      }
    }
  ],

  "rollbacks": [
    {
      "timestamp": "2026-03-10T14:30:00Z",
      "from_version": "v1.2.5",
      "to_version": "v1.2.4",
      "reason": "Error rate spike: 5%",
      "duration_minutes": 2
    }
  ],

  "success_rate": {
    "dev": 1.0,
    "staging": 0.98,
    "production": 0.95
  },

  "avg_deployment_time": {
    "dev": 5,
    "staging": 8,
    "production": 15
  },

  "common_failures": [
    {
      "reason": "Smoke test failure",
      "frequency": 3,
      "last_occurrence": "2026-03-15T10:00:00Z"
    }
  ]
}
```

---

## ⚠️ Gotchas

### 1. Production Deploys Only from Main Branch

**Verification**:
```python
if env == "production":
    current_branch = get_current_branch()
    if current_branch != "main":
        raise Error(f"Production can only deploy from main branch (current: {current_branch})")
```

### 2. Approval Required for Production

**Workflow**:
```python
if env == "production" and not has_approval():
    print("Deployment approval required:")
    print(f"  Version: {version}")
    print(f"  Changes: {changelog}")

    approval = input("Proceed with deployment? (yes/no): ")
    if approval != "yes":
        return {"status": "cancelled"}
```

### 3. Rollback Plan Required

**Principles**:
- Keep previous version for at least 24 hours
- Include rollback command in report
- Configure automatic rollback conditions

### 4. Environment Variable Verification

**Verification**:
```python
required_env_vars = {
    "production": [
        "DATABASE_URL",
        "API_KEY",
        "SECRET_KEY",
        "REDIS_URL"
    ],
    "staging": [
        "DATABASE_URL",
        "API_KEY"
    ]
}

missing = [v for v in required_env_vars[env] if not os.getenv(v)]
if missing:
    raise Error(f"Missing environment variables: {missing}")
```

---

## 📊 Expected Impact

### Before (Manual Deployment)

```
Code merge → Manual build (10 min)
          → Manual deploy (15 min)
          → Manual verification (10 min)
          → Error discovered (hours later)
          → Manual rollback (20 min)
```

**Problems**:
- ❌ Time-consuming (1+ hour)
- ❌ Manual errors possible
- ❌ Slow rollback
- ❌ Inconsistent process

### After (Automated Deployment)

```
PR merge → deploy skill (automatic)
        → Pre-deploy verification (1 min)
        → Canary deployment (15 min)
        → Smoke tests (1 min)
        → Automatic rollback (on error)
```

**Improvements**:
- ✅ Fast (within 20 min)
- ✅ 100% consistency
- ✅ Automatic rollback (2 min)
- ✅ Safety verification

### Target Metrics

| Item | Target |
|------|--------|
| **Deployment Time** | **-60%** |
| **Deployment Failure Rate** | **-80%** |
| **Rollback Time** | **-90%** (2 min) |
| **Downtime** | **0** (Blue-Green) |

---

## 🔗 Integration

### Auto-pipeline Integration

```python
# auto_pipeline.py

# After PR merge
if pr_merged and env == "staging":
    # Automatic deployment (staging)
    deploy_result = self.run_skill("deploy", {
        "env": "staging",
        "auto_deploy": True
    })

    if deploy_result["status"] == "success":
        print(f"✅ Staging deployment complete: {deploy_result['url']}")
    else:
        print(f"❌ Deployment failed: {deploy_result['reason']}")

# Production requires manual approval
if env == "production":
    print("Production deployment ready")
    print(f"  Command: bash scripts/run-skill.sh deploy --env production")
```

### GitHub Actions Integration

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy-staging:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Deploy to staging
        run: |
          bash scripts/run-skill.sh deploy --env staging

  deploy-production:
    runs-on: ubuntu-latest
    needs: deploy-staging
    if: github.event_name == 'workflow_dispatch'
    steps:
      - uses: actions/checkout@v3

      - name: Deploy to production
        run: |
          bash scripts/run-skill.sh deploy --env production
```

---

**Related Documents**:
- [deploy.py](deploy.py) - Implementation
- [deploy-history.json](../../.memory/deploy-history.json) - Deployment history
- [deploy-config.json](deploy-config.json) - Environment configuration
