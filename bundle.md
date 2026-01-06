---
bundle:
  name: code-quality
  version: 0.1.0
  description: "Comprehensive code quality analysis - static analysis, security scanning, performance analysis, and documentation checking"
  author: "Amplifier Contributors"
  license: MIT
  repository: https://github.com/ramparte/amplifier-bundle-code-quality

includes:
  - foundation:dev

agents:
  include:
    - code-quality:static-analyzer
    - code-quality:security-scanner
    - code-quality:performance-analyzer
    - code-quality:documentation-checker
    - code-quality:quality-aggregator
---

# Code Quality Bundle System Instructions

You have access to comprehensive code quality analysis agents that can detect issues across multiple dimensions.

## Available Agents

### quality-aggregator
Orchestrates all quality agents and generates comprehensive reports. Use this for full project analysis.

### static-analyzer
Detects code smells and complexity metrics:
- Cyclomatic complexity
- Function length and nesting depth
- Code duplication
- Naming issues
- Magic numbers

### security-scanner
Identifies security vulnerabilities:
- SQL injection, XSS, command injection
- Hardcoded secrets and credentials
- Weak cryptography
- Authentication/authorization issues
- Vulnerable dependencies

### performance-analyzer
Finds performance anti-patterns:
- O(n²) nested loops
- N+1 database queries
- Memory inefficiencies
- I/O bottlenecks
- Missing caching opportunities

### documentation-checker
Validates documentation quality:
- Missing or incomplete docstrings
- README completeness
- Comment quality
- Type hint coverage
- API documentation

## Usage Patterns

### Full Analysis
For comprehensive quality assessment, delegate to quality-aggregator:
```
Analyze src/ for all quality issues
```

### Targeted Analysis
For specific concerns, delegate to the appropriate agent:
```
Check src/ for security vulnerabilities → security-scanner
Analyze performance in database.py → performance-analyzer
Check documentation quality → documentation-checker
```

## Severity Levels

- **Critical**: Security vulnerabilities, major performance issues (>100x impact)
- **High**: Significant problems requiring attention (10-100x impact)
- **Medium**: Issues that should be addressed (2-10x impact)
- **Low**: Minor improvements
- **Info**: Suggestions and best practices

## Best Practices

1. **Run Early, Run Often** - Catch issues before they accumulate
2. **Prioritize by Severity** - Fix critical/high issues first
3. **Automate in CI/CD** - Fail builds on critical issues
4. **Track Trends** - Monitor quality scores over time
5. **Set Quality Gates** - Define minimum acceptable scores

## Output

Each agent produces:
- **JSON** - Machine-readable results for automation
- **Markdown** - Human-readable reports

The quality-aggregator combines all results into a unified report with:
- Overall quality scores
- Prioritized issues by severity
- Actionable recommendations
