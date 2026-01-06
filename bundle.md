---
bundle:
  name: metacog-code-quality
  version: 1.0.0
  description: "Metacognitive code quality analysis and improvement"
  author: "Amplifier Team"
  license: MIT
  repository: https://github.com/ramparte/amplifier-bundle-metacog-code-quality

includes:
  - bundle: git+https://github.com/microsoft/amplifier-foundation@main
---

# Metacognitive Code Quality Bundle

Enhanced code quality analysis through structured reasoning patterns.

## What This Provides

- **Deep code analysis** - Understand code structure and patterns
- **Quality assessment** - Evaluate code against best practices
- **Improvement suggestions** - Actionable recommendations
- **Refactoring guidance** - Safe transformation patterns

## Usage

```bash
amplifier run --bundle metacog-code-quality "Review this code for quality..."
```
