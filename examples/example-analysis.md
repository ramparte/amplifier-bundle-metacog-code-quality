# Example: Code Quality Analysis

This example demonstrates using the code-quality collection to analyze a Python project.

## Scenario

You have a Python project with several quality issues. Let's run a comprehensive analysis.

## Sample Code (with Issues)

**src/database.py:**
```python
import hashlib

# Bad: Hardcoded credentials
DB_PASSWORD = "admin123"
DB_HOST = "localhost"

def get_users(user_id):
    # Bad: SQL injection vulnerability
    query = f"SELECT * FROM users WHERE id = {user_id}"
    # Bad: No parameterized query
    cursor.execute(query)
    return cursor.fetchall()

def process_users():
    # Bad: N+1 query problem
    users = get_all_users()
    for user in users:
        posts = get_posts_for_user(user.id)  # Query in loop
        user.posts = posts
    return users

def hash_password(password):
    # Bad: Weak hashing algorithm
    return hashlib.md5(password.encode()).hexdigest()
```

**src/processor.py:**
```python
def process_data(data, options):
    # Bad: Missing docstring
    # Bad: High complexity
    if data:
        if options:
            if options.get('validate'):
                if validate(data):
                    if options.get('transform'):
                        if should_transform(data):
                            return transform(data)
                        else:
                            return data
                    else:
                        return data
                else:
                    return None
            else:
                return data
        else:
            return data
    else:
        return None

def load_file(filename):
    # Bad: Loading entire file into memory
    with open(filename) as f:
        data = f.read()  # Could be GBs
    return data

# Bad: O(n²) nested loops
def find_matches(list1, list2):
    matches = []
    for item1 in list1:
        for item2 in list2:
            if item1.id == item2.ref_id:
                matches.append((item1, item2))
    return matches
```

## Running Analysis

### Individual Agent Analysis

```bash
# Static analysis
amplifier task "Run static analysis on src/" --agent static-analyzer

# Security scan
amplifier task "Scan src/ for security vulnerabilities" --agent security-scanner

# Performance analysis
amplifier task "Check src/ for performance issues" --agent performance-analyzer

# Documentation check
amplifier task "Validate documentation in src/" --agent documentation-checker
```

### Comprehensive Analysis

```bash
# Run all analyses together
amplifier task "Analyze src/ for all quality issues" --agent quality-aggregator
```

## Expected Results

### Static Analysis Findings

```json
{
  "findings": [
    {
      "file": "src/processor.py",
      "line": 3,
      "severity": "high",
      "issue_type": "complexity",
      "title": "High cyclomatic complexity",
      "metric_value": 11,
      "threshold": 10,
      "suggestion": "Simplify nested conditionals using guard clauses"
    },
    {
      "file": "src/processor.py",
      "line": 3,
      "severity": "high",
      "issue_type": "missing_docstring",
      "title": "Missing docstring on public function",
      "suggestion": "Add docstring explaining parameters and return value"
    }
  ]
}
```

### Security Findings

```json
{
  "findings": [
    {
      "file": "src/database.py",
      "line": 4,
      "severity": "critical",
      "vulnerability_type": "hardcoded_secret",
      "title": "Hardcoded Password",
      "code_snippet": "DB_PASSWORD = \"admin123\"",
      "suggestion": "Use environment variable: DB_PASSWORD = os.getenv('DB_PASSWORD')"
    },
    {
      "file": "src/database.py",
      "line": 9,
      "severity": "critical",
      "vulnerability_type": "sql_injection",
      "title": "SQL Injection Vulnerability",
      "code_snippet": "query = f\"SELECT * FROM users WHERE id = {user_id}\"",
      "suggestion": "Use parameterized query: cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))"
    },
    {
      "file": "src/database.py",
      "line": 22,
      "severity": "high",
      "vulnerability_type": "weak_crypto",
      "title": "Weak Password Hashing",
      "code_snippet": "hashlib.md5(password.encode())",
      "suggestion": "Use bcrypt or Argon2: bcrypt.hashpw(password.encode(), bcrypt.gensalt())"
    }
  ]
}
```

