# Code Smells and Anti-Patterns

Reference guide for static analysis agents to detect code quality issues.

## Complexity Smells

### Long Method
**Smell:** Functions/methods exceeding 50 lines
**Problem:** Hard to understand, test, and maintain
**Detection:** Count logical lines (exclude blanks/comments)
**Thresholds:**
- Medium: 50-100 lines
- High: 100-200 lines
- Critical: >200 lines

### High Cyclomatic Complexity
**Smell:** Too many decision points in a function
**Problem:** Difficult to test all paths, error-prone
**Detection:** Count branches, loops, and logical operators
**Thresholds:**
- Medium: 7-10 complexity
- High: 10-15 complexity
- Critical: >15 complexity

### Deep Nesting
**Smell:** Code indented more than 4 levels
**Problem:** Difficult to follow logic flow
**Detection:** Track indentation depth
**Thresholds:**
- Medium: 4-5 levels
- High: 5-7 levels
- Critical: >7 levels

### Too Many Parameters
**Smell:** Functions with many parameters
**Problem:** Hard to use, likely doing too much
**Detection:** Count function parameters
**Thresholds:**
- Low: 5-6 parameters
- Medium: 6-8 parameters
- High: >8 parameters

## Duplication Smells

### Duplicated Code
**Smell:** Identical or similar code blocks repeated
**Problem:** Changes must be made in multiple places
**Detection:** Compare code blocks for similarity
**Example:**
```python
# BAD: Duplicated logic
def process_user(user):
    if user.active and user.verified and user.age >= 18:
        return True
    return False

def can_purchase(user):
    if user.active and user.verified and user.age >= 18:
        return True
    return False

# GOOD: Extract common logic
def is_eligible_user(user):
    return user.active and user.verified and user.age >= 18
```

## Naming Smells

### Unclear Names
**Smell:** Variable/function names that don't describe their purpose
**Examples:**
- Single letters: `x`, `y`, `z` (except loop counters)
- Abbreviations: `usr`, `proc`, `tmp`
- Generic names: `data`, `info`, `obj`, `thing`

**Good Naming:**
- Descriptive: `user_account`, `process_payment`, `temporary_file`
- Intention-revealing: `is_valid`, `has_permission`, `can_access`

### Inconsistent Naming
**Smell:** Mixed naming conventions
**Examples:**
- Mixed case: `userName`, `user_email`, `UserAddress`
- Mixed terminology: `get_user`, `fetch_account`, `retrieve_person`

## Data Smells

### Magic Numbers
**Smell:** Hardcoded numbers without explanation
**Problem:** Unclear meaning, hard to maintain
**Example:**
```python
# BAD
if speed > 60:
    issue_ticket()

# GOOD
SPEED_LIMIT_MPH = 60
if speed > SPEED_LIMIT_MPH:
    issue_ticket()
```

### Mutable Default Arguments
**Smell:** Using mutable objects as default values
**Problem:** Shared state across function calls
**Example:**
```python
# BAD
def add_item(item, items=[]):
    items.append(item)
    return items

# GOOD
def add_item(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items
```

## Control Flow Smells

### Nested Conditionals
**Smell:** Multiple levels of if/else nesting
**Problem:** Hard to follow logic
**Example:**
```python
# BAD
def process(data):
    if data:
        if data.valid:
            if data.complete:
                return process_data(data)
            else:
                return "incomplete"
        else:
            return "invalid"
    else:
        return "missing"

# GOOD
def process(data):
    if not data:
        return "missing"
    if not data.valid:
        return "invalid"
    if not data.complete:
        return "incomplete"
    return process_data(data)
```

### Complex Boolean Expressions
**Smell:** Long boolean conditions
**Example:**
```python
# BAD
if (user.active and user.verified and not user.suspended 
    and user.age >= 18 and user.country == 'US'):
    
# GOOD
def is_eligible_us_user(user):
    return (user.active and 
            user.verified and 
            not user.suspended and
            user.age >= 18 and 
            user.country == 'US')

if is_eligible_us_user(user):
```

## Class/Module Smells

### Large Class
**Smell:** Classes with too many methods or responsibilities
**Thresholds:**
- Medium: 200-300 lines
- High: 300-500 lines
- Critical: >500 lines

### God Object
**Smell:** One class doing everything
**Detection:** Class with >10 public methods, many dependencies

### Inappropriate Intimacy
**Smell:** Classes accessing each other's internals
**Detection:** Direct access to private members, excessive coupling

## Comment Smells

### Commented-Out Code
**Smell:** Code left in comments
**Problem:** Clutter, confusion about intent
**Solution:** Use version control, delete commented code

### Obvious Comments
**Smell:** Comments that restate the code
**Example:**
```python
# BAD
# Increment counter
counter += 1

# GOOD (no comment needed, or explain WHY)
# Track failed login attempts for rate limiting
failed_attempts += 1
```

### Outdated Comments
**Smell:** Comments that don't match current code
**Problem:** Misleading, confusing
**Detection:** Compare comment intent with actual code behavior

## Python-Specific Smells

### Bare Except
**Smell:** Catching all exceptions without specificity
```python
# BAD
try:
    risky_operation()
except:
    pass

# GOOD
try:
    risky_operation()
except SpecificError as e:
    logger.error(f"Operation failed: {e}")
```

### Print Statements
**Smell:** Using print() instead of logging
**Problem:** Not configurable, mixes concerns
**Solution:** Use logging module

### Import *
**Smell:** Wildcard imports
**Problem:** Namespace pollution, unclear dependencies
```python
# BAD
from module import *

# GOOD
from module import specific_function, SpecificClass
```

## JavaScript-Specific Smells

### Var Usage
**Smell:** Using `var` instead of `const`/`let`
**Problem:** Function scope instead of block scope

### == Instead of ===
**Smell:** Type coercion in comparisons
**Problem:** Unexpected behavior

### Callback Hell
**Smell:** Deeply nested callbacks
**Solution:** Use Promises or async/await

## Detection Priorities

**High Priority (Always Flag):**
- Cyclomatic complexity >15
- Functions >200 lines
- Security-related code smells
- Mutable default arguments

**Medium Priority (Context-Dependent):**
- Complexity 10-15
- Functions 50-100 lines
- Magic numbers
- Duplicated code

**Low Priority (Suggestions):**
- Minor naming issues
- Unnecessary comments
- Slight redundancy
