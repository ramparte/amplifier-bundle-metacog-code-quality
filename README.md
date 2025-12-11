# Amplifier Collection: Code Quality

**Comprehensive code quality analysis for your projects**

This collection provides specialized agents that analyze code for quality issues, security vulnerabilities, performance bottlenecks, and documentation gaps.

## Features

- 🔍 **Static Analysis** - Detect code smells, complexity issues, and maintainability problems
- 🔒 **Security Scanning** - Find vulnerabilities, insecure patterns, and hardcoded secrets
- ⚡ **Performance Analysis** - Identify bottlenecks, inefficient algorithms, and optimization opportunities
- 📚 **Documentation Checking** - Validate docstrings, comments, and README quality
- 📊 **Comprehensive Reports** - Combined analysis with actionable recommendations

## Quick Start

### Installation

```bash
# Install collection (when published)
amplifier collection add code-quality

# Verify installation
amplifier collection list
amplifier collection show code-quality
```

### Basic Usage

```bash
# Run comprehensive quality analysis
amplifier task "Analyze src/ for all quality issues" --agent quality-aggregator

# Run specific analysis
amplifier task "Check src/ for security vulnerabilities" --agent security-scanner
amplifier task "Analyze performance in database.py" --agent performance-analyzer
amplifier task "Check documentation quality" --agent documentation-checker
```

## Agents

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

### quality-aggregator
Orchestrates all agents and generates unified reports with:
- Overall quality scores
- Prioritized issues by severity
- Actionable recommendations
- Trend analysis

## Output Formats

Each agent produces:
- **JSON** - Machine-readable results for automation
- **Markdown** - Human-readable reports

## Example Report

```markdown
# Comprehensive Code Quality Report

**Overall Quality Score:** 74/100

## Critical Issues (3)
- 🔴 SQL Injection - src/database.py:45
- 🔴 N+1 Query - src/database.py:67
- 🔴 High Complexity - src/processor.py:45

## Recommendations
1. Fix critical security issues immediately
2. Optimize database queries (100x speedup possible)
3. Refactor complex functions
4. Add missing documentation
```

## Configuration

Create a profile for customized analysis:

```yaml
# profiles/my-quality-profile.yaml
agents:
  - quality-aggregator
  - static-analyzer
  - security-scanner
  
context:
  - code-quality:context/code-smells-patterns.md
  - code-quality:context/security-patterns.md
```

## Best Practices

1. **Run Early, Run Often** - Catch issues before they accumulate
2. **Prioritize by Severity** - Fix critical/high issues first
3. **Automate in CI/CD** - Fail builds on critical issues
4. **Track Trends** - Monitor quality scores over time
5. **Set Quality Gates** - Define minimum acceptable scores

## Severity Levels

- **Critical**: Security vulnerabilities, major performance issues (>100x impact)
- **High**: Significant problems requiring attention (10-100x impact)
- **Medium**: Issues that should be addressed (2-10x impact)
- **Low**: Minor improvements
- **Info**: Suggestions and best practices

## Supported Languages

Currently optimized for:
- Python
- JavaScript/TypeScript

Patterns are extensible to other languages.

## Philosophy

This collection embodies Amplifier's core principles:

- **Ruthless Simplicity**: Each agent has a focused responsibility
- **Actionable Feedback**: Every issue includes specific suggestions
- **Objective Metrics**: Severity based on measurable impact
- **Independent & Composable**: Agents work alone or together

## Examples

See [examples/](examples/) directory for:
- Example analysis reports
- CI/CD integration patterns
- Custom configuration examples

## Testing

```bash
# Run collection tests
pytest tests/

# Test on a real project
amplifier task "Analyze the metacognition collection" --agent quality-aggregator
```

## Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md)

## License

MIT License - See [LICENSE](LICENSE)

## Version

**Collection Version**: 0.1.0  
**Last Updated**: 2025-12-10

---

**Built with** ❤️ **using Amplifier**