### Performance Findings

```json
{
  "findings": [
    {
      "file": "src/database.py",
      "line": 14,
      "severity": "critical",
      "issue_type": "n_plus_1_query",
      "title": "N+1 Query Problem",
      "description": "Query inside loop generates 1+N database calls",
      "impact": "100 users = 101 queries instead of 1-2",
      "estimated_speedup": "100x faster",
      "suggestion": "Use JOIN or eager loading"
    },
    {
      "file": "src/processor.py",
      "line": 35,
      "severity": "high",
      "issue_type": "algorithm_complexity",
      "title": "O(n²) nested loops",
      "complexity": "O(n²)",
      "better_approach": "O(n)",
      "suggestion": "Use dictionary: {item.ref_id: item for item in list2}"
    },
    {
      "file": "src/processor.py",
      "line": 26,
      "severity": "medium",
      "issue_type": "memory_inefficiency",
      "title": "Loading entire file into memory",
      "suggestion": "Use streaming: for line in file: process(line)"
    }
  ]
}
```

### Comprehensive Report

```markdown
# Comprehensive Code Quality Report

**Overall Quality Score:** 42/100 (Poor - Needs Improvement)

| Category | Score | Grade |
|----------|-------|-------|
| Security | 25/100 | F |
| Performance | 40/100 | D- |
| Code Quality | 55/100 | D |
| Documentation | 45/100 | D- |

---

## Critical Issues (Immediate Action Required)

🔴 **3 Critical Security Issues**
1. SQL Injection - src/database.py:9
2. Hardcoded Password - src/database.py:4
3. N+1 Query Problem - src/database.py:14 (100x performance impact)

---

## Priority Actions

### Today (Critical)
- [ ] Fix SQL injection by using parameterized queries
- [ ] Move hardcoded credentials to environment variables
- [ ] Fix N+1 query with JOIN or eager loading

### This Week (High)
- [ ] Replace MD5 with bcrypt for password hashing
- [ ] Refactor high-complexity functions (complexity 11 → <10)
- [ ] Optimize O(n²) nested loops to O(n)

### This Month (Medium/Low)
- [ ] Add missing docstrings (5 functions)
- [ ] Stream large files instead of loading entirely
- [ ] Improve error handling

---

## Recommendations

1. **Security Review**: Critical vulnerabilities need immediate attention
2. **Performance Audit**: Database operations need optimization
3. **Code Refactoring**: Reduce complexity, improve readability
4. **Documentation**: Add docstrings for all public functions

---

**Next Steps:**
1. Assign critical issues to team members
2. Schedule security training session
3. Set up automated quality checks in CI/CD
4. Re-run analysis after fixes to track improvement
```

## After Fixing Issues

Run analysis again to verify improvements:

```bash
amplifier task "Re-analyze src/ to verify fixes" --agent quality-aggregator
```

Expected improvement:
- Overall score: 42 → 85
- Security: 25 → 90
- Performance: 40 → 88
- Critical issues: 3 → 0

## Integration with CI/CD

Add to your GitHub Actions workflow:

```yaml
name: Code Quality Check

on: [push, pull_request]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Install Amplifier
        run: pip install amplifier
      - name: Run Quality Analysis
        run: |
          amplifier collection add code-quality
          amplifier task "Analyze src/ for quality issues" --agent quality-aggregator
      - name: Fail on Critical Issues
        run: |
          # Parse JSON output and fail if critical issues found
          if [ $(jq '.severity_totals.critical' report.json) -gt 0 ]; then
            echo "Critical issues found!"
            exit 1
          fi
```

## Summary

The code-quality collection identified:
- **3 critical issues** requiring immediate fixes
- **5 high-priority issues** for this week
- **8 medium/low issues** for ongoing improvement

Total estimated impact of fixes:
- **100x faster** database operations (N+1 fix)
- **Eliminates critical security vulnerabilities**
- **Doubles overall quality score**

---

**This example demonstrates the value of automated quality analysis in catching issues before they reach production.**
